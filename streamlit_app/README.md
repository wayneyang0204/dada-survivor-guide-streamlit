# 攻略網站與升級工具

Streamlit entry point: `streamlit_app/app.py`. Deploy using the existing GitHub
`main` branch connected to Streamlit Community Cloud. The `.openai` manifest at
the repository root belongs to the separate earlier Sites build; this Python
application is not a Cloudflare Worker.

## Guide website

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
  controls. `ui_art.py` contains the decorative sprout guide-buddy SVG; it needs
  no downloaded images, external fonts or new dependencies. Text and status
  colors retain their contrast, and reduced-motion settings disable hover motion.
- Home offers three task entries (upgrade planning, event budgeting, collectible
  lookup), then a collapsed directory by system. Search replaces the directory
  with a matching answer and table facts; it does not mix browsing and results.
  Historical source summaries remain separately grouped in search and the index.
- Visible navigation uses task names (升級路線、我的配置、活動試算、攻略索引).
  Internal page IDs remain stable for saved session state and article return paths.
- Event results survive reruns within a session, but are hidden when the selected
  event or any calculator input changes. Recalculation never shows a stale result.
- The same search also looks up local collectible names, aliases and IDs. Those
  hits are explicitly catalog metadata, not fabricated star effects or advice.
- Set-member lists, linkage comparisons and crit-overflow guidance include their
  source dates. Article tables remain expanded; explanatory prose and FAQs fold.
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

- Original, decorative SVG mascot and icons are in `ui_art.py`; no remote images,
  font downloads or third-party scripts are needed. They are not game assets.
- `ui_theme.py` is the single stylesheet for home, planner, profile, activity and
  article routes. Pale mint, peach and lavender surfaces retain dark text.
- Home topic shelves show actual article counts and remain collapsed until a
  deliberate choice. Responsive row stacking preserves category reading order.
- The five native radio routes remain keyboard accessible. Phone navigation uses
  five columns, with a three-column fallback below 380 px; no sideways menu.
- Contrast checks cover all five reading surfaces. App tests also cover original
  artwork, real counts, topic order and warm-cache reload of the shared artwork.
  Automated checks do not replace rendered desktop and phone inspection.
