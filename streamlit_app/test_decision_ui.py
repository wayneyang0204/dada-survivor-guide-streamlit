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
    assert a.session_state["player_profile"]["awakening_cores"] is None
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
