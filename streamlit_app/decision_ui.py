"""One decision at a time. Profiles are isolated in Streamlit session state."""
from __future__ import annotations

from datetime import datetime
import html
import streamlit as st
import next_step as engine
from direction_tools import execution_plan, related_guide, operating_steps
from ui_art import guide_icon




def profile() -> dict:
    return engine.clean_profile(st.session_state.get("player_profile", {}))


def navigate(page: str) -> None:
    st.session_state["主導覽"] = page


def edit_resource(resource: str) -> None:
    section = {"收藏之心": "普通典藏館", "高級收藏之心": "進階典藏館",
               "傳奇收藏自選": "收藏品", "覺醒核心": "角色與模式",
               "神器核心": "裝備與科技", "科技配件": "裝備與科技", "寵物材料": "寵物"}.get(resource, "角色與模式")
    st.session_state["profile_section"] = section
    navigate("我的帳號")


def complete_step(step: dict) -> None:
    """User confirms an in-game action; update notes only, not the game."""
    try:
        preview = engine.completion_preview(profile(), step)
        save(preview["profile"], completed_title=step["title"])
    except ValueError as exc:
        st.error(str(exc))


def save(values: dict, completed_title: str | None = None, restoring: bool = False) -> None:
    try:
        before = profile()
        combined = engine.clean_profile({**before, **values})
        if not completed_title and not restoring:
            # Saving an edited balance is the user's confirmation of its value.
            combined["estimated_balances"] = [key for key in combined["estimated_balances"] if key not in values]
            combined = engine.invalidate_pet_verification(before, combined)
        st.session_state["completion_undo"] = None
        if completed_title:
            st.session_state["completion_undo"] = {"before": before, "title": completed_title}
            st.session_state.setdefault("completed_steps", []).append(completed_title)
        st.session_state["player_profile"] = combined
        st.session_state.pop("route_selected_id", None)
        st.session_state["profile_updated"] = datetime.now().isoformat(timespec="minutes")
        st.session_state["editor_revision"] = st.session_state.get("editor_revision", 0)+1
        st.session_state["profile_notice"] = "配置已儲存，升級順序已重算。"
        st.session_state["pending_navigation"] = "下一步"
        st.rerun()
    except ValueError as exc:
        st.error(str(exc))


def undo_completion() -> None:
    if previous := st.session_state.pop("completion_undo", None):
        st.session_state["player_profile"] = previous["before"]
        st.session_state.pop("route_selected_id", None)
        st.session_state["completed_steps"] = st.session_state.get("completed_steps", [])[:-1]
        st.session_state["editor_revision"] = st.session_state.get("editor_revision", 0)+1
        st.session_state["profile_notice"] = "已撤回剛才的完成紀錄，回到升級前的資料。沒有操作遊戲。"
        st.rerun()


def number(label: str, key: str, p: dict, maximum: int = 10000000):
    return st.number_input(label, min_value=0, max_value=maximum, value=p.get(key), step=1,
                           placeholder="尚未填寫", key=f"profile_{key}_{st.session_state.get('editor_revision', 0)}_{p.get('_input_scope', '')}")


def choice(label: str, key: str, values: tuple, p: dict, label_visibility: str = "visible"):
    options = (None, *values)
    return st.selectbox(label, options, index=options.index(p.get(key)) if p.get(key) in options else 0,
        label_visibility=label_visibility,
        format_func=lambda x: "尚未確認" if x is None else "是" if x is True else "否" if x is False else str(x),
        key=f"profile_{key}_{st.session_state.get('editor_revision', 0)}_{p.get('_input_scope', '')}")


def stars(label: str, key: str, p: dict):
    return st.text_input(label, value="、".join(engine.STARS[n] for n in p.get(key, [])),
        placeholder="例如：紅5、黃5、黃3；空格填 0", key=f"profile_{key}_{st.session_state.get('editor_revision', 0)}")


def star_choice(label: str, key: str, p: dict):
    return st.selectbox(label, (None, *range(11)), index=0 if p[key] is None else p[key]+1,
        format_func=lambda x: "尚未確認" if x is None else engine.STARS[x],
        key=f"profile_{key}_{st.session_state.get('editor_revision', 0)}")


def render_backup(p: dict, first_visit: bool = False) -> None:
    with st.popover("接續上次紀錄" if first_visit else "備份與匯入", width="stretch"):
        st.caption("本次連線切頁會保留；重新整理、斷線或換裝置可能重置。可下載 JSON 備份再匯入，不需要遊戲帳號密碼。")
        if not first_visit:
            st.download_button("下載我的帳號紀錄", engine.export_profile(p), "dada-profile.json", "application/json", on_click="ignore")
        upload = st.file_uploader("匯入本站帳號紀錄", type=["json"])
        if st.button("套用匯入紀錄", disabled=upload is None):
            try:
                imported = engine.import_profile(upload.getvalue())
                st.session_state["completed_steps"] = []
                save(imported, restoring=True)
            except ValueError as exc:
                st.error(str(exc))


def render_step_inputs(step: dict, p: dict) -> None:
    """One small, target-bound form instead of a trip through the whole profile."""
    kind, sid = step.get("quote_kind"), step["id"]
    p = {**p, "_input_scope": step.get("quote_key") or sid}
    advanced = sid.startswith("adv") and sid.rsplit("_", 1)[-1].isdigit()
    if not (kind or advanced or sid in ("venato", "hall_open", "lance_e1", "twin_drone", "pet_umbral", "pet_node")):
        return
    if step["status"] in ("星數未達", "資料未齊"):
        return
    with st.expander("只核對這一步的材料", expanded=any(c["state"] == "unknown" for c in step.get("checks", []))):
        st.caption(f"本次只核對：{step['title']}。沒有資料的項目留白。")
        with st.form(f"step_inputs_{sid}_{st.session_state.get('editor_revision', 0)}", border=False):
            values = {}
            if kind:
                if sid == "boots_set":
                    values["ice_armor_ready"] = choice("SS鞋永恆神鑄的冰甲已啟用", "ice_armor_ready", (True, False), p)
                if sid == "memory" and step["update"]["memory"] in (3, 5):
                    crit_profile = {**p, "crit_more_useful": p["crit_more_useful"] if p["crit_mode"] == p["mode"] else None}
                    values["crit_more_useful"] = choice("目前模式追加暴率仍有收益（含溢出轉換）", "crit_more_useful", (True, False), crit_profile)
                    values["crit_mode"] = p["mode"]
                stock_key = "red_boxes" if kind == "collection" else "awakening_cores"
                label = "現有傳奇收藏自選箱" if kind == "collection" else "現有覺醒核心"
                values[stock_key] = number(label, stock_key, p, 10000)
                quote = p["step_quotes"].get(step["quote_key"], {"cost": None, "materials_ready": None})
                cost = st.number_input("從目前狀態到目標，合計要用多少箱" if kind == "collection" else "從目前覺醒到目標，合計需要多少核心",
                    min_value=0, max_value=10000000, value=quote["cost"], step=1, placeholder="核對整段需求，不只下一小階")
                ready = st.selectbox("箱子可選目標期數，且其他碎片／條件都符合" if kind == "collection" else "目標角色碎片、量子碎片與連攜條件都符合",
                    (None, True, False), index=(None, True, False).index(quote["materials_ready"]),
                    format_func=lambda x: "尚未確認" if x is None else "已核對，符合" if x else "尚未齊全")
                st.caption("需要多階升級時，請合計整段材料；不同期自選箱不可只加總箱數。這是你核對的材料，不是本站推算成本。")
                if sid == "boots_set":
                    st.warning("本目標是四件全部達到黃三星：請合計所有缺件，並確認鞋子永恆神鑄的冰甲已啟用。只升好一件，請到「我的帳號」更新實際星數。")
                quotes = dict(p["step_quotes"])
                quotes[step["quote_key"]] = {"cost": cost, "materials_ready": ready}
                values["step_quotes"] = dict(list(quotes.items())[-32:])
            elif sid == "venato":
                values["awakening_cores"] = number("現有覺醒核心", "awakening_cores", p, 10000)
                values["s_shards"] = number("可用於主位的S特工碎片", "s_shards", p, 100000)
                values["quantum_ready"] = choice("量子碎片是否足夠升主位下一階", "quantum_ready", (True, False), p)
            elif sid == "hall_open":
                values["hearts"] = number("現有收藏之心", "hearts", p)
                values["next_slot_cost"] = number("下一格的遊戲顯示價格", "next_slot_cost", p)
            elif advanced:
                values["advanced_hearts"] = number("現有高級收藏之心", "advanced_hearts", p, 100000)
                quoted = p["advanced_cost"] if p["advanced_quote"] == sid else None
                values["advanced_cost"] = number("這一格的進階顯示價格", "advanced_cost", {**p, "advanced_cost": quoted}, 100000)
                values["advanced_quote"] = sid
            elif sid == "lance_e1":
                values["relic_cores"] = number("現有神器核心", "relic_cores", p, 10000)
                values["gear_materials_ready"] = choice("E1所需S裝及其他材料是否齊全", "gear_materials_ready", (True, False), p)
            elif sid in ("pet_node", "pet_umbral"):
                if sid == "pet_umbral":
                    values["pet_preview_matches"] = choice("幽暗之靈目標效果與遊戲預覽一致", "pet_preview_matches", (True, False), p)
                values["pet_materials_ready"] = choice("到本節點的全部本體、碎片、核心及其他材料已足", "pet_materials_ready", (True, False), p)
                st.caption("核對整段需求；沒有寵物剩餘庫存資料時不推算扣款，也不消耗特工覺醒核心。")
            else:
                values["forcefield_red"] = choice("已有紅力場配件", "forcefield_red", (True, False), p)
            if st.form_submit_button("更新這一步的材料", type="primary", width="stretch"):
                save(values)


def next_check(p: dict, scope: str) -> str | None:
    """Choose the next unanswered system; never demand every field at once."""
    groups = {
        "普通典藏館": any(p[k] is None for k in ("slots", "red_owned", "red_placed")),
        "進階典藏館": any(p[f"adv{n}"] is None or not p[f"stars{n}"] for n in (1, 2)),
        "收藏品": p["neck"] is None or p["neck"] == "破壞者徽記" and p["memory"] is None
                   or p["ss_boots"] is None or p["ss_boots"] and len(p["boot_stars"]) != 4
                   or (p["drone_red"] or p["twin_drone"]) and p["dark_matter"] is None,
        "角色與模式": p["survivor"] is None or p["awakening"] is None
                     or p["survivor"] == "維納托" and p["taloxa"] is None,
        "裝備與科技": p["weapon"] is None or p["weapon"] == "雙絕槍" and (p["weapon_e"] is None or p["weapon_v"] is None)
                     or p["twin_drone"] is None or p["twin_drone"] is False and p["drone_red"] is None,
        "寵物": p["pet_kind"] is None or p["pet_kind"] == "未持有" or not p["pet_target"]
                 and not (p["pet_kind"] == "異世寵物" and p["pet_name"] == "幽暗之靈" and p["pet_star"] is not None and p["pet_star"] > 0),
    }
    relevant = {"收藏之心": ("普通典藏館",), "高級收藏之心": ("進階典藏館",),
        "傳奇收藏自選": ("普通典藏館", "收藏品", "裝備與科技"), "覺醒核心": ("角色與模式", "裝備與科技"),
        "神器核心": ("裝備與科技",), "科技配件": ("裝備與科技",), "寵物材料": ("寵物",)}
    return next((section for section in relevant.get(scope, groups) if groups[section]), None)


def render_next_check(p: dict, scope: str) -> None:
    section = next_check(p, scope)
    with st.container():
        if section:
            st.subheader(f"待核對：{section}")
            st.write("補齊這組資料，才能判斷下一個升級目標。目前先保留資源。")
            # The three hall counts uncover zero-cost actions before asking for costs.
            if section == "普通典藏館":
                with st.form("next_check_hall"):
                    values = {key: number(label, key, p, 100) for label, key in (
                        ("全部已開槽位", "slots"), ("不同紅品質收藏持有數", "red_owned"), ("已放入普通槽位的紅收藏數", "red_placed"))}
                    st.caption("這裡的紅收藏指原生傳奇品質；黃一星就算一件。")
                    if st.form_submit_button("檢查有沒有免費提升", type="primary", width="stretch"):
                        save(values)
            else:
                if st.button(f"只填{section}", type="primary"):
                    st.session_state["profile_section"] = section
                    st.session_state["pending_navigation"] = "我的帳號"
                    st.rerun()
        else:
            st.subheader("目前沒有可確認的下一個門檻")
            st.write("先保留資源。這不代表你的帳號已經滿配；高階六件神鑄、同調與協同互換，需要更完整配置或同場實測。")
            st.link_button("開啟高階配置試算工具", engine.CALCULATOR)
            st.button("校正帳號現況", on_click=edit_resource, args=(scope,))


def page_heading(title: str, description: str) -> None:
    st.markdown(f'<h1 class="page-heading">{html.escape(title)}</h1><p class="page-deck">{html.escape(description)}</p>',
                unsafe_allow_html=True)


def workflow(active: int) -> None:
    labels = ("1 填配置", "2 看目標", "3 核材料")
    spans = "".join(f'<span class="{"active" if index == active else ""}">{label}</span>' for index, label in enumerate(labels))
    st.markdown(f'<div class="workflow-strip" aria-label="升級規劃流程">{spans}</div>', unsafe_allow_html=True)


def render_completion(p: dict, step: dict) -> None:
    if not step.get("update"):
        return
    # Re-mount the confirmation surface when its account/target changes.
    # Older supported Streamlit versions do not need a keyed-popover API.
    with st.container(key=f"completion_scope_{engine.action_token(p, step)}"):
        with st.popover("記錄遊戲內完成", width="stretch"):
            st.write(f"記錄的完整目標：{step['target']}")
            try:
                preview = engine.completion_preview(p, step)
                for row in preview["balances"]:
                    st.caption(f"{row['resource']}：{row['before']:,} − {row['used']:,} → 推算剩餘 {row['after']:,}")
                if preview["unknown"]:
                    st.caption("無法可靠扣除，完成後需重新核對：" + "、".join(preview["unknown"]))
                st.caption("僅更新本站紀錄，不操作遊戲。已知成本才計算結餘；下一目標的價格與附加材料重新核對。")
                if st.button("我已在遊戲完成，排下一步", type="primary", key=f"complete_{engine.action_token(p, step)}"):
                    complete_step(step)
            except ValueError as exc:
                st.warning(str(exc))


def render_decision(p: dict, step: dict) -> None:
    esc = lambda key: html.escape(str(step.get(key) or ""))
    state_class = "" if step["status"] in ("現在可做", "材料已足") else "blocked" if step["status"] in ("星數未達", "資料未齊") else "pending"
    lead = "優先執行" if step["status"] in ("現在可做", "材料已足") else "儲備目標" if step["status"] == "先存資源" else "待核對目標"
    if step["status"] == "先做玩法調整":
        lead = "先調整玩法"
    global_first = engine.recommend(p)["primary"]
    if global_first and step["id"] != global_first["id"]:
        lead = "比較目標（非全帳號第一順位）"
    with st.container(key="route_layout"):
        main, notes = st.columns([2.15, 1], gap="large")
        with main:
            st.markdown(f'''<section aria-label="優先升級目標">
              <div class="decision-lead"><span class="section-index">01</span>{lead} / {esc('resource')}
              <span class="decision-state {state_class}">{esc('status')}</span></div>
              <h2 class="decision-title">{esc('title')}</h2>
              <dl class="decision-facts"><div><dt>目標門檻</dt><dd>{esc('target')}</dd></div>
              <div><dt>所需資源</dt><dd>{esc('cost')}</dd></div></dl></section>''', unsafe_allow_html=True)
            st.markdown(f'<p class="decision-because"><b>為什麼排這一步</b> {esc("why")}</p>', unsafe_allow_html=True)
            if step.get("quote_kind") or step["id"] in ("pet_node", "pet_umbral"):
                st.caption("依據：你核對的遊戲預覽；帳號增傷未實測。")
            elif step["id"] == "hall_fill" or step["id"].endswith("_rearrange"):
                st.caption("依據：已填的持有與槽位資料；這一步不需新材料。")
            elif step["id"] not in ("zone", "survival_check"):
                st.caption("依據：已收錄社群門檻與帳號材料；帳號增傷未實測。")
            if step.get("update"):
                after = engine.following_step(p, step)
                target = f"{engine.SYSTEMS[after['resource']]} · {after['title']}（{after['status']}）" if after else "先補其他系統資料，再決定投入"
                st.markdown(f'<p class="roadmap-after"><b>這一步完成後 →</b> {html.escape(target)}</p>', unsafe_allow_html=True)
            plan = execution_plan(step)
            verify = f'<p>{html.escape(plan["verify"])}</p>' if plan["verify"] else ""
            operation = operating_steps(step)
            instructions = "".join(f"<li>{html.escape(item)}</li>" for item in operation["steps"])
            st.markdown(f'''<section class="action-brief" aria-label="現在要做什麼">
                <h3>操作步驟</h3><p>{html.escape(plan['action'])}</p>{verify}
                <div class="operation-entry">遊戲入口：{html.escape(operation['entry'])}</div>
                <ol class="operation-steps">{instructions}</ol></section>''', unsafe_allow_html=True)
            if step.get("checks"):
                indicators = {"ready": "已足", "short": "缺", "unknown": "待確認"}
                rows = "".join(f'<div class="decision-check {c["state"]}" role="listitem"><b>{indicators[c["state"]]} · {html.escape(c["label"])}</b><span>{html.escape(c["detail"])}</span></div>' for c in step["checks"])
                st.markdown(f'<h3 class="ledger-title">材料核對</h3><div class="decision-checks" role="list" aria-label="這一步的必要條件">{rows}</div>', unsafe_allow_html=True)
            elif step["gap"]:
                st.info(step["gap"])
            render_step_inputs(step, p)
        with notes:
            with st.container(key="route_notes"):
                note_rows = ""
                for label, key, css in (("解鎖效果", "effect", ""), ("停手條件", "stop", "stop"), ("目前紀錄", "current", "")):
                    if step.get(key):
                        note_rows += f'<dl class="route-note {css}"><dt>{label}</dt><dd>{esc(key)}</dd></dl>'
                st.markdown(f'<aside aria-label="執行備忘"><h3 class="notes-heading">執行備忘</h3>{note_rows}</aside>', unsafe_allow_html=True)
                render_completion(p, step)
                st.button("補上這一步的資料", width="stretch", on_click=edit_resource, args=(step["resource"],))
                st.button("看這一步的做法與取捨", width="stretch", on_click=read_direction_guide, args=(related_guide(step),))
                st.link_button("查看這個門檻的原始依據", step["source"], width="stretch")
                st.caption("按已收錄門檻排序，非實測傷害排名。投入前須核對材料。")


def read_direction_guide(slug: str) -> None:
    # Import at callback time: guide_ui shares page_heading from this module.
    from guide_ui import open_guide
    open_guide(slug)


def render_reasoning(result: dict) -> None:
    with st.expander("排序依據與其他候選"):
        if result["primary"]:
            st.write(result["primary"]["why"])
            st.write(engine.ranking_reason(result))
            st.caption("各種資源分開比較；排序範圍限於已填配置與已收錄路線。")
            if result["primary"]["caution"]:
                st.warning(result["primary"]["caution"])
            st.caption(f"規則核對：{engine.CHECKED}；來源為社群攻略。材料以遊戲內本次預覽為準。")
        alternatives = result["alternatives"]
        if alternatives:
            st.markdown("#### 其他可比較的目標")
            st.caption("同系統仍可比較的節點；跨系統順序已列在上方。完成一步會重新計算。")
            for index, item in enumerate(alternatives[:3], 2):
                st.markdown(f'''<div class="decision-queue"><span class="queue-index">{index:02d}</span><div>
                  <div class="queue-title">{html.escape(item['title'])} · {html.escape(item['status'])}</div>
                  <p class="queue-detail">停在：{html.escape(item['target'])}。{html.escape(item['gap'] or item['why'])}</p>
                  </div></div>''', unsafe_allow_html=True)
            if len(alternatives) > 3:
                st.caption("其餘候選可從資源選單查看。")
        st.markdown("#### 帳號核對")
        st.caption(f"尚缺 {len(result['missing'])} 組資料。未填不等於零；已完成門檻不代表整個帳號滿配。")
        for item in result["missing"]:
            st.write(f"待補：{item}")
        for item in result["complete"]:
            st.write(f"已完成：{item}")
        for item in st.session_state.get("completed_steps", [])[-3:]:
            st.caption(f"本次已記錄完成：{item}")


def pause_character() -> None:
    p = profile()
    st.session_state["decision_resource"] = "自動排序"
    save({"awakening_goal": p["awakening"]})


def select_route(sid: str) -> None:
    st.session_state["decision_resource"] = "自動排序"
    st.session_state["route_selected_id"] = sid


def render_roadmap(p: dict, shown: dict | None) -> None:
    plan = engine.roadmap(p)
    with st.container(key="cross_system_roadmap"):
        st.markdown('<h2 class="roadmap-heading">跨系統優先順序</h2>', unsafe_allow_html=True)
        st.caption("先完成已備妥的節點；同樣備妥才按已收錄門檻排序。不同材料可分開存，不是總傷害效益排名。")
        for item in plan["queue"]:
            details, open_action = st.columns([5, 1.25], vertical_alignment="center")
            with details:
                badge = "可完成" if item["status"] in engine.READY_STATES else item["status"]
                st.markdown(f'''<div class="roadmap-row"><span class="roadmap-rank">{item['rank']:02d}</span><div>
                  <div class="roadmap-line"><b>{html.escape(item['system'])}</b><span>{html.escape(badge)}</span></div>
                  <p>{html.escape(item['title'])}</p><small>停在：{html.escape(item['target'])}</small>
                  </div></div>''', unsafe_allow_html=True)
            with open_action:
                st.button(f"看 {item['rank']}", key=f"route_open_{item['id']}", width="stretch",
                          on_click=select_route, args=(item["id"],))
        if not plan["queue"]:
            st.write("尚無完整路線；先核對下面的缺項，不把未知配置排成最後一名。")
        for item in plan["complete"]:
            st.caption(f"已達標 · {item}")
        for item in plan.get("deferred", []):
            st.markdown(f'<p class="smart-hold"><b>先不投入 · {html.escape(item["title"])}</b><br>{html.escape(item["reason"])}</p>', unsafe_allow_html=True)
        # Missing coverage is outside the spending queue, never a low score.
        needs_collection = any(x.startswith(("典藏館：", "收藏：", "進階典藏：")) for x in plan["missing"])
        needs_pet = any(x.startswith("寵物：") for x in plan["missing"])
        if needs_collection or needs_pet:
            st.markdown('<p class="roadmap-missing">尚未完整比較所有收藏／寵物缺口：以下資料未核對，不等於低優先。</p>', unsafe_allow_html=True)
            left, right = st.columns(2)
            if needs_collection:
                with left:
                    st.button("補收藏／典藏配置", on_click=edit_resource, args=("傳奇收藏自選",), width="stretch")
            if needs_pet:
                with right:
                    st.button("補寵物配置", on_click=edit_resource, args=("寵物材料",), width="stretch")


def update_focus(key: str) -> None:
    save({"growth_focus": st.session_state[key]})


def render_next_question(p: dict, shown: dict | None = None) -> None:
    question = engine.next_question(p)
    if not question:
        return
    with st.container(key="smart_next_question"):
        st.markdown(f'<h3>現在最值得補的一項</h3><p><b>{html.escape(question["title"])}</b></p><p>{html.escape(question["why"])}</p>', unsafe_allow_html=True)
        has_form = shown and (shown.get("quote_kind") or shown["id"] in ("venato", "hall_open", "lance_e1", "twin_drone")
                              or shown["id"].startswith("adv") and shown["id"].rsplit("_", 1)[-1].isdigit())
        in_current_form = shown and (question["field"] == "crit_more_useful" and shown["id"] == "memory"
                                     or question["field"] == "ice_armor_ready" and shown["id"] == "boots_set")
        if in_current_form:
            st.caption("這項已列在上方「只核對這一步的材料」，不必重填整個帳號。")
        elif question["field"] in ("crit_more_useful", "ice_armor_ready") and shown and not has_form:
            with st.form(f"smart_question_{question['field']}_{st.session_state.get('editor_revision', 0)}", border=False):
                scoped = {**p, "_input_scope": "smart_question"}
                if question["field"] == "crit_more_useful" and p["crit_mode"] != p["mode"]:
                    scoped["crit_more_useful"] = None
                answer = choice(question["title"], question["field"], (True, False), scoped, label_visibility="collapsed")
                if st.form_submit_button("確認這項，重算建議"):
                    values = {question["field"]: answer}
                    if question["field"] == "crit_more_useful":
                        values["crit_mode"] = p["mode"]
                    save(values)
        elif question["field"] != "recipe":
            st.button("只補這組資料", key="smart_question_edit", width="stretch", on_click=edit_resource, args=(question["resource"],))


def render_home() -> None:
    p = profile()
    first_visit = not st.session_state.get("player_profile")
    heading, backup = st.columns([4, 1.2], vertical_alignment="center")
    with heading:
        page_heading("升級路線", "目前目標、停手門檻與跨系統優先順序。")
    with backup:
        render_backup(p, first_visit=first_visit)
    workflow(0 if first_visit else 1)
    if notice := st.session_state.pop("profile_notice", None):
        st.success(notice)
    if previous := st.session_state.get("completion_undo"):
        a, b = st.columns([3, 1], vertical_alignment="center")
        with a:
            st.caption(f"剛才記錄：{previous['title']}")
        with b:
            if st.button("撤回剛才紀錄", width="stretch"):
                undo_completion()
    if first_visit:
        with st.container(key="onboarding"):
            st.markdown(f'<span class="setup-art" aria-hidden="true">{guide_icon("profile")}</span><h2 class="setup-heading">建立角色配置</h2>', unsafe_allow_html=True)
            st.caption("必填：主要模式、主位特工、覺醒等級。其他配置可稍後補充。")
            with st.form("quick_profile", border=False):
                mode = st.selectbox("主要模式", engine.MODES)
                hero_col, level_col = st.columns(2)
                with hero_col:
                    hero = st.selectbox("主位特工", ("維納托", "塔洛莎", "楊大師", "其他"), index=None, placeholder="選目前主位")
                with level_col:
                    level = st.number_input("覺醒等級（不是一般星數）", min_value=0, max_value=8, value=None, placeholder="例如 6")
                if st.form_submit_button("建立我的升級路線", type="primary"):
                    if hero is None or level is None:
                        st.error("請先填主位特工與覺醒等級；不確定的帳號資料可以之後補。")
                    else:
                        save({"mode": mode, "survivor": hero, "awakening": level})
            st.markdown('<p class="setup-note">不需要遊戲帳號密碼。資料只保留於本次連線；離開前可從「備份與匯入」下載紀錄。</p>', unsafe_allow_html=True)
            st.button("查看升級排序方法", on_click=read_direction_guide, args=("upgrade-roadmap",), width="stretch", type="tertiary")
        return
    with st.container(key="route_toolbar"):
        left, context, edit = st.columns([2, 1.4, 1.2], vertical_alignment="bottom")
        with left:
            scope = st.selectbox("這次要安排的資源", ("自動排序", *engine.RESOURCES), key="decision_resource")
        with context:
            hero = f"{p['survivor']} R{p['awakening']}" if p['survivor'] and p['awakening'] is not None else "主位尚未確認"
            st.markdown(f'<div class="route-context">{html.escape(p["mode"])}<strong>{html.escape(hero)}</strong></div>', unsafe_allow_html=True)
        with edit:
            st.button("更新我的帳號", width="stretch", on_click=navigate, args=("我的帳號",))
    if p["awakening"] is not None:
        paused = p["awakening_goal"] is not None and p["awakening"] >= p["awakening_goal"]
        if paused:
            st.caption(f"主位已達階段目標 R{p['awakening_goal']}，不再追加主位核心；協同仍獨立比較。可在角色配置修改目標。")
        else:
            st.button(f"角色先停在 R{p['awakening']}，比較其他系統", on_click=pause_character, type="tertiary")
    if p["estimated_balances"]:
        labels = "、".join(engine.STOCK_LABELS[key] for key in p["estimated_balances"])
        st.caption(f"{labels}為推算結餘，未同步遊戲。有其他收入或消耗時請校正。")
    focus_key = f"decision_focus_{st.session_state.get('editor_revision', 0)}"
    st.selectbox("目前最想解決的問題", engine.FOCUSES, index=engine.FOCUSES.index(p["growth_focus"]),
                 key=focus_key, on_change=update_focus, args=(focus_key,))
    result = engine.recommend(p, scope)
    candidates = ([result["primary"]] if result["primary"] else []) + result["alternatives"]
    step = next((s for s in candidates if s["id"] == st.session_state.get("route_selected_id")), result["primary"])
    if step:
        if step != result["primary"]:
            st.info("正在查看其他順位，不代表它已變成第一優先。材料核對或完成後會重新排序。")
        render_decision(p, step)
    else:
        render_next_check(p, scope)
    render_roadmap(p, step)
    render_next_question(p, step)
    render_reasoning(result)


def render_profile() -> None:
    p = profile()
    page_heading("我的配置", "選一個系統更新，儲存後回到升級路線。留白＝未知；0＝沒有。")
    if p["estimated_balances"]:
        st.caption("部分庫存為推算值；請核對遊戲內數量後重新儲存。")
    if notice := st.session_state.pop("profile_notice", None):
        st.success(notice)
    sections = ("角色與模式", "普通典藏館", "進階典藏館", "收藏品", "裝備與科技", "寵物")
    with st.container(key="profile_layout"):
        nav, editor = st.columns([1, 3], gap="large")
        with nav:
            with st.container(key="profile_nav"):
                section = st.radio("這次更新哪一項", sections, key="profile_section", label_visibility="collapsed")
            st.button("← 回到升級路線", on_click=navigate, args=("下一步",), width="stretch")
            render_backup(p)
        with editor:
            with st.container(key="profile_editor"):
                st.markdown(f'<h2 class="editor-heading">{html.escape(section)}</h2>', unsafe_allow_html=True)
                render_profile_form(p, section)


def render_profile_form(p: dict, section: str) -> None:
    pet_editor = None
    if section == "寵物":
        pet_editor = st.radio("寵物目標怎麼填", ("來源節點：幽暗之靈", "其他寵物：遊戲預覽"),
                              index=0 if p["pet_name"] == "幽暗之靈" else 1, horizontal=True,
                              key=f"pet_editor_mode_{st.session_state.get('editor_revision',0)}")
    with st.form(f"edit_{section}", border=False):
        values = {}
        if section == "角色與模式":
            values["mode"] = st.selectbox("主要模式", engine.MODES, index=engine.MODES.index(p["mode"]))
            values["growth_focus"] = choice("目前最想解決的問題", "growth_focus", engine.FOCUSES, p) or engine.FOCUSES[0]
            values["survivor"] = choice("主位特工", "survivor", ("維納托", "塔洛莎", "楊大師", "其他"), p)
            l, r = st.columns(2)
            with l:
                values["awakening"] = number("主位覺醒等級", "awakening", p, 8)
                values["awakening_cores"] = number("現有覺醒核心", "awakening_cores", p, 10000)
            with r:
                values["taloxa"] = number("塔洛莎覺醒等級", "taloxa", p, 8)
                values["s_shards"] = number("可用於主位的S特工碎片", "s_shards", p, 100000)
            values["quantum_ready"] = choice("量子碎片是否足夠升主位下一階", "quantum_ready", (True, False), p)
            values["awakening_goal"] = number("主位階段目標 R（留白＝繼續比較下一階）", "awakening_goal", p, 8)
            st.caption("目前主位已達這個目標時，暫停追加主位核心，轉比收藏、裝備、科技與寵物；不會停掉協同路線。")
        elif section == "普通典藏館":
            st.write("填所有套裝的合計；紅品質指傳奇收藏，不是史詩收藏的紅星。")
            for label, key in (("全部已開槽位", "slots"), ("不同紅品質收藏持有數", "red_owned"), ("已放入普通槽位的紅收藏數", "red_placed")):
                values[key] = number(label, key, p, 100)
            values["hearts"] = number("現有收藏之心", "hearts", p)
            values["next_slot_cost"] = number("各套比較後，下一個最便宜槽位的顯示價格", "next_slot_cost", p)
            st.caption("開完一格後，請更新下一格價格；各套價格可能不同。")
        elif section == "進階典藏館":
            st.write("只填已持有收藏。前面先填目前已進階槽裡的星數，後面填這套預定使用的其他收藏；未持有填 0。黃5＝5星，紅1＝6星，紅5＝10星。兩套不能重複使用同一件。")
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
            values["memory"] = star_choice("記憶編輯器星數", "memory", p)
            values["dark_matter"] = star_choice("暗物質傀儡星數", "dark_matter", p)
            values["ss_boots"] = choice("是否使用SS冰霜戰靴", "ss_boots", (True, False), p)
            values["ice_armor_ready"] = choice("SS鞋永恆神鑄的冰甲已啟用", "ice_armor_ready", (True, False), p)
            crit_profile = {**p, "crit_more_useful": p["crit_more_useful"] if p["crit_mode"] == p["mode"] else None}
            values["crit_more_useful"] = choice("目前模式追加暴率仍有收益（含溢出轉換）", "crit_more_useful", (True, False), crit_profile)
            values["crit_mode"] = p["mode"]
            st.caption("暴率收益只套用目前模式；切換模式需重新確認。包含條件暴率、減暴與已解鎖溢出轉換，不只看面板100%。")
            bs = stars("SS鞋套裝星數：賽博圖騰柱、複製寶鏡、夢境拼圖、基因編輯器", "boot_stars", p)
            values["red_boxes"] = number("傳奇收藏自選箱庫存", "red_boxes", p, 10000)
            st.caption("升星需求須按可選期數及每箱碎片量核對，不能只看箱數。")
        elif section == "寵物":
            values["pet_kind"] = choice("目前主戰寵物類型", "pet_kind", ("普通輸出寵", "主人增益寵", "異世寵物", "未持有"), p)
            values["pet_skills_ready"] = choice("出戰與助戰技能已按主戰方向核對並裝入", "pet_skills_ready", (True, False), p)
            if pet_editor == "來源節點：幽暗之靈":
                values["pet_name"] = "幽暗之靈"
                values["pet_star"] = star_choice("現役異寵覺醒星級", "pet_star", p)
                values["pet_preview_matches"] = choice("幽暗之靈目標效果與遊戲預覽一致", "pet_preview_matches", (True, False), p)
                values["pet_target"], values["pet_gain"] = None, None
                st.caption("黃4以前查60%易傷20秒；已達黃4時，紅5是下一個收錄節點，不表示立即追滿。不一致就先不按本表投入。")
            else:
                values["pet_name"], values["pet_star"], values["pet_preview_matches"] = "其他", None, None
                values["pet_target"] = st.text_input("遊戲預覽的下一個完整節點（含寵物名稱與等級）", value=p["pet_target"] or "", max_chars=100,
                                                   placeholder="照遊戲填寫，例如：某主戰寵的下一階覺醒") or None
                values["pet_gain"] = choice("這個節點實際解鎖的效果", "pet_gain", ("主人增傷／有效增益", "寵物自身傷害", "只有面板／尚未確認"), p)
            values["pet_materials_ready"] = choice("本節點全部本體、碎片、核心及其他材料已足", "pet_materials_ready", (True, False), p)
            st.caption("材料需包含到目標整段。更換已填寵物／星級／目標時，舊材料確認會清除；儲存後只需核對新目標。")
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
            st.caption("高階神鑄需比較六件裝備；拆解前須計入現役裝備的效果損失。")
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
