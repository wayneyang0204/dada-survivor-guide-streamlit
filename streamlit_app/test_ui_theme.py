"""Non-browser regressions for the shared handbook theme and information layout.

These checks do not replace viewport, touch, or screen-reader testing.
"""
from html.parser import HTMLParser
from pathlib import Path
import re
import tomllib

import pytest

from test_decision_ui import boot, by_label
from ui_theme import STYLE


COLORS = dict(re.findall(r"--([a-z-]+):\s*(#[0-9a-f]{6})", STYLE))


def luminance(color):
    values = [int(color[i:i+2], 16) / 255 for i in (1, 3, 5)]
    linear = [v / 12.92 if v <= .04045 else ((v + .055) / 1.055) ** 2.4 for v in values]
    return sum(v * weight for v, weight in zip(linear, (.2126, .7152, .0722)))


def contrast(a, b):
    light, dark = sorted((luminance(a), luminance(b)), reverse=True)
    return (light + .05) / (dark + .05)


@pytest.mark.parametrize("foreground", ["ink", "muted", "accent", "ready", "pending", "blocked"])
@pytest.mark.parametrize("background", ["paper", "wash"])
def test_text_tokens_meet_normal_text_contrast(foreground, background):
    assert contrast(COLORS[foreground], COLORS[background]) >= 4.5


def test_controls_and_primary_button_have_sufficient_contrast():
    assert contrast(COLORS["paper"], COLORS["accent"]) >= 4.5
    assert contrast(COLORS["field"], COLORS["paper"]) >= 3


def test_cloud_theme_matches_the_single_shared_stylesheet():
    config = tomllib.loads((Path(__file__).parent.parent / ".streamlit/config.toml").read_text(encoding="utf-8"))["theme"]
    assert config["base"] == "light"
    for setting, token in (("backgroundColor", "paper"), ("secondaryBackgroundColor", "wash"),
                           ("primaryColor", "accent"), ("textColor", "ink")):
        assert config[setting] == COLORS[token]
    a = boot()
    styles = [m.value for m in a.markdown if "<style>" in m.value]
    assert len(styles) == 1
    assert "--accent:#2449d8" in styles[0]
    assert "gradient(" not in styles[0]


def test_text_can_scale_and_layouts_have_narrow_screen_fallbacks():
    # Protect the authored rules, not a claim about a rendered viewport.
    sizes = [float(n) for n in re.findall(r"font-size:([.\d]+)rem", STYLE)]
    assert sizes and min(sizes) >= .875
    assert "font-size:" not in STYLE.split("html, body", 1)[1].split("}", 1)[0]
    assert "@media(max-width:760px)" in STYLE
    assert "@media(max-width:480px)" in STYLE
    assert "grid-template-columns:1fr;" in STYLE
    assert "prefers-reduced-motion:reduce" in STYLE
    assert "position:fixed" not in STYLE
    assert "input:focus-visible" in STYLE
    # Keep the native visually hidden input; only the decorative circle is hidden.
    assert 'label[data-testid="stRadioOption"] > div:first-child {display:none;}' not in STYLE


class Markup(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))


def test_home_has_one_goal_ledger_and_one_reasoning_drawer():
    a = boot()
    a.session_state["player_profile"] = {"survivor": "維納托", "awakening": 6, "awakening_cores": 20}
    a.run()
    assert not a.exception
    markup = Markup()
    for item in a.markdown:
        if "<style>" not in item.value:
            markup.feed(item.value)
    assert sum(tag == "h1" for tag, _ in markup.tags) == 1
    assert sum(attrs.get("aria-label") == "優先升級目標" for _, attrs in markup.tags) == 1
    assert sum(attrs.get("role") == "listitem" for _, attrs in markup.tags) == 3
    assert any(attrs.get("aria-label") == "執行備忘" for _, attrs in markup.tags)
    assert [e.label for e in a.expander] == ["只核對這一步的材料", "排序依據與其他候選"]
    assert {e.proto.popover.label for e in a.get("popover")} == {"備份與匯入", "記錄遊戲內完成"}
    # Opening the page never records an in-game completion.
    assert a.session_state["player_profile"]["awakening"] == 6


def test_editor_has_visible_categories_and_only_one_form():
    a = boot()
    a.radio[0].set_value("我的帳號").run()
    selector = by_label(a.radio, "這次更新哪一項")
    assert selector.options == ["角色與模式", "普通典藏館", "進階典藏館", "收藏品", "裝備與科技"]
    for section in selector.options:
        by_label(a.radio, "這次更新哪一項").set_value(section).run()
        assert not a.exception
        assert len(a.get("form")) == 1
        assert any(f'class="editor-heading">{section}' in m.value for m in a.markdown)
        assert a.get("download_button")


def test_event_summary_is_visible_and_offline_calculator_is_preserved(monkeypatch):
    import urllib.request

    def offline(*args, **kwargs):
        raise OSError("Offline test")

    monkeypatch.setattr(urllib.request, "urlopen", offline)
    a = boot()
    a.radio[0].set_value("活動").run()
    assert not a.exception
    assert next(e for e in a.expander if e.label == "查看這篇活動的30秒重點").proto.expanded
    for label in ("01 / 活動目標", "02 / 免費進度", "03 / 寶石成本"):
        assert any(label in m.value for m in a.markdown)
    by_label(a.button, "一鍵判斷這次活動").click().run()
    assert not a.exception
    assert len(a.metric) == 4
