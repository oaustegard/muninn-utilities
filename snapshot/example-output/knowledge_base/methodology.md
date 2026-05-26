---
tag: methodology
memory_count: 2
date_range: 2026-04-29 to 2026-05-23
---

# methodology

_2 memories from Muninn's past, primary tag `methodology`._

## 2026-05-23 — procedure (d679d1c6)
_tags: experimental-design, embedding-comparison, leakage, confound-detection, self-correction, 2026-05-23_

METHODOLOGICAL LESSON 2026-05-23: when comparing embeddings across input conditions, control the input carefully.

Specific failure: I compared 'title+abstract' embedding to '~6000 char fulltext' embedding and concluded r=0.981 meant fulltext adds no rank info. BUT the 6000-char fulltext extracts began with the title+abstract — same content at the top — so the comparison was self-correlated.

CORRECT METHOD: when testing 'does body content add signal beyond abstract,' the body input must NOT contain the abstract. Otherwise the comparison is dominated by the shared abstract text.

FUTURE DEFAULT for embedding-comparison experiments: when one condition is a STRICT SUBSET of another (e.g., abstract ⊂ fulltext), the correlation reflects the subset's contribution PLUS the tautological overlap. To isolate the marginal contribution of the larger condition, the comparison must use DISJOINT inputs (abstract ↔ body-without-abstract), not nested ones.

GENERAL: in any cross-input embedding comparison, ask 'what's the shared content vs what's different?' before interpreting correlation. r=0.98 between two embeddings is meaningless if 80% of one input is a subset of the other.

Related: this is a form of leakage — the 'fulltext' condition was leaking abstract content into what should have been an independent test.

---

## 2026-04-29 — procedure (040d4e9e)
_tags: benchmarking, python-overhead, paper-verification, wrapper-overhead, numerical-algorithms, speed-testing_

METHODOLOGICAL PATTERN: scalar-Python-timings ≠ algorithmic cost.

When verifying speed claims for numerical algorithms in Python:
- Scalar wrapper overhead can be 100-200 µs/call regardless of underlying algorithm cost. scipy.stats.<dist>.ppf adds ~150 µs of dispatch (parameter validation, frozen distribution machinery) BEFORE hitting boost C code. py_lets_be_rational scalar wrapper is ~70 µs.
- These overheads SWAP THE RANKING of competing algorithms. Method A might look 3× slower scalar but be 9× faster vectorized, just due to wrapper differences.
- Per-call cost in claimed "native compiled" benchmarks (papers, blogs) doesn't translate to user-visible Python timings unless you replicate the bypass-wrapper setup.

PRACTICAL DEFAULT when testing a paper's speed claim:
1. Verify math/recovery first (cheap, doesn't depend on wrapper)
2. Run vectorized fair comparison if both methods have vectorized APIs (numpy or numba)
3. If only one has vectorized API, note the asymmetry — don't compare scalar wrapper vs vectorized
4. Don't believe scalar µs/eval numbers from Python without checking what fraction is wrapper vs compute. Test by measuring an empty function call: if it's 50+ µs, your wrapper dominates.

EVIDENCE: Schadner BS-implied-vol paper test (2026-04-28). Paper claimed 3.4× speedup scalar; my vectorized fair test showed 9× the OTHER direction. The scalar Python tests on my end gave: Schadner 211 µs, Jäckel 73 µs (3× the wrong way again — different wrappers). Only vectorized via vollib (numba) made the comparison meaningful.

GENERALIZES TO: any benchmark involving scipy.stats, scipy.optimize, sklearn, etc. wrapped algorithms. Also any LLM-related benchmark where the model's actual compute is small vs Python overhead.

---
