"""Automatic decorative red-kite flight; no controls or player-data changes."""
from __future__ import annotations

import streamlit as st

from ui_art import FIELD_BUDDY, GUIDE_BUDDY

def kite_markup(variant: str = "field") -> str:
    # Only allow bundled artwork. Old pose/toggle session values are ignored.
    artwork = GUIDE_BUDDY if variant == "brand" else FIELD_BUDDY
    return artwork.replace('<svg ', '<svg class="kite-animated" data-kite-motion="flight" ', 1)


def render_motion() -> None:
    # Decorative motion starts automatically. OS reduced-motion still wins in CSS.
    st.markdown('<span class="motion-preferences" data-motion-enabled="on" aria-hidden="true"></span>', unsafe_allow_html=True)
