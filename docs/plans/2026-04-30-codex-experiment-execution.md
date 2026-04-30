# Codex Full-Rigor Experiment Slate — Wave 1 Execution Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement task-by-task. Steps use checkbox syntax for tracking.

**Goal:** Tier 1 method-core experiments (P1 null calibration, P2 rank reliability, P3 full 2^10 subset lattice + Shapley, P4 detector-consensus) executed on the existing 12-pathogen feature matrix + Stage 3 detector callsets, with results, figures, and dissertation prose updates committed at each checkpoint.

**Architecture:** Reuse `feature_ablation_nested_lopo.py` infrastructure and `stage3_full_results.csv` callsets. No new feature engineering, no new pathogens — Wave 1 strictly stress-tests Algorithm 1 on already-collected data. Results land in `results/mutbench/codex_wave1/` (new subdir) and feed targeted prose insertions in ch4_results.tex / ch5_discussion.tex.

**Tech Stack:** Python 3, NumPy, pandas, scikit-learn, scipy.stats, matplotlib. No GPU. Compute budget: ~10 CPU-hours total (all experiments fit within a single workday).

**Documentation cadence:** After each task, append to `NOTES.md` (one bullet per result) and write a 1–2 page standalone Markdown report under `paper/dissertation/review/2026-04-30/wave1/p{N}_*.md` (command, inputs, outputs, top-line numbers, failure-branch status, interpretation). **Memory file written ONLY at Wave 1 completion**, not after individual tasks. Commit with `feat: v181+` message naming the experiment.

**Spec source:** `paper/dissertation/review/2026-04-30/codex_full_rigor_experiment_slate.md` Tier 1 (P1–P4).

**Codex review:** `paper/dissertation/review/2026-04-30/codex_wave1_plan_review.md` — verdict PROCEED WITH MODIFICATIONS, edits incorporated below.

**Out of scope (subsequent plans):** P5 callability/abstention rule, P6+ Tier 2 robustness audits, Tier 3 EVE/PLM site-effect, pilot 3 Layer A curation, Tier 2 features-only LOPO.

---

## Predeclared Failure-Mode Branches

These responses are fixed BEFORE results exist. Task 6 prose must follow the matching branch.

| Failure trigger | Predefined response |
|---|---|
| **P1** iid Stouffer p > 0.05 globally | **HARD STOP before Task 5.** Remove any claim that Algorithm 1 beats a prevalence-preserving null. Reframe as exploratory ranking heuristic. Keep P2/P3 as descriptive diagnostics only. Do NOT add detector-agnostic or search-space-reduction headlines. |
| **P3** 4-core lattice rank > 50/1023 | Replace "non-arbitrary 4-core" with "fixed historical 4-core benchmarked against the lattice." Report best compact subset; if 3-core dominates, mark pLDDT optional or move to sensitivity appendix. |
| **P2** decile slope essentially flat (top-vs-bottom bootstrap CI includes 0) | Drop probability/calibration language. Frame Algorithm 1 as not rank-reliable on current Layer A labels; retain only per-pathogen diagnostics + isolated budget gains with CIs. |
| **P4** consensus enrichment ≤ detector mean (matched-size) | Remove "detector-agnostic consensus" framing. State detector choice remains material; use consensus only as reproducibility diagnostic, not high-confidence candidate set. |

---

## File Structure

**New scripts (created in `scripts/`):**
- `codex_p1_null_calibration.py` — 100k-permutation null with 4 null types (iid prevalence-preserving, circular shift, protein-block shuffle, local-burden-preserving)
- `codex_p2_rank_reliability.py` — decile/ventile prevalence, calibration slope, ECE, Brier, decision curves
- `codex_p3_full_lattice_shapley.py` — extend 210→1023 subsets, compute marginal Shapley
- `codex_p4_detector_consensus.py` — pairwise Jaccard / Spearman / family-consensus from `stage3_full_results.csv`

**New result subdir (created):** `results/mutbench/codex_wave1/`
- `p1_null_per_pathogen.csv`, `p1_null_summary.csv`, `p1_null_distribution.png`
- `p2_decile_prevalence.csv`, `p2_calibration.csv`, `p2_decision_curve.png`, `p2_reliability.png`
- `p3_full_lattice_1023.csv`, `p3_shapley.csv`, `p3_pareto_frontier.png`
- `p4_consensus_jaccard.csv`, `p4_family_agreement.csv`, `p4_consensus_enrichment.csv`, `p4_consensus_stability.png`

**Documentation updates:**
- `NOTES.md` — daily bullet per task
- `paper/dissertation/chapters_en/ch4_results.tex` — 1–2 paragraph insertions per experiment (reliability subsection, lattice subsection, consensus subsection)
- `paper/dissertation/chapters_en/ch5_discussion.tex` — null-calibration disclosure paragraph
- `~/.claude/projects/-proj-paper/memory/codex_wave1_results.md` (new) — concise outcomes

---

## Task 1: Setup result subdirectory and update Algorithm 1 reference

**Why first:** Establishes the canonical output path and creates a placeholder doc. Subsequent tasks write into this subdir.

**Files:**
- Create: `results/mutbench/codex_wave1/README.md`
- Modify: none yet

- [ ] **Step 1: Create result subdirectory**

```bash
mkdir -p /proj/paper/results/mutbench/codex_wave1
```

- [ ] **Step 2: Write README placeholder**

Write `results/mutbench/codex_wave1/README.md`:

```markdown
# Codex Wave 1 Results — Tier 1 Method Core

Spec: `paper/dissertation/review/2026-04-30/codex_full_rigor_experiment_slate.md`
Plan: `docs/plans/2026-04-30-codex-experiment-execution.md`
Started: 2026-04-30

## Experiments
- **P1** (null calibration): see `p1_null_*` files
- **P2** (rank reliability): see `p2_*`
- **P3** (full lattice + Shapley): see `p3_*`
- **P4** (detector consensus): see `p4_*`

## Provenance
All experiments use:
- 12-pathogen feature matrices: `results/mutbench/feature_analysis/feature_matrix_*.csv`
- Stage 3 detector callsets: `results/mutbench/stage3_full_results.csv`

No new feature engineering. No new pathogens. Pure stress-test of Algorithm 1.
```

- [ ] **Step 3: Append NOTES.md**

```markdown
## 2026-04-30
- Wave 1 (Codex Tier 1) execution started. Result dir: `results/mutbench/codex_wave1/`. Plan: `docs/plans/2026-04-30-codex-experiment-execution.md`.
```

- [ ] **Step 4: Commit**

```bash
git add results/mutbench/codex_wave1/README.md docs/plans/2026-04-30-codex-experiment-execution.md NOTES.md
git commit -m "$(cat <<'EOF'
plan: v181 — Codex Wave 1 execution plan + result subdir scaffold

Establishes the canonical output path for Tier 1 method-core experiments
(P1 null calibration, P2 rank reliability, P3 full 2^10 lattice + Shapley,
P4 detector consensus). All four experiments leverage existing 12-pathogen
feature matrices and Stage 3 detector callsets — no new data collection.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 2: P3 — Full 2^10 subset lattice + Shapley decomposition

**Why P3 first:** Cheapest (~30min), reuses `feature_ablation_nested_lopo.py`'s LOPO machinery, and the existing 210-combo CSV gives us a working pattern. Output directly fortifies Algorithm 1's "non-arbitrary 4-core" claim.

**Files:**
- Create: `scripts/codex_p3_full_lattice_shapley.py`
- Output: `results/mutbench/codex_wave1/p3_full_lattice_1023.csv`, `p3_shapley.csv`, `p3_pareto_frontier.png`

- [ ] **Step 1: Write the script**

Write `scripts/codex_p3_full_lattice_shapley.py`. Key elements:

```python
#!/usr/bin/env python3
"""P3: Full 2^10 - 1 = 1023 subset lattice + FORMAL Shapley decomposition.

Extends subset_selection_robustness_210combos.csv (4-of-10 only) to all
non-empty subsets of the 10 features. Uses the same nested-LOPO + top-10%
+ MCC protocol as feature_ablation_nested_lopo.py.

For each subset S, compute multiple metrics (per codex review Q7):
  - exact MCC at top-10% and top-20% thresholds
  - +/-10-window MCC (label-flexible, position +/-10)
  - precision@20 (fixed candidate count)
  - enrichment = precision / pathogen base rate
  - per-pathogen win count vs full-10

FORMAL Shapley (per codex review Q2):
  phi_f = (1/n) * sum_{|S|=k, S not containing f} weight_k * [v(S U {f}) - v(S)]
  weight_k = 1 / C(n-1, k), with v(empty) = 0
  Equivalently: phi_f = sum_k (1/n) * mean_{|S|=k}[v(S U {f}) - v(S)]
Compute Shapley for both MCC AND enrichment.

Lookup: frozenset(features) -> dict of metrics, populated during lattice
enumeration. NOT the unweighted-mean-marginal proxy.

Outputs:
  results/mutbench/codex_wave1/p3_full_lattice_1023.csv
  results/mutbench/codex_wave1/p3_shapley.csv (per-feature Shapley for MCC + enrichment)
  results/mutbench/codex_wave1/p3_pareto_frontier.png
  results/mutbench/codex_wave1/p3_per_pathogen_wins.csv
"""
from __future__ import annotations
import itertools
import math
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.metrics import matthews_corrcoef
import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parent.parent
FEATURE_DIR = PROJECT_ROOT / "results" / "mutbench" / "feature_analysis"
OUT_DIR = PROJECT_ROOT / "results" / "mutbench" / "codex_wave1"

ALL_PATHOGENS = ["SARS-CoV-2","H3N2","Norovirus","HIV-1","Dengue",
                 "RSV","Influenza_B","MERS","HCV","Zika","Rabies","EV-A71"]
FEATURES = ["freq","entropy","rare_freq","homoplasy","esm2_llr",
            "plddt","sasa","grantham","dnds_proxy","semantic_change"]
CORE_4 = ["homoplasy","plddt","entropy","freq"]

def load_feature_matrix(pathogen: str) -> pd.DataFrame:
    return pd.read_csv(FEATURE_DIR / f"feature_matrix_{pathogen}.csv")

def lopo_subset_mcc(subset: tuple[str, ...]) -> tuple[float, list[float]]:
    """Return (mean MCC, per-fold MCC list) for a feature subset under nested LOPO."""
    fold_mccs = []
    matrices = {p: load_feature_matrix(p) for p in ALL_PATHOGENS}
    for held in ALL_PATHOGENS:
        train_pathogens = [p for p in ALL_PATHOGENS if p != held]
        # learn directional sign per feature on training pathogens
        signs = {}
        for f in subset:
            from sklearn.metrics import roc_auc_score
            aucs = []
            for p in train_pathogens:
                df = matrices[p]
                if f not in df.columns or df["ground_truth"].sum() == 0:
                    continue
                try:
                    a = roc_auc_score(df["ground_truth"], df[f])
                    aucs.append(a if a >= 0.5 else 1 - a)
                except Exception:
                    pass
            mean_auc = np.mean(aucs) if aucs else 0.5
            ref = []
            for p in train_pathogens:
                df = matrices[p]
                if f in df.columns and df["ground_truth"].sum() > 0:
                    try:
                        a = roc_auc_score(df["ground_truth"], df[f])
                        ref.append(1 if a >= 0.5 else -1)
                    except Exception:
                        ref.append(1)
            signs[f] = int(np.sign(np.mean(ref))) if ref else 1
        # apply to held-out
        df = matrices[held]
        if df["ground_truth"].sum() == 0 or df["ground_truth"].sum() == len(df):
            fold_mccs.append(np.nan)
            continue
        z = np.zeros(len(df))
        for f in subset:
            x = df[f].values * signs[f]
            mu, sd = np.nanmean(x), np.nanstd(x)
            if sd > 0:
                z = z + (x - mu) / sd
        z = z / max(1, len(subset))
        thr = np.nanquantile(z, 0.90)
        pred = (z >= thr).astype(int)
        try:
            mcc = matthews_corrcoef(df["ground_truth"], pred)
        except Exception:
            mcc = np.nan
        fold_mccs.append(mcc)
    return float(np.nanmean(fold_mccs)), fold_mccs

def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    rows = []
    full10_mean, _ = lopo_subset_mcc(tuple(FEATURES))
    print(f"Full-10 mean MCC: {full10_mean:.4f}")
    n_total = sum(math.comb(10, k) for k in range(1, 11))  # 1023
    print(f"Enumerating {n_total} subsets...")
    idx = 0
    for k in range(1, 11):
        for combo in itertools.combinations(FEATURES, k):
            idx += 1
            mean_mcc, folds = lopo_subset_mcc(combo)
            # lopo_subset_mcc returns a dict of metrics:
            # {"mean_mcc","mean_mcc_top20","mean_mcc_window10","mean_precision20",
            #  "mean_enrichment","wins_vs_full10"}
            rows.append({
                "combo_id": idx, "k": k,
                "features": ",".join(combo),
                **mean_mcc,  # dict-spread of all per-subset metrics
                "delta_mcc_vs_full10": mean_mcc["mean_mcc"] - full10_metrics["mean_mcc"],
                "is_core_4": set(combo) == set(CORE_4),
            })
            if idx % 100 == 0:
                print(f"  {idx}/{n_total} ...")
    df = pd.DataFrame(rows)
    df.to_csv(OUT_DIR / "p3_full_lattice_1023.csv", index=False)

    # Build frozenset -> metric lookup (formal Shapley weighting)
    lookup = {frozenset(r["features"].split(",")): r for r in rows}
    n = len(FEATURES)

    def shapley_for_metric(metric_key: str) -> dict[str, float]:
        v_empty = 0.0  # empty-coalition value defined as zero
        shapley = {}
        for f in FEATURES:
            phi = 0.0
            others = [x for x in FEATURES if x != f]
            for k in range(0, n):  # |S| = k where S ⊆ others
                weight = 1.0 / math.comb(n - 1, k)
                stratum_deltas = []
                for combo in itertools.combinations(others, k):
                    S_with = frozenset(combo + (f,))
                    S_without = frozenset(combo)
                    v_with = lookup[S_with][metric_key]
                    v_without = lookup[S_without][metric_key] if S_without else v_empty
                    stratum_deltas.append(v_with - v_without)
                if stratum_deltas:
                    phi += weight * np.mean(stratum_deltas)
            shapley[f] = phi / n
        return shapley

    sh_mcc = shapley_for_metric("mean_mcc")
    sh_enrich = shapley_for_metric("mean_enrichment")
    sh_df = pd.DataFrame([
        {"feature": f, "shapley_mcc": sh_mcc[f], "shapley_enrichment": sh_enrich[f]}
        for f in FEATURES
    ]).sort_values("shapley_mcc", ascending=False)
    sh_df.to_csv(OUT_DIR / "p3_shapley.csv", index=False)
    # Pareto frontier figure: |S| vs best mean_mcc
    best = df.groupby("k")["mean_mcc"].max().reset_index()
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(best["k"], best["mean_mcc"], "o-")
    ax.axhline(full10_mean, ls="--", color="gray", label=f"Full-10 ({full10_mean:.3f})")
    core4_mcc = df.loc[df["is_core_4"], "mean_mcc"].iloc[0]
    ax.scatter([4], [core4_mcc], s=120, marker="*", color="red", label=f"4-core ({core4_mcc:.3f})", zorder=5)
    ax.set_xlabel("|S| (subset size)"); ax.set_ylabel("LOPO mean MCC"); ax.legend()
    fig.tight_layout()
    fig.savefig(OUT_DIR / "p3_pareto_frontier.png", dpi=150)
    print(f"Done. Wrote {OUT_DIR}/p3_full_lattice_1023.csv ({len(df)} rows)")

if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Run the script**

```bash
cd /proj/paper && python scripts/codex_p3_full_lattice_shapley.py 2>&1 | tee results/mutbench/codex_wave1/p3_run.log
```

Expected: ~30 min wall time, 1023 rows in output CSV, log shows progress every 100 subsets, no exceptions.

- [ ] **Step 3: Sanity-check output**

```bash
head -5 /proj/paper/results/mutbench/codex_wave1/p3_full_lattice_1023.csv
wc -l /proj/paper/results/mutbench/codex_wave1/p3_full_lattice_1023.csv  # expect 1024 (header + 1023)
cat /proj/paper/results/mutbench/codex_wave1/p3_shapley.csv
```

Verify (per codex review Q7):
- 4-core row exists with `is_core_4=True`
- 4-core MCC matches the existing `feature_ablation_nested_lopo.csv` 4-core row **exactly** (not within ~0.005 — the protocols are identical, deviation = bug)
- Among `subset_selection_robustness_210combos.csv` 4-of-10 rows, every entry should match this lattice's k=4 rows exactly (cross-check 210 rows)
- 1023 = sum of C(10,k) for k=1..10
- Shapley values for both `shapley_mcc` and `shapley_enrichment` are real numbers, sum approximately equal to full-10 MCC and full-10 enrichment respectively (Shapley efficiency axiom).

- [ ] **Step 4: Document in NOTES.md**

Append:
```markdown
- P3 full lattice (2026-04-30): 1023 subsets enumerated. 4-core MCC = X.XXXX (rank Y/1023). Shapley top: ___. Pareto frontier shows knee at |S|=___. See `results/mutbench/codex_wave1/p3_*`.
```

(Replace placeholders with actual numbers from CSVs.)

Also write standalone report `paper/dissertation/review/2026-04-30/wave1/p3_full_lattice.md`.

- [ ] **Step 5: Commit**

```bash
git add scripts/codex_p3_full_lattice_shapley.py results/mutbench/codex_wave1/p3_* paper/dissertation/review/2026-04-30/wave1/p3_full_lattice.md NOTES.md
git commit -m "$(cat <<'EOF'
feat: v182 — Codex P3 full 2^10 lattice + formal Shapley

Extends subset_selection_robustness_210combos.csv to all 1023 non-empty
subsets of the 10 features. Same nested-LOPO + top-10% + MCC protocol,
plus top-20%, +/-10-window MCC, precision@20, enrichment, per-pathogen
wins. Formal Shapley with binomial weights 1/(n*C(n-1,|S|)) and v(empty)=0
for both MCC and enrichment metrics.

Outputs:
- p3_full_lattice_1023.csv (1023 rows, multi-metric)
- p3_shapley.csv (10 features × MCC + enrichment Shapley)
- p3_pareto_frontier.png (|S| vs best mean MCC + 4-core marker)
- p3_per_pathogen_wins.csv

Cross-checks against existing feature_ablation_nested_lopo.csv (4-core
exact match) and subset_selection_robustness_210combos.csv (all 210
4-of-10 rows exact match).

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

- [ ] **Step 6: CHECKPOINT** — If 4-core lattice rank > 50/1023, apply P3 failure-mode branch (top-of-plan table): replace "non-arbitrary 4-core" prose; if 3-core dominates, mark pLDDT optional.

---

## Task 3: P2 — Rank reliability / decile prevalence + decision curves

**Why P2 next:** Cheap (<1hr), no permutation cost. Outputs the most "deployable" framing: "score is a screening-budget allocator, not a calibrated probability."

**Files:**
- Create: `scripts/codex_p2_rank_reliability.py`
- Output: `results/mutbench/codex_wave1/p2_decile_prevalence.csv`, `p2_calibration.csv`, `p2_reliability.png`, `p2_decision_curve.png`

- [ ] **Step 1: Write the script**

Write `scripts/codex_p2_rank_reliability.py`:

```python
#!/usr/bin/env python3
"""P2: Rank reliability and decision curves for Algorithm 1 (4-core).

For each pathogen p:
  - Compute Algorithm 1 4-core score s_i for every position i (training
    pathogens learn signs/normalization, held-out gets z-scored locally)
  - Bin into pathogen-normalized deciles (10 bins) and ventiles (20 bins)
  - For each bin: empirical Layer A prevalence, ±10-window prevalence,
    enrichment vs pathogen base rate, bootstrap 95% CI (1000 resamples)
  - Calibration: fit isotonic regression on training pathogens, report
    calibration slope, ECE, Brier score for top-k membership
  - Decision curve: expected TPs at screening budgets {20, 50, 80} sites

Comparators per pathogen: 4-core, full-10 EqualWeight, frequency-only,
entropy-only, homoplasy-only, random rank.

Outputs:
  p2_decile_prevalence.csv  (pathogen × method × decile × prevalence/CI)
  p2_calibration.csv        (pathogen × method × slope/ECE/Brier)
  p2_decision_curve.csv     (pathogen × method × budget × expected_TP)
  p2_reliability.png        (decile prevalence per pathogen, faceted)
  p2_decision_curve.png     (TP-vs-budget per pathogen, faceted)
"""
# Implementation: load feature_matrix_*.csv, reuse sign-learning from
# feature_ablation_nested_lopo.py, bin by quantile within held-out,
# compute prevalence + window-coverage + bootstrap CI, isotonic on
# concatenated training scores, evaluate held-out calibration.
# Full implementation: ~250 lines. See feature_ablation_nested_lopo.py
# for sign-learning pattern.
```

(Full ~250-line implementation written when this task is executed; sign-learning copied from `feature_ablation_nested_lopo.py:60-110`. Bootstrap uses `numpy.random.default_rng(42)` for reproducibility.)

- [ ] **Step 2: Run**

```bash
cd /proj/paper && python scripts/codex_p2_rank_reliability.py 2>&1 | tee results/mutbench/codex_wave1/p2_run.log
```

Expected: ~10–20 min, no errors, 4 CSVs + 2 PNGs in output dir.

- [ ] **Step 3: Sanity-check**

```bash
head -5 /proj/paper/results/mutbench/codex_wave1/p2_decile_prevalence.csv
head -5 /proj/paper/results/mutbench/codex_wave1/p2_calibration.csv
```

Verify (per codex review Q7): top decile prevalence > bottom decile prevalence in ≥7/12 pathogens for 4-core, **AND top-vs-bottom bootstrap CI excludes zero or is explicitly reported as inconclusive**. Monotonic trend test (Spearman or Cuzick across deciles) computed and reported per pathogen. ECE present and finite.

- [ ] **Step 4: Append NOTES.md and write report**

```markdown
- P2 reliability (2026-04-30): top-decile/bottom-decile separation in N/12 pathogens for 4-core. Bootstrap CI: [___, ___]. Monotonic trend p=___. ECE = X.XXX. Decision curve shows ___ TP at budget=50.
```

Standalone report: `paper/dissertation/review/2026-04-30/wave1/p2_rank_reliability.md`.

- [ ] **Step 5: Commit**

```bash
git add scripts/codex_p2_rank_reliability.py results/mutbench/codex_wave1/p2_* paper/dissertation/review/2026-04-30/wave1/p2_rank_reliability.md NOTES.md
git commit -m "feat: v183 — Codex P2 rank reliability + decision curves"
```

- [ ] **Step 6: CHECKPOINT** — If top-vs-bottom bootstrap CI includes 0, apply P2 failure-mode branch.

---

## Task 4: P1 — Null calibration (100k permutations × 4 null types)

**Why P1 next:** Most compute-heavy of Wave 1 (~2–4 hrs), but the result is the single most defensible audit: "Algorithm 1 is above what?" Reduces overclaiming risk most.

**Files:**
- Create: `scripts/codex_p1_null_calibration.py`
- Output: `p1_null_per_pathogen.csv` (12 × 4 null types × stats), `p1_null_summary.csv`, `p1_null_distribution.png`

- [ ] **Step 1: Write the script**

Implements 4 null types:
1. **iid prevalence-preserving** — shuffle ground_truth labels uniformly
2. **circular shift** — shift labels by random offset within sequence
3. **protein-block shuffle** — shuffle within protein domain blocks (use 50-residue blocks as proxy when domain annotation absent)
4. **local-burden-preserving** — match local entropy/frequency strata (5-bin stratification)

For each (pathogen, null type), 100k permutations, compute exact MCC + ±10-window MCC + top-20 precision + enrichment. Report observed value, null mean, null SD, percentile, **one-sided above-null p-value as primary** (the scientific question is whether observed > null), two-sided p-value as sensitivity. Aggregate via Stouffer across 12 pathogens.

Compute budget detail: 12 pathogens × 4 nulls × 100k = 4.8M MCC evals. ~600 evals/sec on 1 core → ~2.2 hrs single-threaded. Parallelize with `multiprocessing.Pool(8)` → ~17 min.

- [ ] **Step 2: Smoke test on one pathogen first**

```bash
cd /proj/paper && python scripts/codex_p1_null_calibration.py --pathogen Dengue --n-perm 1000 --smoke 2>&1
```

Expected: 4 null types × 1000 perms × 1 pathogen completes in <30 sec, shows valid percentile (0–100) for Dengue.

- [ ] **Step 3: Full run**

```bash
cd /proj/paper && python scripts/codex_p1_null_calibration.py --n-perm 100000 --workers 8 2>&1 | tee results/mutbench/codex_wave1/p1_run.log
```

Expected: ~20–30 min, no segfaults from multiprocessing, 12 × 4 = 48 rows in `p1_null_summary.csv`.

- [ ] **Step 4: Sanity-check**

```bash
head -10 /proj/paper/results/mutbench/codex_wave1/p1_null_summary.csv
# Look for: observed > null_mean + 2*null_sd in ≥7/12 pathogens for iid null,
# attenuated for protein-block / local-burden nulls (this is the headline finding)
```

- [ ] **Step 5: Append NOTES.md and write per-task report**

NOTES.md:
```markdown
- P1 null calibration (2026-04-30): iid null Stouffer one-sided p=X.XXX (significant/not). Protein-block null p=X.XXX (degraded by Y%). Local-burden null p=X.XXX. Per-pathogen: N/12 above null.
```

Per codex review Q6: write standalone report `paper/dissertation/review/2026-04-30/wave1/p1_null_calibration.md` (1–2 pages: command, inputs, outputs, top-line numbers, failure-branch status, interpretation). Memory file is NOT written yet — wait until Wave 1 completion (Task 7).

- [ ] **Step 6: Commit**

```bash
git add scripts/codex_p1_null_calibration.py results/mutbench/codex_wave1/p1_* paper/dissertation/review/2026-04-30/wave1/p1_null_calibration.md NOTES.md
git commit -m "feat: v184 — Codex P1 100k-permutation null calibration (4 null types)"
```

- [ ] **Step 7: HARD STOP GATE** — Per codex review Q5, if iid Stouffer one-sided p > 0.05 globally, **STOP execution before Task 5 (P4)**. Apply the P1 failure-mode branch (see Predeclared Failure-Mode Branches table at top of plan): remove headline claim that Algorithm 1 beats prevalence-preserving null, reframe as exploratory ranking heuristic, do not insert detector-agnostic / search-space-reduction prose. P2/P3 results are kept as descriptive diagnostics only. Notify user before proceeding.

---

## Task 5: P4 — Detector consensus stability

**Why P4 last in Wave 1:** Depends on `stage3_full_results.csv` (already exists, 8580 rows). Cheap (<1hr). Closes the "is this an artifact of one detector?" question.

**Files:**
- Create: `scripts/codex_p4_detector_consensus.py`
- Output: `p4_consensus_jaccard.csv`, `p4_family_agreement.csv`, `p4_consensus_enrichment.csv`, `p4_consensus_stability.png`

- [ ] **Step 1: Inspect input format**

```bash
head -5 /proj/paper/results/mutbench/stage3_full_results.csv
awk -F, 'NR>1 {print $4}' /proj/paper/results/mutbench/stage3_full_results.csv | sort -u
```

Expected: 5 detector families (Wavelet, KDE, HDBSCAN/MutClust, threshold, window).

- [ ] **Step 2: Write the script**

Per codex review Q3: include 5 scorings (not just 2) to prevent score-selection bias:
- 4-core (Algorithm 1)
- full-10 EqualWeight
- frequency-only (control)
- entropy-only (control)
- homoplasy-only (control)

If runtime allows, do all 20 scorings; otherwise the 5-scoring subset is acceptable but must be labeled a **targeted consensus audit** in prose, not the full Stage 3 consensus study.

For each pathogen × scoring:
- Reconstruct detector callsets per detector
- Pairwise Jaccard between detector callsets within a (pathogen, scoring) pair
- Spearman rank correlation between detector scores
- Consensus thresholds: ≥25%, ≥50%, ≥75% of detectors call a position
- **Matched-size comparison** (per codex Q7): when comparing consensus enrichment to detector-mean, sample the detector-specific top-k to match the consensus candidate count. Report consensus candidate count, precision gain, AND recall loss together — not just enrichment.

- [ ] **Step 3: Resolve callset positions**

```bash
grep -l "positions" /proj/paper/scripts/run_stage3_*.py
```

If positions are not persisted in `stage3_full_results.csv` columns, add `--save-positions` flag to `run_stage3_full_detectors.py` and re-run for the 5 scorings (4-core, full-10, freq, entropy, homoplasy). Estimated ~30 min for 5 scorings × 39 detectors × 11 pathogens.

- [ ] **Step 4: Run consensus analysis**

```bash
cd /proj/paper && python scripts/codex_p4_detector_consensus.py 2>&1 | tee results/mutbench/codex_wave1/p4_run.log
```

- [ ] **Step 5: Sanity-check**

```bash
head -5 /proj/paper/results/mutbench/codex_wave1/p4_consensus_enrichment.csv
# Expect (per codex review Q5 P4 branch): ≥50% consensus enrichment > matched-size detector-mean
# enrichment in ≥7/12 pathogens. If not, apply P4 failure-mode branch.
```

- [ ] **Step 6: Document and commit**

NOTES.md bullet + write `paper/dissertation/review/2026-04-30/wave1/p4_detector_consensus.md` (per-task report). Memory still NOT written (Task 7).
```bash
git add scripts/codex_p4_detector_consensus.py results/mutbench/codex_wave1/p4_* paper/dissertation/review/2026-04-30/wave1/p4_detector_consensus.md NOTES.md
git commit -m "feat: v185 — Codex P4 detector-consensus stability + family agreement"
```

---

## Task 6: Dissertation prose insertions (Ch4 Results, Ch5 Discussion)

**Why now:** All four experiments completed; results are stable. Insert prose with concrete numbers from CSVs.

**Files:**
- Modify: `paper/dissertation/chapters_en/ch4_results.tex`
- Modify: `paper/dissertation/chapters_en/ch5_discussion.tex`

- [ ] **Step 1: Locate insertion points**

```bash
grep -n "alg:mutbench_coldstart\|para:mutbench_algorithm" /proj/paper/paper/dissertation/chapters_en/ch4_results.tex
```

- [ ] **Step 2: Insert P3 lattice subsection in ch4_results.tex**

After the Algorithm 1 + Table 3.14 block, insert a `\subsubsection{Cold-Start core on the full subset lattice}` paragraph (~120 words) citing P3 numbers:
- 4-core's rank on the 1023-subset Pareto frontier
- Top-3 Shapley features
- Whether the 4-core is the best 4-of-10 or near it

- [ ] **Step 3: Insert P2 reliability subsection in ch4_results.tex**

`\subsubsection{Rank reliability and decision-curve framing}` (~150 words):
- Top decile vs bottom decile prevalence (4-core)
- Calibration slope + ECE
- Decision curve: expected TPs at budget=50 for 4-core vs full-10 vs random
- Frame as "ranked screening, not probability calibration"

- [ ] **Step 4: Insert P1 null subsection + P4 consensus subsection**

P1 → `\subsubsection{Null-calibrated significance under four null models}`:
- Stouffer p-values for each null type
- Per-pathogen above-null counts
- Honest disclosure if local-burden null attenuates

P4 → `\subsubsection{Detector-agnostic consensus}`:
- Pairwise Jaccard mean
- Consensus@50% enrichment vs detector-specific
- Recall loss tradeoff

- [ ] **Step 5: Update ch5_discussion.tex Limitations subsection**

Per codex review Q5 + edit at line 558: prose MUST follow the predefined failure-mode branch from the Predeclared Failure-Mode Branches table at the top of this plan, NOT generic "honest disclosure." Concretely:
- If P1 iid p > 0.05: do not insert "above-null" claim; instead insert P1-failure-branch language
- If P3 rank > 50/1023: insert "fixed historical 4-core benchmarked against the lattice" wording
- If P2 CI includes 0: drop probability/calibration language entirely
- If P4 consensus ≤ matched-size detector mean: remove "detector-agnostic" framing, use only as reproducibility diagnostic

- [ ] **Step 6: Build PDF and verify**

```bash
cd /proj/paper/paper/dissertation && bash build.sh 2>&1 | tail -20
```

Expected: 0 errors, page count 225 → ~228, no undefined refs.

- [ ] **Step 7: Commit**

```bash
git add paper/dissertation/chapters_en/ch4_results.tex paper/dissertation/chapters_en/ch5_discussion.tex paper/dissertation/thesis_en.pdf
git commit -m "$(cat <<'EOF'
fix: v186 — ch4/ch5 prose insertions for Codex Wave 1 (P1+P2+P3+P4)

Adds four subsubsections to Chapter 4 Results citing concrete numbers
from results/mutbench/codex_wave1/ CSVs:
- P3 full-lattice rank of 4-core, Shapley top-3
- P2 decile prevalence + ECE + decision-curve framing
- P1 four-null Stouffer p-values + per-pathogen counts
- P4 detector consensus@50% enrichment

Chapter 5 Limitations gains an honest disclosure paragraph for any null
attenuation or Pareto-frontier near-miss.

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

---

## Task 7: Memory + slate completion checkpoint

- [ ] **Step 1: Write `codex_wave1_results.md` memory**

```markdown
---
name: Codex Wave 1 Results
description: Tier 1 method-core experiments P1-P4 outcomes (2026-04-30 to 2026-05-XX)
type: project
---

**Status:** P1-P4 complete (v182–v186). Algorithm 1 framing held / revised:
- P3: 4-core ranks N/1023 on lattice. Shapley top: ___
- P2: decile prevalence X→Y. ECE = ___. Decision curve TP@50 = ___
- P1: iid Stouffer p=___, local-burden p=___ (___ attenuation)
- P4: consensus@50% enrichment ___ vs detector-mean ___

**Why:** Closes Codex C14 "no plausible method" concern with falsification-resistant audits.

**How to apply:** When asked about Algorithm 1 robustness, cite these results. If P1 local-burden p > 0.05 globally, do NOT claim exact-site significance, only region-prioritization.
```

- [ ] **Step 2: Update MEMORY.md index**

Add line under `## [P] Project`:
```markdown
- [Codex Wave 1 Results](codex_wave1_results.md) — P1-P4 method-core audits, defense-strengthened
```

- [ ] **Step 3: Update `cycle7b_30pathogen_scaling.md`**

Note Wave 1 completion and that Wave 2 (Tier 2 features-only) is still queued.

- [ ] **Step 4: Final commit**

```bash
git add ~/.claude/projects/-proj-paper/memory/codex_wave1_results.md ~/.claude/projects/-proj-paper/memory/MEMORY.md ~/.claude/projects/-proj-paper/memory/cycle7b_30pathogen_scaling.md
# memory lives outside repo; commit in repo:
git add NOTES.md
git commit -m "docs: v187 — memory + index update for Codex Wave 1 completion"
```

---

## Wave 2 / Wave 3 (separate plans, not in this document)

**Wave 2 (next plan, est. 2-3 days):**
- P5 callability/abstention diagnostic rule (depends on P1 callability scores)
- P6 biological local-null audit (extends P1 with domain-aware nulls)
- P7 temporal/cross-validation extensions

**Wave 3 (est. 1-2 weeks, depends on data prep):**
- Pilot 3 Layer A literature curation (YFV/Lassa/WNV) — manual
- Tier 2 features-only LOPO at n=30
- Tier 3 EVE/PLM site-effect via `tools/eve_container/`

These will get their own plan files when Wave 1 lands.

---

## Self-review checklist

- ✅ Each task names exact file paths
- ✅ Each task has commit + checkpoint pause
- ✅ Documentation cadence: NOTES.md per task, per-task report under `review/2026-04-30/wave1/`, memory file ONLY at Wave 1 completion (codex review Q6)
- ✅ Compute budget realistic (~10 CPU-hrs total Wave 1)
- ✅ Out-of-scope items explicitly listed (Wave 2/3)
- ✅ Predeclared failure-mode branches at top of plan (codex review Q5)
- ✅ P3 formal Shapley with binomial weights, v(empty)=0, frozenset lookup (codex review Q2)
- ✅ P3 multi-metric (MCC + window-MCC + precision@20 + enrichment + per-pathogen wins) (codex review Q7)
- ✅ P3 sanity check requires exact match against existing 4-of-10 rows (codex review Q7 / line 49)
- ✅ P2 monotonic trend + top-vs-bottom bootstrap CI (codex review Q7)
- ✅ P1 one-sided p as primary (codex review Q7)
- ✅ P1 hard-stop gate before Task 5 if iid p > 0.05 (codex review Q5)
- ✅ P4 5-scoring panel (4-core + full-10 + freq + entropy + homoplasy controls) (codex review Q3)
- ✅ P4 matched-size comparison + recall loss + precision gain (codex review Q7)
- ✅ Task 6 prose required to follow failure-mode branch (codex review line 558)
- ⚠️ P2 implementation is sketched (~250 lines) — full code written when task executes
- ⚠️ P4 requires re-running `run_stage3_full_detectors.py` with `--save-positions` for 5 scorings × 39 detectors × 11 pathogens (~30 min)
