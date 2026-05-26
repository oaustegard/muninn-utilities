# snapshot

Build a static snapshot of Muninn for use in another Claude.ai project. Pulls
config and memories from the live Turso DB, filters out personal-project
scope, redacts residual references, clusters surviving memories by topic
tag, and writes a `PROJECT_INSTRUCTION.md` + `knowledge_base/*.md` set ready
to upload to a Claude.ai project.

## Why this exists

Muninn's earned experience lives in Turso (config keys + memories) and gets
composed into a boot output every session. The boot wires up storage/recall
APIs, hub-spoke GitHub routing, the Cloudflare+Gemini sub-agent gateway,
personal-project triggers (mac, bsky, strava), and other infrastructure
specific to the live instance.

A snapshot replica in a different Claude.ai project has none of that
substrate — no Turso, no env files, no constellation, no sub-agent gateway.
What it does have is Claude.ai's native memory (nightly summaries) and
project knowledge files (RAG-indexed). The snapshot maps Muninn's
durable past onto those two surfaces:

- **Project instruction** = filtered + lightly-rewritten boot output.
  Loads every turn. Carries voice, values, tensions, universal craft
  triggers, operating discipline.
- **Project knowledge base** = surviving memories clustered by topic tag.
  Loaded on demand via project search.

See the discussion in [conversation thread / PR description] for the design.

## Usage

```python
from snapshot import build_snapshot
result = build_snapshot(out_dir="/home/claude/snapshot-out")
print(result["stats"])
```

Or from CLI:

```bash
python3 -m snapshot.build --out /home/claude/snapshot-out
```

Output structure:

```
/home/claude/snapshot-out/
  PROJECT_INSTRUCTION.md    # upload to project custom instructions
  knowledge_base/
    INDEX.md                # human-readable cluster index
    agents.md               # one .md per cluster
    paper-insight.md
    anthropic.md
    ...
    _misc.md                # memories with no clusterable home
  manifest.json             # build metadata + cluster list
  snapshot.zip              # everything above, ready to upload
```

## What gets filtered

The snapshot drops three categories of content:

1. **Turso-dependent ops** — anything that references `remember()`, `recall()`,
   `config_get()`, `task()`, `deliver()`, the recall vocabulary, refs
   semantics, the egress proxy retry pattern, etc. The destination uses
   Claude.ai's native memory instead.

2. **Personal-project scope** — austegard.com, muninn.austegard.com, aeyu.io,
   Bluesky channels, Strava, Norwegian politics, the perch/fly publishing
   mechanics, the hub-spoke GitHub workflow, CCotw handoffs, the
   muninns-inbox routine.

3. **Hard-drop tokens in bodies** — credentials, email addresses, JWT-shaped
   strings, GitHub PATs, `muninn-utilities` / `claude-workspace` references.
   Memories containing any of these are dropped entirely rather than
   sentence-redacted.

What survives is the substantive intellectual content: papers read, syntheses
made, calibrations earned, AI-research notes, methodology decisions. The
universal craft triggers (skill-authoring, procedure-authoring,
backend-impl, cross-frame-retrieval) stay in the instruction since the
destination has the matching skills available via `claude-skills`.

## How clustering works

Each surviving memory gets a primary tag chosen from its tags:

1. Skip meta tags (dates, PR/issue numbers, generic descriptors like
   `correction`/`preference`/`analysis`).
2. Canonicalize via `TAG_ALIASES` (e.g. `agentic`, `ai-agents`,
   `agent-architecture` all → `agents`).
3. Pick the highest-frequency candidate in the surviving corpus.
4. If the resulting cluster would be a singleton, fall back to the
   next-highest-frequency candidate whose cluster has ≥2 members.
5. If no candidate has a real cluster home, the memory lands in `_misc`.

Cluster files exceeding 50 memories get split chronologically into
`{tag}-1.md`, `{tag}-2.md`, etc.

## Extending the filters

All the static data lives in `config.py`:

- `PROFILE_KEEP` / `OPS_KEEP` — config keys that survive into the instruction
- `TAG_EXCLUDE` / `TAG_EXCLUDE_PATTERNS` — tags that drop a whole memory
- `TAG_ALIASES` — tag canonicalization
- `TAG_META` / `TAG_META_PATTERNS` — tags that can't be primary cluster names
- `HARD_DROP_PATTERNS` — regex hits on body that drop the whole memory
- `REDACT_TOKENS` / `REDACT_TOKEN_PATTERNS` — sentence-level redaction
- `LINE_DROP_PATTERNS` — drop whole lines (Turso-storage idioms)
- `INSTRUCTION_PREAMBLE_TEMPLATE` / `INSTRUCTION_FOOTER_TEMPLATE` — the
  dual-memory framing wrapper around the composed boot output

Per-entry rewrites (e.g. `boot-behavior` → "static snapshot — no per-session
boot") live in `compose_instruction.py:_REWRITES`.

## Updating an existing snapshot

The build is idempotent: every run regenerates the entire output directory
from scratch. To update an existing destination project:

1. Run `python3 -m snapshot.build`
2. Compare `manifest.json` against the previous build's `instruction_hash`
3. If changed, re-upload `PROJECT_INSTRUCTION.md` and replace the knowledge
   base files in the destination project

Future enhancement: emit a diff against last build, or build only the
delta. Out of scope for v1.

## Module layout

```
snapshot/
  __init__.py              # exports build_snapshot
  build.py                 # orchestrator + CLI entry
  config.py                # static keep/exclude/redact data
  pull.py                  # Turso queries via remembering.scripts.turso
  filter.py                # tag filter + body redactor + hard-drop check
  cluster.py               # primary-tag picker + bucketing
  compose_instruction.py   # PROJECT_INSTRUCTION.md from filtered configs
  kb.py                    # knowledge_base/*.md + INDEX.md
  example-output/          # sample run, committed for inspection
  README.md
```

## Dependencies

Reads from the live Muninn DB via `remembering.scripts.turso._exec` — the
boot script wires that into `sys.path`. No new client code. Requires
`TURSO_TOKEN` and `TURSO_URL` in the environment.
