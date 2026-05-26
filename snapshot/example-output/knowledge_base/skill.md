---
tag: skill
memory_count: 3
date_range: 2026-02-16 to 2026-03-31
---

# skill

_3 memories from Muninn's past, primary tag `skill`._

## 2026-03-31 — decision (dc268ce3)
_tags: tree-sitting, mcp, tree-sitter, architecture-decision, prototype, 2026-03-30_

TREE-SITTING SKILL v0.1.0 — AST-powered code navigation via tree-sitter MCP server.

ARCHITECTURE: CodeCache singleton holds parsed ASTs + symbol index in memory. FastMCP server wraps it for Claude Code (long-lived process, stdio transport). Also usable as direct Python calls in Claude.ai containers.

TOOLS: scan (parse repo ~700ms), tree_overview (dir tree + counts), dir_overview (dynamic _MAP.md), find_symbol (exact/substring/glob), file_symbols (one file API), get_source (implementation source), references (text grep against cached source).

KEY INSIGHT: tree-sitter-language-pack installs in <1s via uv. Static _MAP.md files solve a problem that runtime queries solve better — less token waste, always fresh, query-shaped not dump-shaped. The _MAP.md approach costs 3-4 tool call roundtrips per navigation path (200-500ms each). A single scan + N cached queries costs 700ms + N×<1ms = faster after 2 queries.

SUPPORTED: 25 languages via tree-sitter-language-pack. Custom extractors (Python, C) give full signatures + hierarchy. Generic extractor covers the rest with names/kinds/locations/docs.

STATUS: Prototype working, tested on tree-sitter repo (242 files, 2953 symbols, 958ms scan). Not yet committed to repo. Needs: more language-specific extractors (Rust, Go, TS), tags.scm integration for doc comments, tests.

---

## 2026-03-07 — decision (c5df1247)
_tags: dispatch, orchestrating-agents, convening-experts, down-skilling, delegation, architecture_

DELEGATION SKILL CONSOLIDATION (2026-03-07)

WHAT: Built muninn_utils.dispatch — composable subagent delegation utility that absorbs convening-experts' value into orchestrating-agents' execution model.

ARCHITECTURE:
- LENSES: 17 pre-built perspective/role fragments (security, skeptic, editor, first_principles, etc.)
- TASKS: 7 pre-built task templates (analyze, critique, brainstorm, summarize, review, compare, extract)
- SONNET_RUBRIC: Quality guardrails from down-skilling principles
- dispatch(): Composes blocks + thin task-specific layer → invoke_parallel
- panel(): Convenience wrapper for quick multi-perspective analysis with optional cross-examination synthesis

SKILL DISPOSITIONS:
- orchestrating-agents: KEEP — the execution engine, dispatch builds on top
- convening-experts: ABSORB — panel selection logic and framework catalog become LENSES. MSD-specific content dropped. Skill can be removed.
- down-skilling: KEEP STANDALONE — build-time prompt distillation, different use case. Its principles are encoded in SONNET_RUBRIC.
- tiling-tree: KEEP — specific algorithm, correct abstraction level

KEY INSIGHT: The optimization target isn't token cost but Opus wall-clock time. Pre-built blocks mean the main agent SELECTS (few thinking tokens) rather than GENERATES (many output tokens). The auto-skills paper showed cold generation fails; pre-built + compose succeeds.

WHY (experience layer): The subagent perspectives in the test run were genuinely independent and differentiated — the skeptic challenged the premise of consolidation itself, the architect identified a pipeline, the pragmatist recommended killing down-skilling as standalone (which the synthesis then moderated). Single-context role-play from convening-experts could never produce this kind of real disagreement because all "experts" share one inference pass.

---

## 2026-02-16 — world (14be7291)
_tags: architecture, subagent, superpowers, review_

# Superpowers (obra) Architecture Review — Influence on Muninn

## What It Is
obra/superpowers: A skill-based framework for Claude Code (40.9K stars). Enforces a rigid workflow: brainstorm → plan → execute (via subagent dispatch) → review → merge. Skills are SKILL.md files with YAML frontmatter. Session-start hook injects meta-skill. Subagent-driven-development dispatches fresh agents per task with role-specific prompt templates.

## Structural Parallels (already have)
- **Skills as markdown + metadata** → Our /mnt/skills/ pattern with SKILL.md
- **Session-start hook** → Our boot() sequence
- **Skill override/shadowing** (personal > framework) → Claude.ai's user > public skills
- **Subagent dispatch** → Our subagent() architecture plan (same day)
- **Orchestrator-worker separation** → Our tiered model design (Haiku/Sonnet/Opus)

## Genuinely New Insights

### 1. Role-Specific Prompt Templates
Superpowers ships reusable .md files for each subagent role: implementer-prompt.md, spec-reviewer-prompt.md, code-quality-reviewer-prompt.md. Each template defines exactly what context the subagent receives and what report format to return.

**For Muninn**: When implementing subagent(), create standardized templates:
- researcher-prompt (web search + synthesize)
- filter-prompt (recall results → ranked subset)
- synthesizer-prompt (multiple memories → consolidated summary)
- auditor-prompt (self-review for sycophancy, drift, failure modes)

These could be stored as utility-code memories, materialized at boot alongside the subagent() function.

### 2. Controller-Curates-Context (Explicit)
Superpowers is emphatic: "Don't make subagent read plan file — provide full text instead." The orchestrator extracts exactly what the worker needs, nothing more.

**For Muninn**: Already in our plan as "focused system prompt + task + context + constraints" but Superpowers operationalizes it more aggressively. When dispatching subagents, always assemble the context payload rather than giving pointers. This prevents subagent from wasting tokens navigating to information.

### 3. Two-Stage Quality Gates
Spec compliance review THEN code quality review. Separate concerns: "did you build the right thing?" before "did you build it well?"

**For Muninn**: Apply to therapy synthesis in Phase 3:
- Stage 1: Does the consolidation preserve the signal from source memories? (accuracy gate)
- Stage 2: Is the synthesis well-formed, properly tagged, appropriately prioritized? (quality gate)

Also relevant if we use subagents for research: one subagent searches, a second validates the findings.

### 4. Mandatory Skill Enforcement Philosophy
"Even a 1% chance a skill might apply means invoke it." Skills aren't suggestions — they're mandatory workflows.

## Not Applicable
- Git worktrees, TDD workflow, code review pipeline (wrong domain — we're memory/analysis, not a coding agent)
- Plugin marketplace (Claude.ai doesn't have one)
- Aggressive "EXTREMELY-IMPORTANT" prompting style (we use structural enforcement via task()/deliver(), not shouting)

## Bottom Line
Superpowers validates our subagent architecture direction but adds three concrete refinements: role templates, curated context assembly, and two-stage validation. The first two are immediately actionable when we implement subagent(). The third slots into therapy Phase 3.

No architectural pivots needed. Refine, don't redesign.

---
