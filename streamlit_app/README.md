# 升級決策版

Streamlit entry point: `streamlit_app/app.py`. Deploy using the existing GitHub
`main` branch connected to Streamlit Community Cloud. The `.openai` manifest at
the repository root belongs to the separate earlier Sites build; this Python
application is not a Cloudflare Worker.

## Primary flow

1. 下一步: a three-field initial profile, then a single primary recommendation.
2. 我的帳號: edit one system at a time; saving returns to the recalculated result.
3. Confirm an upgrade already completed in the game to update the local record.
   Resource balances and per-slot price quotes are invalidated after spending.
4. Export/import JSON for subsequent sessions; no cross-user or server-file
   profile persistence is used. Refreshing or disconnecting can reset the session.

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
- Milestones are rule-based advice for the recorded fields, not a full-account
  mathematical optimum. High-end six-slot gear comparisons require the linked
  scenario calculator. Legacy loadouts are labelled as dated references.
- Do not add unsupported fixed spending orders or present percentage modifiers
  as equivalent percentage increases in total damage.

Run tests from the repository root with an environment containing Streamlit and
pytest: `python -m pytest streamlit_app -q -p no:cacheprovider`.
