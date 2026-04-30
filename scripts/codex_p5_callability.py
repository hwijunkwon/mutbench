#!/usr/bin/env python3
"""P5: Callability / abstention rule (codex P1 hard-stop consultation §3,
plus all 8 edits from the Wave 2 codex plan review).

For each LOPO fold (held-out p_k, training = 11 others) and each method
(3-core primary, 4-core secondary):

  signs = fit_signs(training, FEATURES)  # Pearson sign per feature on
                                         # training labels (no held-out)

  Diagnostics on the 11 training pathogens (no held-out info):
    D1 top-decile separation
       per training pathogen: top-bot decile prevalence delta + 1k-bootstrap CI
       method passes if lower CI > 0.02 AND point > 0.05 in >= 7/11
    D2 null-adjusted enrichment
       per training pathogen: observed top-decile enrichment / mean null
       enrichment under 10k iid permutations
       method passes if 1k-bootstrap lower 95% of ratio across 11 training > 1.10
    D3 perturbation stability
       per training pathogen: 200 perturbations
         (a) jitter feature z-scores by 0.10 * per-feature SD (fixed stress)
         (b) re-fit signs on bootstrap of training pathogens
       Jaccard of top-10% callsets across all C(200,2) perturbation pairs
       method passes if median Jaccard >= 0.60 AND 10th pct >= 0.40
       (aggregated over 11 training pathogens)

  Diagnostic on the held-out (annotation-density metadata only):
    D4 sparse-label red flag
       held-out has >= 10 Layer A positives, >= 200 rankable positions,
       prev in [1%, 20%]

  Inversion guardrail (per-method):
    method not callable if >= 2 training pathogens have bootstrap CI
    upper < 0 OR median Spearman rho across decile prevalence <= 0

  Callable = D1 AND D2 AND D3 AND D4 AND NOT inversion.
  any_method_inversion (interpretive only) = 3-core_inv OR 4-core_inv.

  If callable: deploy method on held-out; record observed MCC, TP@20,
  TP@50, TP@80, enrichment.
  If abstained: emit ALL diagnostic component values (no short-circuit)
  + abstention_reason string.

Outputs:
  results/mutbench/codex_wave2/p5_diagnostics_per_fold.csv
  results/mutbench/codex_wave2/p5_callable_decisions.csv
  results/mutbench/codex_wave2/p5_endpoint_summary.csv
  results/mutbench/codex_wave2/p5_callable_subset.png
"""
from __future__ import annotations

import argparse
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats
from sklearn.metrics import matthews_corrcoef

warnings.filterwarnings("ignore", category=RuntimeWarning)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
FEATURE_DIR = PROJECT_ROOT / "results" / "mutbench" / "feature_analysis"
OUT_DIR = PROJECT_ROOT / "results" / "mutbench" / "codex_wave2"

ALL_PATHOGENS = [
    "SARS-CoV-2", "H3N2", "Norovirus", "HIV-1", "Dengue",
    "RSV", "Influenza_B", "MERS", "HCV",
    "Zika", "Rabies", "EV-A71",
]
FEATURES = [
    "freq", "entropy", "rare_freq", "homoplasy", "esm2_llr",
    "plddt", "sasa", "grantham", "dnds_proxy", "semantic_change",
]
METHODS = {
    "3-core": ("freq", "entropy", "homoplasy"),
    "4-core": ("freq", "entropy", "homoplasy", "plddt"),
}

# Default thresholds (per codex spec, all predeclared)
D1_QUORUM = 7              # >= 7/11 training pathogens pass top-decile separation
D1_LOWER_CI_MIN = 0.02
D1_POINT_MIN = 0.05
D2_LOWER_CI_MIN = 1.10
D2_NULL_PERMS = 10_000
D2_RATIO_BOOT = 1_000
D3_N_PERTURB = 200
D3_NOISE_SCALE = 0.10
D3_MEDIAN_MIN = 0.60
D3_PCT10_MIN = 0.40
D4_MIN_POS = 10
D4_MIN_RANKABLE = 200
D4_PREV_LO = 0.01
D4_PREV_HI = 0.20
INVERSION_COUNT_THRESH = 2  # >= 2 training pathogens with CI upper < 0
INVERSION_RHO_THRESH = 0.0  # median Spearman <= 0
TOP10_FRAC = 0.10
N_DECILES = 10
BUDGETS = [20, 50, 80]
N_BOOT_CI = 1_000
RANDOM_SEED = 42


def safe_mcc(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    y_true = np.asarray(y_true, dtype=int)
    y_pred = np.asarray(y_pred, dtype=int)
    if y_pred.sum() == 0 or y_pred.sum() == len(y_pred):
        return 0.0
    if y_true.sum() == 0 or y_true.sum() == len(y_true):
        return 0.0
    return float(matthews_corrcoef(y_true, y_pred))


def load_data() -> dict:
    data = {}
    for p in ALL_PATHOGENS:
        path = FEATURE_DIR / f"feature_matrix_{p}.csv"
        if not path.exists():
            continue
        df = pd.read_csv(path)
        if "layer_a" not in df.columns:
            continue
        y = df["layer_a"].values.astype(int)
        if y.sum() == 0 or y.sum() == len(y):
            continue
        data[p] = {"df": df, "y": y, "n": len(y), "base_rate": float(y.mean())}
    return data


def fit_signs(training_data: dict, features: tuple[str, ...] | list[str]) -> dict[str, float]:
    signs = {}
    for f in features:
        xs, ys = [], []
        for p, d in training_data.items():
            x = np.nan_to_num(d["df"][f].values.astype(float), nan=0.0, posinf=0.0, neginf=0.0)
            y = d["y"].astype(float)
            xs.append(x)
            ys.append(y)
        x_all = np.concatenate(xs)
        y_all = np.concatenate(ys)
        if x_all.std() < 1e-12:
            signs[f] = 1.0
        else:
            r = np.corrcoef(x_all, y_all)[0, 1]
            signs[f] = -1.0 if (np.isfinite(r) and r < 0) else 1.0
    return signs


def equalweight_score(df: pd.DataFrame, feature_subset: tuple[str, ...],
                       signs: dict[str, float]) -> np.ndarray:
    if not feature_subset:
        return np.zeros(len(df))
    F = np.nan_to_num(
        df[list(feature_subset)].values.astype(float),
        nan=0.0, posinf=0.0, neginf=0.0,
    )
    n_feat = F.shape[1]
    Z = np.zeros_like(F)
    w = np.zeros(n_feat)
    for j, fname in enumerate(feature_subset):
        col = F[:, j] * signs.get(fname, 1.0)
        s = col.std()
        if s > 1e-10:
            Z[:, j] = (col - col.mean()) / s
            w[j] = 1.0 / n_feat
    if w.sum() < 1e-10:
        return np.zeros(len(df))
    w /= w.sum()
    return Z @ w


def make_top10_pred(scores: np.ndarray) -> np.ndarray:
    thr = np.percentile(scores, 100 * (1 - TOP10_FRAC))
    return (scores >= thr).astype(int)


def make_topk_indicator(scores: np.ndarray, k: int) -> np.ndarray:
    n = len(scores)
    k = min(k, n)
    out = np.zeros(n, dtype=int)
    out[np.argsort(-scores)[:k]] = 1
    return out


def top_bot_delta_with_ci(scores: np.ndarray, y: np.ndarray,
                           rng: np.random.Generator) -> tuple[float, float, float, float, float]:
    """Returns (point delta, lower 95%, upper 95%, spearman_rho, spearman_p) for top-bot decile prevalence delta."""
    n = len(scores)
    ranks = stats.rankdata(scores, method="average") / n
    decile = np.minimum(N_DECILES - 1, (ranks * N_DECILES).astype(int))
    top_idx = np.where(decile == N_DECILES - 1)[0]
    bot_idx = np.where(decile == 0)[0]
    if len(top_idx) == 0 or len(bot_idx) == 0:
        return float("nan"), float("nan"), float("nan"), float("nan"), float("nan")
    obs = float(y[top_idx].mean() - y[bot_idx].mean())
    boot = []
    for _ in range(N_BOOT_CI):
        t_samp = rng.choice(top_idx, size=len(top_idx), replace=True)
        b_samp = rng.choice(bot_idx, size=len(bot_idx), replace=True)
        boot.append(y[t_samp].mean() - y[b_samp].mean())
    lo, hi = np.percentile(boot, [2.5, 97.5])
    decile_means = np.array([y[decile == d].mean() if (decile == d).any() else np.nan
                              for d in range(N_DECILES)])
    valid = ~np.isnan(decile_means)
    if valid.sum() < 3:
        rho, p = float("nan"), float("nan")
    else:
        rho_, p_ = stats.spearmanr(np.where(valid)[0], decile_means[valid])
        rho, p = float(rho_), float(p_)
    return obs, float(lo), float(hi), rho, p


def vectorized_iid_null_enrichment(y: np.ndarray, pred: np.ndarray, n_perm: int,
                                     rng: np.random.Generator) -> np.ndarray:
    """For a fixed prediction (top-10% indicator), shuffle y n_perm times and
    compute enrichment = precision_at_top10 / base_rate per permutation."""
    n = len(y)
    pred_pos = pred.sum()
    base_rate = y.mean()
    if pred_pos == 0 or base_rate < 1e-12:
        return np.zeros(n_perm)
    Y = np.tile(y, (n_perm, 1))
    for i in range(n_perm):
        rng.shuffle(Y[i])
    precision = (Y @ pred) / pred_pos
    return precision / base_rate


def d1_top_decile_separation(training_data: dict, feature_subset: tuple[str, ...],
                              signs: dict[str, float], rng: np.random.Generator) -> dict:
    """Returns per-pathogen results + aggregate pass/fail."""
    rows = []
    n_pass = 0
    n_total = 0
    for p, d in training_data.items():
        scores = equalweight_score(d["df"], feature_subset, signs)
        obs, lo, hi, rho, sp = top_bot_delta_with_ci(scores, d["y"], rng)
        passed = (np.isfinite(lo) and np.isfinite(obs) and lo > D1_LOWER_CI_MIN
                  and obs > D1_POINT_MIN)
        rows.append({"pathogen": p, "delta": obs, "ci_lo": lo, "ci_hi": hi,
                     "spearman_rho": rho, "passed": int(passed)})
        if np.isfinite(obs):
            n_total += 1
            if passed:
                n_pass += 1
    return {
        "per_pathogen": rows,
        "n_pass": n_pass,
        "n_total": n_total,
        "passed": n_pass >= D1_QUORUM,
    }


def d2_null_adjusted_enrichment(training_data: dict, feature_subset: tuple[str, ...],
                                  signs: dict[str, float], rng: np.random.Generator) -> dict:
    """For each training pathogen: observed top-decile enrichment / mean null
    enrichment under 10k iid perms. Bootstrap of ratio across 11 pathogens.
    Pass if lower 95% bootstrap > 1.10."""
    ratios = []
    rows = []
    for p, d in training_data.items():
        scores = equalweight_score(d["df"], feature_subset, signs)
        pred = make_top10_pred(scores)
        if pred.sum() == 0:
            rows.append({"pathogen": p, "obs_enr": float("nan"),
                         "null_mean_enr": float("nan"), "ratio": float("nan")})
            continue
        precision = float(d["y"][pred == 1].mean())
        base_rate = d["base_rate"]
        obs_enr = precision / base_rate if base_rate > 1e-12 else 0.0
        null_enr = vectorized_iid_null_enrichment(d["y"], pred, D2_NULL_PERMS, rng)
        null_mean = float(null_enr.mean())
        ratio = obs_enr / null_mean if null_mean > 1e-12 else float("nan")
        if np.isfinite(ratio):
            ratios.append(ratio)
        rows.append({"pathogen": p, "obs_enr": obs_enr,
                     "null_mean_enr": null_mean, "ratio": ratio})
    if len(ratios) < 3:
        return {"per_pathogen": rows, "ratios": ratios,
                "boot_lo": float("nan"), "boot_hi": float("nan"), "passed": False}
    ratios_arr = np.array(ratios)
    boot = []
    for _ in range(N_BOOT_CI):
        idx = rng.integers(0, len(ratios_arr), size=len(ratios_arr))
        boot.append(ratios_arr[idx].mean())
    lo, hi = np.percentile(boot, [2.5, 97.5])
    return {
        "per_pathogen": rows,
        "ratios": ratios,
        "boot_lo": float(lo),
        "boot_hi": float(hi),
        "passed": float(lo) > D2_LOWER_CI_MIN,
    }


def d3_perturbation_stability(training_data: dict, training_pathogens: list[str],
                                feature_subset: tuple[str, ...],
                                rng: np.random.Generator) -> dict:
    """For each training pathogen, 200 perturbations: jitter z-scores by
    0.10*SD AND re-fit signs on bootstrap of training pathogens. Compute
    Jaccard of top-10% callsets across all pairs of perturbations.
    Pass if median Jaccard >= 0.60 AND 10th pct >= 0.40 over 11 pathogens."""
    rows = []
    medians, pcts10 = [], []
    for p in training_pathogens:
        d = training_data[p]
        n = d["n"]
        # Pre-compute z-scored feature values for this pathogen
        F = np.nan_to_num(d["df"][list(feature_subset)].values.astype(float),
                           nan=0.0, posinf=0.0, neginf=0.0)
        n_feat = F.shape[1]
        Fz = np.zeros_like(F)
        sds = np.zeros(n_feat)
        for j in range(n_feat):
            col = F[:, j]
            s = col.std()
            if s > 1e-10:
                Fz[:, j] = (col - col.mean()) / s
                sds[j] = s
            else:
                sds[j] = 0.0
        # 200 perturbations
        callsets = []
        for k in range(D3_N_PERTURB):
            # (a) jitter z-scores
            noise = rng.normal(0, D3_NOISE_SCALE, Fz.shape)
            Z_pert = Fz + noise
            # (b) re-fit signs on bootstrap of training pathogens
            others = [q for q in training_pathogens if q != p]
            boot_idx = rng.integers(0, len(others), size=len(others))
            boot_others = [others[i] for i in boot_idx]
            boot_data = {q: training_data[q] for q in set(boot_others)}
            signs_k = fit_signs(boot_data, feature_subset)
            # apply signs to perturbed z-scores
            Z_signed = Z_pert.copy()
            for j, fname in enumerate(feature_subset):
                Z_signed[:, j] *= signs_k[fname]
            scores = Z_signed.mean(axis=1)
            pred = make_top10_pred(scores)
            callsets.append(set(np.where(pred == 1)[0].tolist()))
        # Pairwise Jaccard
        jaccards = []
        for i in range(D3_N_PERTURB):
            for j in range(i + 1, D3_N_PERTURB):
                a, b = callsets[i], callsets[j]
                if not a and not b:
                    jaccards.append(1.0)
                else:
                    jaccards.append(len(a & b) / max(1, len(a | b)))
        med = float(np.median(jaccards))
        p10 = float(np.percentile(jaccards, 10))
        rows.append({"pathogen": p, "median_jaccard": med, "pct10_jaccard": p10})
        medians.append(med)
        pcts10.append(p10)
    agg_median = float(np.median(medians))
    agg_p10 = float(np.median(pcts10))
    return {
        "per_pathogen": rows,
        "aggregate_median": agg_median,
        "aggregate_pct10": agg_p10,
        "passed": agg_median >= D3_MEDIAN_MIN and agg_p10 >= D3_PCT10_MIN,
    }


def d4_sparse_label_red_flag(held_data: dict) -> dict:
    """Held-out annotation-density metadata only."""
    n_pos = int(held_data["y"].sum())
    n_rankable = int(held_data["n"])  # all positions are rankable in our setup
    prev = float(held_data["base_rate"])
    n_pos_ok = n_pos >= D4_MIN_POS
    n_rank_ok = n_rankable >= D4_MIN_RANKABLE
    prev_ok = D4_PREV_LO <= prev <= D4_PREV_HI
    return {
        "n_pos": n_pos,
        "n_rankable": n_rankable,
        "prevalence": prev,
        "n_pos_ok": n_pos_ok,
        "n_rankable_ok": n_rank_ok,
        "prev_ok": prev_ok,
        "passed": n_pos_ok and n_rank_ok and prev_ok,
    }


def inversion_guardrail(training_data: dict, feature_subset: tuple[str, ...],
                          signs: dict[str, float], rng: np.random.Generator) -> dict:
    """Per-method: not callable if >=2 training pathogens have bootstrap CI
    upper < 0 OR median Spearman rho across decile prevalence <= 0."""
    n_upper_neg = 0
    rhos = []
    rows = []
    for p, d in training_data.items():
        scores = equalweight_score(d["df"], feature_subset, signs)
        obs, lo, hi, rho, _ = top_bot_delta_with_ci(scores, d["y"], rng)
        upper_neg = bool(np.isfinite(hi) and hi < 0)
        if upper_neg:
            n_upper_neg += 1
        if np.isfinite(rho):
            rhos.append(rho)
        rows.append({"pathogen": p, "ci_upper": hi, "spearman_rho": rho,
                     "upper_neg": int(upper_neg)})
    median_rho = float(np.median(rhos)) if rhos else float("nan")
    fired = (n_upper_neg >= INVERSION_COUNT_THRESH or
             (np.isfinite(median_rho) and median_rho <= INVERSION_RHO_THRESH))
    return {
        "per_pathogen": rows,
        "n_upper_neg": n_upper_neg,
        "median_spearman_rho": median_rho,
        "fired": fired,
        "passed": not fired,  # passes guardrail iff guardrail does not fire
    }


def deploy_on_held_out(held_data: dict, feature_subset: tuple[str, ...],
                         signs: dict[str, float]) -> dict:
    scores = equalweight_score(held_data["df"], feature_subset, signs)
    pred10 = make_top10_pred(scores)
    mcc = safe_mcc(held_data["y"], pred10)
    base_rate = held_data["base_rate"]
    if pred10.sum() > 0:
        precision = float(held_data["y"][pred10 == 1].mean())
        enrichment = precision / base_rate if base_rate > 1e-12 else 0.0
    else:
        enrichment = 0.0
    out = {"observed_mcc": mcc, "observed_enrichment": enrichment}
    for b in BUDGETS:
        topk = make_topk_indicator(scores, b)
        out[f"observed_tp{b}"] = int((held_data["y"] * topk).sum())
    return out


def run_one_fold(held_p: str, data: dict, rng: np.random.Generator,
                  smoke: bool = False) -> list[dict]:
    """Returns rows for both methods on this fold."""
    training_data = {p: d for p, d in data.items() if p != held_p}
    training_pathogens = list(training_data.keys())
    held_data = data[held_p]

    # D4 is held-out characteristic; computed once
    d4 = d4_sparse_label_red_flag(held_data)

    rows = []
    method_inversion_status = {}

    for method_name, feature_subset in METHODS.items():
        signs = fit_signs(training_data, feature_subset)

        d1 = d1_top_decile_separation(training_data, feature_subset, signs, rng)
        d2 = d2_null_adjusted_enrichment(training_data, feature_subset, signs, rng)
        # D3 reduced perturbation count if smoke (for fast smoke test)
        if smoke:
            global D3_N_PERTURB
            saved_d3 = D3_N_PERTURB
            D3_N_PERTURB = 20
        d3 = d3_perturbation_stability(training_data, training_pathogens, feature_subset, rng)
        if smoke:
            D3_N_PERTURB = saved_d3
        inv = inversion_guardrail(training_data, feature_subset, signs, rng)
        method_inversion_status[method_name] = inv["fired"]

        callable_ = (d1["passed"] and d2["passed"] and d3["passed"]
                     and d4["passed"] and inv["passed"])

        # Build abstention reason
        fail_components = []
        if not d1["passed"]: fail_components.append("D1")
        if not d2["passed"]: fail_components.append("D2")
        if not d3["passed"]: fail_components.append("D3")
        if not d4["passed"]: fail_components.append("D4")
        if not inv["passed"]: fail_components.append("INV")
        abstention_reason = ",".join(fail_components) if fail_components else ""

        # Always emit deployment metrics (no short-circuit per codex review)
        deploy = deploy_on_held_out(held_data, feature_subset, signs)

        row = {
            "pathogen": held_p,
            "method": method_name,
            "d1_n_pass": d1["n_pass"],
            "d1_n_total": d1["n_total"],
            "d1_pass": int(d1["passed"]),
            "d1_fail": int(not d1["passed"]),
            "d2_boot_lo": d2["boot_lo"],
            "d2_pass": int(d2["passed"]),
            "d2_fail": int(not d2["passed"]),
            "d3_aggregate_median": d3["aggregate_median"],
            "d3_aggregate_pct10": d3["aggregate_pct10"],
            "d3_pass": int(d3["passed"]),
            "d3_fail": int(not d3["passed"]),
            "d4_n_pos": d4["n_pos"],
            "d4_n_rankable": d4["n_rankable"],
            "d4_prevalence": d4["prevalence"],
            "d4_pass": int(d4["passed"]),
            "d4_fail": int(not d4["passed"]),
            "inv_n_upper_neg": inv["n_upper_neg"],
            "inv_median_rho": inv["median_spearman_rho"],
            "inversion_pass": int(inv["passed"]),
            "inversion_fail": int(not inv["passed"]),
            "callable": int(callable_),
            "abstention_reason": abstention_reason,
            "observed_mcc": deploy["observed_mcc"],
            "observed_enrichment": deploy["observed_enrichment"],
            "observed_tp20": deploy["observed_tp20"],
            "observed_tp50": deploy["observed_tp50"],
            "observed_tp80": deploy["observed_tp80"],
        }
        rows.append(row)

    # any_method_inversion flag (interpretive only, NOT affecting callable)
    any_inv = int(method_inversion_status.get("3-core", False) or
                   method_inversion_status.get("4-core", False))
    for r in rows:
        r["any_method_inversion"] = any_inv

    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fold", type=str, default=None,
                    help="Restrict to one held-out pathogen (for smoke testing)")
    ap.add_argument("--smoke", action="store_true",
                    help="Reduce D3 perturbation count and D2 null perms for speed")
    args = ap.parse_args()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    print("MutBench P5: Callability / abstention rule")
    print("=" * 60)
    if args.smoke:
        global D2_NULL_PERMS
        D2_NULL_PERMS = 1000
        print("[smoke] D2_NULL_PERMS=1000, D3_N_PERTURB=20")
    rng = np.random.default_rng(RANDOM_SEED)
    data = load_data()
    pathogens = [args.fold] if args.fold else list(data.keys())
    if args.fold and args.fold not in data:
        raise SystemExit(f"Unknown pathogen {args.fold}")
    print(f"Pathogens: {pathogens}")
    all_rows = []
    for i, p in enumerate(pathogens):
        print(f"\n[{i+1}/{len(pathogens)}] Fold: {p}")
        rows = run_one_fold(p, data, rng, smoke=args.smoke)
        all_rows.extend(rows)
        for r in rows:
            print(f"  {r['method']}: callable={r['callable']} "
                  f"D1={r['d1_pass']}({r['d1_n_pass']}/{r['d1_n_total']}) "
                  f"D2={r['d2_pass']}(lo={r['d2_boot_lo']:.2f}) "
                  f"D3={r['d3_pass']}(med={r['d3_aggregate_median']:.2f},p10={r['d3_aggregate_pct10']:.2f}) "
                  f"D4={r['d4_pass']}(npos={r['d4_n_pos']},prev={r['d4_prevalence']:.3f}) "
                  f"INV={r['inversion_pass']}(neg={r['inv_n_upper_neg']},rho={r['inv_median_rho']:.2f}) "
                  f"reason={r['abstention_reason'] or '-'} "
                  f"MCC={r['observed_mcc']:.3f} TP@50={r['observed_tp50']}")

    df = pd.DataFrame(all_rows)
    df.to_csv(OUT_DIR / "p5_callable_decisions.csv", index=False)

    # Endpoint summary
    print("\n=== Endpoint summary ===")
    summary_rows = []
    for method in METHODS:
        sub = df[df["method"] == method]
        callable_subset = sub[sub["callable"] == 1]
        n_call = len(callable_subset)
        if n_call > 0:
            mean_mcc = float(callable_subset["observed_mcc"].mean())
            sum_tp20 = int(callable_subset["observed_tp20"].sum())
            sum_tp50 = int(callable_subset["observed_tp50"].sum())
            sum_tp80 = int(callable_subset["observed_tp80"].sum())
            callable_ids = list(callable_subset["pathogen"])
        else:
            mean_mcc = float("nan")
            sum_tp20 = sum_tp50 = sum_tp80 = 0
            callable_ids = []
        abstained_ids = list(sub[sub["callable"] == 0]["pathogen"])
        summary_rows.append({
            "method": method,
            "n_callable": n_call,
            "n_total": len(sub),
            "callable_fraction": n_call / max(1, len(sub)),
            "mean_mcc_callable": mean_mcc,
            "sum_tp20_callable": sum_tp20,
            "sum_tp50_callable": sum_tp50,
            "sum_tp80_callable": sum_tp80,
            "callable_pathogens": ";".join(callable_ids),
            "abstained_pathogens": ";".join(abstained_ids),
        })
        print(f"\n{method}: {n_call}/{len(sub)} callable")
        print(f"  callable: {callable_ids}")
        print(f"  abstained: {abstained_ids}")
        if n_call:
            print(f"  mean MCC = {mean_mcc:.4f}")
            print(f"  sum TP@20 = {sum_tp20}, TP@50 = {sum_tp50}, TP@80 = {sum_tp80}")
    summary_df = pd.DataFrame(summary_rows)
    summary_df.to_csv(OUT_DIR / "p5_endpoint_summary.csv", index=False)

    # Diagnostic-level CSV (already in callable_decisions; emit a per-fold per-diagnostic flat view)
    diag_rows = []
    for _, r in df.iterrows():
        for diag in ["d1", "d2", "d3", "d4", "inversion"]:
            diag_rows.append({
                "pathogen": r["pathogen"], "method": r["method"], "diagnostic": diag,
                "passed": r[f"{diag}_pass"],
            })
    pd.DataFrame(diag_rows).to_csv(OUT_DIR / "p5_diagnostics_per_fold.csv", index=False)

    # Figure: per-fold diagnostic bars + callable status
    fig, axes = plt.subplots(2, 1, figsize=(13, 7), sharex=True)
    diag_cols = ["d1_pass", "d2_pass", "d3_pass", "d4_pass", "inversion_pass"]
    for ax, method in zip(axes.flat, METHODS):
        sub = df[df["method"] == method].set_index("pathogen")
        sub = sub.reindex(ALL_PATHOGENS)
        x = np.arange(len(ALL_PATHOGENS))
        width = 0.16
        for i, col in enumerate(diag_cols):
            ax.bar(x + i * width, sub[col].fillna(0), width, label=col.replace("_pass",""))
        for i, p in enumerate(ALL_PATHOGENS):
            row = sub.loc[p] if p in sub.index else None
            if row is not None and not pd.isna(row.get("callable", float("nan"))):
                callable_color = "green" if row["callable"] == 1 else "red"
                ax.text(i + 2 * width, 1.05, "C" if row["callable"] == 1 else "A",
                        color=callable_color, fontweight="bold", ha="center")
        ax.set_xticks(x + 2 * width)
        ax.set_xticklabels(ALL_PATHOGENS, rotation=30, ha="right")
        ax.set_ylim([0, 1.2])
        ax.set_ylabel("diagnostic pass (1)")
        ax.set_title(f"P5: diagnostic outcomes per fold — {method}")
        ax.legend(fontsize=8, ncol=5, loc="upper left")
        ax.grid(axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUT_DIR / "p5_callable_subset.png", dpi=150)
    print(f"\nDone. Outputs: {OUT_DIR}/p5_*")


if __name__ == "__main__":
    main()
