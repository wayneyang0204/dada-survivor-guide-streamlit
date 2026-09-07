"""Resource accounting and explainable, target-bound record transitions."""
import copy

import pytest

from next_step import action_token, clean_profile, completion_preview, export_profile, import_profile, ranking_reason, recommend


def test_known_costs_preserve_exact_zero_and_label_inferred_balances():
    p = {"survivor": "維納托", "awakening": 6, "awakening_cores": 30, "s_shards": 600, "quantum_ready": True}
    before = copy.deepcopy(p)
    step = recommend(p)["primary"]
    result = completion_preview(p, step)
    after = result["profile"]
    assert p == before
    assert after["awakening_cores"] == 0
    assert after["s_shards"] == 50
    assert after["quantum_ready"] is None
    assert after["estimated_balances"] == ["awakening_cores", "s_shards"]
    assert len(result["balances"]) == 2
    assert action_token(p, step) != action_token(after, recommend(after)["primary"])


@pytest.mark.parametrize("stock", [None, 0, 29])
def test_old_or_insufficient_stock_is_not_clamped_or_invented(stock):
    p = {"survivor": "維納托", "awakening": 6, "awakening_cores": stock}
    result = completion_preview(p, recommend(p)["primary"])
    assert result["profile"]["awakening"] == 7  # Player reports actual completion.
    assert result["profile"]["awakening_cores"] is None
    assert "覺醒核心" in result["unknown"]
    assert "awakening_cores" not in result["profile"]["estimated_balances"]


def test_slot_cost_is_consumed_once_and_next_slot_price_invalidated():
    p = {"slots": 3, "red_owned": 5, "red_placed": 3, "hearts": 3000, "next_slot_cost": 1000}
    step = recommend(p)["primary"]
    after = completion_preview(p, step)["profile"]
    assert after["hearts"] == 2000
    assert after["slots"] == 4
    assert after["next_slot_cost"] is None
    assert recommend(after)["primary"]["status"] == "待核對材料"
    with pytest.raises(ValueError):
        completion_preview(after, step)  # Old action cannot be applied twice.


def test_unknown_slot_price_never_means_free():
    p = {"slots": 3, "red_owned": 4, "red_placed": 3, "hearts": 1000}
    after = completion_preview(p, recommend(p)["primary"])["profile"]
    assert after["hearts"] is None


def test_collection_requires_valid_current_recipe_to_keep_remaining_boxes():
    p = {"neck": "破壞者徽記", "memory": 3, "red_boxes": 5}
    key = recommend(p)["primary"]["quote_key"]
    p["step_quotes"] = {key: {"cost": 2, "materials_ready": True}}
    after = completion_preview(p, recommend(p)["primary"])["profile"]
    assert after["red_boxes"] == 3
    assert after["memory"] == 5
    assert after["step_quotes"] == {}
    assert recommend(after)["primary"]["status"] == "待核對材料"
    p["step_quotes"][key]["materials_ready"] = False
    assert completion_preview(p, recommend(p)["primary"])["profile"]["red_boxes"] is None


def test_free_actions_preserve_balances_and_unrelated_quotes():
    p = {"slots": 3, "red_owned": 3, "red_placed": 2, "hearts": 123,
         "step_quotes": {"a"*24: {"cost": 1, "materials_ready": True}}, "red_boxes": 3}
    result = completion_preview(p, recommend(p)["primary"])
    assert result["profile"]["hearts"] == 123
    assert result["profile"]["red_boxes"] == 3
    assert result["profile"]["step_quotes"] == p["step_quotes"]
    assert not result["balances"]


def test_bundle_quote_and_completion_cover_every_missing_member_only():
    p = {"ss_boots": True, "boot_stars": [0, 0, 2, 8], "red_owned": 5, "red_boxes": 10}
    step = recommend(p)["primary"]
    assert "四件" in step["title"]
    assert "3 件" in step["why"]
    assert step["update"] == {"boot_stars": [3, 3, 3, 8]}
    p["step_quotes"] = {step["quote_key"]: {"cost": 6, "materials_ready": True}}
    after = completion_preview(p, recommend(p)["primary"])["profile"]
    assert after["red_boxes"] == 4
    assert after["boot_stars"] == [3, 3, 3, 8]
    assert after["red_owned"] == 7
    assert recommend(after, "傳奇收藏自選")["primary"] is None


def test_modified_or_stale_milestone_is_rejected():
    p = {"survivor": "維納托", "awakening": 6}
    step = recommend(p)["primary"]
    with pytest.raises(ValueError):
        completion_preview(p, {**step, "update": {"awakening": 8}})
    with pytest.raises(ValueError):
        completion_preview({**p, "awakening": 7}, step)


def test_estimate_provenance_round_trips_and_validates():
    p = clean_profile({"hearts": 100, "estimated_balances": ["hearts", "hearts", "s_shards"]})
    assert p["estimated_balances"] == ["hearts"]
    assert import_profile(export_profile(p).encode()) == p
    assert import_profile(b'{"schema":1,"profile":{}}')["estimated_balances"] == []
    for value in ([True], ["unknown"], {}, "hearts"):
        with pytest.raises(ValueError):
            clean_profile({"estimated_balances": value})


def test_ranking_explanation_uses_actual_readiness_comparison():
    p = {"slots": 3, "red_owned": 4, "red_placed": 3, "hearts": 1000, "next_slot_cost": 1000,
         "survivor": "維納托", "awakening": 6}
    reason = ranking_reason(recommend(p))
    assert "維納托" in reason
    assert "待核對材料" in reason
    assert "能完成" in reason


def test_single_candidate_does_not_claim_a_global_optimum():
    reason = ranking_reason(recommend({"survivor": "維納托", "awakening": 6}))
    assert "唯一" in reason
    assert "不代表" in reason
