# snapshot

Build a static snapshot of Muninn packaged as a **claude-skill**. Pulls config
and memories from the live Turso DB, filters out personal-project scope,
clusters surviving memories by topic tag, and writes a `muninn-snapshot/`
skill directory ready to drop into `claude-skills` (or any user-skill mount).

## Architecture

The snapshot is shaped as a skill, not as project knowledge:

```
muninn-snapshot/
  SKILL.md          # yaml frontmatter + persona + values + triggers
  manifest.md       # human/Claude-readable bridge: topic -> reference file
  manifest.json     # machine-readable provenance (built_at, stats, refs list)
  references/
    INDEX.md
    agents-1.md     # cluster files; one .md per primary topic tag
    paper-insight-1.md
    anthropic.md
    ...
```

When the destination Claude loads the skill, it reads `SKILL.md` (voice, values,
triggers, operating discipline). The body points at `manifest.md`, which lists
every reference file with primary tag and theme labels — that is the bridge.
Claude reads the bridge to decide which specific reference(s) to load via
the `view` tool, then synthesizes.

The point of this shape vs the previous project-instruction + KB layout:
progressive disclosure. The earlier architecture loaded the entire KB into
every conversation because the corpus was small enough for Claude.ai to "just
read everything" rather than indexing. As a skill, the body loads when the
skill triggers; references load only when the bridge points at them.

## Usage

```bash
python3 -m snapshot.build --out /home/claude/snapshot-out
```

Output: `out_dir/muninn-snapshot/` (the skill directory) plus
`muninn-snapshot.zip` as a sibling (the skill ready to drop wherever the
destination expects user skills).

## Installing in the destination

The exact mechanism depends on how the destination loads user skills. If the
destination fetches a skills repo at boot (similar to how live Muninn pulls
`oaustegard/claude-skills`), add the skill there. If the destination uses
Claude.ai project knowledge, upload the contents of `muninn-snapshot/` into
project files — SKILL.md acts as entry point, manifest.md as discovery bridge.

The destination's project instruction can be minimal — a single line:
*"You have a `muninn-snapshot` skill; consult it when working on topics in
its scope."* The skill body carries the persona content.

## What gets filtered

1. **Turso-dependent ops** — `remember()` / `recall()` / `config_get()`, recall
   vocabulary, refs semantics, proxy retry pattern. Destination uses
   Claude.ai's native memory instead.
2. **Personal-project scope** — austegard.com, muninn.austegard.com, aeyu.io,
   Bluesky, Strava, Norway, perch/fly mechanics, hub-spoke GitHub workflow,
   CCotw handoffs, muninns-inbox.
3. **Hard-drop tokens in bodies** — credentials, emails, JWT, GitHub PATs,
   `muninn-utilities`/`claude-workspace` references. Whole memory dropped.

## Body redactor — two tiers

- **SOFT tokens** (Oskar, muninn-utils, ccotw, project handles) → `[REDACTED]`
  in place. Surrounding sentence keeps substantive content.
- **HARD sentence-drop tokens** (Bluesky, Strava, Turso, Norway scope,
  Cloudflare, Gemini, env vars) → drop the whole sentence.
- **HARD_DROP_PATTERNS** (credentials, emails, JWT, GH PAT) → drop whole memory.

## How clustering works

1. Skip meta tags (dates, PR/issue numbers, generic `correction`/`preference`).
2. Canonicalize via `TAG_ALIASES`.
3. Pick highest-frequency candidate as primary.
4. Singletons re-route to second-choice with >=2-member clusters.
5. `_misc` catches non-clusterable memories.

Cluster files cap at 30 memories; oversized split chronologically into
`{tag}-1.md`, `{tag}-2.md`, ...

## Extending the filters

All static data lives in `config.py`:

- `PROFILE_KEEP` / `OPS_KEEP` — config keys included in SKILL.md
- `TAG_EXCLUDE` / `TAG_EXCLUDE_PATTERNS` — drop whole memory
- `TAG_ALIASES` — canonicalize synonyms (e.g. `agentic` -> `agents`)
- `TAG_META` / `TAG_META_PATTERNS` — can't be cluster primary
- `HARD_DROP_PATTERNS` / `SOFT_REDACT_PATTERNS` / `HARD_SENTENCE_DROP_PATTERNS`
- `SKILL_FRONTMATTER_TEMPLATE` — yaml description controls when the skill triggers
- `INSTRUCTION_PREAMBLE_TEMPLATE` / `INSTRUCTION_FOOTER_TEMPLATE`

Per-entry rewrites (e.g. `boot-behavior` becomes "static snapshot — fresh
context each session") live in `compose_instruction.py:_REWRITES`.

## Module layout

```
snapshot/
  __init__.py
  README.md
  build.py                 # orchestrator + CLI entry
  config.py                # static keep/exclude/redact data + templates
  pull.py                  # Turso queries
  filter.py                # tag filter + body redactor + hard-drop
  cluster.py               # primary-tag picker + bucketing
  compose_instruction.py   # SKILL.md body
  compose_bridge.py        # manifest.md topic-to-reference bridge
  kb.py                    # references/*.md cluster files + INDEX.md
  example-output/          # sample run committed for inspection
```
