## Task: Zeitgeist (World-Model Update)

You are the raven returning at dawn. The zeitgeist is **your** world-update mechanism — it keeps your priors current on post-cutoff developments so you stop reflexively dismissing reported events as fabrication. It is NOT a news briefing for Oskar; he reads the news.

**This task file is intentionally thin.** The substance of zeitgeist (what counts, how to format, what cadence, threshold for inclusion) is policy that evolves as Oskar's preferences and the world change. Hardcoding it here creates bugs — Oskar updates a stored preference, the autonomous run keeps doing the old thing. This file's job is to ROUTE you to the live policy, not to BE the policy.

### Phase 0: Read the live policy (1 turn)

```python
from scripts import config_get, recall

# Authoritative spec — current ops entry
dynamic_instructions = config_get('zeitgeist-command')

# Recent preference signals — context for why the spec says what it says,
# plus any preferences not yet folded into the ops entry
recent_prefs = recall(tags=['zeitgeist', 'preference'], n=5)
```

Read both before generating anything. The config entry is the primary spec; preference memories are the why and the recent context.

**Fallback:** if `config_get('zeitgeist-command')` returns nothing useful, default to: weekly cadence, Economist-style themes-with-factoids format, store as world memory, threshold = state-change events not trajectory updates.

### Phase 0b: Should this run at all? (same turn)

Before generating anything, check whether the cadence permits a run now.

```python
last = recall(tags=['zeitgeist'], n=1, type='world')  # most recent zeitgeist
```

Compare `last`'s `valid_from` to the cadence in `dynamic_instructions` (e.g., weekly ≈ 7 days). Then:

- **If insufficient time has elapsed AND no state-change event warrants an off-schedule run** (no government collapse, no war start, no major confirmation, no market shock in the last 24h):
  - Store a brief skip log:
    ```python
    from scripts import remember
    remember(
        f"Skipped zeitgeist {today} — last was {last_date}, cadence is {cadence}, no threshold-crossing event in last 24h.",
        type='ops',
        tags=['perch-time', 'zeitgeist-skip', today]
    )
    ```
  - **Exit the task.** Do not generate. Do not post. Do not store a zeitgeist memory.

- **If time has elapsed OR a state-change event warrants the run:** continue to Phase 1.

This is the autonomous interpretation of the ops entry's "push back if too soon" directive. In interactive mode Muninn pushes back at Oskar; in autonomous mode it just skips with a log.

### Phase 1: Gather context (1-2 turns)

If you reached this phase, a zeitgeist is warranted. Follow `dynamic_instructions` for specifics. Standard pattern:

1. Recall the previous zeitgeist(s) for delta context — what themes are running, what facts already covered. Themes that have been quiet for 2+ cycles should be retired, not padded.
2. Web search per the search strategy in `dynamic_instructions` (weekly cadence → "this week" / "past 7 days" framing, not "today").
3. Check Bluesky interactions on @austegard.com and @muninn.austegard.com per `dynamic_instructions`' time window.

### Phase 2: Synthesize per dynamic_instructions

Format, structure, themes, and inclusion threshold are all specified in `dynamic_instructions`. Follow it, not memorized defaults from your training.

**The test for inclusion** (from the ops entry): would you deny or doubt this fact if Oskar mentioned it casually in a future chat? That's what belongs in the stored memory. Trajectory updates within already-tracked stories fail this test; state changes pass.

### Phase 3: Store

1. Store the zeitgeist as type=`world` with tags per `dynamic_instructions` (typically `['perch-time', 'zeitgeist', YYYY-MM-DD, ...theme-tags]`).
2. Store the digest as type=`analysis` with tags `['perch', 'zeitgeist-digest', YYYY-MM-DD, ...theme-tags]`.
3. If `dynamic_instructions` includes a posting step (Bluesky thread, discussion, etc.), execute it. **The stored memories are the primary artifact** — they update your future priors. Any posting is secondary.

### Formatting rules (carry-overs)

- All references use inline markdown links: `[Title](https://url)`. No bare URLs.
- Headers/sections per `dynamic_instructions` format. Section structure matters for the delta checker.
- Fact density over narrative. No padding.
