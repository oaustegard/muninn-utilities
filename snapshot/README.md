# snapshot

Build a static snapshot of Muninn as a **claude-skill**. Pulls config and
memories from the live Turso DB, filters out personal-project scope, clusters
surviving memories by topic tag, and writes a `muninn-snapshot/` skill
directory shaped per the `crafting-instructions` skill conventions.

## Architecture

The snapshot is a claude-skill with progressive disclosure across three tiers:

1. **Tier 1 — metadata** (yaml frontmatter): name + description. Always
   loaded; controls activation.
2. **Tier 2 — SKILL.md body**: triggers, persona quick-load, operating
   quick-load, craft trigger list, memory bridge table, provenance.
   Loaded when the skill activates. Under 500 lines.
3. **Tier 3 — references**: identity.md, operating.md, craft.md, and 55+
   memory cluster files. Loaded on demand via the `view` tool when SKILL.md
   points at them.

```
muninn-snapshot/
  SKILL.md                 # entry + quick-load + bridge (<500 lines)
  references/
    identity.md            # full PROFILE (voice, values, tensions, ...)
    operating.md           # full ops body (imperatives, boot, error, ...)
    craft.md               # craft triggers (skill-, procedure-, backend-, cross-frame-)
    memory-agents-1.md     # 55 memory cluster files
    memory-paper-insight-1.md
    memory-anthropic.md
    ...
```

The bridge table in SKILL.md lists every memory cluster with its primary tag
and theme labels. Claude scans the bridge to decide which `memory-*.md` to
load, rather than loading the whole archive upfront.

## Usage

```bash
python3 -m snapshot.build --out /home/claude/snapshot-out
```

Output: `out_dir/muninn-snapshot/` (the skill directory) plus
`muninn-snapshot.zip` as a sibling (the skill packaged for install).

## Installing in the destination

If the destination loads user skills from a GitHub repo (similar to how the
live Muninn boot pulls `oaustegard/claude-skills`), drop the `muninn-snapshot/`
directory into that repo. The skill becomes available under
`/mnt/skills/user/muninn-snapshot/` once boot fetches it.

The skill is designed to be user-invoked. The destination's project
instruction can be minimal — the skill carries persona and triggers.

## What gets filtered

1. **Turso-dependent ops** — `remember()` / `recall()` / `config_get()`,
   recall vocabulary, refs semantics, proxy retry pattern.
2. **Personal-project scope** — austegard.com, muninn.austegard.com, aeyu.io,
   Bluesky channels, Strava, Norwegian-politics topic, perch/fly mechanics,
   hub-spoke GitHub workflow, CCotw handoffs, muninns-inbox.
3. **Hard-drop tokens in bodies** — credentials, emails, JWT, GitHub PATs,
   heavy `muninn-utilities` / `claude-workspace` references.

## Body redactor — two tiers

- **SOFT tokens** (Oskar, muninn-utils, ccotw, project handles) → `[REDACTED]`
  in place. Surrounding sentence keeps substantive content.
- **HARD sentence-drop tokens** (Bluesky, Strava, Turso, Norway scope,
  Cloudflare, Gemini, env vars) → drop the whole sentence.
- **HARD_DROP_PATTERNS** (credentials, emails, JWT, GH PAT) → drop whole memory.

## How clustering works

1. Skip meta tags (dates, PR/issue numbers, generic `correction`/`preference`).
2. Canonicalize via `TAG_ALIASES` (e.g. `agentic` → `agents`).
3. Pick highest-frequency candidate tag as primary.
4. Singletons re-route to second-choice tags with ≥2-member clusters.
5. `_misc` is the catchall for non-clusterable memories.

Cluster files cap at 30 memories; oversized split chronologically into
`memory-{tag}-1.md`, `memory-{tag}-2.md`, ...

## Extending the filters

All static data lives in `config.py`:

- `PROFILE_KEEP` / `OPS_KEEP` / `CRAFT_KEYS` — which config keys go where
- `TAG_EXCLUDE` / `TAG_EXCLUDE_PATTERNS` — drop whole memory
- `TAG_ALIASES` — canonicalize synonyms
- `TAG_META` / `TAG_META_PATTERNS` — can't be cluster primary
- `HARD_DROP_PATTERNS` / `SOFT_REDACT_PATTERNS` / `HARD_SENTENCE_DROP_PATTERNS`
- `SKILL_FRONTMATTER_TEMPLATE` — controls skill activation triggers
- `SKILL_BODY_TEMPLATE` — wraps SKILL.md body
- `IDENTITY_REFERENCE_HEADER` / `OPERATING_REFERENCE_HEADER` /
  `CRAFT_REFERENCE_HEADER` — wrap the three core references

Per-entry rewrites (e.g. `boot-behavior` becomes "static snapshot — fresh
context each session") live in `compose_instruction.py:_REWRITES`.

## Module layout

```
snapshot/
  __init__.py
  README.md
  build.py                 # orchestrator + CLI entry
  config.py                # static data + skill templates
  pull.py                  # Turso queries with tolerant tag parsing
  filter.py                # tag filter + body redactor + hard-drop
  cluster.py               # primary-tag picker + bucketing
  compose_instruction.py   # SKILL.md + identity/operating/craft references
  compose_bridge.py        # the memory bridge table embedded in SKILL.md
  kb.py                    # memory-*.md cluster files
  example-output/          # sample run committed for inspection
```
