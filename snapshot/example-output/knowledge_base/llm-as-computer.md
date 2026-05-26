---
tag: llm-as-computer
memory_count: 7
date_range: 2026-03-12 to 2026-04-24
---

# llm-as-computer

_7 memories from Muninn's past, primary tag `llm-as-computer`._

## 2026-04-24 — decision (9d3c0270)
_tags: lac, blog-writing, audience-analysis, polynomial-evaluator, ff_symbolic, framing, 2026-04-24, eml-sr_

FFN-as-polynomial-evaluator framing — audience diagnosis for LAC writing.

The claim "the feed-forward layer of a hand-compiled transformer is, demonstrably, a polynomial evaluator" lands as crickets because:
1. "Polynomial evaluator" reads as weaker than "universal approximator" — sounds like a demotion
2. "Hand-compiled" cues toy project — undercuts the structural claim
3. "Demonstrably" sounds defensive — readers not in the fight have no side

Real audiences (ranked by who should care):
- Mech-interp / circuits: hand-compiled version = candidate functional form for what learned FFN does in SAE-feature coords
- Compilation-to-transformer (RASP/Tracr/Percepta descendants): polynomial evaluator = ALU spec; ff_symbolic.py is the artifact
- Symbolic regression (his own eml-sr): bridge concept — trained FFN = polynomial regression in learned basis; explains where additive distillation breaks (multiplicative catalog rows)
- General ML readers wondering about FFN widths: degree × variables gives quantitative story

The missing explainer has three beats:
1. Undeniable math: W2·sigma(W1 x+b1)+b2 with sigma(z)=z^2 computes degree-2 polynomial EXACTLY, not approximates. Stack n → degree 2^n.
2. Correspondence: coefficients are rational functions of weights — you can read them off. ff_symbolic.py IS the reading-off (running code = "demonstrably")
3. Stake named: hand-compiled = known polynomial; trained = discovered polynomial in learned basis. Same function class. Interp + distillation + compilation = same problem dressed differently.

Crickets diagnosis: claim reads as definition when it needs to read as unification. Without "these are all the same object" beat, nothing to care about.

---

## 2026-03-23 — procedure (52b32878)
_tags: shipped, issue-11, arithmetic, 2026-03-23_

Phase 14 Chunk 1 (Issue #11) SHIPPED: 5 arithmetic opcodes added to llm-as-computer.

NEW OPCODES: MUL(13), DIV_S(14), DIV_U(15), REM_S(16), REM_U(17), plus OP_TRAP(99) for div-by-zero.
FILE: phase14_extended_isa.py extending Phase 13.

ARCHITECTURE DECISION — nonlinear FF dispatch:
MUL/DIV/REM can't be expressed as M_top linear routing (MUL = va*vb, not a linear combo).
Solution: M_top rows for nonlinear ops set to zero; explicit nonlinear computation in forward().
One-hot vector selects which path contributes. Clean extension of compiled transformer paradigm.

TRAP MECHANISM: OP_TRAP=99, appended as TraceStep, executor breaks. No error flags, no new mechanism.
Division semantics: _trunc_div (truncate toward zero, WASM-style), _trunc_rem (sign matches dividend).

NEW ALGORITHMS ENABLED: native multiply (4 steps vs 1109 for 7×100), factorial, GCD (Euclidean with REM_S), native is_even (6 steps vs 506 for n=100).

OPCODE_DIM_MAP: MUL→24, DIV_S→25, DIV_U→26, REM_S→27, REM_U→28 (D_MODEL=36, within range).
OPCODE_IDX: MUL→12 through REM_U→16. N_OPCODES=17.

All 10 test groups pass (87 individual tests). Full Phase 4/11/13 backward compatibility.

---

## 2026-03-23 — decision (3dcba263)
_tags: wasm, roadmap, architecture, 2026-03-23_

LLM-as-computer WASM expansion roadmap (2026-03-23):

CURRENT STATE: 12 opcodes (PUSH/POP/ADD/SUB/DUP/SWAP/OVER/ROT/JZ/JNZ/NOP/HALT). Turing-complete but toy — multiply is O(n) repeated addition, no comparisons, no bitwise ops, no local variables, no memory.

WASM 1.0 has 172 instructions across 5 categories: 13 control, 2 parametric, 5 variable, 25 memory, 127 numeric.

TIER 1 — FF dispatch only (no new attention heads):
  ~39 new opcodes: MUL/DIV/REM (6), comparisons EQ/NE/LT/GT/LE/GE/EQZ (13), bitwise AND/OR/XOR/SHL/SHR/ROTL/ROTR (14), unary CLZ/CTZ/POPCNT/ABS/NEG (5), SELECT (1).
  All are pure "pop→compute→push" — same attention mechanism, just more elif branches in FF dispatch.
  IMPACT: Native MUL alone collapses multiply(7,100) from 1109 steps to ~8.

TIER 2 — New memory spaces (same parabolic mechanism, new attention heads):
  LOCAL.GET/SET: separate "locals" parabolic space, 1 new head pair
  LOAD/STORE (linear memory): separate "heap" space, 1 new head pair. Phase 2b residual addressing → 25M range.
  CALL/RETURN: call stack for return addresses + frame pointers.
  Percepta architecture has 13 reserved heads (5 of 18 active) — plenty of headroom.

TIER 3 — Architectural extensions:
  BLOCK/LOOP/IF/ELSE/END: compile to JZ/JNZ at assembly time (assembler work, not executor)
  BR_TABLE: jump table lookup via attention
  Float ops (f32/f64): analytical compilation of float math in FF layer is harder

KEY INSIGHT: Tier 1 is the sweet spot — 39 opcodes, zero architectural changes, transforms "toy Forth" into "capable integer computer." Effort: hours. Tier 2 is the VM milestone. Tier 3 approaches real WASM compat.

---

## 2026-03-23 — procedure (45f3290c)
_tags: mojo, skill, shipped, 2026-03-23_

SHIPPED: llm-as-computer skill — functional compiled transformer executor.

WHAT: Mojo-based stack machine where every instruction fetch and stack read is a parabolic attention head (dot-product → argmax → value extraction). Full ISA: PUSH/POP/ADD/SUB/DUP/SWAP/OVER/ROT/JZ/JNZ/NOP/HALT. Python runner with built-in algorithm generators (fib, multiply, power2, sum_n).

FILES:
- /mnt/skills/user/llm-as-computer/SKILL.md
- /mnt/skills/user/llm-as-computer/executor.mojo (Mojo source, ~130 lines)
- /mnt/skills/user/llm-as-computer/run.py (Python runner + generators)

PERFORMANCE:
- fib(50) = 12,586,269,025 in 1.3ms (591 steps, 470K steps/s)
- power2(20) = 1,048,576 in 141µs (206 steps, 1.5M steps/s)
- sum(1..500) = 125,250 in 64ms (5006 steps, 78K steps/s — slows due to O(n) stack scan)

LIMITATION: Append-only stack model means stack scans grow linearly with total writes. Programs with deep loops over large accumulators (multiply(7,100), sum_n(500)) slow down. This is inherent to the attention-based memory model — could be mitigated with garbage collection of old stack entries.

NEEDS: coding-mojo skill for Mojo install. First run builds binary (~30s), subsequent calls instant.
STATUS: Working in compute environment, not yet in GitHub repo. Needs PR to persist.

---

## 2026-03-23 — analysis (5821d515)
_tags: mojo, benchmark, percepta, satisfaction, 2026-03-23_

LLM-as-computer Mojo port benchmark results (2026-03-23):

PHASE 12 (Compiled Transformer Executor) — countdown test (14-step loop program):
  Mojo:    0.75 µs/exec → 18.6M steps/s
  Python:  46.4 µs/exec → 301K steps/s  (62× slower)
  NumPy:   301 µs/exec  → 47K steps/s   (401× slower)
  PyTorch: 1011 µs/exec → 13.8K steps/s (1348× slower)

PHASE 1 (Parabolic KV Cache) at 50K entries:
  Mojo ternary:  0.21 µs/query → 7.5M queries/s
  Mojo brute:    67.7 µs/query (510× slower — O(n) vs O(log n))
  Python ternary: 6.98 µs/query (33× slower than Mojo ternary)
  Python brute:  2771 µs/query
  NumPy brute:   61.4 µs/query (competitive with Mojo brute due to SIMD)

KEY INSIGHT: Framework overhead dominates for tiny tensors. PyTorch (nn.Linear + argmax dispatch) is 1348× slower than Mojo on 36-dim embeddings. NumPy is 6× slower than pure Python because array creation exceeds computation. The algorithm wins (O(log n) ternary) compound with language wins (native code): Mojo ternary at 100K entries is 693× faster than Mojo brute.

PRACTICAL IMPLICATION: The Percepta compiled-transformer thesis extends from "theoretically correct" to "viable compute substrate" — 18M instructions/sec in native code means real programs can execute through attention.

WHY (experience layer): The surprising result wasn't Mojo vs Python speed — that was predicted. It was NumPy being SLOWER than pure Python. This validates the hypothesis that framework overhead is the real bottleneck for compiled transformers, not algorithmic complexity. The per-step computation (4 attention heads on 36-dim vectors) is so small that any abstraction layer costs more than the work itself.

---

## 2026-03-12 — analysis (76c24b03)
_tags: curriculum-learning, research, satisfaction, 2026-03-12_

LLM-as-computer Phase 6 DIAGNOSTIC FINDING: The bottleneck is numeric vocabulary, not execution logic.

EXPERIMENT: PUSH+HALT only, 137K param model (d=64, h=4, L=2), 1000 training samples.

max_push_val=50 (51 values): 58% val accuracy, 0/50 perfect traces. PLATEAUED.
max_push_val=5 (6 values):   87.5% val accuracy, 50/50 PERFECT traces. Still climbing at wall-clock.

WHY: With 1000 samples and 51 values, each number appears ~20 times. With 6 values, ~167 times. The model needs sufficient examples per numeric token to learn the attention-based copying pattern from program section to trace section.

IMPLICATION: Phase 5's "56% accuracy gap" was NOT about difficulty learning execution structure or arithmetic. It was about insufficient data density per numeric token. The model learned execution grammar perfectly when the numeric vocabulary was tractable.

REVISED PLAN: Keep max_push_val small (0-5 or 0-10) for the curriculum stages. The research question is "does curriculum learning help with ADD?" not "can the model memorize 50 numbers." ADD with values 0-5 still produces sums 0-10, which is testable.

WHY (experience layer): This was genuinely surprising. I expected the PUSH+HALT stage to be trivially solved regardless of numeric range — I thought the "attention heads have clean roles" finding from Phase 4 meant copying was easy. But copying requires learning a lookup table from POSITION to VALUE, and that table has as many entries as the vocabulary. With small vocab, the model nails it. With large vocab, it fails to generalize. The structural insight holds — the attention mechanism CAN implement the lookup — but the LEARNING of that lookup requires adequate data per symbol.

---

## 2026-03-12 — procedure (3f5d01a1)
_tags: curriculum-learning, research, 2026-03-12_

PLAN: LLM-as-computer Phase 6 — Curriculum Learning

HYPOTHESIS: Phase 5's 56% accuracy gap is because the model must simultaneously learn state tracking AND arithmetic. Curriculum learning decomposes this — teach tracking first, arithmetic last.

STAGES:

Stage 1: PUSH + HALT only
  - Programs: PUSH x, PUSH y, ..., HALT (3-8 instructions)
  - What model learns: opcode prediction, SP always increments by 1, TOP = last pushed value
  - This is near-trivial — establishes baseline weights for token embedding, position encoding
  - Success: >95% token accuracy
  - Data: 1000 train / 150 val / 50 test, max_push_val=50

Stage 2: PUSH + POP + DUP + HALT (all non-arithmetic ops)
  - Initialize from Stage 1 checkpoint
  - Programs: mix of PUSH/POP/DUP with validity constraints
  - What model learns: SP can decrement (POP), TOP can come from stack recall (POP/DUP)
  - Harder than Stage 1 because TOP after POP requires attending to earlier stack state
  - Success: >85% token accuracy
  - Data: 1000 train / 150 val / 50 test

Stage 3: Full instruction set (add ADD)
  - Initialize from Stage 2 checkpoint
  - Programs: same distribution as Phase 5 (all ops valid)
  - What model learns: ADD requires reading two stack values and computing their sum
  - This is the hardest stage — the arithmetic gap from Phase 5
  - Success: >70% token accuracy AND at least 1 perfect trace
  - Data: 1000 train / 150 val / 50 test, max_push_val=30 (keep sums in range)

IMPLEMENTATION:

Single new file: phase6_curriculum.py
  - Reuses Phase 5 model architecture (MicroTransformer, d=64, h=4, L=2, 137K params)
  - Reuses Phase 5 encoding/decoding, TraceDataset
  - New: constrained_random_program(allowed_ops=[...]) for stage-specific data gen
  - New: checkpoint save/load functions with stage metadata
  - New: stage runner that trains, evaluates, saves, and prints metrics

EXECUTION PROTOCOL (per the iterative-container-work ops config):
  1. Write phase6_curriculum.py → push to GitHub immediately
  2. Run Stage 1 → push checkpoint metrics to GitHub (or memory if >5MB)
  3. Run Stage 2 → push
  4. Run Stage 3 → push
  5. Update FINDINGS.md with results → push
  6. Update stash

CHECKPOINT FORMAT:
  {model_state_dict, optimizer_state_dict, stage, epoch, metrics_history, best_val_acc}
  Saved as phase6_checkpoint_stageN.pt locally
  Metrics summary pushed to GitHub as phase6_results.json

RISK: Container timeout. Mitigations:
  - Each bash call trains max 30 epochs (estimated ~120s for 1000 samples)
  - Checkpoint saved BEFORE evaluation (eval can be re-run)
  - If approaching 180s, stop early and save
  - Resume from checkpoint in next bash call

COMPARISON TO PHASE 5 BASELINE:
  Phase 5 best: 56% token accuracy, 0/50 perfect traces (all ops from scratch)
  If curriculum Stage 3 exceeds this, curriculum learning is validated
  If not, the bottleneck is model capacity, not training order

WHAT THIS DOESN'T TEST:
  - Larger models (needs GPU)
  - Whether the model discovers parabolic encoding (needs attention visualization)
  - WASM fragment execution (Phase 7, needs much bigger model)

---
