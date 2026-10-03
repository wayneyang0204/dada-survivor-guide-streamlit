"""Behaviour checks complement, but do not replace, real animation visual QA."""
from copy import deepcopy
from xml.etree import ElementTree as ET

import pytest
from streamlit.testing.v1 import AppTest

from test_decision_ui import APP, by_label
from test_ui_theme import Markup
from ui_interactions import POSES, eagle_markup
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
    assert '<script>' not in art and 'data-eagle-pose="auto"' in art


def home():
    return AppTest.from_file(APP).run(timeout=15)


def test_home_motion_coverage_exceeds_thirty_percent_of_main_content_blocks():
    app = home()
    markup = Markup()
    for item in app.markdown:
        if "<style>" not in item.value:
            markup.feed(item.value)
    regions = {attrs["data-ui-region"]: attrs["data-ui-motion"] for _, attrs in markup.tags if "data-ui-region" in attrs}
    # One search/hero panel, three tools and six topics. No practice panel.
    assert set(regions) == {"home-search", "tool-upgrade", "tool-event", "tool-collection", *(f"topic-{n}" for n in range(6))}
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


def test_home_has_automatic_eagle_but_no_practice_or_sample_sliders():
    app = home()
    assert not app.exception and not app.slider and not app.tabs
    assert not any("練習" in item.label for item in app.expander)
    assert not any("核對答案" in button.label for button in app.button)
    markup = "\n".join(m.value for m in app.markdown if "<style>" not in m.value)
    assert markup.count('data-eagle-pose="auto"') == 2
    assert 'practice' not in markup
    for pose in POSES:
        assert by_label(app.button, pose)


@pytest.mark.parametrize("pose", POSES)
def test_pose_controls_only_change_the_mascot(pose):
    app = home()
    by_label(app.button, pose).click().run()
    assert not app.exception
    assert app.session_state["ui_eagle_pose"] == pose
    assert "player_profile" not in app.session_state
    assert not app.query_params
    markup = "\n".join(m.value for m in app.markdown if "<style>" not in m.value)
    assert markup.count(f'data-eagle-pose="{POSES[pose]}"') == 2


def test_eagle_has_separate_head_wings_page_shadow_and_continuous_motion():
    root = ET.fromstring(eagle_markup("field", "自動"))
    classes = {node.attrib.get("class") for node in root.iter()}
    assert {"eagle-character", "eagle-head", "eagle-wing-left", "eagle-wing-right",
            "eagle-page-leaf", "eagle-shadow", "eagle-sleep-marks"} <= classes
    for animation in ("eagle-greet 8s", "eagle-stretch 8s", "eagle-look 8s",
                      "eagle-page 2.6s", "eagle-flap-right .85s", "eagle-flap-left .85s"):
        assert f"animation:{animation} ease-in-out infinite" in STYLE
    assert 'rotate(-48deg)' in STYLE and 'translateY(-14px)' in STYLE
    assert '.hero-companion {flex-basis:96px;}' in STYLE
