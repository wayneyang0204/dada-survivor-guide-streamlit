# 攻略網站與升級工具

Streamlit entry point: `streamlit_app/app.py`. Deploy using the existing GitHub
`main` branch connected to Streamlit Community Cloud. The `.openai` manifest at
the repository root belongs to the separate earlier Sites build; this Python
application is not a Cloudflare Worker.

## Guide website

- 2026-10-28 adaptive intake: players can start without a character, or add one
  observation at a time directly below their current recommendation. Weapon E,
  drone form, Taloxa R, relevant collection stars, pet type/skills and Umbral
  awakening are explicit selections. Each answer reranks immediately; inventory
  is optional until a material-gap calculation is needed. Dependent questions
  stay together, known fields are not reasked, and skipped answers remain unknown.
  The latest answer can be undone until another profile update occurs. Pausing a
  main survivor now leads directly into these questions and has an inline resume.
- An optional `hall_can_fill` observation finds a free placement without asking
  for three counts. Exact/partial counts that disprove space or spare collections
  take precedence. Completion records only that no immediately fillable slot
  remains, clears the unknown placement count, and spends nothing. Changes to
  hall counts invalidate this observation. Old schema-1 backups remain valid.
  This intake exposes existing documented rules; it does not infer unknown
  stock, add unsupported pet breakpoints, or claim a global damage optimum.

- 2026-10-28 task-first flow: the home screen starts with three direct entries
  (next upgrade, selector boxes, current activity). Search/categories remain in
  place; question answers have no automatic selection, and updates/the full
  directory are opt-in expansions. The existing flying red kite uses a shorter
  stage, retains native controls and respects reduced motion.
- First-time planning offers click-only character/R-level selectors or a separate
  paste tab. No character or R-level is preselected. The main card includes the
  game entry, target and shortages; its material form is one popover away and is
  never duplicated in the detailed comparison. Choosing another comparison moves
  the active form there; a return-to-priority action restores the global target.
  Completion/undo, unknown inventory handling and backup formats are unchanged.

- 2026-10-23 flow repairs: search accepts Chinese star numerals, spaced R/E/V
  notation and common question wording while retaining unknown terms. A category
  mismatch offers an explicit all-category search, including catalog-only hits;
  clearing a query keeps the current category. Expanded results retain matching
  table facts. Article roundtrips keep the broadened search context.
- The main priority button resets prior resource/comparison filters before opening
  detail. Twin-tech hints carry the exact part and recorded energy into the tool;
  only explicitly recorded twin forms seed values. Each part/reading has its own
  scenario and effect confirmation, and simulations never change account records.

- 2026-10-22 priority/phase update: the saved planner promotes one engine-ranked
  action, shows its unmet conditions, and previews the following action only for
  an already-ready node. Other candidates and source notes remain available in
  deliberate expansions. The summary button opens the matching material detail
  without changing account data or recording game completion.
  If no engine action remains, a supplied twin-tech form/energy can expose the
  nearest listed energy breakpoint as an unverified hint, never an affordable
  upgrade or DPS ranking. Ordinary tech does not inherit twin-tech effects.
- One-line intake now accepts ordinary-hall counts (opened, owned, placed) and
  validates the merged configuration before offering Apply. It can find free
  placements without asking for stock or a full manual profile.
- `activity_status.py` distinguishes scheduled play, exchange-only, expired and
  unverified windows. Current answers, featured cards, articles and the activity
  screen share these phases. Outside the play window, budgeting requires explicit
  hypothetical/history mode and acknowledgement. Event links preserve the chosen
  activity on later reruns; progress and ticket prices never transfer between
  different event periods. Time Jigsaw exchange uses the dated community table;
  the next Beach Treasure card confirms its schedule and mechanics, not a cost or
  milestone table. Official card windows are not presented as observed openings.

- 2026-10-18 low-input update: home and first-time planner offer six question
  playbooks with three concrete actions, stopping rules and article links, without
  requiring an account. A bounded local parser recognises one-line current-state
  notes; it previews recognised fields before an explicit save. Goals, negations,
  conflicts, secrets and invalid numeric ranges cannot be applied. Unrecognised
  text is visible, never guessed. It does not call AI, OCR, or the game.
- One-line updates merge only recognised fields. Retargeting a main survivor or
  gear milestone clears obsolete recipe confirmations; pet scope invalidation
  still applies. Ordinary/twin technology is explicit, not inferred from energy.
  Schema-1 backups support the extra optional fields and old backups still load.
- Saved configurations first show relevant source-based milestone notes and
  known gaps, with material forms/detail ranking collapsed. The original manual
  role form is opt-in; targeted profile editors and completion checks remain.
  This brief is conditional guidance, not a claim of an affordable global optimum.
- SS E/V recipes now have per-stage and interval totals for cores, material
  equipment, faction stones and base materials. Another-path prerequisites are
  separate. The dated 2025 community recipe does not stand in for live game
  previews, Chaos or Starforge costs. New Time Jigsaw coverage separates the
  700/850/1000 milestones, chest retrieval, key costs and random rewards. Its
  community schedule is never labelled official, and expires automatically.
- Activity pages now show operations before a zero-default-input calculator
  toggle. Blank prices, stock and progress are still unknown; the original seven
  budget inputs are available only when the player asks to calculate.

- 2026-10-13 motion/navigation update: the homepage combines a panoramic sky,
  automatic red-kite cruise, native topic choices and the filtered guide shelf.
  Topic selection changes the scene colour, station icon, article count and shelf
  together, without changing player data or auto-opening an article. Mobile topic
  choices use a compact four-by-two grid. Articles keep a small matching topic
  bookmark; returning restores the originating category/search. Decorations never
  take pointer input, and OS reduced-motion disables animation without disabling
  navigation. No animation picker, practice widget or new external asset is used.
- 2026-10-11 editorial expansion: 36 local articles, 75 tables and 48 FAQs.
  `field_content.py` adds dated operating guides for newer survivors, synergy,
  ordinary/xeno pets, vehicles, regional action, specific SS skills and events.
  Each new article states a game entry, stopping point and what to compare next.
  Community mechanisms, official schedules and our own methods are labelled
  separately. An undated official event card is not assigned a fake publication date.
- Articles begin with three concrete points and the operating/stopping checklist.
  Body text and tables remain visible; only FAQs and secondary directory entries
  fold. Homepage has quick questions, three timely articles and two visible entries
  per system. Expired scheduled events leave the featured shelf automatically.
- `field_tools.py` provides bounded Elaine second-pet caps, reserve-module stat
  arithmetic, guild-coin ticket budgets and descriptive A/B medians. They never modify a profile or call the
  game. Published event windows are timezone-aware; an active schedule is not
  represented as a personally observed game opening.
- The planner has a selected Umbral Soul yellow-4/red-5 route. It requires current
  awakening, in-game effect confirmation and the full remaining recipe. This is
  not a full pet tier list, a remaining-cost table, or a global damage optimum.
  Changing a saved pet target clears the previous target's material confirmation.
  Completing a node also clears readiness for the next one; character cores are
  not deducted for pet upgrades. The completion confirmation surface remounts
  when account/target changes, so it closes rather than inviting a second click
  on the next target. Old schema-1 backups remain readable.
- Event budgeting renders from the local dated roster, without waiting for a
  third-party feed. Unconfirmed progress, price and stock fields start blank and
  block calculation until entered; zeros are explicit inputs, not missing data.
  Archived events require an explicit history/reprint acknowledgement. Tide Haven
  uses its own guild-coin budget, never the gemstone reserve/value formula; it does
  not predict the random gems found per ticket or promise a guild milestone.
  Live editorial browsing remains under the latest-articles view.
- The planner shows a visible cross-system execution queue, one leading milestone
  per system, plus a pure preview of what follows after the displayed milestone.
  A main-survivor stage goal pauses further main upgrades when reached, without
  hiding unfinished synergy milestones. Resource filters do not hide the global queue.
- Pet configuration participates in sequencing. Manual paid nodes/effects and
  all full recipe readiness are player-confirmed from the game, not fabricated meta
  rankings. Unknown/panel-only effects stay outside the spending queue. Historical
  pet sources are explicitly marked as no longer updated. Completion clears the
  old pet goal/readiness, and never consumes character cores for a pet upgrade.
- Smart sequencing checks effects before spending: early Memory Editor crit
  nodes require a mode-scoped usefulness confirmation (including overflow),
  and the boots set requires an enabled Ice Armor skill. Inapplicable goals are
  shown as deferred, not silently dropped or ranked as affordable upgrades.
- Players can identify survival or slow skill formation as their current issue.
  Survival diagnoses precede paid damage; the existing E1 milestone is promoted
  for slow formation. Free owned adjustments still come first. These are bounded
  decision rules, not an ML model or proof of a global DPS optimum.
- Only two ready, identical +10% crit-damage milestones compare player-confirmed
  full box recipes. Different effects, unknown prices and ties retain normal
  milestone ordering. Panel gains are explicitly outside that cost comparison.
- The next-question panel asks one decision-changing prerequisite before more
  stock, without duplicating the active milestone form. Evidence labels distinguish
  player-confirmed inputs and community rules from unmeasured account damage.

- New visitors open `攻略首頁`, not an account form. Home and the guide index
  read a local, source-labelled catalog and remain usable without source APIs.
- Cornerstone articles have conclusions, conditions, tables, cautions,
  FAQs, source dates and related reading. Existing summaries are explicitly
  labelled as references awaiting re-verification, not newly verified guides.
- `?guide=<stable-slug>` addresses each article without any account data in the
  URL. Invalid slugs only perform a local lookup and offer an index return.
- Category and full-text search share `guide_content.py`. `guide_ui.py` owns
  reading views and connects articles to the appropriate planner resource.
- Common Chinese questions and collectible aliases are normalized for search;
  title and summary matches rank before incidental body mentions. Epic
  collectibles have their own answer instead of using legendary-box rules.
- Articles preserve the originating search and category through related
  reading. Scenario selectors display costs and stopping points without
  changing account records; the planner remains the account-editing surface.
- In-app navigation preserves session profiles. Reloading a direct article
  link starts a new session as usual; article links are not profile backups.
- The shared white/ink theme is `ui_theme.py`. Existing reference feeds,
  collectible catalog, event calculator, and profile editor remain available.
- The cute visual layer uses a cream-white canvas, pastel task cards and rounded
  controls. `ui_art.py` embeds a local cartoon red-kite WebP cutout with the
  vector UI icons; no external images, fonts or new dependencies are needed. Text and status
  colors retain their contrast, and reduced-motion settings disable hover motion.
- Home offers three task entries (upgrade planning, event budgeting, collectible
  lookup), featured reading and a browsable directory by system. Search replaces
  these sections with up to three visible answers and table facts.
  Historical source summaries remain separately grouped in search and the index.
- Visible navigation uses task names (升級路線、我的配置、活動試算、攻略索引).
  Internal page IDs remain stable for saved session state and article return paths.
- Event results survive reruns within a session, but are hidden when the selected
  event or any calculator input changes. Recalculation never shows a stale result.
- The same search also looks up local collectible names, aliases and IDs. Those
  hits are explicitly catalog metadata, not fabricated star effects or advice.
- Set-member lists, linkage comparisons and crit-overflow guidance include their
  source dates. Article tables and explanatory prose remain expanded; FAQs fold.
- `direction_content.py` adds an upgrade roadmap, selector-box decision tree and
  resonance planning guide. Editorial methods are not labelled as newly verified
  meta rankings. The resonance references remain explicitly dated and do not
  transfer ordinary-drone thresholds to twinborn or lightning parts.
- `direction_tools.py` generates a concise next action from the current step's
  material ledger, retaining every shortage and unknown condition. Its resonance
  calculator takes a player-supplied in-game target; blanks stay unknown, no fixed
  box/chip costs or damage gains are invented, and it never changes the profile.
- Every supported planner route now has a game entry and three conditional
  operating steps, including exact missing set members. These instructions do
  not bypass readiness checks or cause game actions.
- `tech_routes.py` contains selected, source-dated twinborn drone/lightning
  effect milestones. The article can calculate the next listed skill effect,
  separately from generic stat thresholds. It requires an exact twinborn shape
  and keeps source verification distinct from permission/readiness to spend.
- Cloud startup refreshes direction/tech leaf modules before importing UI
  consumers; a warm-cache regression removes new symbols to reproduce old
  cached helpers meeting a newly deployed interface.

## Planner flow

1. 下一步: a three-field initial profile, then a single primary recommendation.
2. 我的帳號: edit one system at a time; saving returns to the recalculated result.
3. Confirm an upgrade already completed in the game to update the local record.
   Known costs are deducted from known stock and explicitly labelled as inferred
   balances, not live game data. Unknown or inconsistent stock becomes unknown.
   Per-slot price quotes and next-target material confirmations are invalidated.
4. Export/import JSON for subsequent sessions; no cross-user or server-file
   profile persistence is used. Refreshing or disconnecting can reset the session.
   Restore is available on the first screen; backup is available on the result.
5. Check the current target's materials directly on the result screen. Variable
   recipes are explicitly player-confirmed, never fabricated from box count alone.
6. A completion can be undone until the next profile edit. This changes the guide
   record only; no game account is accessed and no game resources are spent.

`next_step.py` contains independent, evidence-labelled milestone rules.
`decision_ui.py` renders the profile and recommendations. The older broad
diagnosis/optimizer functions remain in `data_engine.py` for compatibility but
are not exposed as competing personalized recommendations.

## Recommendation contract

- Unknown is `None`, never zero. Actual zero is an explicit player input.
- Material checks retain each known shortage and each unknown requirement.
  A known shortage takes precedence over unknown details in the headline state;
  it must never disappear because a different material was not entered.
- A user-confirmed zero requirement is distinct from an unknown requirement:
  that resource need not have known stock to satisfy a zero-cost target.
- Incomplete advanced-star positions are missing data, not zero-star holdings.
  The app asks for the star data before opening the material-price form.
- Material-ready actions precede saving goals, then unverified candidates.
- Resource categories are independent, not converted into an invented DPS score.
- General and advanced collector hearts are separate resources.
- Advanced slots require both unlocked slots and legendary star thresholds.
  An eight-slot, 79-star set must never claim the 80-star BOSS milestone.
- Eight red-five-star legendary collectibles mean 80 stars; eight yellow-five
  collectibles mean 40. Assignment order is entered by the player. A collectible
  cannot be duplicated across sets; identities are not automatically validated.
- Per-slot advanced prices apply only to their explicitly selected slot.
- Active advanced bonuses use the total stars in all advanced positions, not an
  arbitrary prefix for each tier. Planned, non-advanced positions are not counted.
  Rearranging already owned collectibles within a set can be a zero-cost action.
- Variable recipes are keyed to the exact target, current milestone, character
  and mode. A recipe for yellow five cannot leak into a red-three recommendation.
  Confirmed spending clears relevant recipe confirmations. Known stock can carry
  forward as a labelled estimate; editing a balance confirms that field only.
- Completion previews use the current recommendation, validate its target and
  update, and never accept a stale milestone. Completion buttons are also bound
  to the exact profile/target so the next awakening has a different widget key.
- SS boots use an entire-set yellow-three target. The recipe covers all missing
  members and completion updates the whole set without lowering any higher star.
  A partial real-game upgrade must be entered as actual stars in the profile.
- Ranking explanations compare actual candidate readiness. A lone candidate
  must not be described as a proven global optimum.
- Memory Editor and Dark Matter Construct routes continue through supported
  yellow-three, yellow-five, red-three and red-five breakpoints; their equipment
  conditions and modifier-vs-total-damage limits remain explicit.
- Milestones are rule-based advice for the recorded fields, not a full-account
  mathematical optimum. High-end six-slot gear comparisons require the linked
  scenario calculator. Legacy loadouts are labelled as dated references.
- Do not add unsupported fixed spending orders or present percentage modifiers
  as equivalent percentage increases in total damage.

Run tests from the repository root with an environment containing Streamlit and
pytest: `python -m pytest streamlit_app -q -p no:cacheprovider`.

## Illustrated field-guide UI

- The cartoon red-kite mascot is AI-generated artwork in `assets/`, retaining
  the previous reference's colors and forked tail, but using a large round eye,
  round head and simplified feathers instead of realistic bird proportions.
  It is a 960px transparent WebP, not a documentary wildlife photo.
  Its prompt and provenance are saved beside it. `ui_art.py` embeds it locally
  alongside original vector icons; no external images/fonts/scripts are needed.
- `ui_theme.py` is the single stylesheet for home, planner, profile, activity and
  article routes. Cream-white, caramel, peach and pale-sky surfaces retain dark
  text. The nest/sky surfaces keep the legacy mint/lilac token names for compatibility.
- Home topic shelves show actual article counts and remain collapsed until a
  deliberate choice. Responsive row stacking preserves category reading order.
- The five native radio routes remain keyboard accessible. Phone navigation uses
  five columns, with a three-column fallback below 380 px; no sideways menu.
- Contrast checks cover all five reading surfaces. App tests also cover original
  artwork, real counts, topic order and warm-cache reload of the shared artwork.
  Automated checks do not replace rendered desktop and phone inspection.
- The illustrated red kite glides left and right within the home sky scene and
  turns at each end. Its pose is not bent by fake wing/eye animations. The small header mascot
  hovers inside its badge. There is no animation chooser or playback control;
  old session preferences are ignored, and OS reduced-motion stops all animation.
- Motion stays in decorative SVG groups inside the illustration, not reading text
  or buttons; no practice quiz or sample-material playground is displayed.
- Cute UI styling uses cream, blush-peach and pale-sky stationery cards, rounded
  icon tiles, small colored shadows and a subtle dotted canvas. All native flows
  and reading/status contrast requirements are retained.
