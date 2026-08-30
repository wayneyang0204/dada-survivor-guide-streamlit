from data_engine import (
    assess_event_plan,
    classify_article,
    diagnose_account,
    match_event_playbook,
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
