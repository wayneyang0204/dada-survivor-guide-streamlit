"""Automatic mascot checks; real rendered animation QA is still required."""
from copy import deepcopy
from xml.etree import ElementTree as ET

import pytest
from streamlit.testing.v1 import AppTest

from test_decision_ui import APP
from test_ui_theme import Markup
from ui_interactions import kite_markup
from ui_theme import STYLE
from guide_content import CATEGORIES


@pytest.mark.parametrize("variant", ("brand", "field"))
def test_flying_red_kite_is_allowlisted_decorative_svg(variant):
    root = ET.fromstring(kite_markup(variant))
    assert root.attrib["data-kite-motion"] == "flight"
    assert root.attrib["data-mascot"] == "red-kite"
    assert root.attrib["data-kite-style"] == "cartoon"
    assert root.attrib["aria-hidden"] == "true"
    assert root.attrib["focusable"] == "false"
    assert not any(node.tag.endswith(("script", "foreignObject")) for node in root.iter())
    images = [node for node in root.iter() if node.tag.endswith("image")]
    assert len(images) == 1 and images[0].attrib["href"].startswith("data:image/webp;base64,")


def test_unknown_variant_cannot_inject_markup():
    assert kite_markup('<script>oops</script>') == kite_markup("field")


def home():
    return AppTest.from_file(APP).run(timeout=15)


def test_home_motion_coverage_exceeds_thirty_percent_of_main_content_blocks():
    app = home()
    markup = Markup()
    for item in app.markdown:
        if "<style>" not in item.value:
            markup.feed(item.value)
    regions = {attrs["data-ui-region"]: attrs["data-ui-motion"] for _, attrs in markup.tags if "data-ui-region" in attrs}
    assert set(regions) == {"home-search", "tool-upgrade", "tool-event", "tool-collection", *(f"topic-{n}" for n in range(len(CATEGORIES)))}
    assert sum(value == "true" for value in regions.values()) / len(regions) >= .3
    assert 'kite-cruise' in STYLE and 'kite-direction' in STYLE and 'icon-hop' in STYLE


def test_home_has_no_animation_choices_practice_or_sample_sliders():
    app = home()
    assert not app.exception and not app.slider and not app.tabs and not app.toggle
    assert not app.get("popover")
    assert not any("練習" in item.label for item in app.expander)
    assert not any(button.label in ("自動", "招手", "拍翅", "翻書", "打盹", "核對答案") for button in app.button)
    markup = "\n".join(m.value for m in app.markdown if "<style>" not in m.value)
    assert markup.count('data-kite-motion="flight"') == 2
    assert 'data-motion-enabled="on"' in markup
    assert 'practice' not in markup and 'data-eagle-pose' not in markup


def test_old_preferences_cannot_stop_flight_or_change_player_data():
    app = home()
    raw = {"survivor": "維納托", "awakening": 6, "awakening_cores": 20}
    app.session_state["player_profile"] = deepcopy(raw)
    app.session_state["ui_motion_enabled"] = False
    app.session_state["ui_eagle_pose"] = "打盹"
    app.run()
    app.radio[0].set_value("我的帳號").run()
    assert not app.exception and app.session_state["player_profile"] == raw
    markup = "\n".join(m.value for m in app.markdown if "<style>" not in m.value)
    assert 'data-motion-enabled="on"' in markup and 'data-kite-motion="flight"' in markup
    assert not app.toggle
    assert not any(e.proto.popover.label == "老鷹・動畫" for e in app.get("popover"))
    assert '@media(prefers-reduced-motion:reduce)' in STYLE


def test_cartoon_red_kite_preserves_gliding_route_without_fake_articulation():
    root = ET.fromstring(kite_markup())
    classes = {node.attrib.get("class") for node in root.iter()}
    assert {"kite-flight", "kite-direction", "kite-artwork"} <= classes
    assert not {"kite-head", "kite-eyes", "kite-wing-left", "kite-wing-right"} & classes
    for animation in ("kite-cruise 12s", "kite-direction 12s"):
        assert f"animation:{animation} ease-in-out infinite" in STYLE
    assert 'translate(-15px,3px)' in STYLE and 'translate(15px,2px)' in STYLE
    assert '.hero-companion {overflow:hidden;isolation:isolate;}' in STYLE
    assert '.hero-companion svg {pointer-events:none;}' in STYLE


def test_markup_does_not_create_a_profile():
    app = home()
    assert "player_profile" not in app.session_state
    assert not app.query_params


def test_cartoon_asset_preserves_alpha_and_has_small_local_payload():
    import json
    from PIL import Image
    from ui_art import KITE_ASSET

    assert KITE_ASSET.name == "red-kite-cute-v3.webp"
    assert KITE_ASSET.with_name("red-kite-storybook-v2.webp").exists()
    assert KITE_ASSET.with_name("red-kite-realistic-v1.webp").exists()
    assert KITE_ASSET.stat().st_size < 150_000
    with Image.open(KITE_ASSET) as image:
        assert image.size == (960, 640)
        assert image.mode == "RGBA" and image.getchannel("A").getextrema()[0] == 0
    provenance = json.loads(KITE_ASSET.with_suffix(".prompt.json").read_text(encoding="utf-8"))
    assert provenance["mode"] == "built-in image_gen"
    assert provenance["reference"] == "red-kite-storybook-v2.webp"
    assert provenance["use_case"] == "style-transfer"
    assert "not a photograph" in provenance["disclosure"]
