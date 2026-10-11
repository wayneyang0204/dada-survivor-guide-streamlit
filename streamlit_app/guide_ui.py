"""Reading-first home, shared guide index, and addressable article pages."""
from __future__ import annotations

import html
from urllib.parse import quote

import streamlit as st

import guide_content as content
from ui_art import TOPIC_ART, guide_icon
from ui_interactions import kite_markup
from data_engine import load_collectible_catalog
from decision_ui import page_heading
from direction_tools import resonance_gap
from tech_routes import TECH_ROUTES, next_tech_effect
from field_tools import elaine_pet_limit, reserve_stat, compare_runs, event_window


PUBLIC_URL = "https://dada-survivor-guide.streamlit.app/"


def clear_article() -> None:
    st.session_state.pop("article_slug", None)
    st.session_state.pop("article_origin", None)
    st.query_params.pop("guide", None)
    st.session_state["seen_guide_query"] = None


def sync_query() -> None:
    slug = st.query_params.get("guide")
    if slug != st.session_state.get("seen_guide_query"):
        st.session_state["seen_guide_query"] = slug
        if slug:
            # Only a local lookup is performed. The URL never controls a request/path.
            st.session_state["article_slug"] = str(slug)[:100]
            st.session_state.pop("article_origin", None)
            st.session_state["主導覽"] = "資料庫"
        else:
            st.session_state.pop("article_slug", None)


def open_guide(slug: str) -> None:
    if not st.session_state.get("article_slug"):
        page = st.session_state.get("主導覽", "攻略首頁")
        query_key = "home_guide_search" if page == "攻略首頁" else "guide_query"
        st.session_state["article_origin"] = {
            "page": page, "query": st.session_state.get(query_key, ""),
            "category": st.session_state.get("home_topic" if page == "攻略首頁" else "guide_topic", "全部"),
        }
    st.session_state["article_slug"] = slug
    st.session_state["pending_navigation"] = "資料庫"
    st.query_params["guide"] = slug
    st.session_state["seen_guide_query"] = slug


def open_index(category: str = "全部") -> None:
    clear_article()
    st.session_state["guide_topic"] = category
    st.session_state["guide_query"] = ""
    st.session_state["資料分類"] = "本站攻略"
    st.session_state["pending_navigation"] = "資料庫"


def return_to_guides(category: str) -> None:
    origin = st.session_state.get("article_origin")
    if not origin:
        open_index(category)
        return
    clear_article()
    page = origin["page"] if origin["page"] in ("攻略首頁", "資料庫") else "資料庫"
    query_key = "home_guide_search" if page == "攻略首頁" else "guide_query"
    st.session_state[query_key] = origin["query"]
    st.session_state["guide_topic"] = origin["category"]
    if page == "攻略首頁":
        st.session_state["home_topic"] = origin["category"]
    st.session_state["資料分類"] = "本站攻略"
    st.session_state["pending_navigation"] = page


def open_collectible_catalog() -> None:
    clear_article()
    st.session_state["資料分類"] = "收藏圖鑑"
    st.session_state["pending_navigation"] = "資料庫"


def open_tool(resource: str | None = None, activity: bool = False) -> None:
    clear_article()
    if resource:
        st.session_state["decision_resource"] = resource
    st.session_state["pending_navigation"] = "活動" if activity else "下一步"


def article_button(guide: dict, prefix: str, label: str | None = None) -> None:
    st.button(label or guide["title"], key=f"{prefix}_{guide['slug']}", on_click=open_guide,
              args=(guide["slug"],), width="stretch", type="tertiary")


def seed_home_search(query: str) -> None:
    st.session_state["home_guide_search"] = query
    st.session_state["home_topic"] = "全部"


def render_library_brief(guides: list[dict]) -> None:
    stats = content.library_stats(guides)
    st.markdown(f'''<div class="library-strip" aria-label="本站收錄範圍">
        <span><b>{stats['articles']}</b>篇詳解</span><span><b>{stats['tables']}</b>張查表</span>
        <span><b>{stats['questions']}</b>個問答</span><span>最近核對 <b>{stats['review_date']}</b></span>
        </div>''', unsafe_allow_html=True)


def render_featured(guides: list[dict]) -> None:
    st.markdown('<div class="guide-results-head"><h2>近期重點</h2><span>活動與養成更新</span></div>', unsafe_allow_html=True)
    event = content.get_guide("autumn-seabed", guides)
    ended = event and event_window(event.get("starts_at"), event.get("ends_at"))["state"] == "ended"
    with st.container(key="featured_guides"):
        columns = st.columns(3, gap="medium")
        for column, slug, label, heading in zip(columns, ("mount-layout" if ended else "autumn-seabed", "elaine-build", "tide-haven"),
                                       ("載具整理" if ended else "官方活動排程", "特工更新", "公會玩法"),
                                       ("載具：主戰與後備 →" if ended else "海底探險：先領任務 →", "伊狑：先查第二寵上限 →", "潮汐祕境：打叉與補券 →")):
            guide = content.get_guide(slug, guides)
            if guide is None:
                continue
            with column, st.container(key=f"feature_{slug}"):
                st.markdown(f'<div class="feature-label">{html.escape(label)}<span>{guide["checked"]}</span></div>', unsafe_allow_html=True)
                article_button(guide, "featured", heading)
                st.caption(guide["summary"])
                first, second = guide.get("takeaways", [])[:2]
                st.markdown(f'<ul class="feature-points"><li>{html.escape(first)}</li><li>{html.escape(second)}</li></ul>', unsafe_allow_html=True)


def render_quick_queries() -> None:
    with st.container(key="quick_queries"):
        st.caption("常查問題")
        queries = (("角色之後升什麼", "升級"), ("黃收藏先升哪件", "史詩收藏"),
                ("協同與連攜", "協同作戰"), ("寵物黃4／紅5", "幽暗"),
                ("雙生諧振門檻", "諧振"), ("神鑄與混沌", "混沌融合"))
        for start in range(0, len(queries), 3):
            columns = st.columns(3, gap="small")
            for offset, (label, query) in enumerate(queries[start:start + 3]):
                columns[offset].button(label, key=f"quick_query_{start + offset}", on_click=seed_home_search,
                                       args=(query,), width="stretch")


def guide_row(guide: dict, prefix: str, query: str = "") -> None:
    with st.container(key=f"guide_row_{prefix}_{guide['slug']}"):
        st.markdown(f'<div class="guide-meta">{html.escape(guide["category"])} <span>/ {html.escape(guide["status"])}</span></div>', unsafe_allow_html=True)
        article_button(guide, prefix)
        answer, condition = content.QUICK_ANSWERS.get(guide["slug"], (guide["summary"], ""))
        st.write(answer)
        if condition:
            st.caption("適用：" + condition)
        if query and not guide.get("reference_only"):
            rows = content.answer_rows(guide, query)
            if rows:
                facts = "".join(f'<li>{html.escape(" · ".join(row))}</li>' for row in rows)
                st.markdown(f'<ul class="search-facts">{facts}</ul>', unsafe_allow_html=True)


def render_catalog_matches(query: str, category: str) -> int:
    if not query.strip() or category not in ("全部", "收藏典藏"):
        return 0
    matches = content.search_collectibles(load_collectible_catalog(), query)
    if matches:
        with st.expander(f"收藏名稱／期數 · {len(matches)} 件", expanded=True):
            for item in matches[:12]:
                st.markdown(f"**{item['name']}**　{item['quality']} · 第{item['edition']}期 · #{item['id']}")
                st.link_button("查外部效果表 ↗", item["link"])
            if len(matches) > 12:
                st.caption("先列12件；縮小名稱或前往完整圖鑑。")
            st.button("查完整收藏圖鑑", on_click=open_collectible_catalog)
            st.caption("此區只核對名稱、品質與期數；外部效果表不等於本站升級推薦。")
    return len(matches)


def render_results(guides: list[dict], query: str, category: str, prefix: str) -> None:
    results = content.search_guides(guides, query, category)
    core = [guide for guide in results if not guide.get("reference_only")]
    references = [guide for guide in results if guide.get("reference_only")]
    heading = "搜尋結果" if query.strip() else "攻略速覽"
    st.markdown(
        f'<div class="guide-results-head"><h2>{heading}</h2>'
        f'<span>{len(core)} 篇詳解 · {len(references)} 篇來源摘要</span></div>',
        unsafe_allow_html=True,
    )
    for guide in (core[:3] if query.strip() else core):
        guide_row(guide, prefix, query)
    if query.strip() and len(core) > 3:
        with st.expander(f"其他相關詳解（{len(core) - 3}）"):
            for guide in core[3:]:
                guide_row(guide, prefix)
    catalog_count = render_catalog_matches(query, category)
    if references:
        with st.expander(f"來源摘要與歷史資料（{len(references)}）", expanded=not core and not catalog_count):
            for guide in references:
                guide_row(guide, prefix)
    if not results and not catalog_count:
        st.info("沒有符合的結果。請改用物品名稱、別名或較短的關鍵字。")
        suggestions = content.suggested_guides(guides, query)
        if suggestions:
            st.caption("部分關鍵字相關（不是完整命中）")
            for guide in suggestions:
                article_button(guide, prefix + "_suggested")


def render_home(legacy: list[dict]) -> None:
    guides = content.all_guides(legacy)
    detailed_count = sum(not guide.get("reference_only") for guide in guides)
    with st.container(key="guide_search_panel"):
        st.markdown('<div class="hero-intro" data-ui-region="home-search" data-ui-motion="true"><div class="hero-copy">'
                    '<h1 class="guide-hero-title">噠噠特攻攻略</h1>'
                    '<p class="guide-hero-deck">特工・裝備・收藏・科技・寵物・載具</p>'
                    f'<div class="hero-library-note">{detailed_count} 篇門檻詳解<span>／</span>{len(content.CATEGORIES)} 個養成主題</div></div>'
                    f'<div class="hero-companion" aria-hidden="true">{kite_markup()}</div></div>',
                    unsafe_allow_html=True)
        search, topic = st.columns([2.25, 1], gap="medium")
        with search:
            query = st.text_input("搜尋攻略", placeholder="暗物質黃5、SS鞋套裝、金R3……", max_chars=160, key="home_guide_search")
        with topic:
            category = st.selectbox("攻略分類", ("全部", *content.CATEGORIES), key="home_topic")
    render_library_brief(guides)
    if query.strip():
        render_results(guides, query, category, "home_search")
        return
    if category == "全部":
        render_quick_queries()
        with st.container(key="task_entries"):
            upgrade, event, catalog = st.columns(3, gap="medium")
            for column, title, detail, artwork, tag, callback, kwargs in (
                (upgrade, "查升級順序", "填入配置，查看目標與材料缺額", "upgrade", "配置與材料", open_tool, {}),
                (event, "計算活動成本", "輸入進度，計算達標所需寶石", "event", "進度與寶石", open_tool, {"activity": True}),
                (catalog, "收藏品圖鑑", "按名稱、品質或期數查詢", "collection", "名稱與效果", open_collectible_catalog, {}),
            ):
                with column:
                    with st.container(key=f"task_entry_{title}"):
                        st.markdown(f'<div class="task-card-head" data-ui-region="tool-{artwork}" data-ui-motion="true"><span class="task-tag">{tag}</span><span class="task-art">{guide_icon(artwork)}</span></div>', unsafe_allow_html=True)
                        st.button(title + " →", on_click=callback, kwargs=kwargs, width="stretch")
                        st.caption(detail)
        render_featured(guides)
    render_directory(guides, category, "home")


def render_directory(guides: list[dict], category: str, prefix: str) -> None:
    """Show two readable entries per shelf; the rest are a deliberate expansion."""
    core = [g for g in guides if not g.get("reference_only")]
    st.markdown('<div class="guide-results-head"><h2>攻略目錄</h2><span>按系統分類</span></div>', unsafe_allow_html=True)
    categories = content.CATEGORIES if category == "全部" else (category,)
    with st.container(key="guide_directory"):
        # Build rows in reading order: phone stacking must not reorder 1,3,5,2,4,6.
        for row_start in range(0, len(categories), 2):
            columns = st.columns(2, gap="medium")
            for offset, topic in enumerate(categories[row_start:row_start + 2]):
                index = row_start + offset
                entries = [g for g in core if g["category"] == topic]
                references = [g for g in guides if g.get("reference_only") and g["category"] == topic]
                with columns[offset]:
                    count = f"{len(entries)} 篇詳解" if entries else f"{len(references)} 篇來源摘要"
                    artwork, description = TOPIC_ART.get(topic, ("book", "門檻與判斷詳解"))
                    with st.container(key=f"topic_cover_{index}"):
                        st.markdown(f'<div class="topic-heading" data-ui-region="topic-{index}" data-ui-motion="true"><span class="topic-art">{guide_icon(artwork)}</span><div><h3>{html.escape(topic)}</h3><p>{html.escape(description)}</p></div><span class="topic-count">{count}</span></div>', unsafe_allow_html=True)
                        shown = entries if category != "全部" else entries[:2]
                        for guide in shown:
                            with st.container(key=f"directory_{prefix}_{guide['slug']}"):
                                article_button(guide, prefix)
                                st.caption(guide["summary"])
                        rest = entries[len(shown):]
                        if rest or not entries:
                            with st.expander(f"瀏覽{topic} · 另{len(rest)}篇" if entries else f"瀏覽{topic}來源", expanded=not entries):
                                if not entries:
                                    st.caption("目前收錄外部來源摘要，尚無本站門檻詳解。")
                                    st.button(f"查{topic}來源 →", key=f"directory_sources_{prefix}_{topic}",
                                              on_click=open_index, args=(topic,), width="stretch")
                                for guide in rest:
                                    with st.container(key=f"directory_{prefix}_{guide['slug']}"):
                                        article_button(guide, prefix)
                                        st.caption(content.QUICK_ANSWERS.get(guide["slug"], (guide["summary"], ""))[0])
    st.caption("歷史文章、外部來源與配裝參考：攻略索引。")


def render_index(legacy: list[dict]) -> None:
    guides = content.all_guides(legacy)
    render_library_brief(guides)
    search, topic = st.columns([2, 1])
    with search:
        query = st.text_input("搜尋本站攻略", placeholder="標題、角色、裝備或內文關鍵字", max_chars=160, key="guide_query")
    with topic:
        category = st.selectbox("攻略分類", ("全部", *content.CATEGORIES), key="guide_topic")
    render_results(guides, query, category, "index")


def table_markup(columns: list[str], rows: list[list[str]]) -> str:
    head = "".join(f'<th scope="col">{html.escape(cell)}</th>' for cell in columns)
    body = "".join("<tr>" + "".join(f"<td>{html.escape(str(cell))}</td>" for cell in row) + "</tr>" for row in rows)
    return f'<div class="guide-table-scroll" role="region" aria-label="攻略門檻表" tabindex="0"><table class="guide-table"><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'


def render_quick_decision(guide: dict) -> None:
    decisions = guide.get("decisions", [])
    if not decisions:
        return
    selected = st.selectbox("選擇目前狀況", [decision["condition"] for decision in decisions],
                            index=None, placeholder="選擇符合目前配置的條件", key=f"guide_scenario_{guide['slug']}")
    if selected is None:
        return
    decision = next(item for item in decisions if item["condition"] == selected)
    st.markdown(f'''<section class="scenario-answer" aria-label="目前情境建議">
        <h3>{html.escape(decision['action'])}</h3><p><b>投入與效果：</b>{html.escape(decision['cost'])}</p>
        <p><b>停在這裡：</b>{html.escape(decision['stop'])}</p></section>''', unsafe_allow_html=True)


def render_field_tool(slug: str) -> None:
    """Article-local checks never change player_profile or spend game resources."""
    if slug == "elaine-build":
        with st.popover("核對我的第二寵上限", width="stretch"):
            stage = st.number_input("伊狑覺醒 R", min_value=0, max_value=8, value=None, key="elaine_limit_r")
            stars = st.selectbox("協同異寵實際覺醒", (None, *range(11)),
                format_func=lambda x: "尚未填寫" if x is None else "未持有" if x == 0 else
                ("黃" + str(x) if x <= 5 else "紅" + str(x - 5)), key="elaine_limit_pet")
            st.caption("依2026-09-24技能表；主寵與協同寵分開核對，不計總傷害。")
        result = elaine_pet_limit(stage, stars)
        if stage is not None:
            st.info(result["message"])
    elif slug == "mount-layout":
        with st.popover("試算後備模組屬性", width="stretch"):
            value = st.number_input("模組該項屬性（%）", min_value=0.0, max_value=10000.0,
                                    value=None, step=0.1, key="reserve_value")
            sync = st.number_input("本台後備同步率（%）", min_value=0.0, max_value=100.0,
                                   value=None, step=1.0, key="reserve_sync")
            st.caption("填遊戲數字；只計單項傳遞，不加總不同類型增傷。")
        result = reserve_stat(value, sync)
        if value is not None or sync is not None:
            st.info(result["message"])
    elif slug == "boss-testing":
        with st.popover("比較兩組同條件成績", width="stretch"):
            a = st.text_input("A配置成績（至少3場）", placeholder="100, 105, 98", max_chars=400, key="boss_a")
            b = st.text_input("B配置成績（至少3場）", placeholder="110, 102, 108", max_chars=400, key="boss_b")
            st.caption("相同首領、時間、規則與數字單位。這是描述性比較，不是統計顯著性檢定。")
        if a or b:
            try:
                result = compare_runs(a, b)
                if result["state"] == "descriptive":
                    st.markdown(table_markup(["配置", "中位數", "最低場"], [
                        ["A", f"{result['median_a']:g}", f"{result['min_a']:g}"],
                        ["B", f"{result['median_b']:g}", f"{result['min_b']:g}"]]), unsafe_allow_html=True)
                    if result["change"] is not None:
                        st.caption(f"B中位數相對A：{result['change']:+.1f}%。不是付費升級收益預測。")
                st.info(result["message"])
            except ValueError as exc:
                st.warning(str(exc))


def render_article(slug: str, legacy: list[dict]) -> None:
    guides = content.all_guides(legacy)
    guide = content.get_guide(slug, guides)
    if guide is None:
        page_heading("找不到這篇攻略", "連結可能已變更，請返回攻略索引查找。")
        st.button("返回攻略索引", on_click=open_index, type="primary")
        return
    with st.container(key="article_actions"):
        back, link = st.columns([4, 1])
        origin = st.session_state.get("article_origin", {})
        back_label = "← 搜尋結果" if origin.get("query") else "← 攻略首頁" if origin.get("page") == "攻略首頁" else "← 攻略索引"
        back.button(back_label, on_click=return_to_guides, args=(guide["category"],))
        with link:
            with st.popover("文章連結", width="stretch"):
                st.caption("可收藏或複製此連結；連結不含個人帳號資料。")
                st.code(PUBLIC_URL + "?guide=" + quote(guide["slug"], safe=""), language=None, wrap_lines=True)
    page_heading(guide["title"], "")
    date = f"來源更新：{guide['source_date']}" if guide["source_date"] else "來源未標發布日" if guide["sources"] else "本站方法說明"
    checked = f" · 本站核對：{guide['checked']}" if guide["checked"] else " · 既有摘要，待重新核對" if guide.get("reference_only") else " · 非官方規則／排行"
    if guide["audience"] != "想確認操作與下一個有效門檻的玩家":
        st.caption("適用：" + guide["audience"])
    st.markdown(f'<div class="article-dateline"><span>{html.escape(guide["category"])}</span>'
                f'<span>{html.escape(guide["status"])}</span><span>{html.escape(date + checked)}</span></div>', unsafe_allow_html=True)
    if guide.get("starts_at"):
        window = event_window(guide["starts_at"], guide["ends_at"])
        if window["state"] == "ended":
            st.warning(window["label"])
        else:
            st.caption(window["label"])
    toc = "".join(f'<a href="#guide-part-{i}" target="_self">{i:02d} {html.escape(section["title"])}</a>' for i, section in enumerate(guide["sections"], 1))
    toc += '<a href="#guide-cautions" target="_self">適用限制</a>'
    if guide["faq"]:
        toc += '<a href="#guide-faq" target="_self">常見問題</a>'
    toc += '<a href="#guide-sources" target="_self">資料來源</a>'
    st.markdown(f'<details class="mobile-toc"><summary>本文目錄</summary><nav class="article-toc" aria-label="手機版本文目錄">{toc}</nav></details>', unsafe_allow_html=True)
    with st.container(key="guide_article_layout"):
        body, rail = st.columns([2.4, 1], gap="large")
        with body:
            if guide.get("takeaways"):
                items = "".join(f'<li>{html.escape(point)}</li>' for point in guide["takeaways"])
                st.markdown(f'<section class="article-keypoints" aria-label="攻略重點"><h2>先看結論</h2><ul>{items}</ul></section>', unsafe_allow_html=True)
            else:
                st.markdown(f'<section class="guide-verdict"><h2>先看結論</h2><p>{html.escape(guide["verdict"])}</p></section>', unsafe_allow_html=True)
            if guide.get("game_entry"):
                st.markdown(f'''<div class="article-operating" aria-label="實際操作與停止點">
                    <div><span>遊戲入口</span><p>{html.escape(guide['game_entry'])}</p></div>
                    <div><span>本次停點</span><p>{html.escape(guide['stop'])}</p></div>
                    <div><span>完成後</span><p>{html.escape(guide['next_after'])}</p></div></div>''', unsafe_allow_html=True)
            render_quick_decision(guide)
            render_field_tool(guide["slug"])
            if guide.get("takeaways"):
                st.write(guide["verdict"])
            if guide["resource"]:
                st.button("用我的配置排升級順序", on_click=open_tool, args=(guide["resource"],), width="stretch", type="primary")
            elif guide["slug"] == "epic-collectibles":
                st.button("查完整收藏圖鑑", on_click=open_collectible_catalog, width="stretch")
            elif guide["slug"] in ("event-budget", "autumn-seabed"):
                st.button("開啟活動投入試算", on_click=open_tool, kwargs={"activity": True}, width="stretch", type="primary")
            elif guide["slug"] in ("upgrade-roadmap", "red-choice-box"):
                st.button("用我的配置找下一個門檻", on_click=open_tool, args=("自動排序",), width="stretch", type="primary")
            elif guide["slug"] == "resonance-planning":
                with st.popover("試算諧振差額", width="stretch"):
                    st.caption("門檻請查遊戲的對應配件效果；不預設普通或雙生。這裡不會修改帳號配置。")
                    current = st.number_input("目前諧振能量", min_value=0, max_value=1000000, value=None, key="resonance_current")
                    target = st.number_input("遊戲顯示的目標能量", min_value=1, max_value=1000000, value=None, key="resonance_target")
                    result = resonance_gap(current, target)
                    st.info(result["message"])
                st.button("查雙生無人機／雷電的實際效果", on_click=open_guide, args=("twin-tech-milestones",), width="stretch")
            elif guide["slug"] == "twin-tech-milestones":
                with st.popover("找我的下一個諧振效果", width="stretch"):
                    st.caption("只選已持有且正在使用的紅品質以上雙生形態；不套用普通配件，也不改動帳號紀錄。")
                    part = st.selectbox("目前使用的雙生形態", tuple(TECH_ROUTES), index=None, placeholder="選實際形態", key="tech_route_part")
                    energy = st.number_input("這件目前的諧振能量", min_value=0, max_value=1000000, value=None, key="tech_route_energy")
                    unverified = next_tech_effect(part, energy)
                    confirmed = st.checkbox("我已對照遊戲，下一檔效果與來源表一致",
                                            key=f"tech_route_verified_{part}_{unverified.get('target')}",
                                            disabled=not bool(unverified.get("target")))
                result = next_tech_effect(part, energy, confirmed)
                if result.get("target"):
                    st.info(result["message"])
                    st.markdown(f'''<section class="scenario-answer" aria-label="諧振操作目標">
                        <h3>{html.escape(result['effect'])}</h3><p>{html.escape(result['action'])}</p>
                        <p>{html.escape(result['stop'])}</p></section>''', unsafe_allow_html=True)
                else:
                    st.caption(result["message"])
            if guide.get("editorial_note"):
                st.caption(guide["editorial_note"])
            for index, section in enumerate(guide["sections"], 1):
                with st.container(key=f"article_part_{index}"):
                    st.markdown(f'<section id="guide-part-{index}" class="article-anchor"><h2 class="article-section"><span class="section-number">{index:02d}</span> {html.escape(section["title"])}</h2></section>', unsafe_allow_html=True)
                    if section.get("body"):
                        st.write(section["body"])
                    if section.get("rows"):
                        st.markdown(table_markup(section["columns"], section["rows"]), unsafe_allow_html=True)
                    if section.get("steps"):
                        steps = "".join(f'<li>{html.escape(step)}</li>' for step in section["steps"])
                        st.markdown(f'<ol class="article-steps">{steps}</ol>', unsafe_allow_html=True)
            st.markdown('<section id="guide-cautions" class="article-anchor"><h2 class="article-section">適用限制</h2></section>', unsafe_allow_html=True)
            st.warning(guide["caution"])
            if guide["faq"]:
                st.markdown('<section id="guide-faq" class="article-anchor"><h2 class="article-section">常見問題</h2></section>', unsafe_allow_html=True)
                for question, answer in guide["faq"]:
                    with st.expander(question):
                        st.write(answer)
            st.markdown('<section id="guide-sources" class="article-anchor"><h2 class="article-section">資料來源</h2></section>', unsafe_allow_html=True)
            st.caption(date + checked)
            for label, url in guide["sources"]:
                st.link_button(label + " ↗", url)
                source_detail = next((s for s in guide.get("source_details", []) if s["url"] == url), None)
                if source_detail and source_detail["date"]:
                    st.caption("此來源日期：" + source_detail["date"])
            if not guide["sources"]:
                st.caption("本文說明計算與排序方法。遊戲數值請對照相關來源及本次升級預覽。")
            else:
                st.caption("官方更新與社群攻略依連結標示；社群核對不等於官方認證。版本有差異時，以遊戲內資料為準。")
        with rail:
            with st.container(key="article_rail"):
                st.markdown(f'<nav class="article-toc" aria-label="本文目錄"><strong>本文目錄</strong>{toc}</nav>', unsafe_allow_html=True)
    related = [content.get_guide(item, guides) for item in guide["related"]]
    if related:
        st.markdown("## 接著閱讀")
        columns = st.columns(2)
        for i, item in enumerate(related):
            if item:
                with columns[i % 2]:
                    guide_row(item, "related")
