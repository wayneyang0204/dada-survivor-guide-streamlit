"""Copy regressions on rendered pages, not on imported source titles."""
import pytest
import ast
from pathlib import Path
from streamlit.testing.v1 import AppTest

import guide_content as content
from test_decision_ui import APP


REMOVED_COPY = (
    "養成有方向，資源不白花", "查攻略，", "決定下一步。",
    "升什麼、缺多少、何時停手", "小鷹陪你", "現在就做這一件",
    "一鍵判斷這次活動", "路線最優解", "不無腦", "不追空白能量",
    "爆發天花板", "傷害極限", "最平衡的停損點",
)


@pytest.fixture
def offline(monkeypatch):
    import urllib.request

    def unavailable(*args, **kwargs):
        raise OSError("Copy review uses local source fallback")

    monkeypatch.setattr(urllib.request, "urlopen", unavailable)


def assert_plain_copy(app):
    assert not app.exception
    # External article titles are credited source material, not authored slogans.
    visible = "\n".join(str(element.value) for kind in
        ("markdown", "caption", "info", "warning", "success", "error")
        for element in app.get(kind) if "<style>" not in str(element.value))
    controls = "\n".join(element.label for kind in ("button", "expander", "selectbox", "text_input")
                         for element in app.get(kind))
    for phrase in REMOVED_COPY:
        assert phrase not in visible + controls


@pytest.mark.parametrize("page", ["攻略首頁", "下一步", "我的帳號", "活動", "資料庫"])
def test_main_pages_have_functional_copy(page, offline):
    app = AppTest.from_file(APP).run()
    app.radio[0].set_value(page).run()
    assert_plain_copy(app)


@pytest.mark.parametrize("slug", [guide["slug"] for guide in content.GUIDES])
def test_every_authored_guide_renders_without_removed_copy(slug, offline):
    app = AppTest.from_file(APP)
    app.query_params["guide"] = slug
    app.run()
    assert_plain_copy(app)
    assert any("資料來源" in item.value for item in app.markdown)


def test_saved_profile_shows_specific_action_not_slogan(offline):
    app = AppTest.from_file(APP)
    app.session_state["player_profile"] = {
        "survivor": "維納托", "awakening": 6, "taloxa": 4,
        "awakening_cores": 20, "s_shards": 400,
    }
    app.run()
    app.radio[0].set_value("下一步").run()
    assert_plain_copy(app)
    text = "\n".join(item.value for item in app.markdown)
    assert "操作步驟" in text and "遊戲入口" in text
    assert "核心缺 10" in text and "碎片缺 150" in text


@pytest.mark.parametrize("section", ["完整攻略庫", "收藏圖鑑", "最新文章", "配裝參考"])
def test_reference_sections_use_plain_copy(section, offline):
    app = AppTest.from_file(APP).run()
    app.radio[0].set_value("資料庫").run()
    next(item for item in app.selectbox if item.label == "要查什麼").set_value(section).run()
    assert_plain_copy(app)


def test_curated_summaries_and_build_names_do_not_claim_unproven_extremes():
    # Read literal local data only; do not import app.py or run its UI at collection.
    tree = ast.parse(Path(APP).read_text(encoding="utf-8"))
    reviewed = [ast.literal_eval(node.value) for node in tree.body
                if isinstance(node, ast.Assign)
                and any(isinstance(target, ast.Name) and target.id in ("攻略資料", "終局配置")
                        for target in node.targets)]
    assert len(reviewed) == 2
    for phrase in REMOVED_COPY:
        assert phrase not in str(reviewed)
