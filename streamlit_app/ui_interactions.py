"""Local-only mascot preferences and deterministic practice, not game actions."""
from __future__ import annotations

import html
import streamlit as st

from ui_art import FIELD_BUDDY, GUIDE_BUDDY

POSES = {"翻書": "read", "招手": "wave", "打盹": "sleep"}

# Stable facts already documented in our guides. Practice never changes a profile.
PRACTICE = (
    {"id": "set", "label": "收藏套裝缺一件", "question": "已使用對應裝備技能，套裝四件是黃3、黃3、黃3、黃2。要補哪件？",
     "options": ("把黃2補到黃3", "把前三件升黃5", "先把四件平均升高"), "answer": 0,
     "explanation": "四件都到黃3才滿足這個套裝條件。前三件升黃5不能代替第四件。", "guide": "collectible-sets"},
    {"id": "stars", "label": "典藏館星數", "question": "第二套放入八件黃五星傳奇收藏，合計有多少傳奇星？",
     "options": ("80星", "40星", "只看格數，不計星數"), "answer": 1,
     "explanation": "八件 × 五星＝40星；80星需要八件紅五星，仍須核對進階格數。", "guide": "collection-hall"},
    {"id": "cores", "label": "覺醒核心缺額", "question": "某次升級完整需求是30顆核心，現有20顆；核心還缺多少？",
     "options": ("還缺30顆", "20顆已經夠", "還缺10顆"), "answer": 2,
     "explanation": "30－20＝10顆。核心補足後，角色碎片、量子碎片與其他條件仍需核對。", "guide": "survivor-awakening"},
    {"id": "box", "label": "紅色自選箱", "question": "想補科技諧振支援，先確認自選箱的哪一項？",
     "options": ("箱子圖示是不是紅色", "可選清單是否有科技配件", "選大家名字最常提到的物品"), "answer": 1,
     "explanation": "收藏、科技和裝備箱用途不同；以可選清單確認箱種，不能只看紅色圖示。", "guide": "red-choice-box"},
)


def eagle_markup(variant: str = "field", pose: str | None = None) -> str:
    # Only allow known artwork and poses; no user HTML or SVG is interpolated.
    selected = POSES.get(pose or st.session_state.get("ui_eagle_pose", "翻書"), "read")
    artwork = GUIDE_BUDDY if variant == "brand" else FIELD_BUDDY
    return artwork.replace('<svg ', f'<svg class="eagle-animated" data-eagle-pose="{selected}" ', 1)


def set_pose(pose: str) -> None:
    if pose in POSES:
        st.session_state["ui_eagle_pose"] = pose


def render_preferences() -> None:
    with st.container(key="motion_controls"):
        with st.popover("老鷹・動畫", width="content"):
            enabled = st.toggle("播放動畫", value=True, key="ui_motion_enabled")
            st.caption("系統設定減少動態效果時，也會停用動畫。")
            columns = st.columns(3)
            for column, pose in zip(columns, POSES):
                column.button(pose, key=f"eagle_pose_{POSES[pose]}", on_click=set_pose,
                              args=(pose,), width="stretch",
                              type="primary" if st.session_state.get("ui_eagle_pose", "翻書") == pose else "secondary")
    state = "on" if enabled else "off"
    st.markdown(f'<span class="motion-preferences" data-motion-enabled="{state}" aria-hidden="true"></span>', unsafe_allow_html=True)


def practice_result(question: dict, answer: str | None) -> dict | None:
    if answer not in question["options"]:
        return None
    correct = answer == question["options"][question["answer"]]
    return {"id": question["id"], "answer": answer, "correct": correct}


def material_gap(stock: int, target: int) -> tuple[int, float]:
    gap = max(0, target - stock)
    return gap, min(1.0, stock / target) if target else 1.0


def render_playground(open_guide) -> None:
    with st.container(key="interaction_practice"):
        st.markdown('<span class="practice-region" data-ui-region="practice" data-ui-motion="false" aria-hidden="true"></span>', unsafe_allow_html=True)
        with st.expander("互動練習：升級判斷與材料試算"):
            st.caption("練習使用示例，不會修改「我的配置」。")
            decision, materials = st.tabs(["情境練習", "材料差額"])
            with decision:
                label = st.selectbox("選擇練習題", [q["label"] for q in PRACTICE], key="practice_question")
                question = next(q for q in PRACTICE if q["label"] == label)
                st.write(question["question"])
                answer = st.radio("你的選擇", question["options"], index=None, key=f"practice_answer_{question['id']}")
                if st.button("核對答案", key="practice_check", disabled=answer is None):
                    st.session_state["practice_result"] = practice_result(question, answer)
                result = st.session_state.get("practice_result")
                if result and result["id"] == question["id"] and result["answer"] == answer:
                    status = "correct" if result["correct"] else "review"
                    title = "答對了" if result["correct"] else "再核對條件"
                    st.markdown(f'<section class="practice-feedback {status}" role="status">'
                                f'<span class="feedback-feather" aria-hidden="true">✦</span>'
                                f'<h3>{title}</h3><p>{html.escape(question["explanation"])}</p></section>', unsafe_allow_html=True)
                    st.button("閱讀對應攻略", key="practice_read", on_click=open_guide,
                              args=(question["guide"],), width="stretch")
            with materials:
                st.caption("自訂核心數字，只計算差額；實際成本以遊戲升級預覽為準。")
                stock = st.slider("示例庫存核心", min_value=0, max_value=60, value=20, key="practice_stock")
                target = st.slider("示例目標核心需求", min_value=0, max_value=60, value=30, key="practice_target")
                gap, ratio = material_gap(stock, target)
                st.markdown(f'<div class="material-flight" aria-hidden="true"><span class="flight-track"></span>'
                            f'<span class="flight-eagle" style="left:{ratio * 100:.2f}%">{eagle_markup("brand", "招手")}</span></div>', unsafe_allow_html=True)
                st.progress(ratio, text=f"庫存 {stock} ／ 需求 {target}")
                st.info(f"核心還缺 {gap} 顆。其他材料須另行核對。" if gap else "示例核心數量已足；不代表其他材料也已備齊。")
