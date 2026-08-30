from data_engine import (
    assess_event_plan,
    classify_article,
    diagnose_account,
    match_event_playbook,
    optimize_player_plan,
    rank_rewards,
    strip_html,
)


def test_strip_html_and_classification() -> None:
    assert strip_html("<p>音樂&nbsp;圓盤</p>") == "音樂 圓盤"
    assert classify_article("音樂圓盤大作戰攻略") == "活動攻略"
    assert classify_article("新版區域行動攻略") == "關卡模式"


def test_music_event_has_complete_professional_summary() -> None:
    playbook = match_event_playbook("音樂圓盤大作戰｜麥克風與音符攻略")
    assert playbook["name"] == "音樂圓盤大作戰"
    assert playbook["target"] == 980
    assert len(playbook["summary_sections"]) == 4
    assert sum(len(section["items"]) for section in playbook["summary_sections"]) == 16


def test_reward_ranking_respects_account_stage() -> None:
    early = rank_rewards("不確定，幫我排", "尚未紅裝成套")
    assert early[0]["name"] == "S 級裝備自選箱"
    endgame = rank_rewards("神器核心", "紅裝成套、神器核心不足")
    assert endgame[0]["name"] == "神器核心自選箱"


def test_event_assessment_covers_free_and_stop_cases() -> None:
    reward = {"gem_value": 18000, "adjusted_gem_value": 18000}
    free = assess_event_plan(
        current_progress=700,
        days_remaining=3,
        free_progress_per_day=100,
        target_progress=980,
        progress_per_paid_action=1,
        gems_per_paid_action=100,
        gems_owned=50000,
        spending_style="無課／只用免費資源",
        target_reward=reward,
    )
    assert free["verdict"] == "值得追，但不用花寶石"

    reached = assess_event_plan(
        current_progress=980,
        days_remaining=3,
        free_progress_per_day=0,
        target_progress=980,
        progress_per_paid_action=1,
        gems_per_paid_action=100,
        gems_owned=50000,
        spending_style="無課／只用免費資源",
        target_reward=reward,
    )
    assert reached["verdict"] == "已達標，立刻停手"


def test_account_diagnosis_returns_mode_specific_plan() -> None:
    result = diagnose_account(
        main_stage="塔洛莎覺醒5＋暴率70%",
        chaos_stage="混沌之力9～17",
        play_mode="長場首領",
        divine_stage="只有哪吒",
    )
    assert result["phase"] == "高端成熟期"
    assert result["build"] == "長戰疊層傷害極限"
    assert result["next_breakpoint"] == "混沌之力18"
    assert len(result["priorities"]) == 3

    zone = diagnose_account(
        main_stage="塔洛莎覺醒5＋暴率70%",
        chaos_stage="混沌之力9～17",
        play_mode="區域行動",
        divine_stage="哪吒R4＋伏爾坎R4支援鏈",
    )
    assert zone["build"] == "新版區域行動路線最優解"
    assert "不帶入局外裝備" in zone["mode_instruction"]


def _optimize(**overrides):
    values = {
        "goal": "長期帳號成長",
        "account_stage": "紅裝成套、神器核心不足",
        "play_mode": "長場首領",
        "spending_style": "無課／只用免費資源",
        "risk_style": "平衡收益",
        "horizon_days": 30,
        "gems": 50000,
        "relic_cores": 4,
        "resonance_chips": 0,
        "xeno_cores": 0,
        "awakening_cores": 0,
        "daily_minutes": 30,
    }
    values.update(overrides)
    return optimize_player_plan(**values)


def test_optimizer_prefers_relic_breakpoint_for_core_limited_boss_account() -> None:
    result = _optimize()
    assert result["best"]["id"] == "relic_breakpoint"
    assert result["best"]["feasible"] is True
    assert result["spendable_gems"] == 20000


def test_optimizer_changes_to_new_zone_route_for_zone_goal() -> None:
    result = _optimize(
        goal="區域行動穩定",
        account_stage="主要裝備斷點已完成",
        play_mode="區域行動",
        horizon_days=7,
        gems=30000,
        relic_cores=0,
        daily_minutes=25,
        risk_style="穩定優先",
    )
    assert result["best"]["id"] == "zone_stability"
    assert "局內" in result["best"]["summary"] or "區域" in result["best"]["name"]
    assert "局外面板" in result["mode_protocol"]["title"]
    assert "污染必須為 0" in result["mode_protocol"]["finish"]


def test_optimizer_protects_low_resource_account_with_reserve_route() -> None:
    result = _optimize(
        goal="不確定，自動判斷",
        account_stage="尚未紅裝成套",
        play_mode="綜合養成",
        gems=10000,
        relic_cores=0,
        daily_minutes=15,
        risk_style="穩定優先",
    )
    assert result["best"]["id"] == "reserve"
    assert result["spendable_gems"] == 0


def test_optimizer_uses_ab_testing_for_near_max_account() -> None:
    result = _optimize(
        goal="不確定，自動判斷",
        account_stage="接近滿配",
        play_mode="長場首領",
        spending_style="課金／只看效率",
        gems=100000,
        relic_cores=50,
        resonance_chips=30,
        xeno_cores=30,
        awakening_cores=20,
        daily_minutes=45,
    )
    assert result["best"]["id"] == "ab_test"
    assert result["confidence"] < 80


def test_optimizer_schedule_never_exceeds_daily_budget() -> None:
    for minutes in (4, 15, 30, 60):
        result = _optimize(daily_minutes=minutes)
        assert result["schedule"]["minutes_used"] <= minutes
        assert result["schedule"]["tasks"]
        assert all(0 <= item["score"] <= 97 for item in result["ranked"])
