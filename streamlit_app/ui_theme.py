"""One shared, light-theme visual system for the player handbook."""

STYLE = """
<style>
:root {
  color-scheme:light;
  --paper:#ffffff; --ink:#20242b; --muted:#606873; --line:#dfe3e8;
  --accent:#2449d8; --wash:#f5f6f8; --ready:#176446;
  --pending:#805510; --blocked:#a0392b; --field:#838c9a;
}
html, body, .stApp {font-family:"Inter","Noto Sans TC","PingFang TC","Microsoft JhengHei",sans-serif;color:var(--ink);background:var(--paper);}
.stApp {background:var(--paper);}
.block-container {max-width:1140px;padding:1.4rem 2rem 4rem;}
[data-testid="stHeader"] {background:var(--paper);height:1rem;}
[data-testid="stToolbar"], [data-testid="stDecoration"], [data-testid="stSidebar"], [data-testid="collapsedControl"], footer {display:none;}
h1, h2, h3, h4 {color:var(--ink);letter-spacing:-.035em;line-height:1.4;}
h1 {font-size:2rem;font-weight:800;}
h2 {font-size:1.6rem;font-weight:750;}
h3 {font-size:1.2rem;font-weight:750;}
[data-testid="stMarkdownContainer"] p, [data-testid="stMarkdownContainer"] li {font-size:1rem;line-height:1.75;color:var(--ink);overflow-wrap:anywhere;}
[data-testid="stCaptionContainer"] p {font-size:.875rem;line-height:1.6;color:var(--muted);}
[data-testid="stWidgetLabel"] p {font-size:.875rem;font-weight:600;color:var(--ink);}
a {color:var(--accent);text-underline-offset:.2em;}
hr {border-color:var(--line);}
button, a, input, summary {touch-action:manipulation;}
button:focus-visible, a:focus-visible, summary:focus-visible {outline:2px solid var(--accent)!important;outline-offset:3px;}

/* A masthead and an ordinary tab line, not a floating marketing header. */
.masthead {display:flex;align-items:center;justify-content:space-between;gap:1rem;padding:.5rem 0 1.4rem;}
.masthead-brand {display:flex;align-items:center;gap:.8rem;}
.brand-mark {display:grid;place-items:center;width:2.7rem;height:2.7rem;background:var(--ink);color:#fff;font-size:1.4rem;font-weight:900;flex-shrink:0;}
.brand-title {font-size:1.2rem;font-weight:800;letter-spacing:.04em;}
.brand-subtitle {display:block;font-size:.875rem;color:var(--muted);margin-top:.15rem;}
.masthead-edition {font-size:.875rem;color:var(--muted);text-align:right;}
.st-key-main_nav {border-bottom:1px solid var(--line);margin-bottom:1rem;}
.st-key-main_nav [role="radiogroup"] {display:flex;flex-wrap:wrap;gap:0;width:100%;}
.st-key-main_nav label[data-testid="stRadioOption"] {display:flex;flex:1 1 0;min-width:0;justify-content:center;margin:0;padding:.75rem .5rem;border-bottom:3px solid transparent;cursor:pointer;}
.st-key-main_nav label[data-testid="stRadioOption"] > div > div > div:first-child {display:none;}
.st-key-main_nav label p {font-size:1rem;font-weight:600;color:var(--muted);}
.st-key-main_nav label:has(input:checked) {border-bottom-color:var(--accent);}
.st-key-main_nav label:has(input:checked) p {color:var(--accent);}
.st-key-main_nav label:hover {background:var(--wash);}
.st-key-main_nav label:has(input:focus-visible), .st-key-profile_nav label:has(input:focus-visible) {outline:2px solid var(--accent);outline-offset:-2px;}

/* Route title, resource toolbar, and a single prominent upgrade target. */
.page-heading {margin:.4rem 0 .25rem;font-size:clamp(1.7rem,3.5vw,2.15rem);font-weight:800;}
.page-deck {margin:0 0 .6rem;color:var(--muted)!important;}
.st-key-route_toolbar {border-bottom:1px solid var(--line);padding-bottom:1rem;margin-bottom:.5rem;}
.route-context {padding:.6rem 0;font-size:.875rem;color:var(--muted);line-height:1.65;}
.route-context strong {display:block;font-size:1.05rem;color:var(--ink);}
.decision-lead {display:flex;align-items:center;flex-wrap:wrap;gap:.6rem;margin:.25rem 0 .8rem;font-size:.875rem;font-weight:650;color:var(--muted);}
.section-index {color:var(--accent);font-variant-numeric:tabular-nums;font-weight:750;padding-right:.6rem;border-right:1px solid var(--line);}
.decision-title {font-size:clamp(1.6rem,3.2vw,2rem);line-height:1.4;margin:0 0 .6rem;padding:0;}
.decision-intro {margin:0 0 1rem;max-width:48rem;}
.decision-state {display:inline-block;font-size:.875rem;color:var(--ready);font-weight:650;}
.decision-state::before {content:"";display:inline-block;width:.4rem;height:.4rem;margin:0 .4rem .1rem 0;background:currentColor;border-radius:50%;}
.decision-state.pending {color:var(--pending);}.decision-state.blocked {color:var(--blocked);}
.decision-facts {display:grid;grid-template-columns:1fr 1fr;border-top:2px solid var(--ink);border-bottom:1px solid var(--line);margin:1.1rem 0 1.3rem;}
.decision-facts > div {padding:.9rem 1rem .9rem 0;}
.decision-facts > div + div {border-left:1px solid var(--line);padding-left:1rem;}
.decision-facts dt {font-size:.875rem;color:var(--muted);margin:0 0 .35rem;}
.decision-facts dd {margin:0;font-size:1.05rem;font-weight:700;line-height:1.65;overflow-wrap:anywhere;font-variant-numeric:tabular-nums;}
.ledger-title {font-size:1rem;font-weight:700;margin:0 0 .4rem;}
.decision-checks {border-top:1px solid var(--line);margin-bottom:.5rem;}
.decision-check {display:flex;justify-content:space-between;align-items:baseline;flex-wrap:wrap;gap:.25rem 1rem;padding:.8rem 0;border-bottom:1px solid var(--line);font-size:1rem;line-height:1.65;}
.decision-check b {color:var(--ready);font-size:.875rem;font-weight:650;}
.decision-check.short b {color:var(--blocked);}.decision-check.unknown b {color:var(--pending);}
.decision-check span {color:var(--ink);font-variant-numeric:tabular-nums;overflow-wrap:anywhere;}
.st-key-route_notes {border-left:1px solid var(--line);padding-left:1.5rem;}
.notes-heading {font-size:1rem;letter-spacing:.04em;margin:.25rem 0 1.1rem;}
.route-note {margin:0 0 1.2rem;}
.route-note dt {font-size:.875rem;color:var(--muted);margin-bottom:.35rem;}
.route-note dd {margin:0;font-size:1rem;line-height:1.75;overflow-wrap:anywhere;}
.route-note.stop {border-top:1px solid var(--line);padding-top:1rem;}
.route-note.stop dd {font-weight:600;}
.decision-queue {display:grid;grid-template-columns:2rem 1fr;gap:.75rem;padding:1rem 0;border-bottom:1px solid var(--line);}
.queue-index {color:var(--muted);font-size:.875rem;font-variant-numeric:tabular-nums;}
.queue-title {font-weight:700;font-size:1rem;}.queue-detail {margin:.25rem 0 0!important;color:var(--muted)!important;}
.setup-heading {font-size:1.5rem;margin:.4rem 0;}
.st-key-onboarding {max-width:760px;}
.setup-note {border-top:1px solid var(--line);padding-top:1rem;font-size:.875rem;color:var(--muted);line-height:1.7;}

/* Account sections stay visible, with only one editor open. */
.st-key-profile_nav {padding-top:.5rem;}
.st-key-profile_nav [role="radiogroup"] {gap:.2rem;}
.st-key-profile_nav label[data-testid="stRadioOption"] {margin:0;padding:.6rem .7rem;border-left:3px solid transparent;min-height:44px;}
.st-key-profile_nav label[data-testid="stRadioOption"] > div > div > div:first-child {display:none;}
.st-key-profile_nav label:has(input:checked) {background:var(--wash);border-left-color:var(--accent);}
.st-key-profile_nav label p {font-size:1rem;color:var(--muted);}
.st-key-profile_nav label:has(input:checked) p {color:var(--accent);font-weight:650;}
.st-key-profile_editor {border-left:1px solid var(--line);padding-left:1.5rem;}
.editor-heading {font-size:1.4rem;padding:0;margin:.35rem 0 1rem;}

/* Native controls: comfortable hit areas, visible labels and keyboard focus. */
[data-baseweb="select"] > div, [data-baseweb="input"], [data-baseweb="textarea"],
.react-aria-ComboBox > div[role="group"], .react-aria-NumberField > div[role="group"] {
  min-height:2.85rem;border:1px solid var(--field);border-radius:5px;background:var(--paper);box-shadow:none;
}
input, textarea {font-size:1rem!important;color:var(--ink);font-variant-numeric:tabular-nums;}
input::placeholder, textarea::placeholder {color:var(--muted);opacity:1;}
[data-baseweb="select"]:focus-within, [data-baseweb="input"]:focus-within,
.react-aria-ComboBox > div[role="group"]:focus-within, .react-aria-NumberField > div[role="group"]:focus-within {outline:2px solid var(--accent);outline-offset:1px;}
[role="listbox"], [data-baseweb="popover"] {background:var(--paper);color:var(--ink);}
[data-testid="stButton"] button, [data-testid="stFormSubmitButton"] button,
[data-testid="stDownloadButton"] button, [data-testid="stPopover"] button,
[data-testid="stLinkButton"] a {min-height:44px;border-radius:5px;box-shadow:none;font-weight:600;}
button[kind="primary"], button[data-testid="stBaseButton-primary"] {background:var(--accent);border-color:var(--accent);color:#fff;}
button[kind="primary"] p, button[data-testid="stBaseButton-primary"] p {color:#fff!important;}
button[kind="primary"]:hover {background:#193bbd;border-color:#193bbd;}
[data-testid="stForm"] {border:0;padding:0;}
[data-testid="stExpander"] {border:0;border-top:1px solid var(--line);border-bottom:1px solid var(--line);border-radius:0;background:var(--paper);box-shadow:none;}
[data-testid="stExpander"] summary {padding:.8rem .2rem;min-height:44px;}
[data-testid="stExpander"] summary p {font-size:.9375rem;font-weight:600;}
[data-testid="stAlert"] {border-radius:5px;}
[data-testid="stMetric"] {border-top:1px solid var(--line);padding:.8rem 0;}
[data-testid="stMetricValue"] {font-variant-numeric:tabular-nums;font-size:1.8rem;font-weight:700;}
[data-testid="stDataFrame"] {border:1px solid var(--line);border-radius:4px;}
[data-baseweb="tab-list"] {gap:1rem;border-bottom:1px solid var(--line);}
[data-baseweb="tab"] {font-size:1rem;min-height:44px;background:transparent;}
[data-baseweb="tab"][aria-selected="true"] {color:var(--accent);}

/* Reference pages share the handbook's ruled sections, not a wall of cards. */
.重點速覽 {padding:.4rem 0 1rem;}
.速覽頂列 {display:flex;justify-content:space-between;flex-wrap:wrap;gap:.5rem;color:var(--muted);font-size:.875rem;}
.速覽徽章 {color:var(--accent);font-weight:700;}
.重點速覽 h3 {font-size:1.5rem;line-height:1.5;margin:.7rem 0;}
.速覽標籤列 {display:flex;flex-wrap:wrap;gap:.4rem 1rem;font-size:.875rem;color:var(--muted);}
.速覽結論 {font-size:1.05rem!important;background:var(--wash);padding:1rem;margin:1rem 0!important;}
.速覽結論 b, .速覽停損 b {display:block;margin-bottom:.4rem;font-size:.875rem;}
.速覽清單 {display:grid;grid-template-columns:1fr 1fr;gap:1.5rem;}
.速覽區塊 {border-top:2px solid var(--ink);padding:.9rem 0;}
.速覽區塊標題 {display:flex;align-items:baseline;gap:.65rem;margin-bottom:.65rem;}
.速覽區塊標題 strong {font-size:1.05rem;}
.速覽號 {color:var(--accent);font-size:.875rem;font-weight:700;}
.速覽區塊 ul {padding-left:1.15rem;margin:0;}
.速覽區塊 li {font-size:1rem;line-height:1.8;margin:.5rem 0;}
.速覽停損 {border-top:1px solid var(--line);padding-top:1rem;margin:0!important;}
.速覽停損 b {color:var(--pending);}
.攻略卡 {border-top:1px solid var(--line);padding:1.1rem 0 .6rem;}
.卡片頂列 {display:flex;justify-content:space-between;align-items:center;gap:1rem;font-size:.875rem;}
.分類 {color:var(--accent);font-weight:650;}
.狀態 {font-size:.875rem;}
.攻略卡 h3 {font-size:1.25rem;margin:.6rem 0 .4rem;}
.攻略卡 p {margin:.4rem 0;}
.更新日 {font-size:.875rem;color:var(--muted);}
.配置詳情 {border-top:2px solid var(--ink);padding:1rem 0;}
.配置詳情 ul {padding-left:1.2rem;}
.獎勵格 {display:grid;grid-template-columns:1fr;}
.獎勵項 {display:grid;grid-template-columns:2rem 1fr auto;align-items:baseline;gap:.75rem;padding:1rem 0;border-bottom:1px solid var(--line);}
.獎勵序 {color:var(--accent);font-size:.875rem;font-variant-numeric:tabular-nums;}
.獎勵名稱 {font-weight:650;font-size:1rem;}.獎勵數據 {font-size:.875rem;color:var(--muted);}
[class*="st-key-source_article_"], [class*="st-key-latest_article_"] {border-top:1px solid var(--line);padding:1rem 0;}
.site-footer {border-top:1px solid var(--line);margin-top:2rem;padding-top:1rem;color:var(--muted);font-size:.875rem;line-height:1.75;}

/* Reading-first guide home and articles use the same paper/ink palette. */
.st-key-guide_search {max-width:760px;}
.st-key-topic_directory {border-bottom:1px solid var(--line);padding:.3rem 0 1.1rem;}
.st-key-topic_directory button {text-align:left;justify-content:flex-start;border:0;border-left:2px solid var(--accent);border-radius:0;background:var(--wash);}
.st-key-guide_frontpage {padding:.8rem 0 1rem;border-bottom:1px solid var(--line);}
.frontpage-feature {padding:.6rem 0;}
.guide-kicker {font-size:.875rem;font-weight:700;color:var(--accent);margin-bottom:.8rem;}
.frontpage-feature h2 {font-size:clamp(1.5rem,3vw,1.9rem);line-height:1.5;margin:0 0 .8rem;}
.frontpage-feature p {margin:0 0 1rem;}
.feature-bottom {display:flex;flex-wrap:wrap;gap:.5rem 1.5rem;color:var(--muted);font-size:.875rem;border-top:1px solid var(--line);padding-top:.8rem;}
.st-key-frontpage_quick {border-left:1px solid var(--line);padding-left:1.5rem;}
.st-key-frontpage_quick button[kind="tertiary"] {justify-content:flex-start;text-align:left;padding:.4rem 0;}
[class*="st-key-guide_row_"] {border-top:1px solid var(--line);padding:1rem 0 .7rem;}
.guide-meta {font-size:.875rem;font-weight:650;color:var(--accent);}
.guide-meta span {color:var(--muted);font-weight:400;}
[class*="st-key-guide_row_"] [data-testid="stButton"] button {padding:.2rem 0;justify-content:flex-start;text-align:left;}
[class*="st-key-guide_row_"] [data-testid="stButton"] button p {font-size:1.125rem;font-weight:750;line-height:1.6;}
[class*="st-key-guide_row_"] [data-testid="stButton"] button:hover p {color:var(--accent);text-decoration:underline;text-underline-offset:.2em;}
.st-key-guide_standards {border-top:1px solid var(--line);padding-top:1rem;margin-top:.5rem;}
.guide-verdict {border-top:3px solid var(--accent);background:var(--wash);padding:1.2rem 1.3rem;margin:.5rem 0 1.5rem;}
.guide-verdict h2 {font-size:1rem;margin:0 0 .5rem;color:var(--accent);}
.guide-verdict p {margin:0;}
.article-section {font-size:1.4rem;padding-top:.6rem;margin:1.5rem 0 .8rem;scroll-margin-top:1rem;}
.guide-table-scroll {max-width:100%;overflow-x:auto;margin:.8rem 0 1rem;}
.guide-table-scroll:focus-visible {outline:2px solid var(--accent);outline-offset:2px;}
.guide-table {width:100%;border-collapse:collapse;font-size:1rem;line-height:1.65;}
.guide-table th {font-size:.875rem;font-weight:700;text-align:left;background:var(--wash);padding:.75rem;border-top:2px solid var(--ink);}
.guide-table td {padding:.75rem;vertical-align:top;border-bottom:1px solid var(--line);font-variant-numeric:tabular-nums;}
.st-key-article_rail {border-left:1px solid var(--line);padding:1rem 0 0 1.5rem;}
.article-toc {margin-bottom:1.2rem;}
.article-toc strong {display:block;font-size:.875rem;letter-spacing:.06em;margin-bottom:.5rem;}
.article-toc a {display:block;color:var(--muted);font-size:.9375rem;line-height:1.6;padding:.55rem 0;text-decoration:none;}
.article-toc a:hover {color:var(--accent);text-decoration:underline;}
.mobile-toc {display:none;}

@media(max-width:760px) {
  .block-container {padding:1rem 1rem 3rem;}
  .masthead {padding:.3rem 0 1rem;}.masthead-edition {display:none;}
  .brand-title {font-size:1.1rem;}.brand-subtitle {font-size:.875rem;}
  .st-key-main_nav label[data-testid="stRadioOption"] {padding:.7rem .25rem;}
  .st-key-route_layout > [data-testid="stHorizontalBlock"],
  .st-key-profile_layout > [data-testid="stHorizontalBlock"] {flex-direction:column;}
  .st-key-route_layout > [data-testid="stHorizontalBlock"] > [data-testid="stColumn"],
  .st-key-profile_layout > [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {width:100%!important;flex:1 1 100%;min-width:0;}
  .st-key-route_notes {border-left:0;border-top:1px solid var(--line);padding:1rem 0 0;}
  .st-key-profile_editor {border-left:0;padding-left:0;}
  .st-key-profile_nav [role="radiogroup"] {display:flex;flex-direction:row;flex-wrap:wrap;gap:.25rem;}
  .st-key-profile_nav label[data-testid="stRadioOption"] {padding:.5rem .6rem;}
  .速覽清單 {grid-template-columns:1fr;gap:.5rem;}
  .st-key-main_nav label p {font-size:.875rem;}
  .st-key-guide_frontpage > [data-testid="stHorizontalBlock"],
  .st-key-guide_article_layout > [data-testid="stHorizontalBlock"] {flex-direction:column;}
  .st-key-guide_frontpage > [data-testid="stHorizontalBlock"] > [data-testid="stColumn"],
  .st-key-guide_article_layout > [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {width:100%!important;flex:1 1 100%;min-width:0;}
  .st-key-frontpage_quick, .st-key-article_rail {border-left:0;border-top:1px solid var(--line);padding:1rem 0 0;}
  .st-key-article_rail .article-toc {display:none;}
  .mobile-toc {display:block;border-bottom:1px solid var(--line);padding-bottom:.8rem;}
  .mobile-toc summary {min-height:44px;font-size:1rem;font-weight:650;cursor:pointer;}
  .guide-table {min-width:27rem;}
}
@media(max-width:480px) {
  .decision-facts {grid-template-columns:1fr;}
  .decision-facts > div + div {border-left:0;border-top:1px solid var(--line);padding-left:0;}
  .decision-check {display:block;}.decision-check span {display:block;margin-top:.2rem;}
  .獎勵項 {grid-template-columns:1.6rem 1fr;}.獎勵數據 {grid-column:2;}
}
@media(prefers-reduced-motion:reduce) {* {scroll-behavior:auto!important;transition:none!important;animation:none!important;}}
</style>
"""
