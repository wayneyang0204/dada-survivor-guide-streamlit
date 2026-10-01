"""Actionable summaries, guide routing and unknown-safe threshold calculations."""
from copy import deepcopy

import pytest
from streamlit.testing.v1 import AppTest

import guide_content as content
import next_step as engine
from direction_tools import execution_plan, resonance_gap
from test_decision_ui import APP, boot, by_label


def test_action_plan_names_all_shortages_and_unknown_conditions():
    raw = {"survivor": "維納托", "awakening": 6, "taloxa": 4,
           "awakening_cores": 20, "s_shards": 400}
    original = deepcopy(raw)
    step = engine.recommend(raw, "覺醒核心")["primary"]
    plan = execution_plan(step)
    assert "覺醒核心缺 10" in plan["action"]
    assert "角色碎片缺 150" in plan["action"]
    assert "量子" in plan["verify"]
    assert "不要按升級" in plan["action"]
    assert plan["stop"] == step["stop"]
    assert raw == original


def test_action_plan_requires_all_materials_before_ready():
    raw = {"survivor": "維納托", "awakening": 6, "taloxa": 4,
           "awakening_cores": 30, "s_shards": 550}
    waiting = execution_plan(engine.recommend(raw, "覺醒核心")["primary"])
    assert "先打開遊戲升級預覽" in waiting["action"]
    assert "先完成" not in waiting["action"]
    raw["quantum_ready"] = True
    ready = execution_plan(engine.recommend(raw, "覺醒核心")["primary"])
    assert "先完成" in ready["action"] and "覺醒7" in ready["action"]


def test_free_action_and_mode_adjustment_do_not_claim_material_upgrade():
    step = engine.recommend({"slots": 3, "red_owned": 2, "red_placed": 1})["primary"]
    assert step["id"] == "hall_fill"
    assert "填滿" in execution_plan(step)["action"]
    zone = engine.recommend({"mode": "新版區域行動"})["primary"]
    assert "先不花局外養成材料" in execution_plan(zone)["action"]


@pytest.mark.parametrize("current,target,state,fragment", [
    (None, 1700, "unknown", "空白"), (1600, None, "unknown", "空白"),
    (1600, 1700, "short", "100"), (3000, 3000, "reached", "已達到"),
    (3000, 1650, "reached", "已達到"), (0, 50, "short", "50"),
    (-1, 50, "invalid", "不能小於"), (0, 0, "invalid", "大於"),
])
def test_resonance_gap_does_not_assume_a_fixed_next_threshold(current, target, state, fragment):
    result = resonance_gap(current, target)
    assert result["state"] == state and fragment in result["message"]


@pytest.mark.parametrize("query,slug", [
    ("下一步先升什麼", "upgrade-roadmap"),
    ("紅色自選箱要選什麼", "red-choice-box"),
    ("諧振要升多少", "resonance-planning"),
    ("無人機3000", "twin-tech-milestones"),
])
def test_new_decision_questions_have_a_relevant_first_result(query, slug):
    assert content.search_guides(content.GUIDES, query)[0]["slug"] == slug


def test_result_has_clear_action_and_opens_relevant_guide_without_mutation():
    a = boot()
    profile = {"survivor": "維納托", "awakening": 6, "taloxa": 4,
               "awakening_cores": 20, "s_shards": 400}
    a.session_state["player_profile"] = deepcopy(profile)
    a.run()
    assert not a.exception
    text = "\n".join(item.value for item in a.markdown)
    assert "現在就做這一件" in text and "核心缺 10" in text and "碎片缺 150" in text
    by_label(a.button, "看這一步的做法與取捨").click().run()
    assert not a.exception
    assert a.query_params["guide"] == ["survivor-awakening"]
    assert a.session_state["player_profile"] == profile


def test_resonance_calculator_preserves_profile_and_values_across_scenario_selection():
    a = AppTest.from_file(APP)
    profile = {"survivor": "維納托", "awakening": 6}
    a.session_state["player_profile"] = deepcopy(profile)
    a.query_params["guide"] = "resonance-planning"
    a.run()
    assert not a.exception
    assert [item.value for item in a.number_input] == [None, None]
    by_label(a.number_input, "目前諧振能量").set_value(1600).run()
    by_label(a.number_input, "遊戲顯示的目標能量").set_value(1700).run()
    assert any("還差 100 諧振能量" in item.value for item in a.info)
    by_label(a.selectbox, "選擇目前狀況").select_index(2).run()
    assert not a.exception
    assert "下一檔一定是1650" in "\n".join(item.value for item in a.markdown)
    assert by_label(a.number_input, "目前諧振能量").value == 1600
    assert a.session_state["player_profile"] == profile


def test_roadmap_can_open_planner_without_forcing_a_resource_or_profile():
    a = AppTest.from_file(APP)
    a.query_params["guide"] = "upgrade-roadmap"
    a.run()
    by_label(a.button, "用我的配置找下一個門檻").click().run()
    assert not a.exception
    assert a.radio[0].value == "下一步"
    assert "guide" not in a.query_params
    assert "player_profile" not in a.session_state


def test_general_roadmap_resets_stale_resource_filter_but_keeps_account():
    a = AppTest.from_file(APP)
    profile = {"survivor": "維納托", "awakening": 6}
    a.session_state["player_profile"] = deepcopy(profile)
    a.session_state["decision_resource"] = "神器核心"
    a.query_params["guide"] = "upgrade-roadmap"
    a.run()
    by_label(a.button, "用我的配置找下一個門檻").click().run()
    assert not a.exception
    assert by_label(a.selectbox, "這次要安排的資源").value == "自動排序"
    assert a.session_state["player_profile"] == profile
