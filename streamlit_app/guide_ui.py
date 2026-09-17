"""Reading-first home, shared guide index, and addressable article pages."""
from __future__ import annotations

import html
from urllib.parse import quote

import streamlit as st

import guide_content as content
from data_engine import load_collectible_catalog
from decision_ui import page_heading


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
    st.caption(f"{len(core)} 篇詳解 · {len(references)} 篇來源摘要")
    for guide in (core[:1] if query.strip() else core):
        guide_row(guide, prefix, query)
    if query.strip() and len(core) > 1:
        with st.expander(f"其他相關詳解（{len(core) - 1}）"):
            for guide in core[1:]:
                guide_row(guide, prefix)
    catalog_count = render_catalog_matches(query, category)
    if references:
        with st.expander(f"來源摘要與歷史資料（{len(references)}）", expanded=not core and not catalog_count):
            for guide in references:
                guide_row(guide, prefix)
    if not results and not catalog_count:
        st.info("尚未收錄符合的答案。試試物品名稱、別名或縮短問題；不會以不相關攻略代替。")


def render_home(legacy: list[dict]) -> None:
    guides = content.all_guides(legacy)
    with st.container(key="guide_search"):
        query = st.text_input("搜尋攻略", placeholder="例如：暗物質黃5、SS鞋套裝、金R3、黃收藏", max_chars=160, key="home_guide_search")
    category = st.selectbox("攻略分類", ("全部", *content.CATEGORIES), key="home_topic")
    render_results(guides, query, category, "home_search" if query.strip() else "home")


def render_index(legacy: list[dict]) -> None:
    guides = content.all_guides(legacy)
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
                            index=None, placeholder="選相符情境，直接看投入與停手點", key=f"guide_scenario_{guide['slug']}")
    if selected is None:
        return
    decision = next(item for item in decisions if item["condition"] == selected)
    st.markdown(f'''<section class="scenario-answer" aria-label="目前情境建議">
        <h3>{html.escape(decision['action'])}</h3><p><b>投入與效果：</b>{html.escape(decision['cost'])}</p>
        <p><b>停在這裡：</b>{html.escape(decision['stop'])}</p></section>''', unsafe_allow_html=True)


def render_article(slug: str, legacy: list[dict]) -> None:
    guides = content.all_guides(legacy)
    guide = content.get_guide(slug, guides)
    if guide is None:
        page_heading("找不到這篇攻略", "連結可能已變更，請返回攻略索引查找。")
        st.button("返回攻略索引", on_click=open_index, type="primary")
        return
    back, link = st.columns([4, 1])
    origin = st.session_state.get("article_origin", {})
    back_label = "← 搜尋結果" if origin.get("query") else "← 攻略首頁" if origin.get("page") == "攻略首頁" else "← 攻略索引"
    back.button(back_label, on_click=return_to_guides, args=(guide["category"],))
    with link:
        with st.popover("文章連結", width="stretch"):
            st.caption("可收藏或複製此連結；連結不含個人帳號資料。")
            st.code(PUBLIC_URL + "?guide=" + quote(guide["slug"], safe=""), language=None, wrap_lines=True)
    st.caption(f"攻略 / {guide['category']} / {guide['status']}")
    page_heading(guide["title"], "")
    date = f"來源更新：{guide['source_date']}" if guide["source_date"] else "本站試算方法"
    checked = f" · 本站核對：{guide['checked']}" if guide["checked"] else " · 既有摘要，待重新核對" if guide.get("reference_only") else " · 非當期活動公告"
    st.caption("適用：" + guide["audience"])
    toc = "".join(f'<a href="#guide-part-{i}" target="_self">{i:02d} {html.escape(section["title"])}</a>' for i, section in enumerate(guide["sections"], 1))
    toc += '<a href="#guide-cautions" target="_self">適用限制</a>'
    if guide["faq"]:
        toc += '<a href="#guide-faq" target="_self">常見問題</a>'
    toc += '<a href="#guide-sources" target="_self">資料來源</a>'
    st.markdown(f'<details class="mobile-toc"><summary>本文目錄</summary><nav class="article-toc" aria-label="手機版本文目錄">{toc}</nav></details>', unsafe_allow_html=True)
    with st.container(key="guide_article_layout"):
        body, rail = st.columns([2.4, 1], gap="large")
        with body:
            st.markdown(f'<section class="guide-verdict"><h2>先看結論</h2><p>{html.escape(guide["verdict"])}</p></section>', unsafe_allow_html=True)
            render_quick_decision(guide)
            if guide["resource"]:
                st.button("用我的配置排升級順序", on_click=open_tool, args=(guide["resource"],), width="stretch", type="primary")
            elif guide["slug"] == "epic-collectibles":
                st.button("查完整收藏圖鑑", on_click=open_collectible_catalog, width="stretch")
            elif guide["slug"] == "event-budget":
                st.button("開啟活動投入試算", on_click=open_tool, kwargs={"activity": True}, width="stretch", type="primary")
            if guide.get("editorial_note"):
                st.caption(guide["editorial_note"])
            for index, section in enumerate(guide["sections"], 1):
                st.markdown(f'<div id="guide-part-{index}"></div>', unsafe_allow_html=True)
                with st.expander(section["title"], expanded=bool(section.get("rows"))):
                    if section.get("body"):
                        st.write(section["body"])
                    if section.get("rows"):
                        st.markdown(table_markup(section["columns"], section["rows"]), unsafe_allow_html=True)
                    for number, step in enumerate(section.get("steps", []), 1):
                        st.markdown(f"{number}. {step}")
            st.markdown('<h2 class="article-section" id="guide-cautions">適用限制</h2>', unsafe_allow_html=True)
            st.warning(guide["caution"])
            if guide["faq"]:
                st.markdown('<h2 class="article-section" id="guide-faq">常見問題</h2>', unsafe_allow_html=True)
                for question, answer in guide["faq"]:
                    with st.expander(question):
                        st.write(answer)
            st.markdown('<h2 class="article-section" id="guide-sources">資料來源</h2>', unsafe_allow_html=True)
            st.caption(date + checked)
            for label, url in guide["sources"]:
                st.link_button(label + " ↗", url)
            if not guide["sources"]:
                st.caption("本文為本站計算說明，不是對當期活動數值的查核。")
            else:
                st.caption("由本站重新整理判斷條件；來源為社群攻略，非官方保證。版本有差異時，以遊戲內資料為準。")
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
