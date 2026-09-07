"""Interaction tests for the actual Streamlit entry point, without a browser."""
from pathlib import Path
import sys

from streamlit.testing.v1 import AppTest

sys.path.insert(0, str(Path(__file__).parent))
APP = str(Path(__file__).with_name("app.py"))


def boot():
    return AppTest.from_file(APP).run(timeout=15)


def by_label(elements, label):
    return next(item for item in elements if item.label == label)


def test_first_visit_is_a_short_setup_not_an_article_feed():
    a = boot()
    assert not a.exception
    assert a.radio[0].options == ["下一步", "我的帳號", "活動", "資料庫"]
    assert len(a.get("form")) == 1
    assert len(a.number_input) == 1
    assert not any("本期活動完整作戰簡報" in x.value for x in a.markdown)


def test_onboarding_contextual_edit_save_navigation_and_completion():
    a = boot()
    by_label(a.selectbox, "主位特工").select("維納托")
    by_label(a.number_input, "覺醒等級（不是一般星數）").set_value(6)
    by_label(a.button, "建立我的升級路線").click().run()
    assert not a.exception
    assert a.session_state["player_profile"]["awakening"] == 6
    assert any("維納托 R6 → R7" in x.value for x in a.markdown)
    by_label(a.button, "補上這一步的資料").click().run()
    assert a.radio[0].value == "我的帳號"
    assert by_label(a.selectbox, "這次更新哪一項").value == "角色與模式"
    by_label(a.number_input, "現有覺醒核心").set_value(30)
    by_label(a.number_input, "可用於主位的S特工碎片").set_value(550)
    by_label(a.selectbox, "量子碎片是否足夠升主位下一階").set_value(True)
    by_label(a.button, "儲存並重新排序").click().run()
    assert not a.exception
    assert a.radio[0].value == "下一步"
    assert any("材料已足" in x.value for x in a.markdown)
    by_label(a.button, "我已在遊戲完成，排下一步").click().run()
    assert not a.exception
    assert a.session_state["player_profile"]["awakening"] == 7
    assert a.session_state["player_profile"]["awakening_cores"] == 0
    assert "awakening_cores" in a.session_state["player_profile"]["estimated_balances"]
    assert any("維納托 R7 → R8" in x.value for x in a.markdown)


def test_profile_survives_switching_sections_and_pages():
    a = boot()
    a.session_state["player_profile"] = {"survivor": "維納托", "awakening": 6, "hearts": 12345}
    a.radio[0].set_value("我的帳號").run()
    for section in ("普通典藏館", "進階典藏館", "收藏品", "裝備與科技", "角色與模式"):
        by_label(a.selectbox, "這次更新哪一項").select(section).run()
        assert not a.exception
    a.radio[0].set_value("下一步").run()
    assert a.session_state["player_profile"]["hearts"] == 12345
    assert a.session_state["player_profile"]["awakening"] == 6


def test_invalid_star_input_shows_error_and_preserves_profile():
    a = boot()
    a.session_state["player_profile"] = {"survivor": "維納托", "awakening": 6}
    a.radio[0].set_value("我的帳號").run()
    by_label(a.selectbox, "這次更新哪一項").select("進階典藏館").run()
    by_label(a.text_input, "第二套預定放入的傳奇收藏星數（最多8件）").set_value("紅6")
    by_label(a.button, "儲存並重新排序").click().run()
    assert a.error
    assert not a.exception
    assert a.session_state["player_profile"]["awakening"] == 6


def test_sessions_do_not_share_player_data():
    a = boot()
    a.session_state["player_profile"] = {"survivor": "維納托", "awakening": 8}
    b = boot()
    assert "player_profile" not in b.session_state


def test_old_navigation_state_migrates():
    a = AppTest.from_file(APP)
    a.session_state["主導覽"] = "養成"
    a.run()
    assert not a.exception
    assert a.radio[0].value == "下一步"


def test_remaining_pages_work_when_sources_are_offline(monkeypatch):
    import urllib.request
    def offline(*args, **kwargs):
        raise OSError("Offline test")
    monkeypatch.setattr(urllib.request, "urlopen", offline)
    a = boot()
    a.radio[0].set_value("活動").run()
    assert not a.exception
    by_label(a.button, "一鍵判斷這次活動").click().run()
    assert not a.exception
    a.radio[0].set_value("資料庫").run()
    assert not a.exception
    for page in ("配裝參考", "收藏圖鑑", "最新文章", "完整攻略庫"):
        by_label(a.selectbox, "要查什麼").select(page).run()
        assert not a.exception


def test_home_can_fill_only_the_current_awakening_recipe():
    a = boot()
    a.session_state["player_profile"] = {"survivor": "維納托", "awakening": 6}
    a.run()
    assert len(a.number_input) == 2
    by_label(a.number_input, "現有覺醒核心").set_value(30)
    by_label(a.number_input, "可用於主位的S特工碎片").set_value(550)
    by_label(a.selectbox, "量子碎片是否足夠升主位下一階").set_value(True)
    by_label(a.button, "更新這一步的材料").click().run()
    assert not a.exception
    assert a.radio[0].value == "下一步"
    assert any("材料已足" in x.value for x in a.markdown)


def test_collection_quote_completion_and_undo_restore_exact_prior_state():
    a = boot()
    a.session_state["player_profile"] = {"survivor": "維納托", "awakening": 8, "neck": "破壞者徽記", "memory": 3}
    a.run()
    by_label(a.number_input, "現有傳奇收藏自選箱").set_value(3)
    by_label(a.number_input, "從目前狀態到目標，合計要用多少箱").set_value(2)
    by_label(a.selectbox, "箱子可選目標期數，且其他碎片／條件都符合").set_value(True)
    by_label(a.button, "更新這一步的材料").click().run()
    assert not a.exception
    before = dict(a.session_state["player_profile"])
    assert any("材料已足" in x.value for x in a.markdown)
    by_label(a.button, "我已在遊戲完成，排下一步").click().run()
    assert not a.exception
    assert a.session_state["player_profile"]["memory"] == 5
    assert a.session_state["player_profile"]["red_boxes"] == 1
    assert "red_boxes" in a.session_state["player_profile"]["estimated_balances"]
    assert not a.session_state["player_profile"]["step_quotes"]
    assert any("紅3星" in x.value for x in a.markdown)
    assert by_label(a.number_input, "從目前狀態到目標，合計要用多少箱").value is None
    by_label(a.button, "撤回剛才紀錄").click().run()
    assert not a.exception
    assert a.session_state["player_profile"] == before
    assert not a.session_state["completed_steps"]


def test_unknown_endgame_profile_gets_three_targeted_counts_not_empty_result():
    a = boot()
    a.session_state["player_profile"] = {"survivor": "維納托", "awakening": 8}
    a.run()
    assert not a.exception
    assert len(a.number_input) == 3
    by_label(a.number_input, "全部已開槽位").set_value(8)
    by_label(a.number_input, "不同紅品質收藏持有數").set_value(8)
    by_label(a.number_input, "已放入普通槽位的紅收藏數").set_value(7)
    by_label(a.button, "檢查有沒有免費提升").click().run()
    assert not a.exception
    assert any("把已持有紅收藏放進空槽" in x.value for x in a.markdown)


def test_resource_scope_routes_missing_advanced_data_to_correct_form():
    a = boot()
    a.session_state["player_profile"] = {"survivor": "維納托", "awakening": 8}
    a.run()
    by_label(a.selectbox, "這次要安排的資源").select("高級收藏之心").run()
    by_label(a.button, "只填進階典藏館").click().run()
    assert not a.exception
    assert a.radio[0].value == "我的帳號"
    assert by_label(a.selectbox, "這次更新哪一項").value == "進階典藏館"


def test_unlocking_a_collectible_also_updates_distinct_owned_count():
    a = boot()
    a.session_state["player_profile"] = {"survivor": "維納托", "awakening": 8, "twin_drone": True,
        "dark_matter": 0, "slots": 3, "red_owned": 3, "red_placed": 3}
    a.run()
    assert any("暗物質傀儡" in x.value for x in a.markdown)
    by_label(a.button, "我已在遊戲完成，排下一步").click().run()
    assert not a.exception
    assert a.session_state["player_profile"]["red_owned"] == 4
    assert a.session_state["player_profile"]["red_placed"] == 3


def test_backup_restore_is_visible_on_first_visit_and_home():
    a = boot()
    assert by_label(a.button, "套用匯入紀錄").disabled
    assert any(x.label == "接續上次紀錄" for x in a.expander)
    a.session_state["player_profile"] = {"survivor": "維納托", "awakening": 8}
    a.run()
    assert not a.exception
    assert a.get("download_button")


def test_free_rearrangement_preserves_material_stock_and_recalculates():
    a = boot()
    a.session_state["player_profile"] = {"survivor": "維納托", "awakening": 8,
        "adv2": 2, "stars2": [1, 1, 10, 10, 10, 10, 10, 10], "advanced_hearts": 250,
        "advanced_quote": "adv2_3", "advanced_cost": 100}
    a.run()
    assert any("先調整第2套擺放" in x.value for x in a.markdown)
    assert not a.get("form")  # No material confirmation for a free rearrangement.
    by_label(a.button, "我已在遊戲完成，排下一步").click().run()
    assert not a.exception
    assert a.session_state["player_profile"]["advanced_hearts"] == 250
    assert a.session_state["player_profile"]["adv2"] == 2
    assert any("進階第2套第3格" in x.value for x in a.markdown)
    assert by_label(a.number_input, "這一格的進階顯示價格").value == 100


def test_all_resource_filters_work_on_a_mixed_endgame_profile():
    import next_step
    a = boot()
    a.session_state["player_profile"] = {"survivor": "維納托", "awakening": 6,
        "taloxa": 3, "awakening_cores": 30, "slots": 10, "red_owned": 11, "red_placed": 10,
        "adv1": 0, "stars1": [5, 5, 5, 5], "adv2": 7, "stars2": [10]*8,
        "neck": "破壞者徽記", "memory": 5, "ss_boots": True, "boot_stars": [3, 2, 3, 3],
        "weapon": "雙絕槍", "weapon_e": 0, "weapon_v": 2,
        "drone_red": True, "forcefield_red": True, "twin_drone": False, "dark_matter": 3}
    a.run()
    for scope in (*next_step.RESOURCES, "自動排序"):
        by_label(a.selectbox, "這次要安排的資源").select(scope).run()
        assert not a.exception
        assert len(a.get("form")) <= 1


def test_editing_one_estimated_balance_preserves_other_resource_provenance():
    a = boot()
    a.session_state["player_profile"] = {"survivor": "維納托", "awakening": 6,
        "hearts": 1000, "awakening_cores": 20, "estimated_balances": ["hearts", "awakening_cores"]}
    a.radio[0].set_value("我的帳號").run()
    by_label(a.selectbox, "這次更新哪一項").select("普通典藏館").run()
    by_label(a.number_input, "現有收藏之心").set_value(1200)
    by_label(a.button, "儲存並重新排序").click().run()
    assert not a.exception
    assert a.session_state["player_profile"]["hearts"] == 1200
    assert a.session_state["player_profile"]["estimated_balances"] == ["awakening_cores"]


def test_whole_set_confirmation_and_next_action_have_distinct_buttons():
    a = boot()
    a.session_state["player_profile"] = {"survivor": "維納托", "awakening": 8,
        "ss_boots": True, "boot_stars": [2, 2, 3, 5]}
    a.run()
    assert any("四件全部達到" in x.value for x in a.warning)
    by_label(a.number_input, "現有傳奇收藏自選箱").set_value(5)
    by_label(a.number_input, "從目前狀態到目標，合計要用多少箱").set_value(4)
    by_label(a.selectbox, "箱子可選目標期數，且其他碎片／條件都符合").set_value(True)
    by_label(a.button, "更新這一步的材料").click().run()
    original_key = by_label(a.button, "我已在遊戲完成，排下一步").key
    by_label(a.button, "我已在遊戲完成，排下一步").click().run()
    assert not a.exception
    assert a.session_state["player_profile"]["boot_stars"] == [3, 3, 3, 5]
    assert a.session_state["player_profile"]["red_boxes"] == 1
    assert not any(button.key == original_key for button in a.button)


def test_completion_buttons_are_bound_to_precise_awakening_target():
    a = boot()
    a.session_state["player_profile"] = {"survivor": "維納托", "awakening": 6,
        "awakening_cores": 60, "s_shards": 1200, "quantum_ready": True}
    a.run()
    old_key = by_label(a.button, "我已在遊戲完成，排下一步").key
    by_label(a.button, "我已在遊戲完成，排下一步").click().run()
    assert not a.exception
    assert by_label(a.button, "我已在遊戲完成，排下一步").key != old_key
    assert a.session_state["player_profile"]["awakening_cores"] == 30
    assert a.session_state["player_profile"]["quantum_ready"] is None


def test_home_separates_known_shortfall_from_unknown_requirements():
    a = boot()
    a.session_state["player_profile"] = {"survivor": "維納托", "awakening": 6, "awakening_cores": 20}
    a.run()
    assert not a.exception
    content = "\n".join(x.value for x in a.markdown)
    assert "先存資源" in content
    assert "缺 · 覺醒核心" in content
    assert "還差 10" in content
    assert "待確認 · 角色碎片" in content
    assert "待確認 · 量子碎片" in content
    assert next(e for e in a.expander if e.label == "只核對這一步的材料").proto.expanded


def test_missing_stars_do_not_open_an_irrelevant_material_form():
    a = boot()
    a.session_state["player_profile"] = {"survivor": "維納托", "awakening": 8, "adv2": 1, "stars2": [10]}
    a.run()
    assert not a.exception
    assert any("資料未齊" in x.value for x in a.markdown)
    assert not a.get("form")
    by_label(a.button, "補上這一步的資料").click().run()
    assert by_label(a.selectbox, "這次更新哪一項").value == "進階典藏館"
