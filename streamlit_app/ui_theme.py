"""One shared, light-theme visual system for the player handbook."""

from urllib.parse import quote

from ui_art import guide_icon

STYLE = """
<style>
:root {
  color-scheme:light;
  --paper:#ffffff; --canvas:#fffdf8; --ink:#302b26; --muted:#6b6054;
  --line:#e7e1d5; --accent:#79513a; --accent-deep:#593c2c;
  --wash:#faf4e8; --ready:#176446; --pending:#805510;
  --blocked:#a0392b; --field:#968571;
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
.brand-mark {display:grid;place-items:center;width:3.25rem;height:3.25rem;border-radius:18px;background:#edf6e6;border:1px solid #d6e5ce;flex-shrink:0;transform:rotate(-5deg);}
.brand-mark svg {width:3.1rem;height:3.1rem;}
.brand-title {font-size:1.16rem;font-weight:800;letter-spacing:.03em;}
.brand-subtitle {display:block;font-size:.875rem;color:var(--muted);margin-top:.15rem;}
.masthead-edition {font-size:.875rem;color:var(--muted);text-align:right;letter-spacing:.04em;}
.st-key-main_nav {border-bottom:1px dashed #d7decf;padding-bottom:.8rem;margin-bottom:1.25rem;overflow-x:auto;scrollbar-width:thin;}
.st-key-main_nav [role="radiogroup"] {display:flex;flex-wrap:nowrap;gap:.45rem;width:max-content;}
.st-key-main_nav label[data-testid="stRadioOption"] {display:flex;flex:none;min-width:max-content;justify-content:center;margin:0;padding:.65rem 1rem;border:1px solid transparent;border-radius:14px;cursor:pointer;white-space:nowrap;}
.st-key-main_nav label[data-testid="stRadioOption"] div:not([data-testid]):not(:has([data-testid="stMarkdownContainer"])):not(:has(input)) {display:none;}
.st-key-main_nav label p {font-size:.95rem;font-weight:650;color:var(--muted);white-space:nowrap;}
.st-key-main_nav label:has(input:checked) {border-color:#c3dcc9;background:#e3f0df;box-shadow:0 3px 0 #c5d9be;}
.st-key-main_nav label:has(input:checked) p {color:var(--accent);}
.st-key-main_nav label:hover {background:#edf5e8;}
.st-key-main_nav label:has(input:focus-visible), .st-key-profile_nav label:has(input:focus-visible) {outline:2px solid var(--accent);outline-offset:-2px;}

/* Route title, resource toolbar, and a single prominent upgrade target. */
.page-heading {margin:.4rem 0 .25rem;font-size:clamp(1.7rem,3.5vw,2.15rem)!important;font-weight:800;}
.page-deck {margin:0 0 .6rem;color:var(--muted)!important;}
.st-key-route_toolbar {border-bottom:1px solid var(--line);padding-bottom:1rem;margin-bottom:.5rem;}
.route-context {padding:.6rem 0;font-size:.875rem;color:var(--muted);line-height:1.65;}
.route-context strong {display:block;font-size:1.05rem;color:var(--ink);}
.decision-lead {display:flex;align-items:center;flex-wrap:wrap;gap:.6rem;margin:.25rem 0 .8rem;font-size:.875rem;font-weight:650;color:var(--muted);}
.section-index {color:var(--accent);background:#e3f0df;border-radius:8px;font-variant-numeric:tabular-nums;font-weight:750;padding:.25rem .55rem;}
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
.st-key-onboarding {max-width:760px;background:var(--paper);border:1px solid var(--line);border-radius:22px;padding:1.6rem 1.8rem;box-shadow:0 5px 0 #f0e8da;}
.setup-note {border-top:1px solid var(--line);padding-top:1rem;font-size:.875rem;color:var(--muted);line-height:1.7;}

/* Account sections stay visible, with only one editor open. */
.st-key-profile_nav {padding-top:.5rem;}
.st-key-profile_nav [role="radiogroup"] {gap:.2rem;}
.st-key-profile_nav label[data-testid="stRadioOption"] {margin:0;padding:.6rem .7rem;border-left:3px solid transparent;border-radius:12px;min-height:44px;}
.st-key-profile_nav label[data-testid="stRadioOption"] div:not([data-testid]):not(:has([data-testid="stMarkdownContainer"])):not(:has(input)) {display:none;}
.st-key-profile_nav label:has(input:checked) {background:var(--wash);border-left-color:var(--accent);}
.st-key-profile_nav label p {font-size:1rem;color:var(--muted);}
.st-key-profile_nav label:has(input:checked) p {color:var(--accent);font-weight:650;}
.st-key-profile_editor {border-left:1px solid var(--line);padding-left:1.5rem;}
.editor-heading {font-size:1.4rem;padding:0;margin:.35rem 0 1rem;}

/* Native controls: comfortable hit areas, visible labels and keyboard focus. */
[data-baseweb="select"] > div, [data-baseweb="input"], [data-baseweb="textarea"],
.react-aria-ComboBox > div[role="group"], .react-aria-NumberField > div[role="group"] {
  min-height:3rem;border:1px solid var(--line);border-radius:13px;background:var(--paper);box-shadow:0 2px 0 #e7ebdf;
}
input, textarea {font-size:1rem!important;color:var(--ink);font-variant-numeric:tabular-nums;}
input::placeholder, textarea::placeholder {color:var(--muted);opacity:1;}
[data-baseweb="select"]:focus-within, [data-baseweb="input"]:focus-within,
.react-aria-ComboBox > div[role="group"]:focus-within, .react-aria-NumberField > div[role="group"]:focus-within {outline:2px solid var(--accent);outline-offset:1px;}
[role="listbox"], [data-baseweb="popover"] {background:var(--paper);color:var(--ink);}
[data-testid="stButton"] button, [data-testid="stFormSubmitButton"] button,
[data-testid="stDownloadButton"] button, [data-testid="stPopover"] button,
[data-testid="stLinkButton"] a {min-height:44px;border-radius:13px;box-shadow:none;font-weight:600;}
button[data-testid^="stBaseButton-primary"] {background:var(--accent);border-color:var(--accent);color:#fff;}
button[data-testid^="stBaseButton-primary"] p {color:#fff!important;}
button[data-testid^="stBaseButton-primary"]:hover {background:var(--accent-deep);border-color:var(--accent-deep);}
[data-testid="stForm"] {border:0;padding:0;}
[data-testid="stExpander"] {border:1px solid var(--line);border-radius:16px;background:var(--paper);box-shadow:0 3px 0 #f1eadf;overflow:hidden;}
[data-testid="stExpander"] summary {padding:.8rem 1rem;min-height:44px;}
[data-testid="stExpander"] summary p {font-size:.9375rem;font-weight:600;}
[data-testid="stAlert"] {border-radius:14px;}
[data-testid="stMetric"] {border-top:1px solid var(--line);padding:.8rem 0;}
[data-testid="stMetricValue"] {font-variant-numeric:tabular-nums;font-size:1.8rem;font-weight:700;}
[data-testid="stDataFrame"] {border:1px solid var(--line);border-radius:14px;}
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
.st-key-guide_search_panel {padding:1.35rem 1.8rem 1.15rem;margin:0 0 .8rem;background:linear-gradient(115deg,#edf7e9 0%,#fffdf7 70%,#fff0e4 100%);border:1px solid #d8e6ce;border-radius:26px;box-shadow:0 5px 0 #e5ebda;}
.hero-intro {display:flex;align-items:center;justify-content:space-between;gap:1.25rem;}
.hero-copy {min-width:0;}
.hero-companion {flex:0 0 132px;background:#ffffffa0;border:1px dashed #c7d9be;border-radius:42% 48% 43% 45%;padding:.3rem;transform:rotate(5deg);}
.hero-companion svg {display:block;width:100%;height:auto;}
.st-key-task_entries {margin-bottom:1.3rem;}
[class*="st-key-task_entry_"] {background:var(--paper);border:1px solid var(--line);border-radius:20px;padding:.8rem 1.1rem;box-shadow:0 4px 0 #e8eedf;transition:transform .15s ease,box-shadow .15s ease;}
.st-key-task_entries [data-testid="stColumn"]:nth-child(1) [class*="st-key-task_entry_"] {background:#eff7e9;border-color:#d2e2c9;}
.st-key-task_entries [data-testid="stColumn"]:nth-child(2) [class*="st-key-task_entry_"] {background:#fff0e5;border-color:#efdbc9;box-shadow:0 4px 0 #f1dfcf;}
.st-key-task_entries [data-testid="stColumn"]:nth-child(3) [class*="st-key-task_entry_"] {background:#f3eefc;border-color:#ded5ef;box-shadow:0 4px 0 #e6ddf2;}
[class*="st-key-task_entry_"] [data-testid="stVerticalBlock"] {gap:.2rem;}
[class*="st-key-task_entry_"] button {border:0;background:transparent;padding:0!important;text-align:left;justify-content:flex-start!important;}
[class*="st-key-task_entry_"] button > div {justify-content:flex-start!important;width:100%;}
[class*="st-key-task_entry_"] button p {font-size:1.05rem;font-weight:750;color:var(--accent);}
[class*="st-key-task_entry_"]:hover {transform:translateY(-2px);}
[class*="st-key-directory_"] {border-bottom:1px solid var(--line);padding:.45rem 0 .65rem;}
[class*="st-key-directory_"]:last-child {border-bottom:0;}
[class*="st-key-directory_"] [data-testid="stVerticalBlock"] {gap:.1rem;}
[class*="st-key-directory_"] button {justify-content:flex-start!important;text-align:left!important;padding:.15rem 0;}
[class*="st-key-directory_"] button > div {justify-content:flex-start!important;width:100%;}
[class*="st-key-directory_"] button p {font-size:1rem;font-weight:700;text-align:left!important;}
.workflow-strip {display:flex;gap:1.4rem;border-bottom:1px solid var(--line);padding:.4rem 0 1rem;margin:0 0 1.25rem;font-size:.875rem;color:var(--muted);}
.workflow-strip span {line-height:1.65;}
.workflow-strip .active {font-weight:750;color:var(--accent);background:#e3f0df;border-radius:8px;padding:0 .4rem;}
.event-verdict {border-left:3px solid var(--accent);background:var(--wash);padding:.9rem 1.1rem;border-radius:0 10px 10px 0;}
.event-verdict strong {color:var(--accent);font-size:.875rem;}
.event-verdict p {margin:.35rem 0 0!important;}
.guide-hero-title {font-size:clamp(1.6rem,2.5vw,2.4rem)!important;line-height:1.35;letter-spacing:-.04em;font-weight:800;padding:0!important;margin:.45rem 0 .3rem!important;}
[data-testid="stMarkdownContainer"] .guide-hero-deck {font-size:.95rem;line-height:1.6;color:var(--muted);margin:0 0 .45rem;}
.st-key-guide_search_panel [data-testid="stWidgetLabel"] p {font-size:.875rem;letter-spacing:.04em;}
.st-key-guide_search_panel [data-baseweb="input"],
.st-key-guide_search_panel [data-baseweb="select"] > div,
.st-key-guide_search_panel .react-aria-ComboBox > div[role="group"] {min-height:3.25rem;background:#fff;border-color:#c7d8ce;}
.guide-results-head {display:flex;justify-content:space-between;align-items:baseline;gap:.5rem 1rem;border-bottom:1px solid var(--line);margin:.4rem 0 1rem;padding:0 0 .7rem;}
.guide-results-head h2 {font-size:1.22rem;font-weight:780;letter-spacing:-.02em;margin:0;}
.guide-results-head span {font-size:.875rem;color:var(--muted);font-variant-numeric:tabular-nums;}
[class*="st-key-guide_row_"] {background:var(--paper);border:1px solid var(--line);border-radius:20px;padding:1.05rem 1.4rem;margin:0 0 .75rem;box-shadow:0 4px 0 #eee9de;}
[class*="st-key-guide_row_"]:hover {border-color:#aecbbb;box-shadow:0 5px 18px #213c2b12;}
[class*="st-key-guide_row_"] [data-testid="stVerticalBlock"] {gap:.28rem;}
.guide-meta {font-size:.875rem;letter-spacing:.035em;font-weight:750;color:var(--accent);}
.guide-meta span {color:var(--muted);font-weight:450;}
[class*="st-key-guide_row_"] [data-testid="stButton"] button {width:100%;padding:.12rem 0;justify-content:flex-start!important;text-align:left!important;}
[class*="st-key-guide_row_"] [data-testid="stButton"] button > div {justify-content:flex-start!important;width:100%;}
[class*="st-key-guide_row_"] [data-testid="stButton"] button p {font-size:1.16rem;font-weight:760;line-height:1.5;text-align:left!important;}
[class*="st-key-guide_row_"] [data-testid="stButton"] button:hover p {color:var(--accent);text-decoration:underline;text-underline-offset:.2em;}
[class*="st-key-guide_row_"] [data-testid="stMarkdownContainer"] > p {margin:.1rem 0;font-size:.99rem;line-height:1.65;}
.guide-verdict {border:1px solid #cddfd1;border-left:4px solid var(--accent);border-radius:8px 18px 18px 8px;background:#f0f7f1;padding:1.1rem 1.35rem;margin:.5rem 0 1.25rem;}
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
.action-brief {border:1px solid #cddfd1;border-radius:18px;background:#f0f7f1;padding:1rem 1.2rem;margin:.4rem 0 1.2rem;}
.action-brief h3 {font-size:.9375rem;color:var(--accent);margin:0 0 .4rem;}
.action-brief p {font-size:1.06rem;line-height:1.65;margin:.35rem 0;}
.action-brief span {display:block;font-size:.875rem;color:var(--muted);margin-top:.65rem;line-height:1.6;}
.operation-entry {font-size:.9375rem;font-weight:650;border-top:1px solid #cddfd1;padding-top:.7rem;margin-top:.8rem;}
.operation-steps {margin:.6rem 0 0;padding-left:1.35rem;}
[data-testid="stMarkdownContainer"] .operation-steps li {font-size:.9375rem;line-height:1.7;padding:.2rem 0;}
.search-facts {padding:.75rem 1rem .75rem 2rem;margin:.6rem 0;background:var(--wash);border-radius:8px;}
[data-testid="stMarkdownContainer"] .search-facts li {font-size:.9375rem;line-height:1.65;margin:.2rem 0;}
.page-deck:empty {display:none;}

@media(max-width:760px) {
  .block-container {padding:2.4rem 1rem 3rem;}
  .st-key-guide_search_panel {padding:1.2rem 1rem 1rem;border-radius:22px;margin-bottom:1.2rem;}
  .hero-intro {gap:.6rem;align-items:flex-start;}
  .hero-companion {flex-basis:64px;padding:.1rem;}
  .st-key-guide_search_panel [data-testid="stHorizontalBlock"] {flex-direction:column;gap:.4rem;}
  .st-key-guide_search_panel [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {width:100%!important;flex:1 1 100%;min-width:0;}
  .guide-hero-title {font-size:1.65rem!important;}
  .st-key-task_entries [data-testid="stHorizontalBlock"] {flex-direction:column;gap:.6rem;}
  .st-key-task_entries [data-testid="stColumn"] {width:100%!important;flex:1 1 100%;min-width:0;}
  [class*="st-key-task_entry_"] {padding:.6rem 1rem;}
  .st-key-onboarding {padding:1rem;}
  .workflow-strip {gap:.65rem;justify-content:space-between;}
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
  .st-key-main_nav [role="radiogroup"] {gap:.25rem;}
  .st-key-main_nav label[data-testid="stRadioOption"] {padding:.65rem .25rem;border-radius:10px;}
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


# One final, scoped layer for the illustrated field-guide edition. Native
# Streamlit controls retain their labels, keyboard behaviour, and state.
_FIELD_GUIDE = """
/* Little eagle edition: cream nest, caramel ink and pale sky. The mint/lilac
   token names are retained for compatibility; their surfaces are now nest/sky. */
:root {--canvas:#fffdf8;--peach:#fff0e8;--mint:#faf3e4;--lilac:#eef4f9;--shadow:#4636270b;}
.block-container {padding-top:2rem;}
[data-testid="stHeader"] {display:none;}
[data-testid="stElementContainer"] [data-testid="stCaptionContainer"] {opacity:1;}
.masthead {padding:0 0 1.1rem;}
.brand-mark {width:3.6rem;height:3.6rem;border-radius:20px;background:#fff5e1;transform:none;border:1px solid #eadcc4;}
.brand-mark svg {width:3.2rem;height:3.2rem;}
.brand-title {font-size:1.35rem;letter-spacing:.025em;}
.brand-subtitle {font-size:.875rem;}
.masthead-edition {display:flex;flex-direction:column;gap:.35rem;font-size:.875rem;}
.edition-label {align-self:flex-end;color:var(--accent);background:var(--mint);border:1px solid #eadcc4;border-radius:30px;padding:.3rem .75rem;font-size:.875rem;font-weight:700;letter-spacing:.08em;}
.st-key-main_nav {background:var(--paper);border:1px solid var(--line);border-radius:18px;padding:.4rem;margin:.3rem 0 1.5rem;box-shadow:0 3px 10px var(--shadow);overflow:visible;}
.st-key-main_nav [data-testid="stElementContainer"]:has(> [data-testid="stRadio"]) {width:100%!important;}
.st-key-main_nav [role="radiogroup"] {display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:.3rem;width:100%;}
.st-key-main_nav label[data-testid="stRadioOption"] {gap:.5rem;min-width:0;padding:.75rem .4rem;border-radius:13px;min-height:52px;}
.st-key-main_nav label[data-testid="stRadioOption"]::before {content:"";display:block;flex:0 0 1.5rem;width:1.5rem;height:1.5rem;background-position:center;background-repeat:no-repeat;background-size:contain;}
.st-key-main_nav label:has(input:checked) {background:var(--mint);border-color:#e5d6bb;box-shadow:none;}
.st-key-main_nav label p {font-size:.9375rem;font-weight:650;}
.st-key-main_nav label:hover {background:#fffbf2;}

/* Home: one searchable desk, three distinct tools, six topic shelves. */
.st-key-guide_search_panel {position:relative;background:var(--paper);border:1px solid #e8e4d9;border-radius:28px;padding:1.6rem 1.8rem 1.35rem;box-shadow:0 6px 20px var(--shadow);overflow:hidden;}
.st-key-guide_search_panel::before {content:"";position:absolute;left:0;right:0;top:0;height:5px;background:linear-gradient(90deg,#e7c17b 0% 45%,#c5d8e6 45% 73%,#e8cebb 73%);}
.hero-intro {gap:1rem;margin-bottom:.85rem;}
.guide-hero-title {font-size:clamp(1.8rem,3.1vw,2.7rem)!important;line-height:1.5;margin:.45rem 0!important;}
.hero-library-note {font-size:.875rem;color:var(--muted);margin-top:.9rem;line-height:1.6;font-variant-numeric:tabular-nums;}
.hero-library-note span {padding:0 .6rem;color:#a5ab98;}
.hero-companion {position:relative;flex:0 0 220px;background:#eff5f8;border:0;border-radius:46% 45% 40% 44%;padding:.35rem .1rem;transform:none;}
.hero-companion svg {width:100%;height:auto;}
.st-key-guide_search_panel [data-baseweb="input"] {border:1px solid #c5d3c7!important;box-shadow:none;background:#fff!important;}
.st-key-guide_search_panel input {background:#fff!important;}
[data-testid="stTextInputRootElement"], [data-testid="stTextAreaRootElement"] {border:1px solid var(--field);border-radius:12px;background:var(--paper);min-height:3rem;}
[data-testid="stTextInputRootElement"]:focus-within, [data-testid="stTextAreaRootElement"]:focus-within {outline:2px solid var(--accent);outline-offset:2px;}
.st-key-guide_search_panel [data-testid="stTextInputRootElement"] {min-height:3.25rem;}
.st-key-task_entries {margin:.6rem 0 1.2rem;}
[class*="st-key-task_entry_"] {gap:.25rem;padding:.9rem 1.05rem 1rem;border-radius:20px;box-shadow:0 3px 12px var(--shadow)!important;transition:border-color .15s ease;}
[class*="st-key-task_entry_"]:hover {transform:none;}
.st-key-task_entries [data-testid="stColumn"]:nth-child(1) [class*="st-key-task_entry_"] {background:var(--mint);border-color:#eadcc4;}
.st-key-task_entries [data-testid="stColumn"]:nth-child(2) [class*="st-key-task_entry_"] {background:var(--peach);border-color:#efded3;}
.st-key-task_entries [data-testid="stColumn"]:nth-child(3) [class*="st-key-task_entry_"] {background:var(--lilac);border-color:#d8e5ee;}
.task-card-head {display:flex;align-items:center;justify-content:space-between;gap:.5rem;margin-bottom:.1rem;}
.task-tag {font-size:.875rem;color:var(--muted);font-weight:650;}
.task-art {display:grid;place-items:center;width:2.65rem;height:2.65rem;border-radius:14px;background:#ffffffb8;}
.task-art svg {width:2.15rem;height:2.15rem;}
[class*="st-key-task_entry_"] button {min-height:44px;}
[class*="st-key-task_entry_"] button p {font-size:1.13rem;font-weight:750;color:var(--ink);}
[class*="st-key-task_entry_"] button:hover p {color:var(--accent);text-decoration:underline;text-underline-offset:.22em;}
[class*="st-key-task_entry_"] [data-testid="stCaptionContainer"] p {margin:0;font-size:.875rem;}
[class*="st-key-task_entry_"] [data-testid="stCaptionContainer"] {margin-bottom:0;}
.guide-results-head {margin:.5rem 0 .85rem;border-bottom:0;padding:0;}
.guide-results-head h2 {font-size:1.2rem;}
[class*="st-key-topic_cover_"] {background:var(--paper);border:1px solid var(--line);border-radius:20px;padding:1rem;margin-bottom:.55rem;box-shadow:0 3px 12px var(--shadow);}
.topic-heading {display:flex;align-items:center;gap:.7rem;margin-bottom:.6rem;}
.topic-art {display:grid;place-items:center;flex:0 0 2.9rem;width:2.9rem;height:2.9rem;background:var(--mint);border-radius:15px;}
.topic-art svg {width:2.35rem;height:2.35rem;}
.st-key-topic_cover_1 .topic-art, .st-key-topic_cover_4 .topic-art {background:var(--peach);}
.st-key-topic_cover_2 .topic-art, .st-key-topic_cover_3 .topic-art {background:var(--lilac);}
.topic-heading > div {flex:1;min-width:0;}
.topic-heading h3 {font-size:1.05rem;margin:0;padding:0;}
[data-testid="stMarkdownContainer"] .topic-heading p {font-size:.875rem;color:var(--muted);line-height:1.5;margin:.2rem 0 0;}
.topic-count {font-size:.875rem;color:var(--muted);white-space:nowrap;font-variant-numeric:tabular-nums;}
.st-key-guide_directory [data-testid="stExpander"] {background:#fcfcf9;border:1px solid #ecece2;box-shadow:none;border-radius:12px;}
.st-key-guide_directory [data-testid="stExpander"] summary {padding:.55rem .75rem;}
[class*="st-key-guide_row_"] {border-radius:20px;box-shadow:0 3px 12px var(--shadow);border-color:#e5e5da;}
.guide-meta {display:flex;align-items:center;gap:.5rem;font-size:.875rem;}
.guide-meta::before {content:"";width:.4rem;height:.4rem;background:#c29865;border-radius:50%;}
.guide-meta span {color:var(--muted);}

/* Reading and planning: pale accents never replace high-contrast text. */
.page-heading {padding:0;letter-spacing:-.025em;}
.page-deck {line-height:1.7;}
.guide-verdict {position:relative;background:var(--mint);border:1px solid #eadcc4;border-radius:20px;padding:1.25rem 1.3rem;margin:.5rem 0 1rem;box-shadow:0 3px 10px var(--shadow);}
.guide-verdict h2 {display:flex;align-items:center;gap:.45rem;letter-spacing:.04em;}
.guide-verdict h2::before {content:"";display:inline-block;width:.5rem;height:.5rem;background:#c29865;border-radius:3px;transform:rotate(45deg);}
.guide-verdict p {font-size:1.03rem!important;}
.guide-table-scroll {border:1px solid #e3e5d9;border-radius:14px;}
.guide-table th {border-top:0;background:var(--mint);}
.guide-table tbody tr:nth-child(even) {background:#fffcf6;}
.guide-table tbody tr:last-child td {border-bottom:0;}
.st-key-article_rail {border:1px solid var(--line);background:#fffdf9;border-radius:18px;padding:1rem;}
.article-toc a {padding:.45rem .5rem;border-radius:9px;}
.article-toc a:hover {background:var(--mint);text-decoration:none;}
.scenario-answer {background:#fffcf6;border:1px solid #eaddc4;border-radius:17px;}
.workflow-strip {gap:0;padding:.4rem;background:var(--paper);border:1px solid var(--line);border-radius:15px;margin:.6rem 0 1.1rem;}
.workflow-strip span {flex:1;text-align:center;padding:.5rem .3rem!important;border-radius:10px;}
.workflow-strip .active {background:var(--mint);}
.st-key-onboarding {max-width:820px;border-radius:24px;box-shadow:0 5px 20px var(--shadow);border-color:#e4e5da;padding:1.5rem;}
.st-key-onboarding [data-testid="stMarkdownContainer"] .setup-heading {font-size:1.4rem;line-height:1.45;margin:.2rem 0 .3rem;padding:0;}
.setup-art {float:right;width:3.1rem;height:3.1rem;display:grid;place-items:center;background:var(--mint);border-radius:16px;}
.setup-art svg {width:2.45rem;height:2.45rem;}
.st-key-route_toolbar {background:var(--paper);border:1px solid var(--line);border-radius:18px;padding:1rem;margin:0 0 .7rem;}
.st-key-route_layout > [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:first-child {background:var(--paper);border:1px solid var(--line);border-radius:23px;padding:1.15rem 1.35rem;box-shadow:0 4px 16px var(--shadow);}
.st-key-route_notes {border:1px solid #d8e5ee;background:var(--lilac);border-radius:20px;padding:1.15rem!important;}
.notes-heading {margin-top:0;}
.decision-facts {border-top:1px solid #eaddc6;background:#fffcf4;border-radius:14px;padding:0 .85rem;}
.decision-title {font-size:clamp(1.45rem,2.7vw,1.9rem);}
.action-brief {background:var(--mint);border-color:#eadcc4;border-radius:18px;}
.operation-steps {list-style:none;counter-reset:operation;padding:0;}
.operation-steps li {counter-increment:operation;position:relative;padding:.45rem 0 .45rem 2rem!important;}
.operation-steps li::before {content:counter(operation);position:absolute;left:0;top:.55rem;display:grid;place-items:center;width:1.4rem;height:1.4rem;border-radius:8px;background:#fff;color:var(--accent);font-size:.875rem;font-weight:750;border:1px solid #e3d2b5;}
.st-key-profile_nav {background:#f7f6f1;border:1px solid var(--line);border-radius:18px;padding:.4rem;}
.st-key-profile_editor {border:1px solid var(--line);background:var(--paper);border-radius:22px;padding:1.25rem;box-shadow:0 4px 16px var(--shadow);}
.editor-heading {margin:.15rem 0 1rem;}
[data-testid="stMarkdownContainer"] .editor-heading {font-size:1.35rem;line-height:1.45;padding:0;}
[data-testid="stMarkdownContainer"] .topic-heading h3 {font-size:1.05rem;line-height:1.5;padding:0;margin:0;}
[data-testid="stMarkdownContainer"] .guide-results-head h2 {font-size:1.2rem;line-height:1.5;padding:0;margin:0;}
.event-verdict {background:var(--peach);border:1px solid #efded3;border-radius:18px;padding:1rem 1.2rem;}
.重點速覽 {border:1px solid var(--line);background:var(--paper);border-radius:22px;padding:1.2rem;}
.速覽結論 {border-radius:14px;}
[data-testid="stButton"] button, [data-testid="stFormSubmitButton"] button, [data-testid="stDownloadButton"] button, [data-testid="stPopover"] button, [data-testid="stLinkButton"] a {border-radius:12px;}
button[data-testid^="stBaseButton-primary"] {box-shadow:0 3px 0 var(--accent-deep);}
button[data-testid^="stBaseButton-primary"]:active {box-shadow:none;}
[data-testid="stExpander"] {box-shadow:none;border-radius:15px;}
[data-testid="stAlert"] {border-radius:15px;}
.site-footer {font-size:.875rem;text-align:center;border-top:1px solid var(--line);padding-top:1.25rem;}

@media(max-width:760px) {
  .block-container {padding:1.5rem 1rem 3rem;}
  .brand-title {font-size:1.2rem;}.masthead-edition {display:none;}
  .st-key-main_nav {padding:.3rem;margin-bottom:1rem;border-radius:16px;}
  .st-key-main_nav [role="radiogroup"] {display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:.1rem;}
  .st-key-main_nav label[data-testid="stRadioOption"] {display:flex;flex-direction:column;gap:.3rem;padding:.5rem .05rem;min-height:64px;border-radius:11px;}
  .st-key-main_nav label[data-testid="stRadioOption"]::before {flex:0 0 1.4rem;width:1.4rem;height:1.4rem;}
  .st-key-main_nav label p {font-size:.875rem;letter-spacing:-.035em;}
  .st-key-guide_search_panel {padding:1.3rem 1rem 1rem;border-radius:23px;margin-bottom:.6rem;}
  .hero-intro {gap:.1rem;margin-bottom:.4rem;align-items:center;}
  .hero-companion {flex-basis:110px;padding:0;}
  .guide-hero-title {font-size:1.8rem!important;line-height:1.45;}
  .hero-library-note {font-size:.875rem;margin-top:.5rem;}
  .hero-library-note span {padding:0 .2rem;}
  .st-key-task_entries [data-testid="stHorizontalBlock"] {flex-direction:column;gap:.6rem;}
  [class*="st-key-task_entry_"] {position:relative;padding:.7rem .95rem;}
  .task-card-head {position:absolute;right:.95rem;top:.65rem;margin:0;}
  .task-tag {display:none;}.task-art {width:2.6rem;height:2.6rem;}
  [class*="st-key-task_entry_"] button {width:calc(100% - 3rem)!important;}
  [class*="st-key-task_entry_"] button p {font-size:1.05rem;}
  .guide-results-head span {font-size:.875rem;}
  .st-key-guide_directory > [data-testid="stVerticalBlock"] > [data-testid="stHorizontalBlock"],
  .st-key-guide_directory > [data-testid="stHorizontalBlock"] {flex-direction:column;gap:.5rem;}
  .st-key-guide_directory [data-testid="stColumn"] {width:100%!important;flex:1 1 100%;min-width:0;}
  [class*="st-key-topic_cover_"] {padding:.9rem;margin-bottom:.4rem;}
  .topic-count {font-size:.875rem;}
  .st-key-route_layout > [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:first-child {padding:1rem;}
  .st-key-route_notes {padding:1rem!important;}
  .st-key-profile_editor {padding:1rem;}
  .st-key-onboarding {padding:1.1rem;}
  .workflow-strip {gap:.1rem;}.workflow-strip span {font-size:.875rem;}
  .st-key-route_toolbar {padding:.85rem;}
  .st-key-route_toolbar [data-testid="stHorizontalBlock"] {flex-wrap:wrap;gap:.6rem;}
  .st-key-route_toolbar [data-testid="stColumn"]:first-child {flex:1 1 100%;width:100%!important;}
  .st-key-article_rail {display:none;}
  .guide-verdict {padding:1rem!important;border-radius:18px;}
  .guide-table th, .guide-table td {font-size:.875rem;}
}
@media(max-width:380px) {
  .block-container {padding-left:.75rem;padding-right:.75rem;}
  .st-key-main_nav [role="radiogroup"] {grid-template-columns:repeat(3,minmax(0,1fr));gap:.2rem;}
  .hero-companion {flex-basis:64px;}.guide-hero-title {font-size:1.5rem!important;}
  .topic-count {white-space:normal;max-width:4rem;}
}
@media(prefers-reduced-motion:reduce) {* {transition:none!important;animation:none!important;}}
"""

_NAV_ART = "\n".join(
    f'.st-key-main_nav label[data-testid="stRadioOption"]:has(input[value="{index}"])::before '
    f'{{background-image:url("data:image/svg+xml,{quote(guide_icon(name), safe="")}");}}'
    for index, name in enumerate(("home", "upgrade", "profile", "event", "book"))
)
_MOTION_GUIDE = """
/* Motion is decorative and local. No scrolling takeover, sound, or remote player. */
[data-testid="stElementContainer"]:has(.motion-preferences) {display:none;}
.kite-flight,.kite-direction {transform-box:view-box;transform-origin:120px 98px;}
.kite-sparkle {transform-box:fill-box;transform-origin:center;}
body:has([data-motion-enabled="on"]) .kite-animated .kite-flight {animation:kite-cruise 12s ease-in-out infinite;}
body:has([data-motion-enabled="on"]) .kite-animated .kite-direction {animation:kite-direction 12s ease-in-out infinite;}
body:has([data-motion-enabled="on"]) .kite-animated .kite-cloud {animation:kite-cloud-drift 12s ease-in-out infinite;}
body:has([data-motion-enabled="on"]) .kite-animated .cloud-front {animation-delay:-6s;}
body:has([data-motion-enabled="on"]) .kite-animated .kite-sparkle {animation:kite-twinkle 3s ease-in-out infinite;}
/* Header stays inside its badge. Horizontal flight belongs to the sky scene. */
body:has([data-motion-enabled="on"]) .brand-mark .kite-flight {animation:kite-hover 3s ease-in-out infinite;}
.brand-mark .kite-direction {transform:scale(1.12);}
body:has([data-motion-enabled="on"]) .brand-mark .kite-direction {animation:none;}
.hero-companion {overflow:hidden;isolation:isolate;}
.hero-companion svg {pointer-events:none;}
body:has([data-motion-enabled="on"]) .st-key-main_nav label:has(input:checked)::before {animation:icon-hop .38s ease-out;}
body:has([data-motion-enabled="on"]) .st-key-main_nav label:hover::before {animation:icon-wave .5s ease-out;}
body:has([data-motion-enabled="on"]) [class*="st-key-task_entry_"] {transition:transform .2s ease,box-shadow .2s ease;}
body:has([data-motion-enabled="on"]) [class*="st-key-task_entry_"]:is(:hover,:focus-within) {transform:translateY(-3px);box-shadow:0 7px 18px var(--shadow)!important;}
body:has([data-motion-enabled="on"]) [class*="st-key-task_entry_"]:is(:hover,:focus-within) .task-art {animation:icon-hop .45s ease-out;}
body:has([data-motion-enabled="on"]) [class*="st-key-topic_cover_"] {transition:border-color .2s ease,box-shadow .2s ease;}
[class*="st-key-topic_cover_"]:is(:hover,:focus-within), [class*="st-key-topic_cover_"]:has(details[open]) {border-color:#b79972;}
body:has([data-motion-enabled="on"]) [class*="st-key-topic_cover_"]:is(:hover,:focus-within) .topic-art,
body:has([data-motion-enabled="on"]) [class*="st-key-topic_cover_"]:has(details[open]) .topic-art {animation:icon-wave .55s ease-out;}
body:has([data-motion-enabled="on"]) :is(.guide-verdict,.scenario-answer,.action-brief,.event-verdict) {animation:panel-arrive .32s ease-out;}
body:has([data-motion-enabled="on"]) .workflow-strip .active {animation:step-glow .65s ease-out;}
body:has([data-motion-enabled="on"]) .st-key-profile_editor {animation:panel-arrive .28s ease-out;}
body:has([data-motion-enabled="on"]) [data-testid="stExpander"] details[open] [data-testid="stExpanderDetails"] {animation:panel-arrive .25s ease-out;}
body:has([data-motion-enabled="on"]) .st-key-onboarding:focus-within .setup-art {animation:icon-wave .5s ease-out;}
.decision-check.ready b::before {content:"✓";display:inline-block;margin-right:.35rem;}
body:has([data-motion-enabled="on"]) .decision-check.ready b::before {animation:icon-hop .4s ease-out;}
body:has([data-motion-enabled="on"]) button:active:not(:disabled) {transform:translateY(1px);}
.guide-table tbody tr:hover {background:#f6eedc;}
.hero-companion svg {overflow:visible;}
@media(max-width:760px) {.hero-companion {flex-basis:124px;}}
@media(max-width:380px) {.hero-companion {flex-basis:96px;}}
@keyframes kite-cruise {0%,100% {transform:translate(-15px,3px) rotate(-3deg);}25% {transform:translate(0,-6px) rotate(2deg);}50% {transform:translate(15px,2px) rotate(3deg);}75% {transform:translate(0,-3px) rotate(-2deg);}}
@keyframes kite-direction {0%,44%,100% {transform:scaleX(1);}49%,94% {transform:scaleX(-1);}}
@keyframes kite-hover {0%,100% {transform:translateY(0);}50% {transform:translateY(-4px);}}
@keyframes kite-cloud-drift {0%,100% {transform:translateX(0);}50% {transform:translateX(-12px);}}
@keyframes kite-twinkle {0%,100% {transform:scale(.8);opacity:.45;}50% {transform:scale(1.25);opacity:1;}}
@keyframes icon-hop {0%,100% {transform:translateY(0);}45% {transform:translateY(-4px) rotate(-4deg);}}
@keyframes icon-wave {0%,100% {transform:rotate(0deg);}30% {transform:rotate(-7deg);}65% {transform:rotate(5deg);}}
@keyframes panel-arrive {from {transform:translateY(5px);}to {transform:translateY(0);}}
@keyframes step-glow {0%,100% {box-shadow:0 0 0 0 #e7c17b00;}45% {box-shadow:0 0 0 4px #e7c17b30;}}
/* Keep controls and static state cues usable when motion is disabled. */
body:has([data-motion-enabled="off"]) * {animation:none!important;transition:none!important;}
body:has([data-motion-enabled="off"]) [class*="st-key-task_entry_"]:is(:hover,:focus-within),
body:has([data-motion-enabled="off"]) button:active {transform:none;}
@media(prefers-reduced-motion:reduce) {* {animation:none!important;transition:none!important;} [class*="st-key-task_entry_"]:is(:hover,:focus-within),button:active {transform:none!important;}}
"""

_SOFT_UI = """
/* Cute stationery surfaces, with a realistic bird instead of a cartoon face. */
:root {--canvas:#fffaf8;--mint:#fff6e4;--peach:#fff0f3;--lilac:#eef6fc;--line:#ebded8;--shadow:#8e625912;}
.stApp {background-image:radial-gradient(#dbb8b32b .8px,transparent .8px);background-size:24px 24px;}
.brand-mark {border-radius:50%;background:#f4f8fc;border:1px solid #dfebf3;box-shadow:0 4px 12px #93adbe19;}
.st-key-main_nav {border-radius:24px;background:#ffffffed;box-shadow:0 4px 15px var(--shadow);}
.st-key-main_nav label[data-testid="stRadioOption"] {border-radius:17px;}
.st-key-main_nav label:has(input:checked) {background:#fff3df;border-color:#e7d4b6;box-shadow:0 2px 0 #e8d6bb;}
.st-key-guide_search_panel {background:linear-gradient(125deg,#fffbf3,#ffffff 58%,#fff4f7);border-color:#ecdeda;border-radius:30px;box-shadow:0 7px 24px var(--shadow);}
.st-key-guide_search_panel::before {height:6px;background:linear-gradient(90deg,#f4c3c9 0% 34%,#f2dca7 34% 67%,#c5dfef 67%);}
.hero-companion {flex-basis:240px;background:linear-gradient(155deg,#edf7fc,#f8fbfe);border:5px solid #fff;border-radius:44% 48% 45% 42%;box-shadow:0 4px 16px #9ab7c41c;padding:.1rem;}
.hero-library-note {display:inline-block;background:#fff8e9;border:1px solid #ecdcbf;border-radius:14px;padding:.35rem .65rem;}
[class*="st-key-task_entry_"] {border-radius:24px;box-shadow:0 4px 13px var(--shadow)!important;}
.st-key-task_entries [data-testid="stColumn"]:nth-child(1) [class*="st-key-task_entry_"] {border-color:#eadbc0;}
.st-key-task_entries [data-testid="stColumn"]:nth-child(2) [class*="st-key-task_entry_"] {border-color:#edced7;}
.st-key-task_entries [data-testid="stColumn"]:nth-child(3) [class*="st-key-task_entry_"] {border-color:#cee1ed;}
.task-art {border-radius:16px;background:#fffdfc;border:1px solid #ffffff;box-shadow:0 3px 0 #d3b7a521;}
[class*="st-key-topic_cover_"] {border-radius:24px;background:#fffefd;}
.topic-art {border-radius:18px;box-shadow:0 3px 0 #d3b7a521;}
.st-key-guide_directory [data-testid="stExpander"] {border-radius:16px;background:#fffbf8;border-color:#eee1da;}
.guide-verdict,.action-brief,.scenario-answer,.event-verdict,.st-key-route_notes {border-radius:22px;box-shadow:0 3px 12px var(--shadow);}
.st-key-profile_editor,.st-key-onboarding,.st-key-route_toolbar {border-radius:24px;}
.guide-table th {background:#fff5e2;}.guide-table tbody tr:nth-child(even) {background:#fffbf6;}
.workflow-strip,.st-key-profile_nav {border-radius:20px;}
[data-testid="stButton"] button,[data-testid="stFormSubmitButton"] button,[data-testid="stPopover"] button,[data-testid="stLinkButton"] a {border-radius:15px;}
[data-testid="stTextInputRootElement"],[data-testid="stTextAreaRootElement"] {border-radius:15px;}
@media(max-width:760px) {
 .st-key-main_nav {border-radius:22px;}
 .st-key-guide_search_panel {padding:1.15rem .9rem 1rem;border-radius:27px;}
 .hero-companion {flex-basis:136px;border-width:3px;}
 .guide-hero-title {font-size:1.65rem!important;}
 .hero-library-note {display:block;padding:.3rem .5rem;line-height:1.65;font-size:.875rem;}
 [class*="st-key-task_entry_"] {border-radius:23px;padding:.85rem 1rem;}
 .task-art {border-radius:15px;}
}
@media(max-width:380px) {
 .hero-companion {flex-basis:104px;}
 .guide-hero-title {font-size:1.45rem!important;}
 .hero-library-note span {padding:0 .1rem;}
}
"""

_ROADMAP = """
.st-key-cross_system_roadmap {margin:1.4rem 0;padding:1.25rem;background:#fffefd;border:1px solid var(--line);border-radius:24px;}
.roadmap-heading {font-size:1.2rem!important;margin:0 0 .4rem!important;}
.roadmap-after {padding:.8rem 1rem;background:#edf7fc;border-radius:14px;line-height:1.7;overflow-wrap:anywhere;}
.roadmap-row {display:flex;align-items:flex-start;gap:.8rem;padding:.65rem 0;border-bottom:1px solid var(--line);}
.roadmap-rank {flex:0 0 32px;background:#fff5e2;color:var(--accent-deep);border-radius:10px;text-align:center;padding:.3rem 0;font-weight:750;}
.roadmap-line {display:flex;flex-wrap:wrap;gap:.5rem;align-items:center;}
.roadmap-line span {font-size:.875rem;color:var(--muted);border:1px solid var(--line);border-radius:8px;padding:.1rem .4rem;}
.roadmap-row p {margin:.2rem 0!important;font-size:.95rem;line-height:1.5;overflow-wrap:anywhere;}
.roadmap-row small {color:var(--muted);font-size:.875rem;overflow-wrap:anywhere;}
.roadmap-missing {font-size:.9rem;color:var(--muted);margin-top:1rem!important;}
.decision-because {font-size:.9rem;color:var(--muted);line-height:1.7;margin:.8rem 0!important;}
.decision-because b {display:block;color:var(--ink);}
.smart-hold {background:#fff5e2;border:1px solid #ecdcbf;border-radius:14px;padding:.8rem 1rem;font-size:.9rem;line-height:1.7;}
.st-key-smart_next_question {padding:1rem 1.25rem;border:1px solid var(--line);background:#edf7fc;border-radius:22px;margin-bottom:1rem;}
.st-key-smart_next_question h3 {font-size:1rem!important;}.st-key-smart_next_question p {font-size:.9rem;}
@media(max-width:760px) {
 .st-key-cross_system_roadmap {padding:1rem .85rem;}
 .st-key-cross_system_roadmap [data-testid="stHorizontalBlock"] {flex-wrap:nowrap!important;gap:.65rem!important;}
 .st-key-cross_system_roadmap [data-testid="stColumn"] {min-width:0!important;}
 .st-key-cross_system_roadmap [data-testid="stHorizontalBlock"]:has(.roadmap-row) [data-testid="stColumn"]:last-child {flex:0 0 76px!important;}
 .roadmap-row {gap:.5rem;}.roadmap-rank {flex-basis:27px;}
}
"""

_PRO_GUIDE = """
/* A compact editorial desk: information leads, illustration stays decorative. */
.library-strip {display:flex;align-items:center;flex-wrap:wrap;gap:.5rem 1.5rem;padding:.8rem 1rem;margin:.15rem 0 .9rem;border:1px solid var(--line);border-radius:14px;background:#fffefd;color:var(--muted);font-size:.875rem;font-variant-numeric:tabular-nums;}
.library-strip b {color:var(--ink);font-weight:750;margin-right:.25rem;}
.st-key-quick_queries {padding:.15rem 0 .6rem;}
.st-key-quick_queries [data-testid="stButton"] button {background:#fffaf2;border:1px solid #e8d8c0;min-height:44px;font-size:.875rem;}
.st-key-quick_queries [data-testid="stButton"] button p {font-size:.875rem;line-height:1.4;}
.st-key-featured_guides {margin-bottom:.9rem;}
[class*="st-key-feature_"] {border:1px solid var(--line);border-top:3px solid #b6d2df;border-radius:20px;background:#fffefd;padding:1rem 1.1rem;height:100%;}
[class*="st-key-feature_"]:nth-child(2) {border-top-color:#edc98a;}
.feature-label {display:flex;justify-content:space-between;gap:.4rem;color:var(--accent);font-size:.875rem;font-weight:650;}
.feature-label span {color:var(--muted);font-weight:400;font-variant-numeric:tabular-nums;}
[class*="st-key-feature_"] button p {font-size:1.1rem!important;font-weight:750!important;line-height:1.5!important;}
[class*="st-key-feature_"] [data-testid="stCaptionContainer"] {min-height:2.6rem;}
.feature-points {margin:.15rem 0 0;padding-left:1.2rem;}
[data-testid="stMarkdownContainer"] .feature-points li {font-size:.875rem;line-height:1.65;color:var(--muted);}
.st-key-guide_directory [class*="st-key-directory_"] {padding:.4rem 0 .75rem;border-bottom:1px solid #eee6de;margin-bottom:.15rem;}
.st-key-guide_directory [class*="st-key-directory_"] button p {font-size:1rem;line-height:1.5;font-weight:700;}
.st-key-guide_directory [data-testid="stExpander"] {margin-top:.5rem;box-shadow:none;border-color:#eee6de;}
.article-dateline {display:flex;flex-wrap:wrap;gap:.5rem;font-size:.875rem;margin:.4rem 0 1rem;color:var(--muted);}
.article-dateline span {background:#fff6e7;padding:.3rem .65rem;border-radius:9px;}
.article-keypoints {padding:1rem 1.25rem;border:1px solid #d5e3eb;border-radius:18px;background:#f3f9fc;margin:.75rem 0;}
.article-keypoints h2 {font-size:1rem!important;margin:0 0 .5rem!important;}
.article-keypoints ul {margin:0;padding-left:1.2rem;}
.article-keypoints li {font-weight:600;}
.article-operating {display:grid;grid-template-columns:1fr;gap:0;border:1px solid var(--line);border-radius:18px;background:#fffdf9;margin:1rem 0;overflow:hidden;}
.article-operating > div {padding:.8rem 1rem;display:grid;grid-template-columns:5rem 1fr;gap:.5rem;align-items:start;}
.article-operating > div + div {border-top:1px solid var(--line);}
.article-operating span {font-size:.875rem;color:var(--accent);font-weight:700;line-height:1.75;}
.article-operating p {margin:0!important;font-size:.9375rem!important;line-height:1.75!important;}
[class*="st-key-article_part_"] {margin:1rem 0 .3rem;padding:0;}
.article-section {scroll-margin-top:1.5rem;font-size:1.3rem!important;border-bottom:1px solid var(--line);padding-bottom:.7rem;margin-top:1.4rem!important;}
.article-anchor {scroll-margin-top:1.5rem;}
.article-section .section-number {font-size:.875rem;color:var(--accent);background:#fff4df;padding:.25rem .4rem;border-radius:7px;margin-right:.35rem;vertical-align:middle;}
.article-section [data-testid="stHeaderActionElements"] {display:none;}
.article-steps {padding-left:1.5rem;margin:.5rem 0 1rem;}
.article-steps li {margin:.6rem 0;padding-left:.2rem;}
.article-steps li::marker {color:var(--accent);font-weight:750;}
.st-key-article_rail {position:sticky;top:1.25rem;border:1px solid var(--line);border-radius:18px;background:#fffdf8;padding:1rem;}
.article-toc a {line-height:1.6;padding:.6rem .2rem;border-bottom:1px solid #eee6de;min-height:44px;}
.guide-verdict {border-left:4px solid #c89450;box-shadow:none;}
.guide-table th {font-weight:750;}.guide-table td {vertical-align:top;}
@media(max-width:760px) {
 .library-strip {gap:.5rem .8rem;padding:.65rem .75rem;}
 .library-strip span:last-child {flex-basis:100%;}
 .st-key-quick_queries [data-testid="stHorizontalBlock"] {flex-wrap:nowrap!important;gap:.4rem!important;}
 .st-key-quick_queries [data-testid="stColumn"] {min-width:0!important;}
 .st-key-quick_queries button {padding:.4rem .25rem!important;}
 [class*="st-key-feature_"] {padding:.9rem 1rem;border-radius:17px;}
 [class*="st-key-feature_"] [data-testid="stCaptionContainer"] {min-height:0;}
 .article-operating > div {grid-template-columns:1fr;gap:.25rem;padding:.75rem;}
 .article-keypoints {padding:.85rem 1rem;}
 .article-section {font-size:1.15rem!important;}
 .article-dateline span:last-child {flex-basis:100%;}
}
"""

STYLE = STYLE.replace("</style>", _FIELD_GUIDE + _NAV_ART + _MOTION_GUIDE + _SOFT_UI + _ROADMAP + _PRO_GUIDE + "\n</style>")
