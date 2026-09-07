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
    assert recommend({**p, "memory": 5})["primary"] is None


def test_zone_does_not_recommend_external_spending():
    r = recommend({"mode": "新版區域行動", "survivor": "維納托", "awakening": 6})
    assert r["primary"]["id"] == "zone"
    assert not r["alternatives"]
