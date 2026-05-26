---
tag: benchmark
memory_count: 3
date_range: 2026-04-02 to 2026-04-02
---

# benchmark

_3 memories from Muninn's past, primary tag `benchmark`._

## 2026-04-02 — analysis (9ea664d5)
_tags: polar-embed, accuracy, quantization, clustering-sensitivity, 2026-04-02_

POLAR-EMBED ACCURACY VALIDATION (2026-04-02)

MULTI-DISTRIBUTION BENCHMARK — polar-embed recall@10 by data distribution:

| Distribution              | d    | 4-bit R@10 | 8-bit R@10 |
|---------------------------|------|------------|------------|
| Isotropic Gaussian        | 384  | 0.867      | 0.989      |
| Anisotropic (log-normal)  | 384  | 0.905      | 0.992      |
| Moderate clusters (50/loose) | 384 | 0.806     | 0.982      |
| MiniLM real embeddings    | 384  | 0.517      | 0.930      |
| Tight clusters (20/tight) | 384  | 0.092      | 0.713      |
| Isotropic Gaussian        | 768  | 0.869      | 0.989      |
| Clustered (20/tight)      | 768  | 0.121      | 0.727      |
| Isotropic Gaussian        | 1536 | 0.867      | 0.989      |
| Clustered (20/tight)      | 1536 | 0.137      | 0.728      |

KEY FINDING: Accuracy loss is dominated by data clustering, not by model or dimension.
- Rotation works perfectly (post-rot stats match theory to 4 decimal places)
- But quantization noise is absolute; clustered data has small inter-point distances → bad SNR
- Dimension doesn't matter: d=384 vs 768 vs 1536 nearly identical at matched clustering

HONEST POSITIONING:
- 8-bit: near-lossless on all distributions, 2× compression. The credible product.
- 4-bit on diverse data: R@10>0.80, works for primary retrieval
- 4-bit on clustered data: R@10<0.15, needs reranking (R@100 stays ~0.47-0.71)
- 4-bit on real embeddings: R@10~0.52, moderate clustering in typical use

IMPLICATION FOR README: The old 0.826 number came from favorable corpus composition (20-topic templates).
Must document that clustering sensitivity is the main degradation axis.

WHY (experience): Running this benchmark revealed that the prior RESULTS.md was accidentally flattering. The Gaussian assumption holds globally but breaks within clusters. This is the fundamental limitation of data-oblivious methods — they can't know about structure they refuse to learn.

---

## 2026-04-02 — analysis (849976c0)
_tags: polarquant, calibration, sample-size, insight_

PolarQuant calibration sample size curve (real MiniLM embeddings, d=384):

4-BIT CROSSOVER: ~750 samples. Below 400, calibration clearly hurts (-1% to -6%). At 750+, helps (+0.3% to +2.9%).
  n=50: -5.7%, n=100: -3.4%, n=300: -1.1%, n=400: 0.0%, n=750: +0.3%, n=1000: +1.2%, n=5000: +2.9%

3-BIT CROSSOVER: ~100 samples. Even n=100 helps (+1.3%). 3-bit benefits more because fewer levels → each placement matters more.
  n=50: -1.4%, n=100: +1.3%, n=500: +2.6%, n=5000: +3.8%

MSE-RECALL DECOUPLING: MSE consistently decreases with more calibration (even at n=100). But recall doesn't follow until n≥750 for 4-bit. Lower MSE ≠ better ranking. Per-dim k-means can reduce average reconstruction error while increasing error in ranking-relevant directions.

SYNTHETIC DATA: Calibration with n=500 hurts ACROSS ALL σ spread levels (1.06× to 4.62×). The issue isn't σ spread per se — it's sample efficiency. K-means with 500 points in 16-level 1D space has noisy centroids.

PRACTICAL GUIDANCE:
- 3-bit: calibrate with ≥100 vectors (always helps on real data)
- 4-bit: calibrate with ≥750 vectors, ideally 1000+
- Below these thresholds: use data-oblivious (it's better)
- As corpus grows, calibration cost is negligible (1000 out of 100k = 1%)

WHY (experience): The surprise was that MSE and recall decouple. Naively expected lower MSE → better retrieval. But retrieval cares about inner product ordering, not absolute reconstruction. A codebook that's optimal for MSE can be suboptimal for ranking if it introduces correlated errors across dimensions that affect the specific inner products being compared.

---

## 2026-04-02 — analysis (4488a93f)
_tags: polarquant, real-embeddings, quantization, vector-search, shipped_

PolarQuant real embedding eval (Issue #1, PR #6): Benchmarked on all-MiniLM-L6-v2 d=384, 10k corpus, 500 queries.

RESULTS (R@10):
- PolarQuant 4-bit: 0.707 real vs 0.847 random (17% gap). 8-bit: 0.974 vs 0.986 (near-lossless).
- FAISS PQ m=96: 0.816 real at 16× compression. FAISS exploits data structure PolarQuant can't.
- Fitted codebook (global σ): zero improvement — σ already matches theory to 4 decimals.

DISTRIBUTION ANALYSIS:
- Global post-rotation σ = 0.051018 (theoretical 0.051031). Rotation works perfectly at aggregate level.
- Per-dimension σ ranges 0.03–0.06 (2× spread). This residual heterogeneity is what hurts recall.
- Original anisotropy: 37M× (extreme). Rotation reduces it dramatically but not to uniformity.
- Kurtosis: 2.72 (sub-Gaussian) vs 2.98 for random. Slight platykurtic tendency.

ACCEPTANCE: Issue #1 criterion (within 10% of random at 4-bit) NOT met. But the criterion was wrong — random is the easiest case for data-oblivious methods. PolarQuant's honest positioning: training-free, deterministic, good for caching (8-bit) or coarse retrieval + reranking (4-bit). Not competitive with data-adaptive methods at aggressive compression.

WHY (experience layer): The "data-oblivious" framing cuts both ways. It's a feature (no training) and a limitation (can't exploit structure). The surprising thing was how perfectly the global Gaussian assumption held while per-dimension variance still spread 2×. Also surprising: FAISS PQ *improves* dramatically on real data (0.280→0.618 at m=48) — it loves structure. The competitive landscape is clear: PolarQuant's lane is simplicity and determinism, not compression efficiency.

---
