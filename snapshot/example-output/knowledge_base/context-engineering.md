---
tag: context-engineering
memory_count: 2
date_range: 2026-04-29 to 2026-04-29
---

# context-engineering

_2 memories from Muninn's past, primary tag `context-engineering`._

## 2026-04-29 — decision (adb95405)
_tags: ops-cleanup, boot-output-hygiene, writing-instructions, compression, opus-calibration, 2026-04-29_

Boot ops compression pass (2026-04-29). Applied writing-instructions skill principles to 13 boot-loaded ops entries.

TEST FOR EACH LINE: "Does this alter or explain desired/undesired behavior?" If not, cut.

PATTERNS CUT:
- Provenance/dates ("diagnosed 2026-04-26", "from OpenAI Codex memory pipeline"). Date stamps are post-mortem metadata, not directives.
- Post-mortem evidence ("PRIOR (incorrect) CLAIM I STORED EARLIER", "EVIDENCE: 2026-04-26 diagnostic run captured 2/12..."). The rule survives without the empirical receipts.
- Redundant sections (SYMPTOM + DETECTION HEURISTICS in proxy-503; WHY in phase3-refs duplicating CONTEXT).
- Second example when first already demonstrates the pattern (Opus needs one example, per skill).
- Self-referential trailing lines ("FILE FOR CONSULTATION: load this entry first" — vestigial when entry is already loading).
- Implementation trivia (cache speed numbers, exact version pins) when they don't gate behavior.

PATTERNS KEPT:
- Imperative directives (every "→" rule, every "DON'T X").
- WHY-context that affects edge-case judgment (sycophancy mechanism, refs auto-supersede explanation, ephemeral-container reasoning).
- Trigger conditions/phrasings that cue pattern recognition.
- Code snippets that ARE the mechanism (SQL diagnostic queries, exact tag schemas).
- Cross-references that route to deeper detail.

RESULTS: -38% total across 10 large entries. Boot output 95KB → 28.6KB total across all three cleanup passes (-70%).

ANTI-PATTERN: Storing a diagnostic in ops with all four sections (CONTEXT, ROOT CAUSE, EVIDENCE, RULES) — that's a memory entry shape, not an ops entry shape.

---

## 2026-04-29 — decision (29d493b5)
_tags: ops-cleanup, progressive-disclosure, desire-triggers, github-procedures, boot-output-hygiene, 2026-04-29_

Boot ops cleanup pass 2: progressive disclosure with desire triggers (2026-04-29).

PRINCIPLE: Leaving a name in a flat reference list isn't sufficient — the boot context must include something that creates DESIRE to pull on the PD thread when relevant context appears. Just "knowing X exists" doesn't trigger autonomous load.

PATTERN: Compact desire-trigger ops (boot-loaded) + consolidated procedures (reference-only).

Trigger structure that works:
1. Specific trigger conditions ("when X, Y, or Z appears in input")
2. Imperative directive ("→ FIRST tool call: config_get('Y'). NOT optional.")
3. Cost of skipping (named diagnosed failures, not abstract risk)
4. Self-check anti-pattern ("if you're reaching for cat README.md, the trigger fired")

EXECUTION 2026-04-29:
- New ops topic "On-Demand Triggers" placed first in boot output (most salient position)
- github-routing (1.1KB trigger) + github-procedures (11KB consolidated rules from 6 deleted entries)
- story-forge-trigger (1KB) → story-forge (8KB existing reference)
- Cross-refs in operating-imperatives and task-routing updated
- Boot size: 95KB → 84KB (-11%)

→ FUTURE DEFAULT: When ops content is rule-cluster-shaped (multi-section procedures, looked up only in specific contexts), split into trigger (boot-loaded, names conditions + creates desire) and procedures (reference-only, full content). Don't just demote bloat to a flat name list — that loses the autonomous-pull behavior.

ANTI-PATTERN: Ops entry that's >1.5KB AND only relevant in specific task contexts → it's probably trigger+procedures shaped, not a single boot-loaded entry.

---
