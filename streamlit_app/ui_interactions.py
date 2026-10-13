"""Automatic decorative red-kite scenes; native controls own navigation."""
from __future__ import annotations

import html
import streamlit as st

from ui_art import FIELD_BUDDY, GUIDE_BUDDY, TOPIC_ART, guide_icon


FLIGHT_TOPICS = {"全部": "all", "特工養成": "profile", "裝備神鑄": "gear",
                 "收藏典藏": "collection", "科技配件": "tech", "活動玩法": "event",
                 "寵物與關卡": "pet", "載具與模組": "mount"}
TOPIC_LABELS = {"全部": "全部", "特工養成": "特工", "裝備神鑄": "裝備",
                "收藏典藏": "收藏", "科技配件": "科技", "活動玩法": "活動",
                "寵物與關卡": "寵物", "載具與模組": "載具"}


def _topic(topic: str) -> tuple[str, str, str, str]:
    selected = topic if isinstance(topic, str) and topic in FLIGHT_TOPICS else "全部"
    icon, description = TOPIC_ART.get(selected, ("book", "特工、裝備、收藏、科技、寵物與載具"))
    return selected, FLIGHT_TOPICS[selected], icon, description

def kite_markup(variant: str = "field") -> str:
    # Only allow bundled artwork. Old pose/toggle session values are ignored.
    artwork = GUIDE_BUDDY if variant == "brand" else FIELD_BUDDY
    return artwork.replace('<svg ', '<svg class="kite-animated" data-kite-motion="flight" ', 1)


def flight_scene_markup(topic: str, count: int) -> str:
    """Allowlisted scene only: no scripts, remote images or fake SVG controls."""
    selected, slug, icon, description = _topic(topic)
    count = count if type(count) is int and count >= 0 else 0
    heading = "全部攻略" if selected == "全部" else selected
    return f'''<section class="flight-scene" data-flight-topic="{slug}" data-flight-view="home" data-ui-region="home-search" data-ui-motion="true">
        <div class="flight-scene-heading"><h1 class="guide-hero-title">噠噠特攻攻略</h1><p class="scene-deck">Survivor.io 攻略圖書館</p></div>
        <div class="flight-panorama" aria-hidden="true">
            <span class="scene-sun"></span><span class="scene-cloud cloud-a"></span><span class="scene-cloud cloud-b"></span><span class="scene-cloud cloud-c"></span>
            <span class="scene-wind wind-a"></span><span class="scene-wind wind-b"></span>
            <svg class="scene-route" viewBox="0 0 1000 250" preserveAspectRatio="none" aria-hidden="true" focusable="false"><path d="M-20 202C170 64 230 242 442 173S728 54 1020 184" fill="none" stroke="currentColor" stroke-width="2" stroke-dasharray="4 10"/></svg>
            <div class="scene-station"><span class="station-bg"></span>{guide_icon(icon)}</div>
            <div class="flight-bird">{kite_markup('brand')}</div>
        </div>
        <div class="flight-caption" aria-live="polite"><span class="flight-topic-icon">{guide_icon(icon)}</span><div class="flight-topic-copy"><h2>{html.escape(heading)}</h2><p>{html.escape(description)}</p></div><span class="flight-count">{count} 篇詳解</span></div>
        </section>'''


def article_bookmark_markup(topic: str) -> str:
    selected, slug, icon, _ = _topic(topic)
    return f'''<div class="article-flight-bookmark" data-flight-topic="{slug}" aria-label="{html.escape(selected)}主題書籤">
        <span class="bookmark-bird" aria-hidden="true">{kite_markup('brand')}</span><div class="bookmark-copy"><span>{guide_icon(icon)}</span><p>{html.escape(selected)}</p></div><span class="bookmark-trail" aria-hidden="true"></span></div>'''


def render_motion() -> None:
    # Decorative motion starts automatically. OS reduced-motion still wins in CSS.
    st.markdown('<span class="motion-preferences" data-motion-enabled="on" aria-hidden="true"></span>', unsafe_allow_html=True)
