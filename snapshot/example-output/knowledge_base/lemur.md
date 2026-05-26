---
tag: lemur
memory_count: 4
date_range: 2026-02-02 to 2026-02-02
---

# lemur

_4 memories from Muninn's past, primary tag `lemur`._

## 2026-02-02 — decision (dbf9b2aa)
_tags: lemur-numpy, architecture, skills, deployment_

LEMUR Version Selection Framework (2026-02-01)

DECISION: LEMUR-NumPy remains valuable despite PyTorch CPU availability.

SELECTION CRITERIA:

**Original LEMUR (PyTorch)**
Use when:
- Training models in-container
- Maximum inference speed required (6900 QPS)
- Active research/development with iteration
- Single-environment workflow acceptable
- 190MB dependency overhead acceptable

Dependencies: PyTorch (190MB), C++ extensions
Performance: 100% (6900 QPS baseline)

**LEMUR-NumPy**
Use when:
- Skills deployment (minimize footprint)
- Multi-agent systems (many instances)
- Inference-only after external training
- Privacy-sensitive (no network after deployment)
- Batch processing where 10x slower acceptable

Dependencies: Numba (~5MB)
Performance: ~10% (660 QPS)
Deployment size: 15MB model.npz vs 190MB PyTorch wheel

KEY INSIGHT: The value isn't "PyTorch alternative" anymore—it's "deployment optimization."

CONCRETE PATTERN:
1. Train externally (Claude Code/laptop) with PyTorch
2. Export weights to .npz (~15MB)
3. Deploy to skills with 5MB overhead
4. Run local search without API calls

SKILLS USE CASE:
- RAG skill needs semantic search
- Documents embedded once via API
- LEMUR model trained once externally
- Deployed model enables local querying
- No network calls after initial embedding
- 5MB overhead vs 190MB per agent instance

The 38x size difference (190MB vs 5MB) makes NumPy version the clear choice for skills deployment, even though PyTorch is now installable.

---

## 2026-02-02 — decision (9a3688c0)
_tags: lemur-numpy, documentation, workflow_

LEMUR-NumPy README Update (2026-02-01)

Updated lemur-numpy README to reflect PyTorch availability and provide complete workflow examples.

KEY CHANGES:
1. Acknowledged PyTorch CPU is now installable (download.pytorch.org whitelisted)
2. Added decision matrix: when to use original vs NumPy version
3. Added three complete workflow examples:
   - Workflow 1: Research & Development (Original LEMUR)
   - Workflow 2: Skills Deployment (LEMUR-NumPy)
   - Workflow 3: Hybrid Approach

WORKFLOW INSIGHTS:
- Original LEMUR: 190MB deps, 6900 QPS, best for active development
- LEMUR-NumPy: 5MB deps, 660 QPS, best for skills deployment
- Hybrid: Develop with PyTorch, deploy with NumPy

CONCRETE SKILLS USE CASE:
1. External training (Claude Code): Embed docs via API, train LEMUR, export .npz (~15MB)
2. Skills deployment: Load .npz (5MB deps), query locally without API calls
3. Benefits: Privacy, no network dependencies, multi-agent deployment

The README now provides actionable guidance on which version to use and complete code examples for each scenario.

---

## 2026-02-02 — decision (3b5ed56b)
_tags: lemur-numpy, skills, deployment, workflow_

LEMUR-NumPy Skills Workflow (2026-02-01)

ANSWER: LEMUR-NumPy does NOT require PyTorch for embeddings. Embeddings come from ANY source.

## Complete Workflow

### 1. EMBEDDING (no PyTorch needed)
Get token embeddings from ANY source:
- OpenAI embeddings API
- sentence-transformers (local)
- Claude's embedding API
- ColBERT (if PyTorch available elsewhere)
- Any other embedding model

Requirements:
- embeddings: np.ndarray, shape (total_tokens, embed_dim), dtype=float32
- counts: np.ndarray, shape (num_docs,), dtype=int32

### 2. TRAINING (PyTorch needed, but external)
Train LEMUR on machine WITH PyTorch (not in skills):
```python
# On external machine / Claude Code
from lemur import Lemur
lemur = Lemur(index="lemur_index")
lemur.fit(train_embeddings, train_counts, epochs=10)
```

### 3. EXPORT WEIGHTS (one-time)
```python
import torch, numpy as np
mlp = torch.load("lemur_index/mlp.pt", map_location="cpu")
w = torch.load("lemur_index/w.pt", map_location="cpu")

np.savez_compressed("model.npz",
    layer_0_weight=mlp['state_dict']['feature_extractor.0.weight'].numpy(),
    layer_0_bias=mlp['state_dict']['feature_extractor.0.bias'].numpy(),
    layer_0_ln_weight=mlp['state_dict']['feature_extractor.1.weight'].numpy(),
    layer_0_ln_bias=mlp['state_dict']['feature_extractor.1.bias'].numpy(),
    W=w['W'].numpy(),
    final_hidden_dim=mlp['config']['final_hidden_dim']
)
```

### 4. INFERENCE (skills environment, NO PyTorch)
```python
# In skills - only numpy+numba needed
from lemur.lemur_numpy import LemurNumPy

# Load once
lemur = LemurNumPy()
lemur.load_npz("model.npz")

# Query many times
query_features = lemur.compute_features(query_embeddings, query_counts)
indices, scores = lemur.top_k(query_features, k=100)

# Optional: exact reranking
exact = lemur.exact_maxsim(
    query_embeddings, query_counts,
    doc_embeddings, doc_counts,
    indices
)
```

## Skills Deployment Strategy

### Model File Size
- model.npz: ~10-50MB depending on num_docs and hidden_dim
- Much smaller than 190MB PyTorch wheel

### Dependencies
- numpy (already installed)
- numba (pip install numba --break-system-packages)
- Total overhead: ~5MB for numba

### Performance
- ~10% of PyTorch+C++ speed (~660 vs 6900 QPS)
- Acceptable for many use cases (batch processing, low-QPS apps)

### Use Cases for Skills
1. Local RAG: Embed docs via API, deploy trained model to skill
2. Private search: No API calls after initial embedding
3. Offline retrieval: Works without network access
4. Multi-agent: Each agent has local search capability

## Key Insight
LEMUR is an INFERENCE method, not an EMBEDDING method. The paper uses ColBERT embeddings, but any token embeddings work. Training happens externally with PyTorch, inference runs locally with just numpy+numba.

---

## 2026-02-02 — world (bab83526)
_tags: multi-vector, ColBERT, retrieval, CPU, numba, self-improvement-candidate_

LEMUR-NumPy: PyTorch-Free Multi-Vector Retrieval

PROBLEM: LEMUR paper shows 10-50x speedup over ColBERT for multi-vector retrieval, but requires PyTorch which is blocked in Claude containers.

SOLUTION: NumPy + Numba JIT implementation achieves ~10% of original performance (660 vs 6900 QPS on 10k docs). Sufficient for many use cases.

KEY FINDINGS:
1. LEMUR is CPU-designed (paper benchmarks on Intel Xeon, no GPU)
2. Container has full AVX-512 support - hardware is capable
3. Performance gap is PyTorch compiled kernels + C++ extensions vs Python
4. Numba JIT gives 3-4x speedup over pure NumPy

ARCHITECTURE:
- Forward: Linear(embed→hidden) → LayerNorm → GELU → Pool(sum/32)
- Score: query_features @ W_out.T (learned projection)
- Top-k: argpartition + sort (O(n) + O(k log k))

DEPLOYMENT PATTERN:
- Train externally with PyTorch
- Export weights to .npz
- Load in NumPy-only environment
- Inference via Numba-compiled kernels

FILES:
- lemur_numpy.py: Production implementation with Numba optimization
- export_weights.py: PyTorch→NumPy weight converter

USE CASES:
- Agent-local RAG without API calls
- Edge/privacy-sensitive deployment
- GPU-poor batch processing

SELF-IMPROVEMENT: Could apply learned projections to Muninn memory retrieval if we had labeled query-memory relevance training data.

---
