# MutBench-Adapt: Pathogen-Adaptive Hotspot Detection Tool

## Design Document v1.0

---

## 1. Problem Statement

No single scoring-detection combination works best across all pathogens (ANOVA interaction omega^2 = 0.285, 9/9 unique best combos). Feature importance varies dramatically: homoplasy dominates for Norovirus (RF importance 0.345) but is irrelevant for SARS-CoV-2 (0.070); pLDDT is the top feature for H3N2 (0.338) and MERS (0.294) but anti-predictive for EV-A71 (AUC=0.315). A pathogen-adaptive approach is required.

## 2. Architecture Overview

```
┌──────────────────────────────────────────────────────────────┐
│                      MutBench-Adapt                          │
│                                                              │
│  INPUT: MSA + protein structure (optional)                   │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ Layer 1: Feature Computation (10 features per site)    │  │
│  │ freq, entropy, rare_freq, homoplasy, esm2_llr,        │  │
│  │ plddt, sasa, grantham, dnds_proxy, semantic_change     │  │
│  └──────────────────────┬─────────────────────────────────┘  │
│                         │                                    │
│  ┌──────────────────────▼─────────────────────────────────┐  │
│  │ Layer 2: Pathogen Profile Matching + Feature Weighting │  │
│  │ Extract MSA profile → kNN match → weight vector w      │  │
│  └──────────────────────┬─────────────────────────────────┘  │
│                         │                                    │
│  ┌──────────────────────▼─────────────────────────────────┐  │
│  │ Layer 3: Hotspot Score & Detection                     │  │
│  │ Weighted z-score combination → threshold → output      │  │
│  └────────────────────────────────────────────────────────┘  │
│                                                              │
│  OUTPUT: per-position hotspot score + feature contributions  │
└──────────────────────────────────────────────────────────────┘
```

---

## 3. Layer 1: Feature Computation

### 3.1 Feature Definitions

For a protein sequence alignment with N sequences and L positions, compute for each position i:

| # | Feature | Formula | Source |
|---|---------|---------|--------|
| 1 | `freq` | f_i = (count of non-reference AA at i) / N | MSA |
| 2 | `entropy` | H_i = -sum_a p_a log2(p_a) | MSA |
| 3 | `rare_freq` | r_i = sum_{a: p_a < 0.01} p_a | MSA |
| 4 | `homoplasy` | h_i = observed_mutations_i / expected_under_tree_i | MSA + tree |
| 5 | `esm2_llr` | LLR_i = log P_wt(aa_i) - log P_mut(aa_i) from ESM-2 | ESM-2 model |
| 6 | `plddt` | pLDDT_i from AlphaFold2 predicted structure | AlphaFold DB |
| 7 | `sasa` | Solvent-accessible surface area at position i | Structure |
| 8 | `grantham` | G_i = mean Grantham distance across observed substitutions | MSA |
| 9 | `dnds_proxy` | dN/dS proxy = nonsynonymous_rate_i / synonymous_rate_i | MSA + codon alignment |
| 10 | `semantic_change` | S_i = cosine distance of ESM-2 embeddings before/after mutation | ESM-2 model |

### 3.2 Feature Matrix Output

```
F ∈ R^{L × 10}   # L positions, 10 features
```

### 3.3 Handling Missing Features

If a structural feature (plddt, sasa) is unavailable (no structure in AlphaFold DB):
- Set weight to 0 for that feature
- Renormalize remaining weights

If ESM-2 features (esm2_llr, semantic_change) are unavailable (sequence too long):
- Use ESM-2 with sliding window (window=1022 tokens, stride=511)
- Or set weight to 0 and renormalize

---

## 4. Layer 2: Pathogen Profile Matching

### 4.1 Pathogen Profile Vector

Extract a profile vector p from the MSA that captures alignment-level statistics relevant to feature importance prediction. Based on the `pahd_pathogen_profiles.csv` columns, use the following **13 MSA-level statistics**:

```python
profile_features = [
    "log_seq_length",       # log(protein length in AA)
    "log_n_unique",         # log(number of unique sequences)
    "diversity_ratio",      # n_unique / n_total
    "log_n_seq",            # log(total number of sequences)
    "E_mean",               # mean Shannon entropy across positions
    "E_std",                # std of Shannon entropy
    "E_zero_frac",          # fraction of zero-entropy (invariant) positions
    "P_mean",               # mean allele frequency of most common non-ref AA
    "P_std",                # std of allele frequency
    "Exrare_gini",          # Gini coefficient of rare variant distribution
    "Exrare_skew",          # skewness of rare variant distribution
    "adaptive_density",     # fraction of known adaptive sites (if GT available; else 0)
    "constrained_density",  # fraction of known constrained sites (if GT available; else 0)
]
```

For a novel pathogen where `adaptive_density` and `constrained_density` are unknown, set both to 0. The remaining 11 features suffice for matching (demonstrated below).

Profile vector:
```
p ∈ R^{13}
```

### 4.2 Reference Profile Database

Build from the 12 known pathogens (9 original + 3 extended):

```python
KNOWN_PATHOGENS = [
    "SARS-CoV-2", "H3N2", "Norovirus", "HIV-1", "Dengue",
    "RSV", "Influenza_B", "MERS", "HCV",
    "Zika", "Rabies", "EV-A71"
]

# Profile matrix: P_ref ∈ R^{12 × 13}
# Weight matrix: W_ref ∈ R^{12 × 10} (RF importance per pathogen per feature)
```

### 4.3 Profile Matching Algorithm

**Step 1: Standardize profiles**

Compute z-scores using the reference database statistics:

```
p_std = (p - mu_ref) / sigma_ref
```

where mu_ref, sigma_ref are the column-wise mean and std of P_ref.

**Step 2: Compute distances to all reference pathogens**

Use Euclidean distance in standardized profile space:

```
d_j = ||p_std - P_ref_std[j]||_2   for j = 1..12
```

**Step 3: kNN weight interpolation**

Use k=3 nearest neighbors with inverse-distance weighting:

```python
def get_feature_weights(p_std, P_ref_std, W_ref, k=3):
    distances = [euclidean(p_std, P_ref_std[j]) for j in range(12)]
    nn_indices = argsort(distances)[:k]
    nn_distances = [distances[i] for i in nn_indices]

    # Inverse-distance weights (with epsilon to avoid division by zero)
    eps = 1e-8
    inv_d = [1.0 / (d + eps) for d in nn_distances]
    alpha = [w / sum(inv_d) for w in inv_d]  # normalize to sum=1

    # Interpolate feature weights
    w = sum(alpha[i] * W_ref[nn_indices[i]] for i in range(k))
    return w  # shape: (10,)
```

### 4.4 Handling Features with Inverse Associations (AUC < 0.5)

Some features are anti-predictive for certain pathogens (e.g., freq AUC=0.262 for RSV, plddt AUC=0.162 for MERS). The RF importance captures the importance regardless of direction.

To handle directionality:

**Step 1**: For each reference pathogen j and feature f, store the sign of the Spearman rho from per-feature AUC data:

```python
# Sign matrix: S_ref ∈ R^{12 × 10}, entries in {-1, 0, +1}
S_ref[j, f] = sign(spearman_rho[j, f])
```

**Step 2**: Interpolate signs using the same kNN weights:

```python
s = sum(alpha[i] * S_ref[nn_indices[i]] for i in range(k))
# s ∈ R^{10}, values in [-1, +1]
# Apply sign: if s[f] < 0, negate the feature before combination
```

This ensures that for a novel pathogen similar to RSV, frequency would be used as a negative predictor (higher freq = less likely hotspot).

### 4.5 Feature Weight Table (from RF importance, 9 pathogens with data)

| Feature | SARS2 | H3N2 | Noro | HIV-1 | Dengue | RSV | Flu-B | MERS | HCV |
|---------|-------|------|------|-------|--------|-----|-------|------|-----|
| freq | 0.012 | 0.064 | 0.092 | 0.091 | 0.056 | 0.108 | 0.133 | 0.034 | 0.100 |
| entropy | 0.010 | 0.077 | 0.097 | 0.127 | 0.060 | 0.112 | 0.101 | 0.057 | 0.104 |
| rare_freq | 0.014 | 0.066 | 0.022 | 0.036 | 0.036 | 0.105 | 0.067 | 0.062 | 0.036 |
| homoplasy | 0.070 | 0.069 | **0.345** | 0.143 | **0.236** | 0.044 | 0.167 | 0.136 | 0.139 |
| esm2_llr | **0.331** | 0.070 | 0.133 | **0.214** | 0.101 | **0.173** | 0.058 | 0.105 | 0.098 |
| plddt | **0.286** | **0.338** | 0.060 | 0.114 | **0.231** | 0.144 | 0.096 | **0.294** | 0.054 |
| sasa | 0.202 | 0.072 | 0.114 | 0.074 | 0.083 | 0.084 | 0.061 | 0.055 | 0.097 |
| grantham | 0.015 | 0.064 | 0.026 | 0.061 | 0.084 | 0.055 | 0.081 | 0.071 | 0.116 |
| dnds_proxy | 0.021 | 0.075 | 0.078 | 0.076 | 0.060 | 0.106 | 0.132 | 0.054 | 0.146 |
| semantic_change | 0.039 | 0.105 | 0.033 | 0.067 | 0.054 | 0.070 | 0.105 | 0.134 | 0.112 |

Bold = top-2 features per pathogen. No single feature dominates across all pathogens.

---

## 5. Layer 3: Hotspot Score Computation

### 5.1 Feature Normalization

For each feature f across all L positions, compute z-scores:

```
z_{i,f} = (F_{i,f} - mean_f) / std_f
```

Result: Z ∈ R^{L × 10}

### 5.2 Directional Adjustment

Apply the interpolated sign vector s from Layer 2:

```
Z'_{i,f} = sign(s_f) * z_{i,f}
```

After this step, higher Z' always means "more hotspot-like" regardless of whether the raw feature was positively or negatively associated.

For features with |s_f| < 0.2 (ambiguous direction), set weight to 0 (feature is uninformative for this pathogen type).

### 5.3 Weighted Score Aggregation

Compute the per-position hotspot score using the weight vector w from Layer 2:

```
score_i = sum_{f=1}^{10} w_f * Z'_{i,f}
```

Equivalently in vector form:
```
score = Z' @ w    # shape: (L,)
```

### 5.4 Rank-Based Alternative

As a robustness check, also offer a rank-based aggregation:

```python
def rank_aggregate(F, w, s):
    L, n_features = F.shape
    ranks = np.zeros_like(F)
    for f in range(n_features):
        if s[f] >= 0:
            ranks[:, f] = rankdata(F[:, f]) / L  # higher value = higher rank
        else:
            ranks[:, f] = 1.0 - rankdata(F[:, f]) / L  # invert
    score = ranks @ w
    return score
```

### 5.5 Hotspot Detection Threshold

Three threshold strategies:

**Strategy A: Top-K percentile**
```python
threshold = np.percentile(score, 100 * (1 - expected_hotspot_fraction))
# expected_hotspot_fraction from pathogen profile (adaptive_density)
# default: 0.05 (top 5%)
hotspots = score >= threshold
```

**Strategy B: Z-score cutoff**
```python
score_z = (score - np.mean(score)) / np.std(score)
hotspots = score_z >= 1.645  # one-tailed 95%
```

**Strategy C: Adaptive threshold from profile**

Use the matched pathogen's `adaptive_density` to set the expected fraction:

```python
k_nearest_densities = [profiles[j]["adaptive_density"] for j in nn_indices]
expected_frac = sum(alpha[i] * k_nearest_densities[i] for i in range(k))
if expected_frac < 0.01:
    expected_frac = 0.05  # floor
threshold = np.percentile(score, 100 * (1 - expected_frac))
```

**Default**: Strategy A with 5% unless adaptive_density is known.

---

## 6. Output Format

```python
@dataclass
class MutBenchAdaptResult:
    positions: np.ndarray          # shape (L,), 0-indexed position indices
    scores: np.ndarray             # shape (L,), per-position hotspot scores
    is_hotspot: np.ndarray         # shape (L,), boolean
    feature_contributions: np.ndarray  # shape (L, 10), w_f * Z'_{i,f}
    weights: np.ndarray            # shape (10,), feature weights used
    signs: np.ndarray              # shape (10,), feature direction signs
    matched_pathogens: list        # top-k matched pathogens with distances
    threshold: float               # threshold used
    threshold_strategy: str        # "topk" | "zscore" | "adaptive"
```

---

## 7. Pseudocode: Full Pipeline

```python
def mutbench_adapt(msa_path, structure_path=None, k=3, threshold_strategy="topk"):
    """
    MutBench-Adapt: Pathogen-adaptive hotspot detection.

    Parameters
    ----------
    msa_path : str
        Path to MSA file (FASTA format).
    structure_path : str, optional
        Path to PDB/mmCIF file for structural features.
    k : int
        Number of nearest pathogen neighbors (default: 3).
    threshold_strategy : str
        "topk" | "zscore" | "adaptive"

    Returns
    -------
    MutBenchAdaptResult
    """
    # ── Layer 1: Feature Computation ──
    msa = read_msa(msa_path)
    structure = read_structure(structure_path) if structure_path else None

    F = np.zeros((msa.n_positions, 10))
    F[:, 0] = compute_freq(msa)
    F[:, 1] = compute_entropy(msa)
    F[:, 2] = compute_rare_freq(msa, threshold=0.01)
    F[:, 3] = compute_homoplasy(msa)
    F[:, 4] = compute_esm2_llr(msa)
    F[:, 5] = compute_plddt(msa, structure)       # may be NaN
    F[:, 6] = compute_sasa(msa, structure)         # may be NaN
    F[:, 7] = compute_grantham(msa)
    F[:, 8] = compute_dnds_proxy(msa)
    F[:, 9] = compute_semantic_change(msa)

    available = ~np.isnan(F).all(axis=0)  # shape (10,), True if feature is available

    # ── Layer 2: Profile Matching ──
    profile = extract_profile(msa)          # shape (13,)
    profile_std = (profile - MU_REF) / SIGMA_REF

    distances = [euclidean(profile_std, P_REF_STD[j]) for j in range(N_REF)]
    nn_idx = np.argsort(distances)[:k]
    nn_dist = np.array([distances[j] for j in nn_idx])

    alpha = (1.0 / (nn_dist + 1e-8))
    alpha /= alpha.sum()

    # Interpolate weights and signs
    w = sum(alpha[i] * W_REF[nn_idx[i]] for i in range(k))   # (10,)
    s = sum(alpha[i] * S_REF[nn_idx[i]] for i in range(k))   # (10,)

    # Zero out unavailable features and renormalize
    w[~available] = 0.0
    if w.sum() > 0:
        w /= w.sum()

    # Zero out ambiguous-direction features
    w[np.abs(s) < 0.2] = 0.0
    if w.sum() > 0:
        w /= w.sum()

    # ── Layer 3: Score Computation ──
    # Z-score normalize each feature
    Z = np.zeros_like(F)
    for f in range(10):
        if available[f]:
            mu_f, std_f = np.nanmean(F[:, f]), np.nanstd(F[:, f])
            if std_f > 0:
                Z[:, f] = (F[:, f] - mu_f) / std_f

    # Apply directional sign
    Z_prime = Z * np.sign(s)

    # Weighted combination
    scores = Z_prime @ w                  # (L,)
    contributions = Z_prime * w[None, :]  # (L, 10)

    # Threshold
    if threshold_strategy == "topk":
        frac = 0.05
        thr = np.percentile(scores, 100 * (1 - frac))
    elif threshold_strategy == "zscore":
        score_z = (scores - scores.mean()) / scores.std()
        thr = 1.645
        scores = score_z  # replace with z-scored version
    elif threshold_strategy == "adaptive":
        densities = [PROFILES[nn_idx[i]]["adaptive_density"] for i in range(k)]
        frac = max(0.01, sum(alpha[i] * densities[i] for i in range(k)))
        thr = np.percentile(scores, 100 * (1 - frac))

    is_hotspot = scores >= thr

    return MutBenchAdaptResult(
        positions=np.arange(msa.n_positions),
        scores=scores,
        is_hotspot=is_hotspot,
        feature_contributions=contributions,
        weights=w,
        signs=s,
        matched_pathogens=[(PATHOGEN_NAMES[nn_idx[i]], distances[nn_idx[i]], alpha[i])
                           for i in range(k)],
        threshold=thr,
        threshold_strategy=threshold_strategy,
    )
```

---

## 8. Key Design Decisions

### D1: Why 13 profile features (not more/fewer)?

The 13 features capture three dimensions:
1. **Scale** (log_seq_length, log_n_seq, log_n_unique): protein size and sampling depth
2. **Diversity** (diversity_ratio, E_mean, E_std, E_zero_frac, P_mean, P_std): evolutionary divergence pattern
3. **Evolutionary mode** (Exrare_gini, Exrare_skew): whether variation is dominated by a few high-frequency mutations (low diversity, high skew = founder-effect-dominated like SARS-CoV-2) or distributed (high diversity, low skew = high-diversity like HIV-1)
4. **Prior knowledge** (adaptive_density, constrained_density): optional, set to 0 for novel pathogens

### D2: Why k=3 for kNN?

With 12 reference pathogens:
- k=1 is too sensitive to noise (single pathogen may have atypical importance weights)
- k=5 averages over nearly half the database, losing specificity
- k=3 balances robustness and specificity
- In LOPO evaluation, try k ∈ {1, 2, 3, 5} and select by mean MCC

### D3: Why weighted z-score over rank aggregation?

- Z-score preserves magnitude information (a position 5 std above the mean is more informative than one 1 std above)
- Rank aggregation is more robust to outliers but loses discrimination
- Default: z-score. Rank-based offered as fallback for heavy-tailed distributions.

### D4: Why inverse-distance weighting over learned regression?

- With only 12 reference pathogens (9 with RF importance), there are not enough training points for a regression model from profile to weights
- Inverse-distance kNN is non-parametric, requires no training, and works with small reference sets
- As the reference database grows (>30 pathogens), could switch to a lightweight model (e.g., Ridge regression from profile to weight vector)

### D5: Ambiguous direction cutoff (|s| < 0.2)

- If the interpolated sign is near zero, the feature has conflicting directionality among neighbors
- Setting weight to 0 avoids introducing noise
- 0.2 chosen because with k=3 and binary signs, the smallest non-zero |s| is 1/3 = 0.33

---

## 9. Evaluation Plan

### 9.1 LOPO (Leave-One-Pathogen-Out) Cross-Validation

For each of the 12 pathogens:
1. Remove it from the reference database (use remaining 11)
2. Run MutBench-Adapt on its MSA
3. Evaluate against Layer A ground truth using MCC

```python
def lopo_evaluation():
    results = {}
    for target in KNOWN_PATHOGENS:
        # Build reference from all except target
        ref_pathogens = [p for p in KNOWN_PATHOGENS if p != target]
        P_ref, W_ref, S_ref = build_reference(ref_pathogens)

        # Run MutBench-Adapt
        result = mutbench_adapt(
            msa_path=MSA_PATHS[target],
            structure_path=STRUCTURE_PATHS.get(target),
            k=min(3, len(ref_pathogens)),
            reference=(P_ref, W_ref, S_ref),
        )

        # Evaluate
        gt = load_ground_truth(target, layer="A")
        mcc = matthews_corrcoef(gt, result.is_hotspot)
        results[target] = {
            "mcc": mcc,
            "matched": result.matched_pathogens,
            "weights": result.weights,
        }
    return results
```

### 9.2 Baselines for Comparison

| Baseline | Description |
|----------|-------------|
| **Oracle** | Best individual scoring-detection combo per pathogen (from MutBench results) |
| **Global-Best** | Single best combo across all pathogens |
| **FreqThresh** | Frequency > threshold (0.05), the simplest approach |
| **Random** | Random assignment at expected hotspot rate |
| **Equal-Weight** | MutBench-Adapt with uniform weights (1/10 each), no adaptation |
| **Per-Pathogen RF** | RF trained on same pathogen (upper bound, requires labeled data) |

### 9.3 Ablation Studies

| Ablation | What it tests |
|----------|--------------|
| No sign correction | Remove directional adjustment (all features treated as positive) |
| No ambiguity filter | Keep features with |s| < 0.2 |
| k=1 only | Nearest-neighbor only, no interpolation |
| Profile subset: scale only | Only use log_seq_length, log_n_seq, log_n_unique |
| Profile subset: diversity only | Only use E_mean, E_std, P_mean, P_std, diversity_ratio |
| Drop one feature | 10 runs, each dropping one of the 10 features |

### 9.4 Metrics

Primary: **MCC** (Matthews Correlation Coefficient) against Layer A ground truth

Secondary:
- AUROC (threshold-independent)
- Precision@k (where k = number of true hotspots)
- Mean rank of true hotspots

### 9.5 Statistical Tests

- Paired Wilcoxon signed-rank test (MutBench-Adapt vs each baseline, n=12 pathogens)
- Report effect size (rank-biserial correlation)
- Friedman test across all methods

---

## 10. Implementation Plan

### Phase 1: Core Implementation

```
mutbench_adapt/
├── __init__.py
├── features/
│   ├── __init__.py
│   ├── sequence_features.py    # freq, entropy, rare_freq, dnds_proxy
│   ├── phylo_features.py       # homoplasy
│   ├── structure_features.py   # plddt, sasa
│   ├── llm_features.py         # esm2_llr, semantic_change
│   └── substitution_features.py # grantham
├── profile/
│   ├── __init__.py
│   ├── extractor.py            # extract_profile(msa) → R^13
│   ├── database.py             # load/save reference profiles + weights
│   └── matcher.py              # kNN matching + weight interpolation
├── scoring/
│   ├── __init__.py
│   ├── combiner.py             # weighted z-score / rank aggregation
│   └── threshold.py            # topk / zscore / adaptive
├── pipeline.py                 # mutbench_adapt() main function
├── evaluate.py                 # LOPO evaluation
└── reference_data/
    ├── profiles.json           # 12 pathogen profiles
    ├── weights.json            # RF importance weights
    └── signs.json              # Spearman rho signs
```

### Phase 2: Evaluation

1. Run LOPO on 12 pathogens
2. Compare against baselines
3. Run ablations
4. Generate figures: radar plots of weights, profile PCA, MCC comparison bar chart

### Phase 3: Integration

1. Write Ch5 section for dissertation
2. Package as standalone tool with CLI
3. Add to MutBench framework

---

## 11. Expected Outcomes

Based on the RF CV AUC data (range: 0.606 for SARS-CoV-2 to 0.899 for Norovirus), the per-pathogen RF models show that the 10 features contain sufficient signal. MutBench-Adapt should:

1. **Outperform any single fixed method** (Global-Best), since it adapts weights per pathogen
2. **Approach but not reach the Oracle**, since Oracle uses labeled data for method selection
3. **Substantially outperform FreqThresh** (current MCC: 0.248) and Random (MCC ~0.001)
4. The key question is how close LOPO MCC gets to Per-Pathogen RF AUC (the labeled upper bound)

Conservative estimate: mean LOPO MCC of 0.30-0.45 across 12 pathogens (above FreqThresh 0.248, below Oracle).

---

## 12. Risk Analysis

| Risk | Impact | Mitigation |
|------|--------|------------|
| Profile space too sparse with 12 pathogens | Poor kNN matching for dissimilar novel pathogens | Use k=3+ to smooth; add more reference pathogens over time |
| RF importance overfits per-pathogen | LOPO weights may be suboptimal | Use permutation importance instead of Gini importance |
| Ground truth heterogeneity across pathogens | MCC comparison unfair across pathogens | Report per-pathogen and use rank-based summary |
| Feature correlation (freq-entropy rho=0.97, freq-dnds rho=0.87) | Redundant features inflate certain directions | Consider PCA on correlated feature groups, or use only one from each correlated pair |
| Ambiguous-direction filter too aggressive | Removes useful features | Test |s| thresholds in {0.0, 0.1, 0.2, 0.3} during LOPO |

### Correlated Feature Groups (from correlation matrix)

```
Group 1 (frequency-based):  freq, entropy, dnds_proxy     (pairwise r > 0.85)
Group 2 (rare variation):   rare_freq                      (r ~ 0.54-0.68 with Group 1)
Group 3 (evolutionary):     homoplasy                      (r ~ 0.15-0.23 with Group 1)
Group 4 (protein LLM):      esm2_llr                       (r ~ 0.11 with Group 1)
Group 5 (structure):         plddt, sasa                    (r = -0.19 with each other)
Group 6 (substitution):     grantham, semantic_change       (r = 0.52 with each other)
```

Option: reduce to 6 features (one per group) if multicollinearity degrades performance. Test in LOPO.

---

## 13. API Design

### CLI Interface

```bash
# Basic usage
mutbench-adapt --msa spike.fasta --output results.tsv

# With structure
mutbench-adapt --msa spike.fasta --structure spike.pdb --output results.tsv

# Custom parameters
mutbench-adapt --msa spike.fasta --k 5 --threshold adaptive --output results.tsv

# LOPO evaluation
mutbench-adapt evaluate --data-dir ./data/ --output lopo_results.csv
```

### Python API

```python
from mutbench_adapt import MutBenchAdapt

# Initialize with reference database
adapt = MutBenchAdapt(reference_dir="./reference_data/")

# Run on new pathogen
result = adapt.predict("spike.fasta", structure="spike.pdb", k=3)

# Inspect results
print(f"Detected {result.is_hotspot.sum()} hotspots out of {len(result.positions)} positions")
print(f"Matched pathogens: {result.matched_pathogens}")
print(f"Top feature: {FEATURE_NAMES[np.argmax(result.weights)]}")

# Export
result.to_tsv("results.tsv")
result.plot_scores("scores.png")
```
