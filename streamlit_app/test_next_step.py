import json
import pytest

from next_step import recommend, clean_profile, parse_stars, export_profile, import_profile


def test_unknown_is_not_zero_or_free_recommendation():
    assert recommend({})["primary"] is None
    assert clean_profile({})["awakening_cores"] is None
    p = {"survivor": "維納托", "awakening": 6}
    result = recommend(p)["primary"]
    assert result["id"] == "venato"
    assert result["status"] == "待核對材料"


@pytest.mark.parametrize("cores,shards,quantum,status", [
    (30, 550, True, "材料已足"), (29, 550, True, "先存資源"),
    (30, 549, True, "先存資源"), (30, 550, False, "先存資源"),
    (30, None, True, "待核對材料"),
])
def test_venato_all_resources_required(cores, shards, quantum, status):
    r = recommend({"survivor": "維納托", "awakening": 6,
        "awakening_cores": cores, "s_shards": shards, "quantum_ready": quantum})
    assert r["primary"]["status"] == status
    assert r["primary"]["target"] == "維納托覺醒7"


def test_completed_awakening_not_recommended_again():
    r = recommend({"survivor": "維納托", "awakening": 8}, "覺醒核心")
    assert r["primary"] is None
    assert r["complete"]


def test_free_existing_slot_fill_before_spending():
    r = recommend({"slots": 8, "red_owned": 8, "red_placed": 7, "hearts": 0,
        "survivor": "維納托", "awakening": 6, "awakening_cores": 30,
        "s_shards": 550, "quantum_ready": True})
    assert r["primary"]["id"] == "hall_fill"
    assert r["primary"]["cost"] == "0 收藏之心"


def test_resources_are_not_interchangeable():
    p = {"slots": 8, "red_owned": 9, "red_placed": 8, "hearts": 0, "next_slot_cost": 1000,
        "survivor": "維納托", "awakening": 6, "awakening_cores": 30,
        "s_shards": 550, "quantum_ready": True}
    assert recommend(p)["primary"]["id"] == "venato"
    assert recommend(p, "收藏之心")["primary"]["status"] == "先存資源"


def test_second_set_boss_bonus_requires_eight_slots_and_80_stars():
    p = {"adv2": 7, "stars2": [10]*8, "advanced_hearts": 500, "advanced_cost": 200, "advanced_quote": "adv2_8"}
    result = recommend(p, "高級收藏之心")["primary"]
    assert result["id"] == "adv2_8"
    assert result["status"] == "材料已足"
    assert "BOSS" in result["effect"]
    p["stars2"][-1] = 9
    assert recommend(p, "高級收藏之心")["primary"]["status"] == "星數未達"
    p["adv2"] = 8
    r = recommend(p, "高級收藏之心")
    assert r["primary"]["id"] == "adv2_stars"
    assert not r["complete"]


def test_second_set_80_stars_preferred_when_materials_both_unknown():
    p = {"adv1": 0, "stars1": [5]*4, "adv2": 2, "stars2": [10]*8}
    assert recommend(p, "高級收藏之心")["primary"]["id"] == "adv2_3"


def test_price_cannot_leak_to_a_different_slot():
    p = {"adv2": 7, "stars2": [10]*8, "advanced_hearts": 500, "advanced_cost": 1, "advanced_quote": "adv2_1"}
    assert recommend(p, "高級收藏之心")["primary"]["status"] == "待核對材料"


def test_yellow_five_is_not_red_five():
    assert parse_stars("黃5,紅1、R5 Y3 0", 8) == [5, 6, 10, 3, 0]
    p = {"adv2": 7, "stars2": [5]*8}
    assert recommend(p)["primary"]["status"] == "星數未達"


def test_invalid_imports_and_account_counts_are_rejected():
    for raw in ([], {"slots": -1}, {"stars2": [11]}, {"slots": 3, "red_placed": 4}, {"quantum_ready": 1}):
        with pytest.raises(ValueError):
            clean_profile(raw)
    for payload in (b"{bad", b"[]", b"x"*32769, b'{"schema":99}'):
        with pytest.raises(ValueError):
            import_profile(payload)
    p = clean_profile({"survivor": "維納托", "awakening": 6})
    assert import_profile(export_profile(p).encode()) == p
    normalized = import_profile(b'{"schema":1,"profile":{"mode":null,"stars1":null}}')
    assert normalized["mode"] == "末世迴響"
    assert normalized["stars1"] == []


def test_memory_respects_equipped_neck_and_stops_at_breakpoint():
    p = {"neck": "破壞者徽記", "memory": 3}
    assert recommend(p)["primary"]["target"] == "黃5星"
    assert recommend({**p, "neck": "其他"})["primary"] is None
    assert recommend({**p, "memory": 5})["primary"]["target"] == "紅3星"
    assert recommend({**p, "memory": 8})["primary"]["target"] == "紅5星"
    assert recommend({**p, "memory": 10})["primary"] is None


def test_zone_does_not_recommend_external_spending():
    r = recommend({"mode": "新版區域行動", "survivor": "維納托", "awakening": 6})
    assert r["primary"]["id"] == "zone"
    assert not r["alternatives"]


def test_advanced_bonuses_use_all_active_stars_not_each_position_prefix():
    p = {"adv2": 2, "stars2": [2, 10, 10]}
    result = recommend(p, "高級收藏之心")["primary"]
    assert result["id"] == "adv2_3"  # 12 active stars already meet tiers 1 and 2.
    assert "22／24" in result["gap"]


def test_unopened_slots_do_not_count_as_active_stars():
    p = {"adv2": 2, "stars2": [1, 1, 1, 1, 1, 1, 1, 1]}
    result = recommend(p, "高級收藏之心")["primary"]
    assert result["id"] == "adv2_stars"
    assert "2／5" in result["gap"]


def test_free_reassignment_of_owned_stars_precedes_spending():
    p = {"adv2": 2, "stars2": [1, 1, 10, 10, 10, 10, 10, 10]}
    result = recommend(p, "高級收藏之心")["primary"]
    assert result["id"] == "adv2_rearrange"
    assert result["status"] == "現在可做"
    assert result["cost"] == "0 高級收藏之心"
    assert result["update"]["stars2"] == [10, 10, 10, 10, 10, 10, 1, 1]
    updated = {**p, **result["update"]}
    assert recommend(updated, "高級收藏之心")["primary"]["id"] == "adv2_3"


@pytest.mark.parametrize("owned,cost,ready,status", [
    (3, 3, True, "材料已足"), (2, 3, True, "先存資源"),
    (99, 3, None, "待核對材料"), (99, 3, False, "先存資源"),
    (99, None, True, "待核對材料"), (None, 3, True, "待核對材料"),
])
def test_collection_costs_require_compatible_box_and_full_recipe(owned, cost, ready, status):
    p = {"neck": "破壞者徽記", "memory": 3, "red_boxes": owned}
    key = recommend(p)["primary"]["quote_key"]
    p["step_quotes"] = {key: {"cost": cost, "materials_ready": ready}}
    result = recommend(p)["primary"]
    assert result["status"] == status


def test_quote_never_leaks_to_a_new_star_target_or_another_character():
    p = {"neck": "破壞者徽記", "memory": 3, "red_boxes": 99}
    key = recommend(p)["primary"]["quote_key"]
    p["step_quotes"] = {key: {"cost": 1, "materials_ready": True}}
    assert recommend(p)["primary"]["status"] == "材料已足"
    assert recommend({**p, "memory": 5})["primary"]["status"] == "待核對材料"
    assert recommend({**p, "memory": 4})["primary"]["status"] == "待核對材料"
    assert recommend({**p, "survivor": "塔洛莎"})["primary"]["status"] == "待核對材料"


def test_quotes_are_validated_and_exported_without_breaking_old_backups():
    key = "a" * 24
    for quotes in ([], {"bad": {}}, {key: {"cost": -1, "materials_ready": True}},
                   {key: {"cost": True, "materials_ready": True}},
                   {key: {"cost": 1, "materials_ready": 1}}, {key: {"cost": 1}}):
        with pytest.raises(ValueError):
            clean_profile({"step_quotes": quotes})
    p = clean_profile({"step_quotes": {key: {"cost": 3, "materials_ready": True}}})
    assert import_profile(export_profile(p).encode()) == p
    assert import_profile(b'{"schema":1,"profile":{}}')["step_quotes"] == {}


def test_red_unlock_updates_ownership_and_slot_in_one_action():
    result = recommend({"slots": 3, "red_owned": 2, "red_placed": 2, "neck": "破壞者徽記", "memory": 0})
    assert result["primary"]["id"] == "red_unlock"
    assert result["primary"]["update"] == {"red_owned": 3, "red_placed": 3, "memory": 1}


def test_drone_collectible_route_is_conditional_and_stops_at_each_breakpoint():
    for current, target in ((0, "黃3星"), (3, "黃5星"), (5, "紅3星"), (8, "紅5星")):
        r = recommend({"twin_drone": True, "dark_matter": current}, "傳奇收藏自選")["primary"]
        assert r["id"] == "dark_matter"
        assert r["target"] == target
    assert recommend({"twin_drone": True, "dark_matter": 10}, "傳奇收藏自選")["primary"] is None
    assert recommend({"dark_matter": 0}, "傳奇收藏自選")["primary"] is None


def test_shortfall_reports_core_and_shard_gaps_together():
    r = recommend({"survivor": "維納托", "awakening": 6, "awakening_cores": 20,
                   "s_shards": 500, "quantum_ready": True})["primary"]
    assert "還差 10" in r["gap"]
    assert "角色碎片：500／550，還差 50" in r["gap"]


@pytest.mark.parametrize("cores,shards,quantum,expected", [
    (0, None, None, "先存資源"), (None, 0, None, "先存資源"),
    (None, None, False, "先存資源"), (30, None, True, "待核對材料"),
    (None, 550, True, "待核對材料"), (30, 550, None, "待核對材料"),
    (30, 550, True, "材料已足"),
])
def test_readiness_keeps_known_shortages_visible(cores, shards, quantum, expected):
    step = recommend({"survivor": "維納托", "awakening": 6, "awakening_cores": cores,
                      "s_shards": shards, "quantum_ready": quantum})["primary"]
    assert step["status"] == expected
    assert len(step["checks"]) == 3
    assert (all(c["state"] == "ready" for c in step["checks"])) == (expected == "材料已足")


def test_zero_required_resource_is_not_the_same_as_unknown_cost():
    p = {"neck": "破壞者徽記", "memory": 3}
    key = recommend(p)["primary"]["quote_key"]
    p["step_quotes"] = {key: {"cost": 0, "materials_ready": True}}
    assert recommend(p)["primary"]["status"] == "材料已足"
    assert clean_profile(p)["red_boxes"] is None
    p["step_quotes"][key]["cost"] = None
    assert recommend(p)["primary"]["status"] == "待核對材料"


@pytest.mark.parametrize("opened,stars", [(1, [10]), (3, [10, 10])])
def test_missing_star_positions_are_unknown_not_zero(opened, stars):
    step = recommend({"adv2": opened, "stars2": stars}, "高級收藏之心")["primary"]
    assert step["status"] == "資料未齊"
    assert "填" in step["gap"]


def test_explicit_unowned_star_position_remains_a_real_shortage():
    step = recommend({"adv2": 1, "stars2": [10, 0]}, "高級收藏之心")["primary"]
    assert step["status"] == "星數未達"


def test_equipment_shortage_is_not_hidden_by_unknown_other_materials():
    step = recommend({"weapon": "雙絕槍", "weapon_e": 0, "relic_cores": 0})["primary"]
    assert step["status"] == "先存資源"
    assert [c["state"] for c in step["checks"]] == ["short", "unknown"]
