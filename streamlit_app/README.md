# 升級決策版

Streamlit entry point: `streamlit_app/app.py`. Deploy using the existing GitHub
`main` branch connected to Streamlit Community Cloud. The `.openai` manifest at
the repository root belongs to the separate earlier Sites build; this Python
application is not a Cloudflare Worker.

## Primary flow

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
