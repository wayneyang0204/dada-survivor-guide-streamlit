"""Explicit effect gates, goal-aware priorities and bounded cost comparison."""
from copy import deepcopy
import pytest
import next_step as engine
from test_decision_ui import boot, by_label


def quoted(p, sid, cost):
    p = deepcopy(p)
    result = engine.recommend(p)
    candidates = ([result["primary"]] if result["primary"] else []) + result["alternatives"]
    step = next(s for s in candidates if s["id"] == sid)
    p.setdefault("step_quotes", {})[step["quote_key"]] = {"cost": cost, "materials_ready": True}
    return p


@pytest.mark.parametrize("useful,expected", [(None, "待核對材料"), (True, "材料已足"), (False, None)])
def test_crit_benefit_not_inferred_from_materials_or_panel(useful, expected):
    p = quoted({"neck": "破壞者徽記", "memory": 3, "red_boxes": 10}, "memory", 2)
    p.update(crit_more_useful=useful, crit_mode="末世迴響")
    result = engine.recommend(p)
    assert (result["primary"]["status"] if result["primary"] else None) == expected
    if useful is False:
        assert result["deferred"][0]["id"] == "memory"


def test_crit_decision_is_mode_scoped_and_does_not_hide_later_crit_damage():
    p = {"neck": "破壞者徽記", "memory": 3, "crit_more_useful": False, "crit_mode": "末世迴響"}
    assert engine.recommend(p)["primary"] is None
    r = engine.recommend({**p, "mode": "遠征／月礦首領"})
    assert r["primary"]["id"] == "memory" and not r["deferred"]
    assert engine.next_question({**p, "mode": "遠征／月礦首領"})["field"] == "crit_more_useful"
    assert engine.recommend({**p, "memory": 5})["primary"]["effect"] == "暴擊傷害＋10%"


@pytest.mark.parametrize("ready,status", [(None, "待核對材料"), (True, "材料已足"), (False, None)])
def test_ss_boots_effect_requires_ice_armor_even_with_recipe_ready(ready, status):
    p = quoted({"ss_boots": True, "boot_stars": [2, 3, 3, 3], "red_boxes": 10}, "boots_set", 2)
    p["ice_armor_ready"] = ready
    r = engine.recommend(p)
    assert (r["primary"]["status"] if r["primary"] else None) == status
    if ready is False:
        assert "冰甲" in r["deferred"][0]["reason"]


def test_effect_guard_cannot_be_bypassed_by_resource_filter_or_stale_completion():
    p = quoted({"ss_boots": True, "boot_stars": [2]*4, "red_boxes": 10, "ice_armor_ready": True}, "boots_set", 2)
    old = engine.recommend(p)["primary"]
    p["ice_armor_ready"] = False
    assert engine.recommend(p, "傳奇收藏自選")["primary"] is None
    with pytest.raises(ValueError):
        engine.completion_preview(p, old)


def test_only_same_ready_bonus_uses_cheaper_full_quote():
    p = {"neck": "破壞者徽記", "memory": 5, "drone_red": True, "dark_matter": 5, "red_boxes": 10}
    p = quoted(quoted(p, "memory", 2), "dark_matter", 7)
    before = deepcopy(p)
    assert engine.recommend(p)["primary"]["id"] == "memory"
    assert "較省箱" in engine.recommend(p)["primary"]["why"]
    assert p == before
    p = quoted(p, "dark_matter", 1)
    assert engine.recommend(p)["primary"]["id"] == "dark_matter"


def test_different_effects_unknown_cost_and_ties_keep_normal_rules():
    base = {"neck": "破壞者徽記", "memory": 5, "drone_red": True, "dark_matter": 5, "red_boxes": 10}
    only = quoted(base, "memory", 2)
    assert "較省箱" not in engine.recommend(only)["primary"]["why"]
    tied = quoted(only, "dark_matter", 2)
    assert engine.recommend(tied)["primary"]["id"] == "dark_matter"
    different = {**base, "dark_matter": 3}
    different = quoted(quoted(different, "memory", 1), "dark_matter", 5)
    assert engine.recommend(different)["primary"]["id"] == "dark_matter"


def test_slow_skill_goal_changes_priority_without_beating_free_actions():
    p = {"weapon": "雙絕槍", "weapon_e": 0, "relic_cores": 1, "gear_materials_ready": True,
         "survivor": "維納托", "awakening": 6, "awakening_cores": 30, "s_shards": 550, "quantum_ready": True,
         "slots": 3, "red_owned": 4, "red_placed": 3, "hearts": 100, "next_slot_cost": 10}
    assert engine.recommend(p)["primary"]["id"] == "hall_open"
    p["growth_focus"] = "技能成形太慢"
    assert engine.recommend(p)["primary"]["id"] == "lance_e1"
    p["red_placed"] = 2
    assert engine.recommend(p)["primary"]["id"] == "hall_fill"


def test_survival_problem_promotes_diagnosis_not_paid_damage():
    p = {"growth_focus": "生存不足", "survivor": "維納托", "awakening": 6,
         "awakening_cores": 30, "s_shards": 550, "quantum_ready": True}
    r = engine.recommend(p)
    assert r["primary"]["id"] == "survival_check" and r["primary"]["update"] is None
    assert r["alternatives"][0]["id"] == "venato"
    assert engine.next_question(p) is None
    assert engine.recommend({**p, "slots": 2, "red_owned": 2, "red_placed": 1})["primary"]["id"] == "hall_fill"
    assert engine.recommend({**p, "mode": "新版區域行動"})["primary"]["id"] == "zone"


def test_question_targets_decision_condition_before_more_inventory():
    p = {"neck": "破壞者徽記", "memory": 3}
    assert engine.next_question(p)["field"] == "crit_more_useful"
    p.update(crit_more_useful=True, crit_mode="末世迴響")
    assert engine.next_question(p)["field"] == "hall_counts"
    p.update(slots=2, red_owned=2, red_placed=1)
    assert engine.next_question(p) is None


def test_legacy_backup_default_focus_and_unknown_effects():
    p = engine.clean_profile({"growth_focus": None})
    assert p["growth_focus"] == engine.FOCUSES[0]
    assert p["ice_armor_ready"] is None and p["crit_more_useful"] is None
    assert engine.import_profile(engine.export_profile(p).encode()) == p
    for invalid in ({"growth_focus": "自動付費"}, {"crit_more_useful": 1}, {"ice_armor_ready": 0}):
        with pytest.raises(ValueError):
            engine.clean_profile(invalid)


def test_ui_effect_confirmation_recalculates_and_never_duplicates_form():
    a = boot()
    a.session_state["player_profile"] = {"survivor": "維納托", "awakening": 8, "neck": "破壞者徽記", "memory": 3}
    a.run()
    assert len(a.get("form")) == 1
    by_label(a.selectbox, "目前模式追加暴率仍有收益（含溢出轉換）").set_value(False)
    by_label(a.button, "更新這一步的材料").click().run()
    assert not a.exception
    text = "\n".join(m.value for m in a.markdown if "<style>" not in m.value)
    assert "先不投入" in text and "暴率沒有收益" in text
    assert a.session_state["player_profile"]["memory"] == 3
    by_label(a.selectbox, "目前最想解決的問題").set_value("生存不足").run()
    assert not a.exception
    assert any("先找出死亡原因" in m.value for m in a.markdown)
