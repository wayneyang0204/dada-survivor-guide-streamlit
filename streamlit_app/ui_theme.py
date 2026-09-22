"""One shared, light-theme visual system for the player handbook."""

STYLE = """
<style>
:root {
  color-scheme:light;
  --paper:#ffffff; --canvas:#f7f9f6; --ink:#1b2925; --muted:#54655e;
  --line:#dce5de; --accent:#14604f; --accent-deep:#0b483c;
  --wash:#f2f7f2; --ready:#176446; --pending:#805510;
  --blocked:#a0392b; --field:#84968c;
}
html, body, .stApp {font-family:"Inter","Noto Sans TC","PingFang TC","Microsoft JhengHei",sans-serif;color:var(--ink);background:var(--canvas);}
.stApp {background:var(--canvas);}
.block-container {max-width:1160px;padding:3.2rem 2rem 5rem;}
[data-testid="stHeader"] {background:var(--canvas);height:1rem;}
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
.masthead {display:flex;align-items:center;justify-content:space-between;gap:1rem;padding:.35rem 0 1.15rem;}
.masthead-brand {display:flex;align-items:center;gap:.8rem;}
.brand-mark {display:grid;place-items:center;width:2.75rem;height:2.75rem;border-radius:.7rem;background:var(--accent-deep);color:#fff;font-size:1.45rem;font-weight:900;flex-shrink:0;box-shadow:0 3px 9px #103e3020;}
.brand-title {font-size:1.16rem;font-weight:800;letter-spacing:.03em;}
.brand-subtitle {display:block;font-size:.875rem;color:var(--muted);margin-top:.15rem;}
.masthead-edition {font-size:.875rem;color:var(--muted);text-align:right;letter-spacing:.04em;}
.st-key-main_nav {border-bottom:1px solid var(--line);margin-bottom:1.55rem;overflow-x:auto;scrollbar-width:thin;}
.st-key-main_nav [role="radiogroup"] {display:flex;flex-wrap:nowrap;gap:.35rem;width:max-content;}
.st-key-main_nav label[data-testid="stRadioOption"] {display:flex;flex:none;min-width:max-content;justify-content:center;margin:0;padding:.8rem 1rem .7rem;border-bottom:3px solid transparent;cursor:pointer;white-space:nowrap;}
.st-key-main_nav label[data-testid="stRadioOption"] > div > div > div:first-child {display:none;}
.st-key-main_nav label p {font-size:.95rem;font-weight:650;color:var(--muted);white-space:nowrap;}
.st-key-main_nav label:has(input:checked) {border-bottom-color:var(--accent);}
.st-key-main_nav label:has(input:checked) p {color:var(--accent);}
.st-key-main_nav label:hover {background:#eaf2eb;}
.st-key-main_nav label:has(input:focus-visible), .st-key-profile_nav label:has(input:focus-visible) {outline:2px solid var(--accent);outline-offset:-2px;}

/* Route title, resource toolbar, and a single prominent upgrade target. */
.page-heading {margin:.4rem 0 .25rem;font-size:clamp(1.7rem,3.5vw,2.15rem)!important;font-weight:800;}
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
  min-height:3rem;border:1px solid var(--line);border-radius:9px;background:var(--paper);box-shadow:0 1px 3px #1b29250b;
}
input, textarea {font-size:1rem!important;color:var(--ink);font-variant-numeric:tabular-nums;}
input::placeholder, textarea::placeholder {color:var(--muted);opacity:1;}
[data-baseweb="select"]:focus-within, [data-baseweb="input"]:focus-within,
.react-aria-ComboBox > div[role="group"]:focus-within, .react-aria-NumberField > div[role="group"]:focus-within {outline:2px solid var(--accent);outline-offset:1px;}
[role="listbox"], [data-baseweb="popover"] {background:var(--paper);color:var(--ink);}
[data-testid="stButton"] button, [data-testid="stFormSubmitButton"] button,
[data-testid="stDownloadButton"] button, [data-testid="stPopover"] button,
[data-testid="stLinkButton"] a {min-height:44px;border-radius:9px;box-shadow:none;font-weight:600;}
button[kind="primary"], button[data-testid="stBaseButton-primary"] {background:var(--accent);border-color:var(--accent);color:#fff;}
button[kind="primary"] p, button[data-testid="stBaseButton-primary"] p {color:#fff!important;}
button[kind="primary"]:hover {background:var(--accent-deep);border-color:var(--accent-deep);}
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

/* Field-guide design: quiet search panel, crisp editorial cards, readable facts. */
.st-key-guide_search_panel {padding:1.7rem 1.9rem 1.25rem;margin:0 0 1.55rem;background:linear-gradient(118deg,#e9f2eb 0%,#f7f9f3 75%);border:1px solid #d6e5d9;border-radius:18px;}
.guide-hero-kicker {color:var(--accent);font-size:.875rem;font-weight:800;letter-spacing:.16em;}
.guide-hero-kicker span {color:#b98b47;padding:0 .25rem;}
.guide-hero-title {font-size:clamp(1.6rem,2.5vw,2.4rem)!important;line-height:1.35;letter-spacing:-.04em;font-weight:800;margin:.45rem 0 .3rem;}
[data-testid="stMarkdownContainer"] .guide-hero-deck {font-size:.95rem;line-height:1.6;color:var(--muted);margin:0 0 .45rem;}
.st-key-guide_search_panel [data-testid="stWidgetLabel"] p {font-size:.875rem;letter-spacing:.04em;}
.st-key-guide_search_panel [data-baseweb="input"],
.st-key-guide_search_panel [data-baseweb="select"] > div,
.st-key-guide_search_panel .react-aria-ComboBox > div[role="group"] {min-height:3.25rem;background:#fff;border-color:#c7d8ce;}
.guide-results-head {display:flex;justify-content:space-between;align-items:baseline;gap:.5rem 1rem;border-bottom:1px solid var(--line);margin:.4rem 0 1rem;padding:0 0 .7rem;}
.guide-results-head h2 {font-size:1.22rem;font-weight:780;letter-spacing:-.02em;margin:0;}
.guide-results-head span {font-size:.875rem;color:var(--muted);font-variant-numeric:tabular-nums;}
[class*="st-key-guide_row_"] {background:var(--paper);border:1px solid var(--line);border-radius:13px;padding:1.05rem 1.4rem;margin:0 0 .75rem;box-shadow:0 3px 14px #213c2b08;}
[class*="st-key-guide_row_"]:hover {border-color:#aecbbb;box-shadow:0 5px 18px #213c2b12;}
[class*="st-key-guide_row_"] [data-testid="stVerticalBlock"] {gap:.28rem;}
.guide-meta {font-size:.875rem;letter-spacing:.035em;font-weight:750;color:var(--accent);}
.guide-meta span {color:var(--muted);font-weight:450;}
[class*="st-key-guide_row_"] [data-testid="stButton"] button {width:100%;padding:.12rem 0;justify-content:flex-start!important;text-align:left!important;}
[class*="st-key-guide_row_"] [data-testid="stButton"] button > div {justify-content:flex-start!important;width:100%;}
[class*="st-key-guide_row_"] [data-testid="stButton"] button p {font-size:1.16rem;font-weight:760;line-height:1.5;text-align:left!important;}
[class*="st-key-guide_row_"] [data-testid="stButton"] button:hover p {color:var(--accent);text-decoration:underline;text-underline-offset:.2em;}
[class*="st-key-guide_row_"] [data-testid="stMarkdownContainer"] > p {margin:.1rem 0;font-size:.99rem;line-height:1.65;}
.guide-verdict {border:1px solid #cddfd1;border-left:4px solid var(--accent);border-radius:0 12px 12px 0;background:#f0f7f1;padding:1.1rem 1.35rem;margin:.5rem 0 1.25rem;}
.guide-verdict h2 {font-size:.875rem;letter-spacing:.08em;margin:0 0 .5rem;color:var(--accent);}
.guide-verdict p {margin:0;font-size:1.08rem!important;line-height:1.7;}
.article-section {font-size:1.3rem;padding-top:.6rem;margin:1.5rem 0 .8rem;scroll-margin-top:1rem;}
.guide-table-scroll {max-width:100%;overflow-x:auto;margin:.8rem 0 1rem;}
.guide-table-scroll:focus-visible {outline:2px solid var(--accent);outline-offset:2px;}
.guide-table {width:100%;border-collapse:collapse;font-size:1rem;line-height:1.65;}
.guide-table th {font-size:.875rem;font-weight:700;text-align:left;background:var(--wash);padding:.75rem;border-top:2px solid var(--accent);}
.guide-table td {padding:.75rem;vertical-align:top;border-bottom:1px solid var(--line);font-variant-numeric:tabular-nums;}
.st-key-article_rail {border-left:1px solid var(--line);padding:1rem 0 0 1.5rem;}
.article-toc {margin-bottom:1.2rem;}
.article-toc strong {display:block;font-size:.875rem;letter-spacing:.06em;margin-bottom:.5rem;}
.article-toc a {display:block;color:var(--muted);font-size:.9375rem;line-height:1.6;padding:.55rem 0;text-decoration:none;}
.article-toc a:hover {color:var(--accent);text-decoration:underline;}
.mobile-toc {display:none;}
.scenario-answer {border:1px solid var(--line);border-left:4px solid var(--accent);border-radius:0 10px 10px 0;padding:.85rem 1rem;margin:.5rem 0 1rem;background:var(--paper);}
.scenario-answer h3 {font-size:1.15rem;margin:0 0 .5rem;}
.scenario-answer p {margin:.4rem 0;}
.search-facts {padding:.75rem 1rem .75rem 2rem;margin:.6rem 0;background:var(--wash);border-radius:8px;}
[data-testid="stMarkdownContainer"] .search-facts li {font-size:.9375rem;line-height:1.65;margin:.2rem 0;}
.page-deck:empty {display:none;}

@media(max-width:760px) {
  .block-container {padding:2.4rem 1rem 3rem;}
  .st-key-guide_search_panel {padding:1.2rem 1rem 1rem;border-radius:14px;margin-bottom:1.2rem;}
  .st-key-guide_search_panel [data-testid="stHorizontalBlock"] {flex-direction:column;gap:.4rem;}
  .st-key-guide_search_panel [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {width:100%!important;flex:1 1 100%;min-width:0;}
  .guide-hero-title {font-size:1.65rem!important;}
  .guide-results-head {align-items:center;}
  [class*="st-key-guide_row_"] {padding:1rem 1.05rem;}
  .page-heading {font-size:1.7rem!important;line-height:1.45;}
  .st-key-article_actions [data-testid="stHorizontalBlock"] {flex-direction:row!important;flex-wrap:nowrap!important;gap:.6rem;}
  .st-key-article_actions [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {flex:1 1 0!important;width:0!important;min-width:0;}
  .st-key-guide_article_layout .guide-verdict {padding:.8rem;margin:0 0 .7rem;}
  .guide-table {min-width:0!important;}
  .guide-table th, .guide-table td {padding:.5rem .3rem;font-size:.875rem;overflow-wrap:anywhere;}
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
  .st-key-main_nav label p {font-size:.875rem;white-space:nowrap;}
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
