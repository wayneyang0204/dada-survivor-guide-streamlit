"""Decorative eagle animation preferences; never modify a player profile."""
from __future__ import annotations

import streamlit as st

from ui_art import FIELD_BUDDY, GUIDE_BUDDY

POSES = {"自動": "auto", "招手": "wave", "拍翅": "flap", "翻書": "read", "打盹": "sleep"}


def eagle_markup(variant: str = "field", pose: str | None = None) -> str:
    # Only allow known artwork and poses; no user HTML or SVG is interpolated.
    selected = POSES.get(pose or st.session_state.get("ui_eagle_pose", "自動"), "auto")
    artwork = GUIDE_BUDDY if variant == "brand" else FIELD_BUDDY
    return artwork.replace('<svg ', f'<svg class="eagle-animated" data-eagle-pose="{selected}" ', 1)


def set_pose(pose: str) -> None:
    if pose in POSES:
        st.session_state["ui_eagle_pose"] = pose


def render_preferences() -> None:
    with st.container(key="motion_controls"):
        with st.popover("老鷹・動畫", width="content"):
            enabled = st.toggle("播放動畫", value=True, key="ui_motion_enabled")
            st.caption("自動：招手、拍翅、歪頭與翻書輪流播放。")
            poses = list(POSES)
            for start in range(0, len(poses), 3):
                for column, pose in zip(st.columns(3), poses[start:start + 3]):
                    column.button(pose, key=f"eagle_pose_{POSES[pose]}", on_click=set_pose,
                                  args=(pose,), width="stretch",
                                  type="primary" if st.session_state.get("ui_eagle_pose", "自動") == pose else "secondary")
            st.caption("系統設定減少動態效果時，也會停用動畫。")
    state = "on" if enabled else "off"
    st.markdown(f'<span class="motion-preferences" data-motion-enabled="{state}" aria-hidden="true"></span>', unsafe_allow_html=True)
