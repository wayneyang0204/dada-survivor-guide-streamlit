from streamlit.testing.v1 import AppTest

import guide_content as content
from test_decision_ui import APP, by_label


def test_yellow_collectible_question_finds_epic_answer_first():
    results = content.search_guides(content.GUIDES, "黃收藏先升哪些？")
    assert results and results[0]["slug"] == "epic-collectibles"
    assert "水動推力腳蹼" in str(results[0]["sections"])


def test_natural_awakening_question_finds_materials_and_scenarios():
    results = content.search_guides(content.GUIDES, "維納托R6之後先升什麼")
    assert results and results[0]["slug"] == "survivor-awakening"
    assert "550" in str(results[0]["sections"])
    assert any("塔洛莎" in choice["condition"] for choice in results[0]["decisions"])


def test_reading_and_returning_preserves_home_search():
    app = AppTest.from_file(APP).run()
    by_label(app.text_input, "搜尋攻略").set_value("暗物質").run()
    app.button(key="home_search_collectible-breakpoints").click().run()
    by_label(app.button, "← 搜尋結果").click().run()
    assert not app.exception
    assert app.radio[0].value == "攻略首頁"
    assert by_label(app.text_input, "搜尋攻略").value == "暗物質"
    assert app.button(key="home_search_collectible-breakpoints")


def test_home_search_shows_answers_without_category_wall():
    app = AppTest.from_file(APP).run()
    assert by_label(app.selectbox, "攻略分類")
    by_label(app.text_input, "搜尋攻略").set_value("黃收藏先升哪些？").run()
    assert app.button(key="home_search_epic-collectibles")
    assert not any(str(button.key).startswith("home_topic_") for button in app.button)
    by_label(app.text_input, "搜尋攻略").set_value("").run()
    assert app.button(key="home_epic-collectibles")


def test_reading_related_article_keeps_original_search_context():
    app = AppTest.from_file(APP).run()
    app.radio[0].set_value("資料庫").run()
    by_label(app.selectbox, "攻略分類").select("收藏典藏")
    by_label(app.text_input, "搜尋本站攻略").set_value("暗物質").run()
    app.button(key="index_collectible-breakpoints").click().run()
    app.button(key="related_collection-hall").click().run()
    by_label(app.button, "← 搜尋結果").click().run()
    assert not app.exception
    assert by_label(app.text_input, "搜尋本站攻略").value == "暗物質"
    assert by_label(app.selectbox, "攻略分類").value == "收藏典藏"
    assert "guide" not in app.query_params


def test_scenario_selection_changes_answer_without_rewriting_account():
    app = AppTest.from_file(APP)
    profile = {"survivor": "維納托", "awakening": 6, "taloxa": 4, "awakening_cores": 20}
    app.session_state["player_profile"] = dict(profile)
    app.query_params["guide"] = "survivor-awakening"
    app.run()
    scenario = by_label(app.selectbox, "選擇目前狀況")
    assert scenario.value is None
    scenario.select("維納托 R6，塔洛莎已 R4").run()
    answer = next(item.value for item in app.markdown if 'aria-label="目前情境建議"' in item.value)
    assert "550" in answer and "R7" in answer
    by_label(app.selectbox, "選擇目前狀況").select("維納托 R7，塔洛莎已 R4").run()
    answer = next(item.value for item in app.markdown if 'aria-label="目前情境建議"' in item.value)
    assert "600" in answer and "550" not in answer
    assert app.session_state["player_profile"] == profile


def test_epic_answer_does_not_send_yellow_boxes_to_legendary_planner():
    app = AppTest.from_file(APP)
    app.query_params["guide"] = "epic-collectibles"
    app.run()
    by_label(app.selectbox, "選擇目前狀況").select("普通無人機是主力，腳蹼還沒到黃5").run()
    assert not app.exception
    answer = next(item.value for item in app.markdown if 'aria-label="目前情境建議"' in item.value)
    assert "水動推力腳蹼" in answer and "黃5" in answer
    assert not any(button.label == "用我的配置排升級順序" for button in app.button)
    by_label(app.button, "查完整收藏圖鑑").click().run()
    assert not app.exception
    assert by_label(app.selectbox, "要查什麼").value == "收藏圖鑑"


def test_article_resource_survives_first_time_account_setup():
    app = AppTest.from_file(APP)
    app.query_params["guide"] = "survivor-awakening"
    app.run()
    by_label(app.button, "用我的配置排升級順序").click().run()
    by_label(app.selectbox, "主位特工").select("維納托")
    by_label(app.number_input, "覺醒等級（不是一般星數）").set_value(6)
    by_label(app.button, "建立我的升級路線").click().run()
    assert not app.exception
    assert by_label(app.selectbox, "這次要安排的資源").value == "覺醒核心"
