"""Reading, search, deep-link and planner integration tests (no browser)."""
import ast
from html.parser import HTMLParser
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

import guide_content as content
from test_decision_ui import APP, by_label


def legacy_guides():
    tree = ast.parse(Path(APP).read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "攻略資料" for t in node.targets):
            return ast.literal_eval(node.value)
    raise AssertionError("Missing guide index")


def test_guide_catalog_has_stable_ids_and_honest_source_labels():
    guides = content.all_guides(legacy_guides())
    assert len({g["slug"] for g in guides}) == len(guides)
    assert len(content.GUIDES) == 6
    assert all(g["category"] in content.CATEGORIES for g in guides)
    for guide in guides:
        assert guide["title"] and guide["verdict"] and guide["sections"] and guide["caution"]
        assert all(content.get_guide(slug, guides) for slug in guide["related"])
        if guide.get("reference_only"):
            assert guide["checked"] is None
            assert "待重核" in guide["status"] or "歷史" in guide["status"]
        if guide["checked"]:
            assert guide["source_date"] and guide["sources"]
        for section in guide["sections"]:
            for row in section.get("rows", []):
                assert len(row) == len(section["columns"])
    assert content.get_guide("event-budget", guides)["status"] == "本站試算說明"


@pytest.mark.parametrize("query,slug", [("自定典藏館", "collection-hall"), ("暗物質魁儡", "collectible-breakpoints"),
    ("Ｅ１", "gear-forging"), ("維納托 R6", "survivor-awakening"), ("補鑽", "event-budget"), ("紅力場", "twin-drone")])
def test_search_handles_game_terms_and_common_aliases(query, slug):
    assert slug in [g["slug"] for g in content.search_guides(content.GUIDES, query)]


def test_category_and_query_filters_are_combined():
    assert not content.search_guides(content.GUIDES, "暗物質", "裝備神鑄")
    assert not content.search_guides(content.GUIDES, "不存在的攻略abcd")
    guides = content.all_guides(legacy_guides())
    assert any("第一百二十六" in g["title"] for g in content.search_guides(guides, category="寵物與關卡"))
    assert not any("第一百二十六" in g["title"] for g in content.search_guides(guides, category="活動玩法"))


def test_new_visitor_gets_guides_without_an_account_form_or_network(monkeypatch):
    import urllib.request

    def offline(*args, **kwargs):
        raise AssertionError("Guide home must not require an external API")

    monkeypatch.setattr(urllib.request, "urlopen", offline)
    a = AppTest.from_file(APP).run(timeout=15)
    assert not a.exception
    assert a.radio[0].value == "攻略首頁"
    assert not a.get("form")
    assert not a.number_input
    assert "player_profile" not in a.session_state
    assert a.button(key="featured_collection-hall")
    by_label(a.text_input, "搜尋攻略").set_value("暗物質魁儡").run()
    a.button(key="home_search_collectible-breakpoints").click().run()
    assert not a.exception
    assert a.query_params["guide"] == ["collectible-breakpoints"]


@pytest.mark.parametrize("slug", [g["slug"] for g in content.GUIDES])
def test_every_core_article_has_a_working_direct_link_and_full_content(slug):
    a = AppTest.from_file(APP)
    a.query_params["guide"] = slug
    a.run(timeout=15)
    assert not a.exception
    assert a.radio[0].value == "資料庫"
    text = "\n".join(m.value for m in a.markdown)
    guide = content.get_guide(slug, content.GUIDES)
    assert guide["title"] in text
    assert "先看結論" in text and "常見問題" in text and "資料來源" in text
    assert "本文目錄" in text and "guide-part-1" in text
    assert a.warning
    assert not a.number_input
    assert not a.get("form")


def test_article_to_targeted_planner_preserves_profile():
    a = AppTest.from_file(APP)
    profile = {"survivor": "維納托", "awakening": 6, "awakening_cores": 20}
    a.session_state["player_profile"] = dict(profile)
    a.query_params["guide"] = "survivor-awakening"
    a.run()
    by_label(a.button, "用我的配置排升級順序").click().run()
    assert not a.exception
    assert a.radio[0].value == "下一步"
    assert "guide" not in a.query_params
    assert by_label(a.selectbox, "這次要安排的資源").value == "覺醒核心"
    assert a.session_state["player_profile"] == profile
    assert any("維納托 R6 → R7" in m.value for m in a.markdown)


def test_category_navigation_and_return_from_article():
    a = AppTest.from_file(APP).run()
    a.button(key="home_topic_2").click().run()
    assert not a.exception
    assert by_label(a.selectbox, "攻略分類").value == "收藏典藏"
    catalog = content.all_guides(legacy_guides())
    visible = [content.get_guide(b.key.removeprefix("index_"), catalog) for b in a.button if b.key and b.key.startswith("index_")]
    assert visible and all(g["category"] == "收藏典藏" for g in visible)
    a.button(key="index_collection-hall").click().run()
    by_label(a.button, "← 攻略索引").click().run()
    assert not a.exception
    assert "guide" not in a.query_params
    assert by_label(a.selectbox, "攻略分類").value == "收藏典藏"
    a.radio[0].set_value("攻略首頁").run()
    assert not a.exception
    assert by_label(a.text_input, "搜尋攻略")


def test_invalid_deep_link_is_local_and_recoverable():
    a = AppTest.from_file(APP)
    a.query_params["guide"] = "https://invalid.example/<script>"
    a.run()
    assert not a.exception
    assert any("找不到這篇攻略" in m.value for m in a.markdown)
    by_label(a.button, "返回攻略索引").click().run()
    assert not a.exception
    assert "guide" not in a.query_params
    assert by_label(a.selectbox, "攻略分類").value == "全部"


def test_main_navigation_leaves_article_without_stale_deep_link():
    a = AppTest.from_file(APP)
    a.query_params["guide"] = "collection-hall"
    a.run()
    a.radio[0].set_value("我的帳號").run()
    assert not a.exception
    assert "guide" not in a.query_params
    assert a.radio[0].value == "我的帳號"
    a.radio[0].set_value("資料庫").run()
    assert not a.exception
    assert by_label(a.selectbox, "要查什麼")


class Anchors(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.targets = []

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if "id" in values:
            self.ids.append(values["id"])
        if tag == "a" and values.get("href", "").startswith("#"):
            self.targets.append(values["href"][1:])


def test_article_contents_links_point_to_unique_sections():
    a = AppTest.from_file(APP)
    a.query_params["guide"] = "collection-hall"
    a.run()
    parser = Anchors()
    for m in a.markdown:
        parser.feed(m.value)
    assert parser.targets
    assert len(parser.ids) == len(set(parser.ids))
    assert set(parser.targets) <= set(parser.ids)
