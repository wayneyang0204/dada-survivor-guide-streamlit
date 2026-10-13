"""Local animated-guide navigation contracts, not visual animation quality.

Rendered motion, pointer hit targets, focus, reduced motion, and small viewports
still need browser verification. These tests exercise real Streamlit callbacks.
"""
from copy import deepcopy
from html.parser import HTMLParser
import re

import pytest
from streamlit.testing.v1 import AppTest

import guide_content as content
import ui_interactions
from test_decision_ui import APP, by_label


TOPIC_CODES = {
    "全部": "all",
    "特工養成": "profile",
    "裝備神鑄": "gear",
    "收藏典藏": "collection",
    "科技配件": "tech",
    "活動玩法": "event",
    "寵物與關卡": "pet",
    "載具與模組": "mount",
}


class FlightMarkup(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []
        self.text = []
        self.stack = []
        self.hidden_nodes = set()

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if values.get("aria-hidden") == "true" or any(
                ancestor.get("aria-hidden") == "true" for _, ancestor in self.stack):
            self.hidden_nodes.add(len(self.tags))
        self.tags.append((tag, values))
        if tag not in {"area", "base", "br", "col", "embed", "hr", "img", "input",
                       "link", "meta", "param", "source", "track", "wbr"}:
            self.stack.append((tag, values))

    def handle_endtag(self, tag):
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index][0] == tag:
                del self.stack[index:]
                break

    def handle_data(self, data):
        self.text.append(data)


def parse(markup):
    parser = FlightMarkup()
    parser.feed(markup)
    return parser


def app_markup(app):
    return parse("\n".join(item.value for item in app.markdown
                           if "<style>" not in item.value))


def has_class(attrs, name):
    return name in attrs.get("class", "").split()


def assert_local_decorative_markup(markup):
    parsed = parse(markup)
    for index, (tag, attrs) in enumerate(parsed.tags):
        assert tag not in {"script", "foreignobject", "iframe", "object", "embed"}
        assert not any(name.lower().startswith("on") for name in attrs)
        for name in ("href", "src", "xlink:href"):
            value = attrs.get(name, "").strip().lower()
            assert not value.startswith(("javascript:", "http:", "https:", "//"))
        if tag == "svg":
            # aria-hidden on the panorama also hides its cloud/route SVGs.
            assert index in parsed.hidden_nodes
            assert attrs.get("focusable", "false") == "false"
            assert attrs.get("tabindex", "-1") == "-1"
        if tag == "image":
            assert attrs.get("href", "").startswith("data:image/webp;base64,")
    return parsed


@pytest.mark.parametrize("topic,code", TOPIC_CODES.items())
def test_scene_and_article_bookmark_use_allowlisted_topic_codes(topic, code):
    scene = assert_local_decorative_markup(
        ui_interactions.flight_scene_markup(topic, 37))
    bookmark = assert_local_decorative_markup(
        ui_interactions.article_bookmark_markup(topic))
    assert any(has_class(attrs, "flight-panorama") for _, attrs in scene.tags)
    assert any(has_class(attrs, "flight-bird") for _, attrs in scene.tags)
    assert any(has_class(attrs, "scene-station") for _, attrs in scene.tags)
    assert any(attrs.get("data-flight-topic") == code for _, attrs in scene.tags)
    assert any(attrs.get("data-flight-topic") == code for _, attrs in bookmark.tags)
    text = " ".join(scene.text)
    assert re.search(r"(?<!\d)37(?!\d)", text) and "篇" in text


@pytest.mark.parametrize("unknown", ("不是攻略分類", '<script>alert("x")</script>',
                                      '\" onmouseover=\"alert(1)', "", None, [], {}))
def test_unknown_topic_falls_back_without_injecting_or_echoing_markup(unknown):
    scene = ui_interactions.flight_scene_markup(unknown, 37)
    bookmark = ui_interactions.article_bookmark_markup(unknown)
    assert scene == ui_interactions.flight_scene_markup("全部", 37)
    assert bookmark == ui_interactions.article_bookmark_markup("全部")
    assert_local_decorative_markup(scene)
    assert_local_decorative_markup(bookmark)


@pytest.mark.parametrize("count", (-1, True, None, "37", 1.5,
                                  '<img src=x onerror="alert(1)">'))
def test_invalid_count_is_zero_without_html_or_event_handler_injection(count):
    markup = ui_interactions.flight_scene_markup("全部", count)
    parsed = assert_local_decorative_markup(markup)
    assert not any(tag == "img" for tag, _ in parsed.tags)
    assert "0 篇詳解" in " ".join(parsed.text)


def boot_home(profile=None):
    app = AppTest.from_file(APP)
    if profile is not None:
        app.session_state["player_profile"] = deepcopy(profile)
    app.query_params["ref"] = "synthetic-motion-check"
    return app.run(timeout=15)


def test_home_has_eight_native_radio_choices_without_animation_controls():
    app = boot_home()
    assert not app.exception
    selector = by_label(app.radio, "攻略分類")
    assert selector.key == "home_topic"
    assert selector.value == "全部"
    assert len(selector.options) == 8
    assert len(set(selector.options)) == 8
    assert not any(item.key == "home_topic" for item in app.selectbox)
    assert "player_profile" not in app.session_state
    assert not app.slider and not app.toggle
    assert not any(button.label in {"播放動畫", "核對答案"} for button in app.button)
    assert not any("練習" in expander.label for expander in app.expander)


@pytest.mark.parametrize("topic", content.CATEGORIES)
def test_selecting_topic_changes_scene_and_directory_not_player_or_url(topic):
    profile = {"survivor": "維納托", "awakening": 6, "awakening_cores": 20}
    app = boot_home(profile)
    before_url = deepcopy(app.query_params)
    by_label(app.radio, "攻略分類").set_value(topic).run()
    assert not app.exception
    assert by_label(app.radio, "攻略分類").value == topic
    assert app.query_params == before_url
    assert app.session_state["player_profile"] == profile
    parsed = app_markup(app)
    assert any(attrs.get("data-flight-topic") == TOPIC_CODES[topic]
               for _, attrs in parsed.tags)
    expected_count = sum(guide["category"] == topic for guide in content.GUIDES
                         if not guide.get("reference_only"))
    assert f"{expected_count} 篇詳解" in " ".join(parsed.text)
    directory = [content.get_guide(button.key.removeprefix("home_"), content.GUIDES)
                 for button in app.button if button.key and button.key.startswith("home_")]
    assert directory and all(guide and guide["category"] == topic for guide in directory)


@pytest.mark.parametrize("topic", content.CATEGORIES)
def test_article_bookmark_and_return_preserve_original_topic(topic):
    profile = {"survivor": "維納托", "awakening": 6, "awakening_cores": 20}
    guide = next(guide for guide in content.GUIDES if guide["category"] == topic)
    app = boot_home(profile)
    by_label(app.radio, "攻略分類").set_value(topic).run()
    app.button(key=f"home_{guide['slug']}").click().run()
    assert not app.exception
    assert app.query_params["guide"] == [guide["slug"]]
    assert app.query_params["ref"] == ["synthetic-motion-check"]
    assert app.session_state["article_origin"]["category"] == topic
    assert any(attrs.get("data-flight-topic") == TOPIC_CODES[topic]
               for _, attrs in app_markup(app).tags)
    assert app.session_state["player_profile"] == profile
    by_label(app.button, "← 攻略首頁").click().run()
    assert not app.exception
    assert "guide" not in app.query_params
    assert app.query_params["ref"] == ["synthetic-motion-check"]
    assert by_label(app.radio, "攻略分類").value == topic
    assert app.session_state["player_profile"] == profile
    assert any(attrs.get("data-flight-topic") == TOPIC_CODES[topic]
               for _, attrs in app_markup(app).tags)


def test_all_topics_origin_returns_to_all_but_article_bookmark_uses_its_category():
    guide = content.get_guide("collection-hall", content.GUIDES)
    app = boot_home()
    app.button(key="home_collection-hall").click().run()
    assert not app.exception
    assert app.session_state["article_origin"]["category"] == "全部"
    assert any(attrs.get("data-flight-topic") == TOPIC_CODES[guide["category"]]
               for _, attrs in app_markup(app).tags)
    assert "player_profile" not in app.session_state
    by_label(app.button, "← 攻略首頁").click().run()
    assert not app.exception
    assert by_label(app.radio, "攻略分類").value == "全部"
    assert "guide" not in app.query_params
    assert "player_profile" not in app.session_state
    assert any(attrs.get("data-flight-topic") == "all"
               for _, attrs in app_markup(app).tags)


def test_filtered_search_keeps_the_selected_topic_and_has_no_profile_side_effect():
    app = boot_home()
    by_label(app.radio, "攻略分類").set_value("收藏典藏").run()
    by_label(app.text_input, "搜尋攻略").set_value("暗物質").run()
    assert not app.exception
    assert by_label(app.radio, "攻略分類").value == "收藏典藏"
    assert "player_profile" not in app.session_state
    results = [content.get_guide(button.key.removeprefix("home_search_"), content.GUIDES)
               for button in app.button
               if button.key and button.key.startswith("home_search_")]
    assert results and all(guide and guide["category"] == "收藏典藏" for guide in results)
    assert any(attrs.get("data-flight-topic") == "collection"
               for _, attrs in app_markup(app).tags)


def test_scene_text_palettes_keep_readable_contrast():
    from motion_theme import MOTION_STYLE
    from test_ui_theme import contrast
    pairs = re.findall(r"--scene-sky:(#[a-f0-9]{6}).*?--scene-tint:(#[a-f0-9]{6}).*?--scene-ink:(#[a-f0-9]{6})", MOTION_STYLE, re.S)
    assert len(pairs) == 8
    assert all(contrast(ink, background) >= 4.5 for sky, tint, ink in pairs for background in (sky,tint))


def test_warm_cache_refreshes_new_motion_helpers_before_render(monkeypatch):
    import motion_theme
    for name in ('flight_scene_markup', 'article_bookmark_markup'):
        monkeypatch.delattr(ui_interactions, name)
    monkeypatch.delattr(motion_theme, 'MOTION_STYLE')
    app = boot_home()
    assert not app.exception
    assert callable(ui_interactions.flight_scene_markup)
    assert callable(ui_interactions.article_bookmark_markup)
    assert 'scene-cruise' in motion_theme.MOTION_STYLE
