"""Behaviour checks complement, but do not replace, real animation visual QA."""
from copy import deepcopy
from xml.etree import ElementTree as ET

import pytest
from streamlit.testing.v1 import AppTest

from test_decision_ui import APP, by_label
from test_ui_theme import Markup
from ui_interactions import PRACTICE, POSES, eagle_markup, material_gap, practice_result
from ui_theme import STYLE


@pytest.mark.parametrize("pose", POSES)
@pytest.mark.parametrize("variant", ("brand", "field"))
def test_each_mascot_pose_is_allowlisted_valid_svg(pose, variant):
    root = ET.fromstring(eagle_markup(variant, pose))
    assert root.attrib["data-eagle-pose"] == POSES[pose]
    assert root.attrib["aria-hidden"] == "true"
    assert root.attrib["focusable"] == "false"
    assert not any(node.tag.endswith(("image", "script", "foreignObject")) for node in root.iter())


def test_untrusted_pose_cannot_inject_markup():
    art = eagle_markup("field", '<script>oops</script>')
    assert '<script>' not in art and 'data-eagle-pose="read"' in art


@pytest.mark.parametrize("stock,target,expected", [(20, 30, (10, 2/3)), (40, 30, (0, 1)), (0, 0, (0, 1)), (0, 30, (30, 0))])
def test_material_practice_caps_progress_and_handles_zero(stock, target, expected):
    assert material_gap(stock, target) == expected


@pytest.mark.parametrize("question", PRACTICE, ids=lambda q: q["id"])
def test_practice_answers_are_deterministic_and_invalid_choice_is_ignored(question):
    assert practice_result(question, None) is None
    assert practice_result(question, "not in question") is None
    for index, option in enumerate(question["options"]):
        assert practice_result(question, option)["correct"] == (index == question["answer"])


def home():
    return AppTest.from_file(APP).run(timeout=15)


def test_home_motion_coverage_exceeds_thirty_percent_of_main_content_blocks():
    app = home()
    markup = Markup()
    for item in app.markdown:
        if "<style>" not in item.value:
            markup.feed(item.value)
    regions = {attrs["data-ui-region"]: attrs["data-ui-motion"] for _, attrs in markup.tags if "data-ui-region" in attrs}
    # One search/hero panel, three tools, six topics and one practice panel.
    assert set(regions) == {"home-search", "tool-upgrade", "tool-event", "tool-collection", "practice", *(f"topic-{n}" for n in range(6))}
    assert sum(value == "true" for value in regions.values()) / len(regions) >= .3
    assert 'eagle-blink' in STYLE and 'eagle-wave' in STYLE and 'icon-hop' in STYLE


def test_pause_and_pose_preferences_survive_navigation_without_changing_account():
    app = home()
    raw = {"survivor": "維納托", "awakening": 6, "awakening_cores": 20}
    app.session_state["player_profile"] = deepcopy(raw)
    by_label(app.button, "打盹").click().run()
    assert app.session_state["ui_eagle_pose"] == "打盹"
    by_label(app.toggle, "播放動畫").set_value(False).run()
    app.radio[0].set_value("我的帳號").run()
    assert not app.exception and app.session_state["player_profile"] == raw
    markup = "\n".join(m.value for m in app.markdown if "<style>" not in m.value)
    assert 'data-motion-enabled="off"' in markup and 'data-eagle-pose="sleep"' in markup
    assert by_label(app.toggle, "播放動畫").value is False
    # CSS applies this preference everywhere, including controls and transitions.
    assert 'body:has([data-motion-enabled="off"]) * {animation:none!important;transition:none!important;}' in STYLE
    assert '@media(prefers-reduced-motion:reduce)' in STYLE


def test_practice_feedback_is_not_reused_after_question_or_answer_changes():
    app = home()
    assert by_label(app.button, "核對答案").disabled
    by_label(app.radio, "你的選擇").set_value(PRACTICE[0]["options"][0]).run()
    by_label(app.button, "核對答案").click().run()
    assert any('practice-feedback correct' in m.value for m in app.markdown)
    by_label(app.radio, "你的選擇").set_value(PRACTICE[0]["options"][1]).run()
    assert not any('class="practice-feedback' in m.value for m in app.markdown)
    by_label(app.button, "核對答案").click().run()
    assert any('practice-feedback review' in m.value for m in app.markdown)
    by_label(app.selectbox, "選擇練習題").set_value(PRACTICE[1]["label"]).run()
    assert not any('class="practice-feedback' in m.value for m in app.markdown)


def test_practice_can_open_corresponding_guide_without_creating_profile():
    app = home()
    by_label(app.radio, "你的選擇").set_value(PRACTICE[0]["options"][0]).run()
    by_label(app.button, "核對答案").click().run()
    by_label(app.button, "閱讀對應攻略").click().run()
    assert app.query_params["guide"] == ["collectible-sets"]
    assert "player_profile" not in app.session_state


def test_material_sliders_change_gap_but_not_saved_profile():
    app = home()
    raw = {"survivor": "維納托", "awakening": 6, "awakening_cores": 20}
    app.session_state["player_profile"] = deepcopy(raw)
    by_label(app.slider, "示例庫存核心").set_value(30).run()
    assert any("示例核心數量已足" in info.value for info in app.info)
    by_label(app.slider, "示例目標核心需求").set_value(45).run()
    assert any("核心還缺 15" in info.value for info in app.info)
    assert app.session_state["player_profile"] == raw and not app.exception
