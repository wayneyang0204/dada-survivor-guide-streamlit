"""Non-browser regressions for the shared handbook theme and information layout.

These checks do not replace viewport, touch, or screen-reader testing.
"""
from html.parser import HTMLParser
from pathlib import Path
import re
import tomllib

import pytest

from test_decision_ui import boot, by_label
from ui_theme import STYLE


COLORS = dict(re.findall(r"--([a-z-]+):\s*(#[0-9a-f]{6})", STYLE))


def luminance(color):
    values = [int(color[i:i+2], 16) / 255 for i in (1, 3, 5)]
    linear = [v / 12.92 if v <= .04045 else ((v + .055) / 1.055) ** 2.4 for v in values]
    return sum(v * weight for v, weight in zip(linear, (.2126, .7152, .0722)))


def contrast(a, b):
    light, dark = sorted((luminance(a), luminance(b)), reverse=True)
    return (light + .05) / (dark + .05)


@pytest.mark.parametrize("foreground", ["ink", "muted", "accent", "ready", "pending", "blocked"])
@pytest.mark.parametrize("background", ["paper", "wash", "mint", "peach", "lilac"])
def test_text_tokens_meet_normal_text_contrast(foreground, background):
    assert contrast(COLORS[foreground], COLORS[background]) >= 4.5


def test_controls_and_primary_button_have_sufficient_contrast():
    assert contrast(COLORS["paper"], COLORS["accent"]) >= 4.5
    assert contrast(COLORS["field"], COLORS["paper"]) >= 3
    # Streamlit dims the caption wrapper to 0.6, regardless of our text token.
    assert '[data-testid="stElementContainer"] [data-testid="stCaptionContainer"] {opacity:1;}' in STYLE


def test_cloud_theme_matches_the_single_shared_stylesheet():
    config = tomllib.loads((Path(__file__).parent.parent / ".streamlit/config.toml").read_text(encoding="utf-8"))["theme"]
    assert config["base"] == "light"
    for setting, token in (("backgroundColor", "paper"), ("secondaryBackgroundColor", "wash"),
                           ("primaryColor", "accent"), ("textColor", "ink")):
        assert config[setting] == COLORS[token]
    a = boot()
    styles = [m.value for m in a.markdown if "<style>" in m.value]
    assert len(styles) == 1
    assert "--accent:#14604f" in styles[0]
    assert ".st-key-guide_search_panel" in styles[0]


def test_text_can_scale_and_layouts_have_narrow_screen_fallbacks():
    # Protect the authored rules, not a claim about a rendered viewport.
    sizes = [float(n) for n in re.findall(r"font-size:([.\d]+)rem", STYLE)]
    assert sizes and min(sizes) >= .875
    assert "font-size:" not in STYLE.split("html, body", 1)[1].split("}", 1)[0]
    assert "@media(max-width:760px)" in STYLE
    assert "@media(max-width:480px)" in STYLE
    assert "grid-template-columns:1fr;" in STYLE
    assert "prefers-reduced-motion:reduce" in STYLE
    assert "position:fixed" not in STYLE
    assert "input:focus-visible" in STYLE
    # Keep the native visually hidden input; only the decorative circle is hidden.
    assert 'label[data-testid="stRadioOption"] > div:first-child {display:none;}' not in STYLE


class Markup(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))


def test_home_has_one_goal_ledger_and_one_reasoning_drawer():
    a = boot()
    a.session_state["player_profile"] = {"survivor": "維納托", "awakening": 6, "awakening_cores": 20}
    a.run()
    assert not a.exception
    markup = Markup()
    for item in a.markdown:
        if "<style>" not in item.value:
            markup.feed(item.value)
    assert sum(tag == "h1" for tag, _ in markup.tags) == 1
    assert sum(attrs.get("aria-label") == "優先升級目標" for _, attrs in markup.tags) == 1
    assert sum(attrs.get("role") == "listitem" for _, attrs in markup.tags) == 3
    assert any(attrs.get("aria-label") == "執行備忘" for _, attrs in markup.tags)
    assert [e.label for e in a.expander] == ["只核對這一步的材料", "排序依據與其他候選"]
    assert {e.proto.popover.label for e in a.get("popover")} == {"備份與匯入", "記錄遊戲內完成"}
    # Opening the page never records an in-game completion.
    assert a.session_state["player_profile"]["awakening"] == 6


def test_editor_has_visible_categories_and_only_one_form():
    a = boot()
    a.radio[0].set_value("我的帳號").run()
    selector = by_label(a.radio, "這次更新哪一項")
    assert selector.options == ["角色與模式", "普通典藏館", "進階典藏館", "收藏品", "裝備與科技"]
    for section in selector.options:
        by_label(a.radio, "這次更新哪一項").set_value(section).run()
        assert not a.exception
        assert len(a.get("form")) == 1
        assert any(f'class="editor-heading">{section}' in m.value for m in a.markdown)
        assert a.get("download_button")


def test_event_summary_is_visible_and_offline_calculator_is_preserved(monkeypatch):
    import urllib.request

    def offline(*args, **kwargs):
        raise OSError("Offline test")

    monkeypatch.setattr(urllib.request, "urlopen", offline)
    a = boot()
    a.radio[0].set_value("活動").run()
    assert not a.exception
    assert not next(e for e in a.expander if e.label == "查看這篇活動的30秒重點").proto.expanded
    assert any('class="event-verdict"' in m.value for m in a.markdown)
    for label in ("01 / 活動目標", "02 / 免費進度", "03 / 寶石成本"):
        assert any(label in m.value for m in a.markdown)
    by_label(a.button, "一鍵判斷這次活動").click().run()
    assert not a.exception
    assert len(a.metric) == 4


def test_illustrated_home_has_real_counts_and_accessible_native_routes():
    import guide_content as content
    from ui_art import TOPIC_ART

    a = boot()
    a.radio[0].set_value("攻略首頁").run()
    assert not a.exception
    text = "\n".join(m.value for m in a.markdown if "<style>" not in m.value)
    assert f'{len(content.GUIDES)} 篇門檻詳解' in text
    assert set(TOPIC_ART) == set(content.CATEGORIES)
    assert text.count('class="topic-heading"') == len(content.CATEGORIES)
    positions = [text.index(f'<h3>{topic}</h3>') for topic in content.CATEGORIES]
    assert positions == sorted(positions)
    assert text.count('class="task-card-head"') == 3
    assert 'class="buddy-note"' in text
    assert a.radio[0].options == ["攻略首頁", "升級路線", "我的配置", "活動試算", "攻略索引"]
    assert not a.get("form") and "player_profile" not in a.session_state


def test_original_vector_art_is_decorative_and_has_no_remote_assets():
    from xml.etree import ElementTree as ET
    from ui_art import GUIDE_BUDDY, FIELD_BUDDY, TOPIC_ART, guide_icon

    artwork = [GUIDE_BUDDY, FIELD_BUDDY, *(guide_icon(item[0]) for item in TOPIC_ART.values())]
    for item in artwork:
        root = ET.fromstring(item)
        assert root.attrib["aria-hidden"] == "true"
        assert root.attrib["focusable"] == "false"
        assert root.attrib.get("viewBox")
        assert not any(node.tag.endswith(("image", "script", "foreignObject")) for node in root.iter())
    assert guide_icon('<script>') == guide_icon("book")
    assert STYLE.count("data:image/svg+xml,") == 5
    assert "grid-template-columns:repeat(5,minmax(0,1fr))" in STYLE


def test_warm_cache_refreshes_art_before_theme_and_ui(monkeypatch):
    from streamlit.testing.v1 import AppTest
    from test_decision_ui import APP
    import ui_art

    for symbol in ("FIELD_BUDDY", "guide_icon", "TOPIC_ART"):
        monkeypatch.delattr(ui_art, symbol)
    a = AppTest.from_file(APP).run(timeout=15)
    assert not a.exception
    assert callable(ui_art.guide_icon)
    assert any('class="task-art"' in item.value for item in a.markdown)
