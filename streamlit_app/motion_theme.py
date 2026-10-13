"""The shared sky stage, topic controls, and quiet article bookmark.

Append ``MOTION_STYLE`` after the base theme. All motion is decorative CSS;
the native Streamlit radio remains the only topic-selection control.
"""

MOTION_STYLE = r"""
/* One sky, one topic state: the scene and controls form a single guide desk. */
.st-key-guide_search_panel {
  padding:1.4rem 1.55rem 1.15rem;
  background:#fffefd;
  border:1px solid #e8dfd6;
  border-radius:28px;
  box-shadow:0 8px 24px #9877660b;
}
.st-key-guide_search_panel::before {
  height:4px;
  background:linear-gradient(90deg,#e8c490,#d9eaf1 55%,#ead9d4);
}
.flight-scene,.article-flight-bookmark,.st-key-guide_search_panel {
  --scene-sky:#edf7fc;
  --scene-ground:#f5ead6;
  --scene-tint:#f6f1e7;
  --scene-line:#d7c8ab;
  --scene-ink:#735334;
}
:is(.flight-scene,.article-flight-bookmark)[data-flight-topic="profile"],.st-key-guide_search_panel:has(.flight-scene[data-flight-topic="profile"]) {
  --scene-sky:#fff5e8;--scene-ground:#f4dfbc;--scene-tint:#fff4e4;
  --scene-line:#dcc4a0;--scene-ink:#8b5939;
}
:is(.flight-scene,.article-flight-bookmark)[data-flight-topic="gear"],.st-key-guide_search_panel:has(.flight-scene[data-flight-topic="gear"]) {
  --scene-sky:#edf5fc;--scene-ground:#dce8f1;--scene-tint:#edf5fb;
  --scene-line:#b8cddf;--scene-ink:#4b6984;
}
:is(.flight-scene,.article-flight-bookmark)[data-flight-topic="collection"],.st-key-guide_search_panel:has(.flight-scene[data-flight-topic="collection"]) {
  --scene-sky:#f6f1fb;--scene-ground:#e9dff1;--scene-tint:#f6effa;
  --scene-line:#d2bfdf;--scene-ink:#786088;
}
:is(.flight-scene,.article-flight-bookmark)[data-flight-topic="tech"],.st-key-guide_search_panel:has(.flight-scene[data-flight-topic="tech"]) {
  --scene-sky:#eff9f7;--scene-ground:#dcece5;--scene-tint:#edf7f4;
  --scene-line:#b6d5cb;--scene-ink:#416b62;
}
:is(.flight-scene,.article-flight-bookmark)[data-flight-topic="event"],.st-key-guide_search_panel:has(.flight-scene[data-flight-topic="event"]) {
  --scene-sky:#fff2f2;--scene-ground:#f4dddd;--scene-tint:#fff1f1;
  --scene-line:#e4bfc3;--scene-ink:#8b5963;
}
:is(.flight-scene,.article-flight-bookmark)[data-flight-topic="pet"],.st-key-guide_search_panel:has(.flight-scene[data-flight-topic="pet"]) {
  --scene-sky:#f3f8ec;--scene-ground:#e4eccd;--scene-tint:#f4f8ed;
  --scene-line:#c4d3a7;--scene-ink:#5b6e40;
}
:is(.flight-scene,.article-flight-bookmark)[data-flight-topic="mount"],.st-key-guide_search_panel:has(.flight-scene[data-flight-topic="mount"]) {
  --scene-sky:#f9f4ec;--scene-ground:#eadbc5;--scene-tint:#faf2e7;
  --scene-line:#d9c6a7;--scene-ink:#88694a;
}
.flight-scene-heading {padding:0 .15rem .8rem;}
.flight-scene-heading [data-testid="stHeaderActionElements"] {display:none;}
.flight-scene-heading .guide-hero-title {
  font-size:clamp(1.8rem,3vw,2.4rem)!important;
  line-height:1.4!important;
  margin:0 0 .3rem!important;
}
[data-testid="stMarkdownContainer"] .scene-deck {
  color:var(--muted);font-size:.9375rem;line-height:1.65;margin:0!important;
}
.flight-panorama {
  --bird-size:190px;
  --flight-distance:calc(100cqw - var(--bird-size) - 32px);
  container-type:inline-size;
  position:relative;isolation:isolate;overflow:hidden;
  width:100%;height:250px;
  border:1px solid #ffffff;border-radius:23px;
  background:linear-gradient(180deg,var(--scene-sky),#fffdfb 98%);
  pointer-events:none;
}
.flight-panorama::before {
  content:"";position:absolute;z-index:0;
  width:125%;height:68px;left:-12%;bottom:-40px;
  background:var(--scene-ground);border-radius:50% 50% 0 0;
  opacity:.8;
}
.flight-panorama::after {
  content:"";position:absolute;z-index:0;
  width:56%;height:46px;right:-8%;bottom:-32px;
  background:var(--scene-tint);border-radius:50% 50% 0 0;
}
.scene-sun {
  position:absolute;z-index:0;top:23px;right:8%;
  width:52px;height:52px;border-radius:50%;
  background:#ffefd0;box-shadow:0 0 0 12px #fff5e345;
}
.scene-cloud {
  position:absolute;z-index:1;
  width:96px;height:22px;background:#fffffff0;
  border-radius:40px;filter:drop-shadow(0 2px 0 #dbe7ee30);
}
.scene-cloud::before,.scene-cloud::after {
  content:"";position:absolute;bottom:6px;background:inherit;border-radius:50%;
}
.scene-cloud::before {left:17px;width:35px;height:35px;}
.scene-cloud::after {right:15px;width:27px;height:27px;}
.scene-cloud.cloud-a {left:12%;top:49px;}
.scene-cloud.cloud-b {left:64%;top:37px;width:119px;opacity:.8;}
.scene-cloud.cloud-c {left:37%;top:146px;width:66px;height:17px;opacity:.68;}
.scene-cloud.cloud-c::before {width:24px;height:24px;left:11px;bottom:4px;}
.scene-cloud.cloud-c::after {width:20px;height:20px;right:10px;bottom:4px;}
.scene-wind {
  position:absolute;z-index:1;width:40px;height:17px;
  border-top:2px solid var(--scene-line);border-radius:50%;opacity:.48;
}
.scene-wind::after {
  content:"";position:absolute;top:6px;left:10px;width:22px;
  border-top:2px solid var(--scene-line);border-radius:50%;
}
.scene-wind.wind-a {left:22%;top:114px;}
.scene-wind.wind-b {right:18%;top:169px;width:31px;opacity:.3;}
.scene-route {
  position:absolute;z-index:1;left:5%;bottom:18px;
  width:90%;height:72px;overflow:visible;opacity:.62;
}
.scene-route path {
  stroke:var(--scene-line);stroke-width:1.7;
  stroke-dasharray:3 7;stroke-linecap:round;fill:none;
  vector-effect:non-scaling-stroke;
}
.scene-route circle {fill:var(--scene-line);opacity:.7;}
.scene-station {
  position:absolute;z-index:2;left:50%;bottom:16px;
  width:70px;height:51px;transform:translateX(-50%);
  display:flex;align-items:center;justify-content:center;
}
.scene-station .station-bg {
  position:absolute;z-index:-1;inset:7px 0 0;
  background:#fffefce8;border:1px solid var(--scene-line);
  border-radius:50%;box-shadow:0 4px 0 #d8c8ad21;
}
.scene-station > svg {
  position:relative;width:45px;height:45px;
  filter:drop-shadow(0 3px 0 #e2d5c43a);
}
.flight-bird {
  --hover-rise:-7px;
  position:absolute;z-index:3;left:16px;
  top:calc(50% - var(--bird-size) * .4);
  width:var(--bird-size);height:auto;
  transform:translate3d(0,3px,0);
  pointer-events:none;
}
.flight-bird > svg {
  display:block;width:100%;height:auto;overflow:visible;
  pointer-events:none;
}
.flight-bird .kite-flight,.flight-bird .kite-direction {
  transform-box:view-box;transform-origin:120px 98px;
}
/* Override the old small-badge route without changing the original bird art. */
body:has([data-motion-enabled="on"]) .flight-bird .kite-flight {
  animation:scene-hover 2.8s ease-in-out infinite;
}
body:has([data-motion-enabled="on"]) .flight-bird .kite-direction {
  animation:scene-facing 14s ease-in-out infinite;
}
body:has([data-motion-enabled="on"]) .flight-bird {
  animation:scene-cruise 14s ease-in-out infinite;
}
body:has([data-motion-enabled="on"]) .scene-cloud.cloud-a {
  animation:scene-cloud-drift 20s ease-in-out infinite;
}
body:has([data-motion-enabled="on"]) .scene-cloud.cloud-b {
  animation:scene-cloud-drift 27s ease-in-out -9s infinite reverse;
}
body:has([data-motion-enabled="on"]) .scene-cloud.cloud-c {
  animation:scene-cloud-drift 23s ease-in-out -5s infinite;
}
body:has([data-motion-enabled="on"]) .scene-wind {
  animation:scene-breeze 5.8s ease-in-out infinite;
}
body:has([data-motion-enabled="on"]) .scene-wind.wind-b {animation-delay:-3s;}
body:has([data-motion-enabled="on"]) .scene-route path {
  animation:scene-route-flow 16s linear infinite;
}
body:has([data-motion-enabled="on"]) .scene-route circle {
  animation:scene-route-glint 4s ease-in-out infinite;
}
body:has([data-motion-enabled="on"]) .scene-station > svg {
  animation:scene-station-arrive .45s ease-out both;
}
.flight-caption {
  display:flex;align-items:center;gap:.8rem;
  padding:.9rem .2rem .45rem;min-width:0;
}
.flight-topic-icon {
  display:flex;align-items:center;justify-content:center;flex:0 0 44px;
  height:44px;background:var(--scene-tint);
  border:1px solid var(--scene-line);border-radius:15px;
}
.flight-topic-icon svg {display:block;width:31px;height:31px;}
.flight-topic-copy {min-width:0;flex:1;}
.flight-topic-copy h2 {
  margin:0 0 .15rem!important;padding:0!important;
  font-size:1.06rem!important;line-height:1.5!important;color:var(--scene-ink);
}
[data-testid="stMarkdownContainer"] .flight-topic-copy p {
  margin:0!important;font-size:.875rem;line-height:1.6;color:var(--muted);
}
.flight-count {
  flex:0 0 auto;font-size:.875rem;color:var(--muted);
  border:1px solid #e7dfd6;background:#fffefa;
  border-radius:10px;padding:.3rem .5rem;white-space:nowrap;
}
/* A native radio keeps keyboard selection and labels; no positional icons. */
.st-key-flight_topics {margin:.1rem 0 .35rem;}
.st-key-flight_topics [data-testid="stWidgetLabel"] {margin-bottom:.4rem;}
.st-key-flight_topics [role="radiogroup"] {
  display:flex!important;flex-wrap:wrap!important;
  gap:.45rem!important;width:100%;align-items:stretch;
}
.st-key-flight_topics label[data-testid="stRadioOption"] {
  display:flex;align-items:center;justify-content:center;
  margin:0!important;padding:.52rem .8rem!important;
  min-height:44px;gap:0!important;
  background:#fffefd;border:1px solid #e7ddd2;
  border-radius:14px;box-shadow:none;cursor:pointer;
  transition:background-color .18s,border-color .18s,box-shadow .18s;
}
.st-key-flight_topics label[data-testid="stRadioOption"] div:not([data-testid]):not(:has([data-testid="stMarkdownContainer"])):not(:has(input)) {
  display:none;
}
.st-key-flight_topics label[data-testid="stRadioOption"] p {
  font-size:.9375rem!important;line-height:1.4!important;
  white-space:nowrap;color:var(--ink);margin:0!important;
}
.st-key-flight_topics label[data-testid="stRadioOption"]:hover {
  background:#fbf6ec;border-color:#d7c5ab;
}
.st-key-flight_topics label[data-testid="stRadioOption"]:has(input:checked) {
  background:var(--scene-tint);border-color:var(--scene-line);
  box-shadow:0 2px 0 #e8d6b6;
}
.st-key-flight_topics label[data-testid="stRadioOption"]:has(input:checked) p {
  font-weight:700!important;color:var(--scene-ink);
}
.st-key-flight_topics label[data-testid="stRadioOption"]:has(input:focus-visible) {
  outline:3px solid #88a9c6;outline-offset:3px;
}
body:has([data-motion-enabled="on"]) .st-key-flight_topics label:has(input:checked) {
  animation:scene-topic-settle .3s ease-out;
}
.st-key-guide_search_results,.st-key-flight_topic_preview {min-width:0;}
body:has([data-motion-enabled="on"]) :is(.st-key-guide_search_results,.st-key-flight_topic_preview) {
  animation:scene-panel-arrive .25s ease-out;
}
/* A small shared bookmark connects reading to the selected topic, not a player. */
.article-flight-bookmark {
  display:flex;align-items:center;gap:.8rem;min-height:68px;
  padding:.4rem .9rem;margin:.4rem 0 .75rem;
  border:1px solid #e8ded2;border-radius:18px;
  background:linear-gradient(100deg,var(--scene-sky),#fffefd 75%);
  overflow:hidden;
}
.bookmark-bird {
  --hover-rise:-3px;
  display:block;flex:0 0 64px;width:64px;height:53px;
  border-radius:14px;pointer-events:none;
}
.bookmark-bird svg {display:block;width:100%;height:auto;pointer-events:none;}
body:has([data-motion-enabled="on"]) .bookmark-bird .kite-flight {
  animation:scene-hover 3.8s ease-in-out infinite;
}
.article-flight-bookmark .bookmark-bird .kite-direction {
  animation:none!important;transform:none;
}
.bookmark-copy {display:flex;align-items:center;gap:.55rem;min-width:0;}
.bookmark-copy svg {display:block;width:25px;height:25px;flex-shrink:0;}
.bookmark-copy :is(p,span,strong) {
  margin:0!important;color:var(--scene-ink);font-size:.9375rem;line-height:1.6;
}
@keyframes scene-cruise {
  0%,100% {transform:translate3d(0,3px,0);}
  23% {transform:translate3d(calc(var(--flight-distance) * .5),-8px,0);}
  46%,50% {transform:translate3d(var(--flight-distance),1px,0);}
  73% {transform:translate3d(calc(var(--flight-distance) * .5),-5px,0);}
  96% {transform:translate3d(0,2px,0);}
}
@keyframes scene-facing {
  0%,44%,100% {transform:scaleX(1);}
  48%,94% {transform:scaleX(-1);}
  98% {transform:scaleX(1);}
}
@keyframes scene-hover {
  0%,100% {transform:translateY(0) rotate(-1deg);}
  50% {transform:translateY(var(--hover-rise,-5px)) rotate(1deg);}
}
@keyframes scene-cloud-drift {
  0%,100% {transform:translateX(-10px);}
  50% {transform:translateX(15px);}
}
@keyframes scene-breeze {
  0%,100% {transform:translateX(0);opacity:.22;}
  50% {transform:translateX(9px);opacity:.48;}
}
@keyframes scene-route-flow {to {stroke-dashoffset:-60;}}
@keyframes scene-route-glint {0%,100% {opacity:.3;}50% {opacity:.8;}}
@keyframes scene-station-arrive {
  from {transform:translateY(5px) scale(.95);opacity:.5;}
  to {transform:translateY(0) scale(1);opacity:1;}
}
@keyframes scene-topic-settle {
  0%,100% {transform:translateY(0);}
  55% {transform:translateY(-2px);}
}
@keyframes scene-panel-arrive {
  from {transform:translateY(3px);}
  to {transform:translateY(0);}
}
@supports not (width:1cqw) {
  /* Older browsers get a centered hovering bird, never an off-canvas route. */
  .flight-bird {left:calc(50% - var(--bird-size) / 2);}
  body:has([data-motion-enabled="on"]) .flight-bird,
  body:has([data-motion-enabled="on"]) .flight-bird .kite-direction {
    animation:none;transform:none;
  }
}
@media(max-width:760px) {
  .st-key-guide_search_panel {padding:1.1rem .9rem .9rem;border-radius:25px;}
  .flight-scene-heading {padding-bottom:.65rem;}
  .flight-scene-heading .guide-hero-title {font-size:1.7rem!important;}
  [data-testid="stMarkdownContainer"] .scene-deck {font-size:.875rem;}
  .flight-panorama {--bird-size:120px;height:182px;border-radius:19px;}
  .scene-sun {width:37px;height:37px;top:19px;right:11%;box-shadow:0 0 0 8px #fff5e345;}
  .scene-cloud.cloud-a {left:7%;top:39px;width:72px;height:18px;}
  .scene-cloud.cloud-b {left:60%;top:32px;width:81px;height:18px;}
  .scene-cloud::before {width:27px;height:27px;left:11px;bottom:4px;}
  .scene-cloud::after {width:21px;height:21px;right:10px;bottom:4px;}
  .scene-cloud.cloud-c {left:39%;top:113px;width:54px;height:15px;opacity:.48;}
  .scene-cloud.cloud-c::before {width:19px;height:19px;}
  .scene-cloud.cloud-c::after {width:15px;height:15px;}
  .scene-wind.wind-a {top:91px;left:13%;width:28px;}
  .scene-wind.wind-b {top:133px;right:14%;width:24px;}
  .scene-route {height:51px;bottom:15px;}
  .scene-station {width:57px;height:43px;bottom:12px;}
  .scene-station > svg {width:36px;height:36px;}
  .flight-caption {gap:.6rem;padding:.75rem .1rem .3rem;}
  .flight-topic-icon {flex-basis:38px;height:38px;border-radius:12px;}
  .flight-topic-icon svg {width:28px;height:28px;}
  .flight-topic-copy h2 {font-size:1rem!important;}
  .flight-topic-copy p {overflow-wrap:anywhere;}
  .flight-count {padding:.25rem .35rem;font-size:.875rem;}
  .st-key-flight_topics [role="radiogroup"] {display:grid!important;grid-template-columns:repeat(4,minmax(0,1fr));gap:.4rem!important;}
  .st-key-flight_topics label[data-testid="stRadioOption"] {padding:.48rem .3rem!important;width:100%;min-width:0;}
  .st-key-flight_topics label[data-testid="stRadioOption"] p {font-size:.875rem!important;}
  .article-flight-bookmark {gap:.55rem;min-height:64px;padding:.3rem .65rem;}
  .bookmark-bird {flex-basis:58px;width:58px;height:48px;}
}
@media(max-width:380px) {
  .flight-panorama {--bird-size:116px;height:174px;}
  .flight-scene-heading .guide-hero-title {font-size:1.55rem!important;}
  .flight-caption {flex-wrap:nowrap;}
  .flight-topic-copy {flex:1;}
  .flight-count {margin-left:0;padding:.2rem .25rem;}
  .st-key-flight_topics label[data-testid="stRadioOption"] {padding:.45rem .5rem!important;}
}
@media(max-width:480px) {
  .st-key-main_nav [role="radiogroup"] {grid-template-columns:repeat(5,minmax(0,1fr));}
  .st-key-main_nav label[data-testid="stRadioOption"] {padding:.45rem .1rem;}
  .st-key-main_nav label[data-testid="stRadioOption"] p {white-space:normal;max-width:2.3em;text-align:center;line-height:1.35;}
}
/* Last rules win over the existing animated badge and all interaction motion. */
body:has([data-motion-enabled="off"]) *,
body:has([data-motion-enabled="off"]) *::before,
body:has([data-motion-enabled="off"]) *::after {
  animation:none!important;transition:none!important;
}
@media(prefers-reduced-motion:reduce) {
  *,*::before,*::after {animation:none!important;transition:none!important;scroll-behavior:auto!important;}
  .flight-bird {left:calc(50% - var(--bird-size) / 2);transform:none!important;}
  .flight-bird .kite-flight,.flight-bird .kite-direction,
  .bookmark-bird .kite-flight,.bookmark-bird .kite-direction {transform:none!important;}
  .st-key-flight_topics label {transform:none!important;}
}
"""
