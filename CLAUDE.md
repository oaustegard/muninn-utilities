# CLAUDE.md — muninn-utilities

Source-of-truth for everything Muninn-flavored that runs in a session:
the **memory subsystem** (`remembering/`, Turso-backed, FTS5, decision
traces, autonomous curation) and a **Python utility package**
(`muninn_utils/`, ~14 modules: blog/Bluesky publishing, GitHub issue
closure, reminders, perch triage, diff vetting, KB dedup).

Both used to live elsewhere — `remembering/` in `oaustegard/claude-skills`
as a generic skill, `muninn_utils/*` as Turso `utility-code` memories
materialized at boot. Both became Muninn-specific in practice. This
repo is their dedicated home; `claude-skills` carries a deprecated
mirror kept fresh by a sync workflow for marketplace continuity.

## Context Roadmap

Top-level layout:

| Path | Purpose |
|---|---|
| `remembering/` | Memory subsystem. Skill-shaped (`SKILL.md`, `scripts/`, `references/`, `tests/`) so it can mount as `/mnt/skills/user/remembering/`. |
| `muninn_utils/` | Python package, ~14 modules. Fetched from this repo's tarball at boot, written to `~/muninn_utils/`, importable as `muninn_utils.<module>`. |
| `manifests/` | One install-manifest v0.3 JSON per tool (`tool-id/muninn-<tool-id>.v0.3.json` + `REVOKE.md`). Discoverable via `.well-known/tools.json`. |
| `scripts/` | Build automation. `build-tools-index.py` walks `manifests/` and emits the tools-index. |
| `README.md` | Bootstrapping order, layout, claude-skills mirror deprecation note. |
| `LICENSE` | MIT. |

Read first:
1. `README.md` — boot order, why both halves live here, the deprecated-mirror story.
2. `remembering/SKILL.md` — public API surface for memory ops; the `metadata.version` here gates every commit.
3. `remembering/references/CLAUDE.md` — version-bump mandate, Turso auth, retry pattern, handoff workflow.
4. `muninn_utils/use_when.json` — one-line decision matrix for each utility ("when do I reach for `bsky_limit` vs `bsky_card`?"). Faster than reading source.

## Context Understanding

**`remembering/` is skill-shaped on purpose.** It exposes a public API (`remember`, `recall`, `supersede`, `weaken`, `strengthen`, `prune_by_age`, `decision_trace`, `config_get/set`, `task`, `boot`, …) callable from any session. Turso is the durable backend; an HTTP wrapper in `scripts/turso.py` handles the egress-proxy quirks of CCotw.

**`muninn_utils/` is a flat Python package**, not a skill. Each module is one "tool" — small enough to read end-to-end, focused on one external surface. Boot fetches this repo as a tarball and unpacks `muninn_utils/*.py` into `~/muninn_utils/`, then puts the parent on `sys.path` via the boot's `python_paths` step. Import as `from muninn_utils import blog_publish`.

**The two halves are coupled at boot.** `boot()` (in `remembering/scripts/boot.py`) is the single entry point: load profile + ops + recent memories from Turso (one ~150ms HTTP round trip), detect GitHub capability, write `.muninn/.env` after successful init. Boot also calls `fetch_muninn_utils()` (in `remembering/scripts/utilities.py`) which pulls this repo's tarball and lays down `muninn_utils/*` for the session.

**The deprecated mirror in `claude-skills/remembering/` exists for marketplace continuity.** The hub's boot (`claude-workspace/boot-ccotw.sh`) fetches `claude-skills` first, then overlays `muninn-utilities/remembering/` on top — the canonical version wins. If you're debugging behavior, check this repo's `remembering/`, not the mirror.

## Domain Constants

**Current `remembering/` version:** `5.12.0` (`remembering/SKILL.md` frontmatter `metadata.version`). **Every commit must bump this** — non-negotiable per `references/CLAUDE.md`. Forgetting it means no release fires.

**Module count under `muninn_utils/`:** 14, plus `flowing.py` re-export and `use_when.json`. Tests live in `muninn_utils/tests/`.

| Module | Purpose |
|---|---|
| `blog_publish.py` | Publish HTML page → GitHub Pages, optional Atom feed entry, optional Bluesky announce. Encoded as a `flowing` DAG; bsky chain is detached so its failures never abort the publish. |
| `bsky_card.py` | Post a link to Bluesky with a proper OGP card preview. |
| `bsky_limit.py` | Enforce Bluesky's 300-**grapheme** limit. `fits()` uses the `grapheme` library — `len()` lies on emoji + combining marks. |
| `flowing.py` | Re-export of canonical `/mnt/skills/user/flowing/scripts/flowing.py`. Single source of truth; prevents `.pth` shadowing. |
| `issue_close.py` | Close a GitHub issue + store a behavioral synthesis memory; optional `pending` test tag for the next session. |
| `memory_tfidf.py` | TF-IDF duplicate detection, structural pattern matching, cross-domain dedup. Used by `therapy` Phase 1/2. |
| `news_watch.py` | Parse `claude.com/blog` for new posts; watermarked state in Turso config. Delegates HTTP to the model's `web_fetch` (WAF blocks raw requests). |
| `perch_publish.py` | Publish flight-log discussions to muninn.austegard.com's `perch/` section. |
| `perch_triage.py` | Dream review, morning check-in, flight-log processing. |
| `remind.py` | Schedule/query/manage future reminders. State in Turso config. |
| `task_policy.py` | Load live ops entry + recent preference memories for perch tasks (zeitgeist/fly/sleep/dispatch). Single source of truth for task behavior. |
| `verify_patch.py` | Create PRs, conduct code review, vet handoff specs, validate diffs. |
| `whtwnd.py` | Publish to WhiteWind (ATProto blog): `whtwnd_auth/post/update/delete/list/upload_image`. |
| `zeitgeist_delta.py` | Near-identical story detection before memory storage. Prevents running-story bloat (Iran/Hormuz, Norway F-16s as canonical examples). |

**Manifest convention** (per tool, under `manifests/<tool-id>/`):
- Filename: `muninn-<tool-id>.v0.3.json` (must start with `tool.id` or `build-tools-index.py` aborts).
- Sibling: `REVOKE.md` with kill-switch instructions.
- Tool versions track `tool.version` per manifest (currently `0.1.0` across the board); manifest format itself is pinned at `v0.3`.

**Turso retry budget** (`remembering/scripts/turso.py::_retry_with_backoff`): 5 retries, 0.5s base delay, exponential backoff with jitter. Catches 503, 429, SSL handshake failures, JSON decode failures, egress-proxy "DNS cache overflow" 503s. Boot loosened the budget in v5.8.0 for egress-proxy cold start.

**Memory types required on every write** (per `SKILL.md`): `decision`, `world`, `anomaly`, `experience`, `procedure`, `analysis`. Procedure memories auto-default to `confidence=0.9, priority=1` so they survive pruning.

**Credentials lookup order** (`remembering/scripts/turso.py`): env vars → `turso.env` → `muninn.env` → `~/.muninn/.env` → legacy `/mnt/project/turso-token.txt` → default URL. After successful init, credentials persist to `~/.muninn/.env` (v5.8.0).

## Parsing Schema

**Install-manifest v0.3 shape** (one per tool under `manifests/<tool-id>/`):

```json
{
  "manifest_version": "0.3",
  "tool": {
    "id": "muninn-<tool-id>",
    "version": "0.1.0",
    "name": "...", "summary": "...", "description": "...",
    "tags": ["publishing", "github-pages", "flowing"]
  },
  "runtime": {
    "kind": "python-module",
    "install": { "method": "git" },
    "entrypoint": { "command": ["python", "-m", "muninn_utils.<module>"] }
  },
  "env": [
    { "name": "GH_TOKEN", "secret": true, "required": true, "validate": "^gh[ps]_.+", "obtain_url": "..." }
  ],
  "scopes": [
    { "kind": "github.repo.contents", "rationale": "..." }
  ],
  "actions": [
    { "name": "publish", "input_schema": {...}, "output_schema": {...}, "side_effects": [...], "idempotent": false }
  ],
  "data_boundary": { "reads": [...], "transmits": [...], "persists": [...] },
  "smoke": [{ "shell": "..." }],
  "kill_switch": { "manual": "...", "see": "REVOKE.md" }
}
```

**`use_when.json` shape** (`muninn_utils/use_when.json`): one entry per module, the value is a single sentence describing when to reach for it. This is the routing table; reading it is faster than scanning sources.

**Tools-index output** (`scripts/build-tools-index.py` emits `.well-known/tools.json`): `{ "schema_version": "muninn-tools-index/v1", "tools": [<manifest summaries>] }`. Discoverable by external agents.

**`remembering/scripts/` module layout** (~11.4k LOC across the whole repo):

```
remembering/scripts/
├── __init__.py        public API exports
├── boot.py            session init, loads profile + ops + recent memories
├── memory.py          remember/recall/supersede/weaken/strengthen/prune_by_age
├── turso.py           HTTP client + _retry_with_backoff
├── task.py            task definition + scheduling
├── audit.py           memory audits
├── aliases.py         @accept_aliases decorator with DeprecationWarning
├── config.py          config_get/set/delete (ops + profile access)
├── bootstrap.py       session bootstrap helpers
├── hints.py           proactive memory hints (recall_hints)
├── utilities.py       fetch_muninn_utils() — public tarball pull
├── result.py          MemoryResult, MemoryWriteId, type-safe returns
├── state.py           track failed background writes; failed_writes(), retry_failed_writes()
├── spokes.py          constellation support
├── defaults/          ops.json (~24k), profile.json
├── tasks/             zeitgeist.md, fly.md, sleep.md, dispatch.md, anthropic_news.md
└── migrations/        Turso schema migrations
```

## Error Patterns

**Bump `metadata.version` in `remembering/SKILL.md` on every commit.** No exceptions. The release workflow keys off it; forgetting the bump means no release fires and downstream consumers (claude-skills mirror, hub boot overlay) keep serving the old version. See `references/CLAUDE.md`.

**Manifest filename must start with `tool.id`.** `manifests/blog-publish/muninn-blog-publish.v0.3.json` works; renaming the JSON without renaming `tool.id` (or vice versa) makes `build-tools-index.py` abort. Filename and `tool.id` are coupled.

**Memory writes can fail silently in detached side-effects.** `issue_close`, `blog_publish`, and other flowing-DAG modules route bsky/memory writes through detached edges. Failures land in `flow.detached_failures` (and `failed_writes()` for background memory writes), never aborting the main flow. Call `retry_failed_writes()` to drain; check `state.failed_writes()` for visibility.

**`bsky_limit.fits()`, not `len()`.** Bluesky counts graphemes. Emoji and combining marks are multi-byte; `len("🤦‍♀️")` is 5, but it's one grapheme. `fits()` uses the `grapheme` library. `bsky_limit.py` auto-installs `grapheme` on first import if missing.

**`flowing.py` is a re-export, not a re-implementation.** It pulls from `/mnt/skills/user/flowing/scripts/flowing.py` to keep one source of truth. Tests stub it because muninn_utils tests run from this monorepo where the skill isn't mounted.

**`claude.com/blog` WAF blocks raw HTTP** (403 on `/blog`, `/feed.xml`, `/rss.xml`). `news_watch.py` delegates the fetch to the model's `web_fetch` tool rather than calling directly. If a similar new-source comes online, plan for the same delegation.

**`supersede()` inherits priority from the original** (v5.12.0 fix). Earlier versions silently downgraded to default — a foot-gun that caused important memories to get pruned after supersession.

**Alias-layer DeprecationWarnings are real signals.** `@accept_aliases` translates deprecated kwarg names with a warning; `MemoryResult` field access via `.[content]` warns instead of silently translating. If a warning fires in routine usage, the calling code needs an update, not a suppression.

**No live Turso/GitHub credentials in tests.** `remembering/tests/test_hardening.py` and `muninn_utils/tests/test_*_flow.py` mock both. If a test reaches for the network, it's a bug in the test.

**Cross-test dependency:** muninn_utils tests live in this monorepo but the skill `flowing` is only mounted under `/mnt/skills/user/flowing/` in real sessions. Tests stub `flowing` to decouple. Don't import the real one in test setup.

## Reusable Results

**Boot is one HTTP round trip.** `boot()` loads profile + ops + recent memories + GitHub capability detection in ~150ms. The capabilities block tells the session what tooling is reachable; consume it instead of probing.

**Dual-table design.**
- `config` table: stable (profile + ops + journal), small, mostly static, fast at startup.
- `memories` table: timestamped observations, unbounded, queried as needed.

**Task policy is the routing layer for autonomous work.** `task_policy.load(name)` returns the live ops entry + the last few preference memories + the last run record. Perch tasks (zeitgeist/fly/sleep/dispatch) read this instead of hardcoding behavior — change the ops entry to change the policy, no code change needed.

**Decision traces are how the two wings learn.** After meaningful work, call:

```python
remember(
    "Closed #NNN: [what was learned]. Key decision: [rationale]. "
    "Constraint: [if any]. Future note: [what next session needs to know].",
    "decision",
    tags=["issue-NNN", "relevant-tags"],
    priority=1,  # 1=significant, 0=routine
)
```

Lead with *why*. The diff shows *what*.

**Eleven utilities live here, not Turso.** Migrated per memory `0d63ed4f`. `flowing` remains in Turso as a thin re-export wrapper over `/mnt/skills/user/flowing/`, but everything else (`blog_publish`, `bsky_card`, `bsky_limit`, `issue_close`, `memory_tfidf`, `perch_publish`, `perch_triage`, `remind`, `verify_patch`, `whtwnd`, `zeitgeist_delta`) is here. `news_watch` and `task_policy` are newer additions that never lived in Turso.

**Test entry points:**
- `pytest muninn_utils/tests/` — module flow tests.
- `python3 remembering/tests/test_hardening.py` — memory subsystem hardening.

Both mock Turso and GitHub; no credentials needed to run.

**Where to read next if you only have time for three files:**
- `remembering/SKILL.md` — public API + the version-bump rule.
- `remembering/scripts/turso.py` — `_retry_with_backoff`, the 503-survival pattern that informed `proxy-503-retry-pattern` ops.
- `muninn_utils/use_when.json` — the routing table for everything in the utility package.
