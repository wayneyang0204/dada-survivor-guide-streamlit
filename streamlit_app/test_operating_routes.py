"""Concrete operations and dated tech tables never bypass readiness or profiles."""
from copy import deepcopy
import pytest
from streamlit.testing.v1 import AppTest

import next_step as engine
import guide_content as content
from direction_tools import operating_steps
from tech_routes import TECH_ROUTES, next_tech_effect
from test_decision_ui import APP, boot, by_label


@pytest.mark.parametrize("sid,fragment", [
    ("venato", "維納托"), ("venato6", "維納托"), ("taloxa4", "戰術協議"),
    ("hall_fill", "確認擺入"), ("hall_open", "試煉之路"), ("red_unlock", "原生傳奇"),
    ("adv1_rearrange", "不借另一套"), ("adv2_stars", "先不買"),
    ("adv2_8", "高級收藏之心"), ("memory", "破壞者徽記"),
    ("dark_matter", "暗物質傀儡"), ("boots_set", "基因編輯器"),
    ("lance_e1", "永恆1階"), ("twin_drone", "能量收集器"), ("zone", "不推薦花覺醒核心"),
])
def test_each_supported_rule_has_an_entry_and_three_concrete_steps(sid, fragment):
    step = {"id": sid, "status": "待核對材料", "target": "目標",
            "current": "基因編輯器 黃2→黃3"}
    old = deepcopy(step)
    plan = operating_steps(step)
    assert plan["entry"] and len(plan["steps"]) == 3
    assert fragment in " ".join(plan["steps"])
    assert step == old
    assert "完整材料已足" not in " ".join(plan["steps"])


def test_actual_boots_plan_names_only_missing_members():
    raw = {"ss_boots": True, "boot_stars": [3, 5, 3, 2]}
    step = engine.recommend(raw, "傳奇收藏自選")["primary"]
    text = " ".join(operating_steps(step)["steps"])
    assert "基因編輯器 黃2→黃3" in text
    assert "賽博圖騰柱 黃3→" not in text
    assert "部分完成只更新實際星級" in text


@pytest.mark.parametrize("part,energy,target,gap", [
    ("雙生雷電（雷電態）", 1600, 1650, 50),
    ("雙生雷電（雷電態）", 1650, 2550, 900),
    ("雙生無人機（無人機態）", 3000, 4500, 1500),
    ("雙生無人機（無人機態）", 899, 900, 1),
])
def test_next_selected_effect_is_strictly_above_current_energy(part, energy, target, gap):
    waiting = next_tech_effect(part, energy)
    assert waiting["target"] == target and waiting["gap"] == gap
    assert waiting["state"] == "verify" and "先對照遊戲" in waiting["action"]
    candidate = next_tech_effect(part, energy, True)
    assert candidate["state"] == "candidate"
    assert "到這檔先停" in candidate["action"]
    assert "不得拆掉" in candidate["stop"]


@pytest.mark.parametrize("part,energy,state", [
    (None, 1600, "unknown"), ("普通雷電", 1600, "unknown"),
    ("雙生雷電（雷電態）", None, "unknown"), ("雙生雷電（雷電態）", 4500, "outside"),
    ("雙生雷電（雷電態）", -1, "invalid"), ("雙生雷電（雷電態）", True, "invalid"),
])
def test_unknown_ordinary_and_beyond_table_do_not_get_an_invented_target(part, energy, state):
    result = next_tech_effect(part, energy, True)
    assert result["state"] == state and "target" not in result


def test_effect_table_and_calculator_share_the_same_source_rows():
    guide = content.get_guide("twin-tech-milestones", content.GUIDES)
    for section, route in zip(guide["sections"], TECH_ROUTES.values()):
        assert section["rows"] == [[str(n), effect] for n, effect in route["milestones"]]
        assert route["source"] in [url for _, url in guide["sources"]]
    assert "2025" in guide["editorial_note"] or "來源" in guide["editorial_note"]


def test_article_calculator_uses_correct_shape_and_keeps_account_untouched():
    a = AppTest.from_file(APP)
    profile = {"survivor": "維納托", "awakening": 6}
    a.session_state["player_profile"] = deepcopy(profile)
    a.query_params["guide"] = "twin-tech-milestones"
    a.run()
    by_label(a.selectbox, "目前使用的雙生形態").select("雙生雷電（雷電態）").run()
    by_label(a.number_input, "這件目前的諧振能量").set_value(1600).run()
    assert any("還差 50 能量" in item.value for item in a.info)
    assert "先對照遊戲" in "\n".join(item.value for item in a.markdown)
    by_label(a.checkbox, "我已對照遊戲，下一檔效果與來源表一致").check().run()
    assert not a.exception
    assert "能量補至 1,650" in "\n".join(item.value for item in a.markdown)
    assert a.session_state["player_profile"] == profile
    assert not a.get("form")
    by_label(a.selectbox, "目前使用的雙生形態").select("雙生無人機（無人機態）").run()
    assert not by_label(a.checkbox, "我已對照遊戲，下一檔效果與來源表一致").value
    assert "先對照遊戲" in "\n".join(item.value for item in a.markdown)


def test_planner_shows_game_entry_without_marking_upgrade_done():
    a = boot()
    raw = {"survivor": "維納托", "awakening": 6, "awakening_cores": 20, "s_shards": 400}
    a.session_state["player_profile"] = deepcopy(raw)
    a.run()
    text = "\n".join(item.value for item in a.markdown)
    assert "遊戲入口：" in text and "角色的覺醒頁" in text
    assert "不使用其他角色的報價" in text
    assert a.session_state["player_profile"] == raw


@pytest.mark.parametrize("query", ["雙生雷電1600", "雷電1650", "相位輔助器"])
def test_tech_effect_queries_find_the_specific_table_first(query):
    assert content.search_guides(content.GUIDES, query)[0]["slug"] == "twin-tech-milestones"


def test_warm_cloud_cache_refreshes_leaf_helpers_before_new_consumers(monkeypatch):
    import direction_tools
    import tech_routes
    import field_tools
    # Model a prior helper version in the same long-lived Python process.
    monkeypatch.delattr(direction_tools, "operating_steps")
    monkeypatch.delattr(tech_routes, "next_tech_effect")
    monkeypatch.delattr(field_tools, "pet_milestone")
    monkeypatch.delattr(field_tools, "event_window")
    a = AppTest.from_file(APP)
    a.query_params["guide"] = "twin-tech-milestones"
    a.run(timeout=15)
    assert not a.exception
    assert callable(direction_tools.operating_steps)
    assert callable(tech_routes.next_tech_effect)
    assert callable(field_tools.pet_milestone) and callable(field_tools.event_window)
    assert any("雙生無人機／雷電諧振" in item.value for item in a.markdown)
