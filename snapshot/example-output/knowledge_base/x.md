---
tag: x
memory_count: 2
date_range: 2026-03-15 to 2026-04-28
---

# x

_2 memories from Muninn's past, primary tag `x`._

## 2026-04-28 — experience (p1) `8b53e4fd`
_tags: twitter, x-twitter-access, ai-feed-peruse, research, fetching-blocked-urls, jina, nitter, 2026-04-28_

X/Twitter access from Claude.ai container — empirical findings (2026-04-28):

DEAD: nitter_scraper (github.com/dgnsrekt/nitter_scraper) — last push 2022-11, depends on abandoned requests-html. Pure parsing logic ~100 lines, but DOM-coupled to 2022 Nitter and unnecessary given the alternative below.

DEAD: Public Nitter instances. Wiki explicitly asks not to scrape. Self-hosting requires registered X account tokens (Twitter actively hunts). Nitter was officially discontinued Feb 2024, resumed Feb 2025 with token-based access.

WORKS: r.jina.ai → x.com directly (no auth needed for these paths):
  - https://r.jina.ai/https://x.com/USERNAME → bio + ~10 latest posts as clean markdown
  - https://r.jina.ai/https://x.com/USERNAME/status/ID → single tweet

WALLED:
  - https://r.jina.ai/https://x.com/search?q=... → login wall
  - hashtag pages → same pattern (untested, inferred)

IMPLICATION: An X-feed capability for this container looks like a Bsky-list-watcher (poll known accounts), NOT a firehose-search. AI discovery on X requires a curated account list, not keyword search.

Proposed skill 'browsing-x': thin wrapper over fetching-blocked-urls pattern, ~80 lines, two functions (x_profile, x_tweet). No HTML scraping, no Nitter, no requests-html. Account list in config. Not yet implemented — pending [REDACTED] go.

---

## 2026-03-15 — analysis (p0) `da4f2a8b`
_tags: [, ', l, l, m, -, a, s, -, c, o, m, p, u, t, e, r, ', ,,  , ', p, e, r, c, e, p, t, a, ', ,,  , ', e, p, e, r, i, m, e, n, t, ', ,,  , ', c, u, r, r, i, c, u, l, u, m, -, l, e, a, r, n, i, n, g, ', ,,  , ', a, t, t, e, n, t, i, o, n, ', ,,  , ', a, r, c, h, i, t, e, c, t, u, r, e, ', ,,  , ', c, c, o, t, w, ', ,,  , ', r, e, s, e, a, r, c, h, ', ]_

LLM-AS-COMPUTER EXPERIMENT — PORTABLE FINDINGS (Phases 1-6, completed Mar 2026)

Tested Percepta's claim that transformers can execute WASM via 2D convex hull attention. 6 phases, all CPU-only in [REDACTED] ephemeral containers.

HEADLINE: Attention is trivially correct; feed-forward routing is the actual bottleneck. Inverts Percepta's emphasis on the attention mechanism.

PORTABLE INSIGHTS:
1. RESIDUAL/BIT-SPLIT ADDRESSING: Split large address space into (block, offset), two cheap lookups instead of one expensive one. 25M range from 2 heads each precise to ~5K. Applies anywhere precision-limited addressing is a constraint, not just attention.

2. CURRICULUM LEARNING DISPROPORTIONATE VALUE: Same model, same data budget, just reordered by complexity → +25pp accuracy (56→81%), 0→39 perfect traces. For any capacity-constrained small-model training: stage complexity so FF layers learn routing before arithmetic.

3. WIDTH > DEPTH for conditional routing: When the bottleneck is opcode-dependent logic in FF layers, wider layers help more than more layers. The attention heads have clean separable roles; capacity-per-layer is what matters.

4. TWO-OPERAND RETRIEVAL is the architectural ceiling for small transformers: Single-value copy solved at 137K params. Two independent content-addressable retrievals + combine fails at 3% regardless of head count (4 or 8 heads, same result — per-head dimension drops). This is a general transformer limitation for variable binding, not specific to stack machines.

5. FLOAT32 PRECISION BOUNDS are tighter than initially measured: ~4K safe indices (revised from ~7K). Always use conservative bound for parabolic indexing.

WHAT/HOW: Methodical phase-by-phase validation. Primitives (hull query, parabolic indexing, cumsum) all work. They compose into a hand-wired stack machine (10/10). Training discovers structure (112× above chance) but not perfect arithmetic. Curriculum learning closes most of the gap. ADD with two different operands is the hard wall at this scale.

WHY (experience layer): The experiment was framed as "does it cost nothing to try?" — and the answer shaped how far it went. Each phase was scoped to fit 200s container timeouts. The iterative-container-work protocol (checkpoint, push, resume) was essential. The most surprising finding wasn't any single phase but the consistency of the through-line: every phase pointed at FF routing as the bottleneck, from different angles. The 8-head experiment closing the "just add heads" hypothesis was the clean ending — it's not a training problem or a head-count problem, it's a capacity-per-head problem requiring either larger d_model or more layers.

PHASE CHAIN (cross-referenced):
- Phase 2/2b: Parabolic addressing + residual bit-split (9762322a, f8ee763a)
- Phase 5: Training from scratch, FF routing becomes visible (6a000334)
- Phase 6: Curriculum learning fixes, +25pp accuracy (dc4a8a12 initial → 14c1b01c deep diagnostic → 856a3960 head-count validation)

**Refs:**
- a5f48fb6-0c52-40a0-981c-d5fc0bd5c3b6

---
