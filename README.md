# muninn-utilities

Muninn-flavored Python utilities, packaged for boot-time materialization into
`~/muninn_utils/` at the start of every Muninn session.

These started as `utility-code` memories in Turso, materialized to disk by
the `remembering` skill's `install_utilities()`. Per memory `0d63ed4f`,
source-of-truth has moved from Turso to files: each utility lives in this
repo, gets a flowing-graph refactor where applicable, and ships with tests.

## Layout

```
muninn-utilities/
├── muninn_utils/              # Importable Python package
│   ├── __init__.py
│   ├── blog_publish.py        # publish_and_announce — page → wait → feed; bsky detached
│   ├── bsky_card.py           # compose_link_post — fetch_og + facets → blob → embed → post
│   ├── issue_close.py         # github-procedures §7 (close + capture LEARNING)
│   └── tests/
└── README.md
```

## How it gets to a session

Two paths, both pointed at this repo:

1. **Claude Code on the Web** — `boot-ccotw.sh` in
   [`oaustegard/claude-workspace`](https://github.com/oaustegard/claude-workspace)
   tarballs this repo and copies `muninn_utils/` into `$HOME/muninn_utils/`.
2. **Claude.ai (`remembering.boot()`)** — the `remembering` skill in
   [`oaustegard/claude-skills`](https://github.com/oaustegard/claude-skills)
   does the same fetch from inside Python, after `install_utilities()`.

Both run after `install_utilities()` so disk files override any Turso
materialization for utilities migrated here. Utilities still living in
Turso `utility-code` memories continue to work via the materialization
fallback.

The repo is **public** so the fetch needs no `GH_TOKEN`.

## Adding a utility

1. Land it as `muninn_utils/<name>.py` with a flowing-graph orchestrator
   (see existing utilities for the pattern: `validate=`, `retry_until=`,
   `detached=True`, parallel layers via `depends_on=`)
2. Add tests under `muninn_utils/tests/test_<name>_flow.py` covering
   topology, validate gates, retry budget, and detached-failure isolation
3. Open a PR. Once merged, the next session boot in any environment
   pulls the new file automatically — no Turso edit required.

## Tests

```
python3 -m pytest muninn_utils/tests/
```

Tests resolve the `flowing` skill from `/mnt/skills/user/flowing` (canonical
install) with fallback to a sibling `claude-skills` clone, so they run both
inside a Muninn session and from a plain checkout.

## Background

- [memory `0d63ed4f`](https://github.com/oaustegard/claude-skills) — migration tracker
- [`oaustegard/muninn.austegard.com#124`](https://github.com/oaustegard/muninn.austegard.com/pull/124) — first batch of three (initially landed in mac, since moved here)
- [`oaustegard/claude-workspace#55`](https://github.com/oaustegard/claude-workspace/pull/55) — CCotw boot fetch
- [`oaustegard/claude-skills#625`](https://github.com/oaustegard/claude-skills/pull/625) — Claude.ai boot fetch
