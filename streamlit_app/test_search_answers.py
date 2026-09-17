"""Player questions return relevant facts, not just plausible-sounding titles."""
import pytest
from streamlit.testing.v1 import AppTest

import guide_content as content
from data_engine import load_collectible_catalog
from test_decision_ui import APP, by_label


@pytest.mark.parametrize("query,slug", [
    ("暗物質黃5", "collectible-breakpoints"),
    ("SS鞋套裝有哪些", "collectible-sets"),
    ("召喚替身有哪些", "collectible-sets"),
    ("金R3要不要重置", "link-passives"),
    ("暴擊率超過100%還有區別嗎", "crit-overflow"),
    ("維托爾R6", "survivor-awakening"),
])
def test_full_player_questions(query, slug):
    matches = content.search_guides(content.GUIDES, query)
    assert matches and matches[0]["slug"] == slug


def test_matching_set_returns_its_four_members_not_the_other_set():
    guide = content.get_guide("collectible-sets", content.GUIDES)
    rows = content.answer_rows(guide, "召喚替身有哪些")
    assert len(rows) == 4
    assert "暗物質傀儡" in str(rows) and "預言塔羅牌" in str(rows)
    assert "賽博圖騰柱" not in str(rows)


def test_exact_breakpoint_is_first_in_answer_preview():
    guide = content.get_guide("collectible-breakpoints", content.GUIDES)
    row = content.answer_rows(guide, "暗物質黃5")[0]
    assert row[:2] == ["暗物質傀儡", "黃5"] and "10%" in row[2]
    assert len(content.answer_rows(guide, "暗物質黃5")) == 1
    assert not content.answer_rows(content.get_guide("epic-collectibles", content.GUIDES), "暗物質黃5")


def test_collectible_aliases_and_id_do_not_fabricate_effects():
    catalog = load_collectible_catalog()
    assert content.search_collectibles(catalog, "時間軸魔術方")[0]["id"] == 232
    assert content.search_collectibles(catalog, "231")[0]["name"] == "暗物質傀儡"
    assert not content.search_collectibles(catalog, "不存在123456")


def test_home_has_single_entry_per_guide_and_searches_catalog_without_account():
    app = AppTest.from_file(APP).run()
    titles = [button.label for button in app.button]
    for guide in content.GUIDES:
        assert titles.count(guide["title"]) == 1
    by_label(app.text_input, "搜尋攻略").set_value("231").run()
    text = " ".join(item.value for item in app.markdown)
    assert "暗物質傀儡" in text and "第9期" in text
    assert not app.exception and "player_profile" not in app.session_state


def test_search_shows_answer_numbers_without_opening_article():
    app = AppTest.from_file(APP).run()
    by_label(app.text_input, "搜尋攻略").set_value("暗物質黃5").run()
    assert "guide" not in app.query_params
    text = " ".join(item.value for item in app.markdown)
    assert "10%" in text and "黃5" in text


def test_search_with_category_survives_reading_roundtrip():
    app = AppTest.from_file(APP).run()
    by_label(app.selectbox, "攻略分類").select("收藏典藏")
    by_label(app.text_input, "搜尋攻略").set_value("召喚替身有哪些").run()
    app.button(key="home_search_collectible-sets").click().run()
    by_label(app.button, "← 搜尋結果").click().run()
    assert not app.exception
    assert by_label(app.selectbox, "攻略分類").value == "收藏典藏"
    assert by_label(app.text_input, "搜尋攻略").value == "召喚替身有哪些"
