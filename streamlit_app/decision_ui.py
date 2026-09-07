"""One decision at a time. Profiles are isolated in Streamlit session state."""
from __future__ import annotations

from datetime import datetime
import html
import streamlit as st
import next_step as engine


STYLE = """
<style>
:root {--bg:#f5f7fa;--panel:#fff;--ink:#16283b;--muted:#536378;--line:#dce3ea;--lime:#176253;--lime-strong:#176253;}
.stApp {background:#f5f7fa;color:#16283b;}
.block-container {max-width:1060px;padding-top:1rem;}
[data-testid="stMarkdownContainer"] p, [data-testid="stMarkdownContainer"] li {font-size:1rem;line-height:1.7;color:#293b4c;}
[data-testid="stCaptionContainer"] p {font-size:.875rem;color:#536378;}
[data-testid="stRadio"] {position:static;z-index:auto;}
div[role="radiogroup"] {box-shadow:none;border-color:#dce3ea;background:#fff;}
div[role="radiogroup"] label {font-size:1rem;padding:.65rem 1rem;}
div[role="radiogroup"] label:has(input:checked) {background:#e4f3ee;color:#155548;box-shadow:none;}
button[kind="primary"], button[data-testid="stBaseButton-primary"] {background:#176253!important;border-color:#176253!important;color:white!important;}
button[kind="primary"] p, button[data-testid="stBaseButton-primary"] p {color:white!important;}
[data-testid="stButton"] button, [data-testid="stDownloadButton"] button {min-height:44px;}
.頂導 {padding:.3rem 0 .8rem;}.品牌文字 small {font-size:.75rem;letter-spacing:.05em;}.專業標 {display:none;}
.同步徽章 {font-size:.875rem;background:#fff;color:#536378;border-color:#dce3ea;}
.decision-heading {margin:1.25rem 0 .35rem;font-size:clamp(1.65rem,4vw,2.15rem);font-weight:800;letter-spacing:-.03em;color:#16283b;}
.decision-card {margin:.6rem 0;padding:1.5rem;border:1px solid #c9ddd6;border-left:5px solid #176253;border-radius:14px;background:#fff;}
.decision-card h2 {font-size:clamp(1.4rem,3.2vw,1.9rem);line-height:1.4;margin:.65rem 0;color:#16283b!important;}
.decision-label {font-size:.875rem;font-weight:700;color:#176253;letter-spacing:.03em;}
.decision-state {display:inline-block;padding:.25rem .6rem;margin-left:.5rem;background:#e8f3ee;border-radius:6px;font-size:.875rem;color:#155548;}
.decision-facts {display:grid;grid-template-columns:1fr 1fr;gap:1rem;border-top:1px solid #e5eaf0;margin-top:1rem;padding-top:1rem;}
.decision-facts small {font-size:.875rem;color:#536378;display:block;margin-bottom:.2rem;}
.decision-facts strong {font-size:1rem;color:#16283b;line-height:1.6;}
.decision-note {font-size:.875rem;color:#536378;line-height:1.65;}
.decision-card p {font-size:1rem;line-height:1.75;color:#293b4c;}
.decision-queue {display:flex;gap:1rem;padding:1rem 0;border-bottom:1px solid #e5eaf0;}
.decision-queue b {font-size:1rem;color:#16283b;}.decision-queue span {font-size:.875rem;color:#536378;}
.主視覺 {min-height:0;padding:1rem 1.2rem;background:#fff;box-shadow:none;margin:.8rem 0;}
.主視覺::after,.主視覺徽章,.主視覺 .小標 {display:none;}.主標 {font-size:1.5rem;line-height:1.4;}.主標 br {display:none;}
.主標 span {color:#176253;}.說明 {font-size:1rem;}
.速覽區塊 li {font-size:1rem;}.速覽頂列,.速覽標籤列 span {font-size:.875rem;}
.配置總覽,.配置詳情 {min-height:0;}.配置總覽 p,.配置詳情 p,.配置詳情 li {font-size:1rem;}
.攻略卡 p {font-size:1rem;line-height:1.7;}.攻略卡 h3 {font-size:1.125rem;}.攻略卡 .更新日,.卡片頂列 span {font-size:.875rem;}
@media(max-width:640px) {.block-container {padding:1rem 1rem 3rem;}.decision-card {padding:1rem;}.decision-facts {grid-template-columns:1fr;gap:.65rem;}.同步徽章 {display:none;}div[role="radiogroup"] label {padding:.5rem;font-size:.9rem;}}
@media(prefers-reduced-motion:reduce) {* {scroll-behavior:auto!important;transition:none!important;}}
</style>
"""


def profile() -> dict:
    return engine.clean_profile(st.session_state.get("player_profile", {}))


def navigate(page: str) -> None:
    st.session_state["主導覽"] = page


def edit_resource(resource: str) -> None:
    section = {"收藏之心": "普通典藏館", "高級收藏之心": "進階典藏館",
               "傳奇收藏自選": "收藏品", "覺醒核心": "角色與模式",
               "神器核心": "裝備與科技", "科技配件": "裝備與科技"}.get(resource, "角色與模式")
    st.session_state["profile_section"] = section
    navigate("我的帳號")


def complete_step(step: dict) -> None:
    """User confirms an in-game action; update notes only, not the game."""
    values = dict(step.get("update") or {})
    if not values:
        return
    # Never keep an old balance or a prior slot's price after an upgrade.
    if step["id"] == "hall_open":
        values.update(hearts=None, next_slot_cost=None)
    elif step["resource"] == "高級收藏之心":
        values.update(advanced_hearts=None, advanced_cost=None, advanced_quote=None)
    elif step["resource"] == "覺醒核心":
        values.update(awakening_cores=None, s_shards=None, quantum_ready=None)
    elif step["resource"] == "神器核心":
        values.update(relic_cores=None, gear_materials_ready=None)
    elif step["resource"] == "傳奇收藏自選":
        values.update(red_boxes=None)
    st.session_state.setdefault("completed_steps", []).append(step["title"])
    save(values)


def save(values: dict) -> None:
    try:
        combined = {**profile(), **values}
        st.session_state["player_profile"] = engine.clean_profile(combined)
        st.session_state["profile_updated"] = datetime.now().isoformat(timespec="minutes")
        st.session_state["editor_revision"] = st.session_state.get("editor_revision", 0)+1
        st.session_state["profile_notice"] = "已更新，下一步建議已重新計算。"
        st.session_state["pending_navigation"] = "下一步"
        st.rerun()
    except ValueError as exc:
        st.error(str(exc))


def number(label: str, key: str, p: dict, maximum: int = 10000000):
    return st.number_input(label, min_value=0, max_value=maximum, value=p.get(key), step=1,
                           placeholder="尚未填寫", key=f"profile_{key}_{st.session_state.get('editor_revision', 0)}")


def choice(label: str, key: str, values: tuple, p: dict):
    options = (None, *values)
    return st.selectbox(label, options, index=options.index(p.get(key)) if p.get(key) in options else 0,
        format_func=lambda x: "尚未確認" if x is None else "是" if x is True else "否" if x is False else str(x),
        key=f"profile_{key}_{st.session_state.get('editor_revision', 0)}")


def stars(label: str, key: str, p: dict):
    return st.text_input(label, value="、".join(engine.STARS[n] for n in p.get(key, [])),
        placeholder="例如：紅5、黃5、黃3；空格填 0", key=f"profile_{key}_{st.session_state.get('editor_revision', 0)}")


def render_home() -> None:
    p = profile()
    st.markdown('<h1 class="decision-heading">下一份資源，先升哪裡？</h1>', unsafe_allow_html=True)
    st.caption("先完成一個有效門檻，再決定下一步。")
    if notice := st.session_state.pop("profile_notice", None):
        st.success(notice)
    left, right = st.columns([3, 1])
    with left:
        scope = st.selectbox("這次要安排的資源", ("自動排序", *engine.RESOURCES), key="decision_resource")
    with right:
        st.button("更新我的帳號", width="stretch", on_click=navigate, args=("我的帳號",))
    st.caption(f"主要模式：{p['mode']} · " + (f"{p['survivor']} R{p['awakening']}" if p['survivor'] and p['awakening'] is not None else "主位尚未確認"))
    result = engine.recommend(p, scope)
    step = result["primary"]
    if not st.session_state.get("player_profile"):
        with st.container(border=True):
            st.subheader("先告訴我你正在玩誰")
            st.write("只填三項開始。之後再補典藏館與裝備，不用一次填完整張表。")
            with st.form("quick_profile"):
                mode = st.selectbox("主要模式", engine.MODES)
                hero = st.selectbox("主位特工", ("維納托", "塔洛莎", "楊大師", "其他"), index=None, placeholder="選目前主位")
                level = st.number_input("覺醒等級（不是一般星數）", min_value=0, max_value=8, value=None, placeholder="例如 6")
                if st.form_submit_button("建立我的升級路線", type="primary", width="stretch"):
                    if hero is None or level is None:
                        st.error("請選主位並填覺醒等級；未覺醒填 0。")
                    else:
                        save({"mode": mode, "survivor": hero, "awakening": level})
        st.caption("帳號紀錄只在本次瀏覽工作階段保留；可在「我的帳號」下載與匯入，方便下次接續。")
        return
    if not step:
        with st.container(border=True):
            st.subheader("這個範圍還不能排出下一筆投資")
            st.write("可能是該項資料未填，或已超過目前收錄的門檻。先補資料，再比較；不把已完成項目重排成第一名。")
            st.button("補上會影響順位的資料", type="primary", on_click=navigate, args=("我的帳號",))
    else:
        esc = lambda key: html.escape(str(step.get(key) or ""))
        st.markdown(f'''<section class="decision-card">
          <div class="decision-label">優先 01 · {esc('resource')} <span class="decision-state">{esc('status')}</span></div>
          <h2>{esc('title')}</h2><p>{esc('why')}</p>
          <div class="decision-facts"><div><small>做到這裡</small><strong>{esc('target')}</strong></div>
          <div><small>需要投入</small><strong>{esc('cost')}</strong></div></div>
          <p class="decision-note">停手條件：{esc('stop')}</p></section>''', unsafe_allow_html=True)
        if step["gap"]:
            st.info(step["gap"])
        if step["effect"]:
            st.write(f"**解鎖效果：** {step['effect']}")
        if step["current"]:
            st.caption(f"依據你的資料：{step['current']}")
        a, b = st.columns(2)
        with a:
            st.button("補上這一步的資料", type="primary", width="stretch", on_click=edit_resource, args=(step["resource"],))
        with b:
            st.link_button("查看這個門檻的原始依據", step["source"], width="stretch")
        with st.expander("為什麼先做這個？哪些情況會改變答案？"):
            st.write("排序先看材料齊全且能啟動的項目，再看待存材料的目標。缺星數的進階格不會被標成可執行。")
            st.write("不同資源可分別安排；收藏之心不足，不會阻止你用覺醒核心升主位。自動排序是規則建議，不是實測傷害排名。")
            if step["caution"]:
                st.warning(step["caution"])
            st.caption(f"規則核對：{engine.CHECKED}；來源為社群攻略。材料以遊戲內本次預覽為準。")
        if step.get("update"):
            with st.expander("這一步已在遊戲完成？更新紀錄"):
                st.caption("僅更新本站的星數／槽位紀錄；實際庫存請重新填寫。不會操作遊戲。")
                if st.button("我已在遊戲完成，排下一步", key=f"complete_{step['id']}"):
                    complete_step(step)
        alternatives = result["alternatives"]
        with st.expander(f"接著考慮什麼（{len(alternatives)} 項，先不必同時做）"):
            if not alternatives:
                st.write("目前沒有另一個具備足夠資料的候選目標。")
            for index, item in enumerate(alternatives[:3], 2):
                st.markdown(f"**{index:02d} · {item['title']}** — {item['status']}")
                st.write(f"停在：{item['target']}。{item['gap'] or item['why']}")
            if len(alternatives) > 3:
                st.caption("其他候選可由上方資源選單逐項查看。")
    with st.expander(f"帳號尚缺 {len(result['missing'])} 組資料／已完成門檻"):
        for item in result["missing"]:
            st.write(f"待補：{item}")
        for item in result["complete"]:
            st.success(item)
        for item in st.session_state.get("completed_steps", [])[-3:]:
            st.caption(f"本次已記錄完成：{item}")
        st.caption("只比較已填資料涵蓋的路線；未填不等於零，已完成不代表整個帳號滿配。")


def render_profile() -> None:
    p = profile()
    st.markdown('<h1 class="decision-heading">我的帳號</h1>', unsafe_allow_html=True)
    st.caption("只打開你這次要更新的項目。留白代表未知；0 代表確定沒有。")
    if notice := st.session_state.pop("profile_notice", None):
        st.success(notice)
    st.button("← 回到我的下一步", on_click=navigate, args=("下一步",))
    sections = ("角色與模式", "普通典藏館", "進階典藏館", "收藏品", "裝備與科技")
    section = st.selectbox("這次更新哪一項", sections, key="profile_section")
    with st.form(f"edit_{section}"):
        values = {}
        if section == "角色與模式":
            values["mode"] = st.selectbox("主要模式", engine.MODES, index=engine.MODES.index(p["mode"]))
            values["survivor"] = choice("主位特工", "survivor", ("維納托", "塔洛莎", "楊大師", "其他"), p)
            l, r = st.columns(2)
            with l:
                values["awakening"] = number("主位覺醒等級", "awakening", p, 8)
                values["awakening_cores"] = number("現有覺醒核心", "awakening_cores", p, 10000)
            with r:
                values["taloxa"] = number("塔洛莎覺醒等級", "taloxa", p, 8)
                values["s_shards"] = number("可用於主位的S特工碎片", "s_shards", p, 100000)
            values["quantum_ready"] = choice("量子碎片是否足夠升主位下一階", "quantum_ready", (True, False), p)
        elif section == "普通典藏館":
            st.write("填所有套裝的合計；紅品質指傳奇收藏，不是史詩收藏的紅星。")
            for label, key in (("全部已開槽位", "slots"), ("不同紅品質收藏持有數", "red_owned"), ("已放入普通槽位的紅收藏數", "red_placed")):
                values[key] = number(label, key, p, 100)
            values["hearts"] = number("現有收藏之心", "hearts", p)
            values["next_slot_cost"] = number("各套比較後，下一個最便宜槽位的顯示價格", "next_slot_cost", p)
            st.caption("開完一格後，請更新下一格價格；各套價格可能不同。")
        elif section == "進階典藏館":
            st.write("星數按預定槽位順序填。黃5＝5星，紅1＝6星，紅5＝10星；兩套不能重複放同一件收藏。")
            values["adv1"] = number("第一套已進階格數", "adv1", p, 4)
            s1 = stars("第一套預定放入的傳奇收藏星數（最多4件）", "stars1", p)
            values["adv2"] = number("第二套已進階格數", "adv2", p, 8)
            s2 = stars("第二套預定放入的傳奇收藏星數（最多8件）", "stars2", p)
            values["advanced_hearts"] = number("現有高級收藏之心", "advanced_hearts", p, 100000)
            options = (None, *(f"adv1_{n}" for n in range(1,5)), *(f"adv2_{n}" for n in range(1,9)))
            quote = p["advanced_quote"] if p["advanced_quote"] in options else None
            values["advanced_quote"] = st.selectbox("下面的價格是查哪一格", options, index=options.index(quote),
                format_func=lambda x: "尚未查價" if x is None else f"第{x[3]}套第{x.split('_')[1]}格")
            values["advanced_cost"] = number("進階該格所需高級收藏之心（遊戲顯示）", "advanced_cost", p, 100000)
            st.caption("第二套第8格與80傳奇星同時完成才有菁英／BOSS加成。紅五星八件才是80星。")
        elif section == "收藏品":
            values["neck"] = choice("目前穿的項鍊", "neck", ("破壞者徽記", "其他"), p)
            values["memory"] = st.selectbox("記憶編輯器星數", (None, *range(11)),
                index=0 if p["memory"] is None else p["memory"]+1,
                format_func=lambda x: "尚未確認" if x is None else engine.STARS[x])
            values["ss_boots"] = choice("是否使用SS冰霜戰靴", "ss_boots", (True, False), p)
            bs = stars("SS鞋套裝星數：賽博圖騰柱、複製寶鏡、夢境拼圖、基因編輯器", "boot_stars", p)
            values["red_boxes"] = number("傳奇收藏自選箱庫存", "red_boxes", p, 10000)
            st.caption("每箱碎片量與可選期數不同，本站不會只看箱數就判定必定能升星。")
        else:
            values["weapon"] = choice("主武器", "weapon", ("雙絕槍", "其他"), p)
            l, r = st.columns(2)
            with l:
                values["weapon_e"] = number("雙絕槍永恆神鑄 E", "weapon_e", p, 5)
            with r:
                values["weapon_v"] = number("雙絕槍虛空神鑄 V", "weapon_v", p, 5)
            values["relic_cores"] = number("現有神器核心", "relic_cores", p, 10000)
            values["gear_materials_ready"] = choice("E1所需S裝及其他材料是否齊全", "gear_materials_ready", (True, False), p)
            for label, key in (("已有雙生無人機", "twin_drone"), ("已有紅無人機配件", "drone_red"), ("已有紅力場配件", "forcefield_red")):
                values[key] = choice(label, key, (True, False), p)
            st.caption("高階神鑄需要完整六件裝備比較；本站不會只憑武器就要求你拆掉其他裝備。")
        if st.form_submit_button("儲存並重新排序", type="primary", width="stretch"):
            try:
                if section == "進階典藏館":
                    values["stars1"] = engine.parse_stars(s1, 4)
                    values["stars2"] = engine.parse_stars(s2, 8)
                if section == "收藏品":
                    values["boot_stars"] = engine.parse_stars(bs, 4)
                    if values["boot_stars"] and len(values["boot_stars"]) != 4:
                        raise ValueError("鞋子套裝請填四件星數；沒持有的那件填 0。")
                save(values)
            except ValueError as exc:
                st.error(str(exc))
    with st.expander("備份／接續上次帳號紀錄"):
        st.caption("本次連線中切頁會保留；重新整理、斷線或換裝置可能重置。下載檔案後可隨時匯入。沒有讀取遊戲帳號，也不會替你花遊戲資源。")
        st.download_button("下載我的帳號紀錄", engine.export_profile(p), "dada-profile.json", "application/json")
        upload = st.file_uploader("匯入本站帳號紀錄", type=["json"])
        if st.button("套用匯入紀錄", disabled=upload is None):
            try:
                imported = engine.import_profile(upload.getvalue())
                st.session_state["player_profile"] = imported
                st.session_state["editor_revision"] = st.session_state.get("editor_revision", 0)+1
                st.session_state["pending_navigation"] = "下一步"
                st.rerun()
            except ValueError as exc:
                st.error(str(exc))
