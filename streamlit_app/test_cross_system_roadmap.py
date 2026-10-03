"""Cross-system sequencing, completed role goals and conservative pet coverage."""
from copy import deepcopy

import pytest
import next_step as engine
from test_decision_ui import boot, by_label


def pet(**extra):
    return {"pet_kind": "異世寵物", "pet_skills_ready": True,
            "pet_target": "測試主戰寵・下一個覺醒節點", "pet_gain": "主人增傷／有效增益",
            "pet_materials_ready": True, **extra}


def test_finished_character_moves_to_other_systems_without_forcing_r8():
    p = {"survivor": "維納托", "awakening": 6, "awakening_goal": 6, "taloxa": 4,
         "awakening_cores": 99, "s_shards": 999, "quantum_ready": True, **pet()}
    plan = engine.roadmap(p)
    assert plan["primary"]["id"] == "pet_node"
    assert all(s["id"] != "venato" for s in plan["queue"])
    assert any("暫停" in x for x in plan["complete"])


def test_finished_main_does_not_silence_support_character():
    p = {"survivor": "維納托", "awakening": 6, "awakening_goal": 6,
         "taloxa": 1, "drone_red": True}
    assert engine.recommend(p, "覺醒核心")["primary"]["id"] == "taloxa4"


def test_ready_collection_precedes_pet_after_role_goal_completed():
    p = {"survivor": "維納托", "awakening": 6, "awakening_goal": 6, "taloxa": 4,
         "drone_red": True, "dark_matter": 3, "red_boxes": 10, **pet()}
    key = engine.recommend(p, "傳奇收藏自選")["primary"]["quote_key"]
    p["step_quotes"] = {key: {"cost": 5, "materials_ready": True}}
    q = engine.roadmap(p)["queue"]
    assert [s["system"] for s in q[:2]] == ["收藏品", "寵物"]
    first = engine.following_step(p, q[0])
    assert first["id"] == "pet_node"  # Old collection quote cannot leak to a later star.


def test_ordered_queue_keeps_systems_unique_and_free_actions_first():
    p = {"slots": 4, "red_owned": 4, "red_placed": 3,
         "weapon": "雙絕槍", "weapon_e": 0, "relic_cores": 1, "gear_materials_ready": True,
         "survivor": "維納托", "awakening": 6, "awakening_cores": 30,
         "s_shards": 550, "quantum_ready": True, "drone_red": True, "dark_matter": 1, **pet()}
    q = engine.roadmap(p)["queue"]
    assert [s["id"] for s in q[:4]] == ["hall_fill", "lance_e1", "venato", "pet_node"]
    assert q[-1]["system"] == "收藏品" and q[-1]["status"] == "待核對材料"
    assert [s["rank"] for s in q] == list(range(1, len(q)+1))
    assert len({s["system"] for s in q}) == len(q)


def test_after_completion_preview_is_pure_and_uses_remaining_materials():
    p = {"survivor": "維納托", "awakening": 6, "awakening_goal": 7, "taloxa": 4,
         "awakening_cores": 30, "s_shards": 550, "quantum_ready": True, **pet()}
    before = deepcopy(p)
    first = engine.recommend(p)["primary"]
    assert first["id"] == "venato"
    after = engine.following_step(p, first)
    assert after["id"] == "pet_node"
    assert p == before
    updated = engine.completion_preview(p, first)["profile"]
    assert updated["awakening"] == 7 and updated["awakening_cores"] == 0
    assert engine.recommend(updated)["primary"]["id"] == "pet_node"


@pytest.mark.parametrize("ready,status", [(None, "待核對材料"), (False, "先存資源"), (True, "材料已足")])
def test_pet_requires_player_confirmed_full_recipe(ready, status):
    s = engine.recommend(pet(pet_materials_ready=ready))["primary"]
    assert s["status"] == status and s["checks"]


def test_pet_unknown_is_not_absent_or_an_automatic_purchase():
    assert engine.recommend({})["primary"] is None
    assert engine.recommend({"pet_kind": "未持有"})["primary"] is None
    assert engine.recommend(pet(pet_target="  "))["primary"] is None
    assert engine.recommend(pet(pet_gain="只有面板／尚未確認"))["primary"] is None
    assert engine.recommend(pet(pet_skills_ready=None))["primary"]["id"] == "pet_skills"


def test_pet_completion_invalidates_old_goal_without_touching_character_stock():
    p = pet(awakening_cores=20)
    s = engine.recommend(p)["primary"]
    updated = engine.completion_preview(p, s)["profile"]
    assert updated["pet_target"] is None and updated["pet_materials_ready"] is None
    assert updated["awakening_cores"] == 20
    with pytest.raises(ValueError):
        engine.completion_preview(updated, s)


def test_old_backup_unknown_fields_and_new_backup_roundtrip():
    p = engine.import_profile(b'{"schema":1,"profile":{"awakening":6}}')
    assert p["awakening_goal"] is None and p["pet_kind"] is None
    assert engine.import_profile(engine.export_profile(pet()).encode()) == engine.clean_profile(pet())
    with pytest.raises(ValueError):
        engine.clean_profile(pet(pet_materials_ready=1))


def test_ui_pause_role_exposes_pet_and_completion_recalculates():
    a = boot()
    a.session_state["player_profile"] = {"survivor": "維納托", "awakening": 6, "taloxa": 4, **pet()}
    a.run()
    by_label(a.button, "角色先停在 R6，比較其他系統").click().run()
    assert not a.exception
    assert a.session_state["player_profile"]["awakening_goal"] == 6
    text = "\n".join(m.value for m in a.markdown if "<style>" not in m.value)
    assert "跨系統優先順序" in text and "寵物：測試主戰寵" in text
    assert "維納托 R6 → R7" not in text
    by_label(a.button, "我已在遊戲完成，排下一步").click().run()
    assert not a.exception
    assert a.session_state["player_profile"]["pet_target"] is None
    assert a.session_state["player_profile"]["awakening"] == 6


def test_visible_global_queue_survives_resource_filter_and_can_open_second_step():
    a = boot()
    a.session_state["player_profile"] = {"slots": 2, "red_owned": 2, "red_placed": 1, **pet()}
    a.run()
    by_label(a.selectbox, "這次要安排的資源").set_value("收藏之心").run()
    assert any("寵物：測試主戰寵" in m.value for m in a.markdown)
    by_label(a.button, "看 2").click().run()
    assert not a.exception
    assert by_label(a.selectbox, "這次要安排的資源").value == "自動排序"
    assert any("正在查看其他順位" in e.value for e in a.info)
    assert a.session_state["player_profile"]["red_placed"] == 1
