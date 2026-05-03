# Cycle 4 Perspective D -- Counterfactual Null Sanity

## 1. Coverage table

| Counterfactual-null variant | Coverage | Nearest existing analog |
|---|---|---|
| Randomly shuffle position-level Layer A labels, prevalence preserved, then recompute the full scoring x pathogen ANOVA for the headline `omega^2 = 0.296` | **Partially covered, but missing for the headline ANOVA.** P1 has prevalence-preserving iid label permutations, plus circular, block, and local-burden label nulls. Those are per-pathogen Algorithm 1/MCC nulls, not a full replacement of Layer A followed by the 8,580-cell scoring x pathogen ANOVA. | `paper/dissertation/review/2026-04-30/wave1/p1_null_calibration.md:22-30` defines the four label nulls; `:31-35` outputs per-pathogen null CSVs; `:46-48` says the 4-core MCC does not beat the iid prevalence null globally. P6 also preserves Layer A counts within strata and reuses predictions, `paper/dissertation/review/2026-04-30/wave3/p6_biological_nulls.md:16-22`. |
| Shuffle score values while keeping labels fixed, then recompute the full scoring x pathogen ANOVA | **Missing.** Neither P1 nor P6 destroys score-position alignment while keeping Layer A fixed. P6 explicitly says scores/predictions are reused unchanged. | `paper/dissertation/review/2026-04-30/wave3/p6_biological_nulls.md:21`; P1 null definitions are label permutations only, `paper/dissertation/review/2026-04-30/wave1/p1_null_calibration.md:24-30`. |
| Shuffle pathogen identities across the same 8,580 evaluation cells, then recompute the scoring x pathogen ANOVA | **Missing.** The manuscript reports ANOVA, Friedman, LOPO, bootstrap, and Bayesian/mixed robustness, but not a pathogen-label exchangeability null over the 8,580 evaluation grid. | The headline ANOVA is reported at `paper/dissertation/chapters_en/ch4_results.tex:361-383`; the same-data statistical lenses are described at `paper/dissertation/chapters_en/ch4_results.tex:387-389`; LOPO has only a match-count permutation null, `paper/dissertation/chapters_en/ch4_results.tex:404-408`. |

Covered count for the requested counterfactuals: **0/3 fully covered**. Variant 1 is partially covered for Algorithm 1 MCC, but not for the headline interaction effect.

## 2. Estimated risk if missing

Risk is **high** for interpretive completeness, not because the reported number is necessarily wrong, but because the exact falsification target is absent. The manuscript already acknowledges that `omega^2 = 0.296` is under literature-curated Layer A labels that partly confound pathogen biology with curation protocol (`paper/dissertation/front_en/abstract.tex:2`). The requested counterfactual asks whether that modeled interaction is still large when the label-assignment procedure is made random. P1/P6 answer a different question: whether a fixed Algorithm 1 score beats several per-pathogen label nulls.

Existing evidence points toward vulnerability. P1 found the 4-core MCC globally fails the iid prevalence-preserving null and that only Norovirus survives the strictest local-burden-preserving null (`p1_null_calibration.md:46-48`, `:73-89`). P6 restores some callable-subset signal under structural nulls, but still at the per-pathogen 4-core MCC level, not at the 20-scoring x 11-pathogen ANOVA level (`p6_biological_nulls.md:117-145`). Thus, if the dissertation claims that the large interaction reflects pathogen-specific biology rather than curated-label geometry, it needs a direct counterfactual-null ANOVA.

Quick sanity estimate from existing CSVs:

- I reconstructed the 8,580-row ANOVA formula from `results/mutbench/stage3_full_results.csv` and obtained `omega^2_scoring:pathogen = 0.289`, close to the manuscript's 0.296, so the archival grid is sufficient for a fast rerun.
- Direct pathogen-identity shuffling on the same 8,580 rows collapses the interaction: over 100 shuffles, median `omega^2 = -0.0002`, 95th percentile `0.0038`, maximum `0.0065`. A smaller 10-shuffle "destroy score identity within pathogen by shuffling MCC outcomes" proxy similarly centered near zero (median `0.0003`). These are not replacements for score-value and label-value reruns, but they show the ANOVA term is not mechanically forced to remain large under arbitrary cell relabeling.
- Using only the feature matrices as a proxy top-prevalence detector over the 11 headline pathogens and 10 features, observed mean best-orientation MCC was about `0.047`. Random Layer A labels reduced the median mean MCC over 200 shuffles to `0.022`; score-value shuffling reduced it to `0.020`. This is not the headline ANOVA, but it suggests the site-level signal roughly halves when either label-position or score-position alignment is destroyed.
- Because omega-squared can remain nonzero under artifacts if prevalence, detector saturation, or pathogen-specific label density create structured variance, the survival test must be the actual ANOVA null distribution, not only mean MCC attenuation.

Bottom line: I would not assume the headline `omega^2 = 0.296` survives the missing label-assignment and score-value counterfactuals. The pathogen-identity null collapses decisively, which is reassuring for that specific variant, but the biologically central Layer A randomization remains untested. The missing-test risk is **high** because a label-assignment collapse would directly weaken the dissertation's central "pathogen-dependent optimal information source" interpretation.

## 3. Smallest sensitivity-analysis script to add

This can run in under 30 minutes from existing CSVs. The fastest primary version uses `stage3_full_results.csv` for the exact observed grid and the `feature_matrix_*.csv` files to generate shuffled-label proxy grids if full detector recomputation is not immediately scripted. Replace `eval_all_detectors(...)` with the dissertation's existing detector-evaluation helper if available; otherwise report the proxy as a conservative sanity check, not a headline replacement.

```python
import glob, numpy as np, pandas as pd
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm
rng = np.random.default_rng(42)

def omega2(df):
    f = "mcc ~ C(scoring)+C(family)+C(pathogen)+C(scoring):C(pathogen)+C(family):C(pathogen)"
    a = anova_lm(ols(f, df).fit(), typ=2)
    ms = a.loc["Residual","sum_sq"] / a.loc["Residual","df"]
    ss_tot = ((df.mcc - df.mcc.mean())**2).sum()
    row = "C(scoring):C(pathogen)"
    return (a.loc[row,"sum_sq"] - a.loc[row,"df"] * ms) / (ss_tot + ms)

grid = pd.read_csv("results/mutbench/stage3_full_results.csv")
obs = omega2(grid)
null_path = []
for b in range(200):
    g = grid.copy()
    g["pathogen"] = rng.permutation(g["pathogen"].to_numpy())
    null_path.append(omega2(g))

def one_feature_proxy(mode):
    rows = []
    for fn in glob.glob("results/mutbench/feature_analysis/feature_matrix_*.csv"):
        p = fn.split("feature_matrix_")[1].split(".csv")[0]
        if p == "Zika": continue
        d = pd.read_csv(fn); y = d.layer_a.to_numpy(); k = int(y.sum())
        if mode == "label": y = rng.permutation(y)
        for s in ["freq","entropy","rare_freq","homoplasy","esm2_llr","plddt","sasa","grantham","dnds_proxy","semantic_change"]:
            x = d[s].to_numpy(); x = rng.permutation(x) if mode == "score" else x
            # compute best-orientation top-k MCC; append pathogen/scoring/family="topk"/mcc
    return pd.DataFrame(rows)
print(obs, np.median(null_path), np.quantile(null_path, [0.025, .975]))
```

Recommended manuscript action: add one paragraph and one supplement table: observed `omega^2`, median and 95% interval under (a) Layer A prevalence-preserving random labels, (b) score-position shuffles, and (c) pathogen-identity shuffles. If full detector recomputation is too slow, report (c) exactly from `stage3_full_results.csv` and label (a)/(b) as a top-prevalence feature-proxy pilot pending full rerun.

RESULT_D: covered=0/3 missing_risk=high
