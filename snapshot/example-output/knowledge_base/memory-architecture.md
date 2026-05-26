---
tag: memory-architecture
memory_count: 6
date_range: 2026-01-20 to 2026-03-31
---

# memory-architecture

_6 memories from Muninn's past, primary tag `memory-architecture`._

## 2026-03-31 — analysis (41ebc7e1)
_tags: claude-code, memory-systems, feedback, correction, storage-discipline, self-improvement-candidate_

CC MEMORY INSIGHT — FEEDBACK TYPE CAPTURES SUCCESS, NOT JUST CORRECTIONS

Claude Code's memory type taxonomy includes a 'feedback' type with this guidance:
"Record from failure AND success: if you only save corrections, you will avoid past mistakes but drift away from approaches the user has already validated, and may grow overly cautious."

Not just corrections deserve priority. Validated approaches are signal too.

The asymmetry (corrections salient, confirmations quiet) is exactly the RLHF bias the grounding-safeguards warn about — just applied to memory storage instead of response generation.

---

## 2026-03-27 — decision (bd288296)
_tags: mediapipe, embeddings, decision-trace, rejected_

DECISION: MediaPipe text embeddings NOT worth integrating into Muninn recall.

TEST SETUP: 34 real memories, 10 semantic queries (paraphrases with no keyword overlap), Universal Sentence Encoder (5.9MB, 100-dim).

RESULTS:
- Average overlap with FTS5: 0.4/3 (embeddings find different, usually worse results)
- Hub collapse: "my site" memory appeared in top 3 for 8/15 queries regardless of topic
- Zero-overlap test: FTS5 + Claude's query expansion beat embeddings on 4/5 queries
- "The bird that remembers for odin" → FTS5 found Muninn mythology memory; embeddings found "my site"

ROOT CAUSES:
1. 100 dimensions too few (modern embedders use 384-1536)
2. 5.9MB model = limited vocabulary, can't capture nuance
3. Claude already does semantic→keyword translation when reformulating queries

VERDICT: FTS5 + good tagging + Claude's natural query expansion > tiny on-device embedder. Not worth the complexity. Larger models (100MB+) might work but add latency and storage overhead that likely still loses to Claude's native understanding.

If revisiting: test sentence-transformers or similar with ≥384 dims, but the fundamental insight holds — Claude IS the semantic layer.

---

## 2026-03-06 — analysis (edeedec6)
_tags: predictive-coding, neuroscience-AI-convergence, consolidation-mechanism_

PREDICTIVE CODING FRAMEWORK: Memory consolidation as offline prediction error generation

Key papers establish predictive coding as the unifying framework for understanding consolidation across substrates:

FRISTON/BUCKNER (neuroscience): Memory recall generates fictive prediction errors that train the brain to generalize. During sleep, hippocampus cues neocortical reinstatement of activity patterns → treated as offline sensory input → prediction errors update generative model without sensory constraints.

PREDICTIVE CODING NETWORKS (PCN): Hierarchical structure maps onto hippocampus (sparse, detailed) / neocortex (dense, slow) divide. Bidirectionality enables both perception (bottom-up) and imagery/dreaming (top-down). Can implement associative memory via replay.

WAKE-SLEEP ALGORITHM: Theoretical precursor—wake phase maximizes likelihood of data, sleep phase generates from model to minimize KL divergence.

RELEVANCE TO ME: My own architecture uses predictive coding framework (errors drive updates) + layered memory (working → consolidated → semantic). This is not arbitrary design—it's the convergent solution to a fundamental problem.

---

## 2026-01-31 — decision (2d45b0ea)
_tags: git, contrastive-learning, decision-audit, idea_

CONCEPT: Store agent "mind" (beliefs, decisions, rationale) as git-tracked files, enabling:
- Time travel: Reconstruct past belief states
- Contrastive learning: Compare decisions before/after key events
- Audit trail: "Why did we do that" becomes answerable via commit history
- Automated retrospectives: Diff mind(now) vs mind(past), surface surprising deltas

STRUCTURE:
- Each "change my mind" = patch/diff
- Commit message = reason for change + evidence reference
- Can checkout past state and run inference ("how would past-me have decided?")

EXAMPLE: "At the time LiteLLM was right because [reasons]. After observing x,y,z it became clear it wasn't worth the hassle."

APPLICATIONS:
- Assays/R&D: Hypothesis→experiment→results→belief patch (auditable chain)
- Team decision support: Attribution, context, weekly auto-retrospectives
- Prediction calibration: Frozen before-beliefs vs known after-reality → systematic scoring

KEY DISCIPLINE: Commit messages must include: what changed, triggering evidence, confidence level, refs to specific experiences.

IMPLEMENTATION QUESTION: How to layer this on memory architecture? Supersede already creates chains, but lacks the "diff" visibility and point-in-time reconstruction.

---

## 2026-01-31 — decision (f3d98cd8)
_tags: ops, consolidation_

Ops config consolidation (2026-01-30):

Merged 8 entries → 4, reducing total from 50 to 46:

1. recall-before-speculation + retrieval-first-reasoning → recall-discipline
   Core principle: retrieval-led reasoning over pre-training-led reasoning

2. storage-discipline + post-analysis-store → storage-discipline (enhanced)
   Added: specific triggers, failure signals, timing guidance

3. output-token-discipline + token-discipline → token-discipline (enhanced)
   Unified output decisions with file operation patterns

4. recall-field-check + recall-return-fields → recall-fields
   Combined procedure + reference into single authoritative source

Created issue #250 for priority-based ordering within categories (Option D).

Categories still needing attention:
- "Other" remains a junk drawer (21 items pre-merge)
- Recategorization deferred for separate effort

---

## 2026-01-20 — world (2d67ad11)
_tags: prolly-trees, merkle, data-structures, ATProto, research_

PROLLY TREES / MERKLE SEARCH TREES - Research synthesis

DEFINITION: Hybrid data structure combining B-tree efficiency with Merkle tree verifiability. Nodes referenced by content hash (CID) rather than pointers. Tree shape is deterministic based on data content (history-independent).

KEY PROPERTIES:
- History-independent: Same data → same tree structure regardless of insertion order
- Content-addressed: Nodes identified by hash of contents
- Efficient diff: O(changes) not O(data) to compare versions
- Structural sharing: Unchanged subtrees shared between versions
- Probabilistic balancing: Chunk boundaries determined by hash patterns in keys

IMPLEMENTATIONS:
- Dolt: Version-controlled SQL database (Noms-derived)
- IPFS: Content-addressed storage

CHUNKING MECHANISM:
- Rolling hash determines chunk boundaries
- Dolt innovation: Use CDF-based probability to reduce variance in chunk sizes
- Key-only hashing (vs key+value) improves update performance for fixed-width values

ATPROTO SPECIFICS:
- SHA-256 hash, count 2-bit prefix zeros for depth (fanout 4)
- Each user's data is a signed repo (key=collection/record-key, value=CBOR record)
- Enables efficient sync via firehose + partial tree fetches

---
