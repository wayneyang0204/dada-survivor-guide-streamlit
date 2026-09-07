"""Reading-first home, shared guide index, and addressable article pages."""
from __future__ import annotations

import html
from urllib.parse import quote

import streamlit as st

import guide_content as content
from decision_ui import page_heading


PUBLIC_URL = "https://dada-survivor-guide.streamlit.app/"


def clear_article() -> None:
    st.session_state.pop("article_slug", None)
    st.query_params.pop("guide", None)
    st.session_state["seen_guide_query"] = None


def sync_query() -> None:
    slug = st.query_params.get("guide")
    if slug != st.session_state.get("seen_guide_query"):
        st.session_state["seen_guide_query"] = slug
        if slug:
            # Only a local lookup is performed. The URL never controls a request/path.
            st.session_state["article_slug"] = str(slug)[:100]
            st.session_state["主導覽"] = "資料庫"
        else:
            st.session_state.pop("article_slug", None)


def open_guide(slug: str) -> None:
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


def open_tool(resource: str | None = None, activity: bool = False) -> None:
    clear_article()
    if resource:
        st.session_state["decision_resource"] = resource
    st.session_state["pending_navigation"] = "活動" if activity else "下一步"


def article_button(guide: dict, prefix: str, label: str | None = None) -> None:
    st.button(label or guide["title"], key=f"{prefix}_{guide['slug']}", on_click=open_guide,
              args=(guide["slug"],), width="stretch", type="tertiary")


def guide_row(guide: dict, prefix: str) -> None:
    with st.container(key=f"guide_row_{prefix}_{guide['slug']}"):
        st.markdown(f'<div class="guide-meta">{html.escape(guide["category"])} <span>/ {html.escape(guide["status"])}</span></div>', unsafe_allow_html=True)
        article_button(guide, prefix)
        st.write(guide["summary"])
        date = f"來源更新 {guide['source_date']}" if guide["source_date"] else "本站計算方法"
        st.caption(date + (" · 本站已核對來源表格" if guide["checked"] else ""))


def render_home(legacy: list[dict]) -> None:
    guides = content.all_guides(legacy)
    page_heading("噠噠特攻攻略", "特工養成、裝備神鑄、收藏典藏與活動投入。")
    with st.container(key="guide_search"):
        query = st.text_input("搜尋攻略", placeholder="例如：典藏館、暗物質傀儡、雙絕槍、覺醒", max_chars=160, key="home_guide_search")
    with st.container(key="topic_directory"):
        columns = st.columns(3)
        for index, category in enumerate(content.CATEGORIES):
            columns[index % 3].button(category, key=f"home_topic_{index}", on_click=open_index, args=(category,), width="stretch")
    if query.strip():
        results = content.search_guides(guides, query)
        st.caption(f"{len(results)} 篇符合「{query}」")
        if not results:
            st.info("沒有符合的攻略。試試角色、裝備名稱，或從上方分類查找。")
        for guide in results:
            guide_row(guide, "home_search")
        return
    with st.container(key="guide_frontpage"):
        lead, quick = st.columns([1.8, 1], gap="large")
        with lead:
            featured = content.GUIDES[0]
            st.markdown(f'''<section class="frontpage-feature"><div class="guide-kicker">養成重點 / 收藏典藏</div>
              <h2>{html.escape(featured['title'])}</h2><p>{html.escape(featured['verdict'])}</p>
              <div class="feature-bottom"><span>普通欄位：看品質與件數</span><span>進階欄位：格數與星數都要到</span></div></section>''', unsafe_allow_html=True)
            article_button(featured, "featured", "閱讀典藏館完整攻略 →")
        with quick:
            with st.container(key="frontpage_quick"):
                st.markdown("### 門檻速查")
                for slug, label in (("survivor-awakening", "普通六星 ≠ 覺醒 R6"), ("gear-forging", "SS 神鑄核心：單階與累計"),
                                    ("collectible-breakpoints", "收藏星級：黃3、黃5、紅3")):
                    guide = content.get_guide(slug, guides)
                    article_button(guide, "quick", label)
                st.divider()
                st.caption("已經知道自己的配置？")
                st.button("安排我的下一次升級", on_click=open_tool, width="stretch", type="primary")
    st.markdown("## 核心攻略")
    columns = st.columns(2, gap="large")
    for index, guide in enumerate(content.GUIDES[1:]):
        with columns[index % 2]:
            guide_row(guide, "core")
    st.button("瀏覽全部攻略與摘要索引 →", on_click=open_index, width="stretch")
    with st.container(key="guide_standards"):
        st.markdown("### 閱讀前先分清楚")
        st.write("來源數值會標示資料日期；本站整理不代表官方公告。歷史活動保留供查機制，個人升級順序則由你填入的配置重新判斷。")
        st.caption(f"收錄 {len(content.GUIDES)} 篇站內核心攻略，另有 {len(guides)-len(content.GUIDES)} 篇既有摘要索引。")


def render_index(legacy: list[dict]) -> None:
    guides = content.all_guides(legacy)
    search, topic = st.columns([2, 1])
    with search:
        query = st.text_input("搜尋本站攻略", placeholder="標題、角色、裝備或內文關鍵字", max_chars=160, key="guide_query")
    with topic:
        category = st.selectbox("攻略分類", ("全部", *content.CATEGORIES), key="guide_topic")
    results = content.search_guides(guides, query, category)
    st.caption(f"找到 {len(results)} 篇 · 核心攻略提供站內詳解；摘要索引保留原文入口與版本提醒。")
    if not results:
        st.info("沒有符合的攻略。清除關鍵字或改選其他分類。")
        return
    for guide in results:
        guide_row(guide, "index")


def table_markup(columns: list[str], rows: list[list[str]]) -> str:
    head = "".join(f'<th scope="col">{html.escape(cell)}</th>' for cell in columns)
    body = "".join("<tr>" + "".join(f"<td>{html.escape(str(cell))}</td>" for cell in row) + "</tr>" for row in rows)
    return f'<div class="guide-table-scroll" role="region" aria-label="攻略門檻表" tabindex="0"><table class="guide-table"><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'


def render_article(slug: str, legacy: list[dict]) -> None:
    guides = content.all_guides(legacy)
    guide = content.get_guide(slug, guides)
    if guide is None:
        page_heading("找不到這篇攻略", "連結可能已變更，請返回攻略索引查找。")
        st.button("返回攻略索引", on_click=open_index, type="primary")
        return
    back, link = st.columns([4, 1])
    back.button("← 攻略索引", on_click=open_index, args=(guide["category"],))
    with link:
        with st.popover("文章連結", width="stretch"):
            st.caption("可收藏或複製此連結；連結不含個人帳號資料。")
            st.code(PUBLIC_URL + "?guide=" + quote(guide["slug"], safe=""), language=None, wrap_lines=True)
    st.caption(f"攻略 / {guide['category']} / {guide['status']}")
    page_heading(guide["title"], guide["summary"])
    date = f"來源更新：{guide['source_date']}" if guide["source_date"] else "本站試算方法"
    checked = f" · 本站核對：{guide['checked']}" if guide["checked"] else " · 既有摘要，待重新核對" if guide.get("reference_only") else " · 非當期活動公告"
    st.caption(date + checked)
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
            if guide.get("editorial_note"):
                st.caption(guide["editorial_note"])
            for index, section in enumerate(guide["sections"], 1):
                st.markdown(f'<h2 class="article-section" id="guide-part-{index}">{index:02d} / {html.escape(section["title"])}</h2>', unsafe_allow_html=True)
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
                    st.markdown(f"### {question}")
                    st.write(answer)
            st.markdown('<h2 class="article-section" id="guide-sources">資料來源</h2>', unsafe_allow_html=True)
            for label, url in guide["sources"]:
                st.link_button(label + " ↗", url)
            if not guide["sources"]:
                st.caption("本文為本站計算說明，不是對當期活動數值的查核。")
            else:
                st.caption("由本站重新整理判斷條件；來源為社群攻略，非官方保證。版本有差異時，以遊戲內資料為準。")
        with rail:
            with st.container(key="article_rail"):
                st.markdown(f'<nav class="article-toc" aria-label="本文目錄"><strong>本文目錄</strong>{toc}</nav>', unsafe_allow_html=True)
                if guide["resource"]:
                    st.button("用我的配置排升級順序", on_click=open_tool, args=(guide["resource"],), width="stretch", type="primary")
                elif guide["slug"] == "event-budget":
                    st.button("開啟活動投入試算", on_click=open_tool, kwargs={"activity": True}, width="stretch", type="primary")
                st.caption("閱讀攻略不需要填帳號；需要個人化建議時再使用工具。")
    related = [content.get_guide(item, guides) for item in guide["related"]]
    if related:
        st.markdown("## 接著閱讀")
        columns = st.columns(2)
        for i, item in enumerate(related):
            if item:
                with columns[i % 2]:
                    guide_row(item, "related")
