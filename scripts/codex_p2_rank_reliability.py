#!/usr/bin/env python3
"""P2: Rank reliability and decision curves for Algorithm 1 (4-core).

Per pathogen and method:
  - Z-scored ensemble score (training-fit signs, held-out z-score, uniform mean)
  - Bin into pathogen-normalized deciles (10 bins) and ventiles (20 bins)
  - Empirical Layer A prevalence per bin, +/-10-window prevalence per bin,
    enrichment vs pathogen base rate, bootstrap 95% CI (1000 resamples)
  - Calibration: isotonic regression on training pathogens, evaluated on
    held-out positions; report calibration slope, ECE, Brier score
  - Decision curve: expected TPs at screening budgets {20, 50, 80}
  - Monotonic trend: Spearman rank correlation between decile index and
    empirical prevalence within pathogen
  - Top-vs-bottom bootstrap CI for prevalence delta

Comparators per pathogen (per codex review Q3):
  4-core, 3-core, full-10 EqualWeight, frequency-only, entropy-only,
  homoplasy-only, random rank.

Outputs (under results/mutbench/codex_wave1/):
  p2_decile_prevalence.csv  (pathogen × method × decile × prevalence/CI)
  p2_calibration.csv        (pathogen × method × slope/ECE/Brier)
  p2_decision_curve.csv     (pathogen × method × budget × expected_TP)
  p2_top_vs_bottom.csv      (pathogen × method × delta + bootstrap CI + Spearman)
  p2_reliability.png        (decile prevalence faceted)
  p2_decision_curve.png     (TP vs budget faceted)
"""
from __future__ import annotations

import math
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats
from sklearn.isotonic import IsotonicRegression
from sklearn.metrics import brier_score_loss

warnings.filterwarnings("ignore", category=RuntimeWarning)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
FEATURE_DIR = PROJECT_ROOT / "results" / "mutbench" / "feature_analysis"
OUT_DIR = PROJECT_ROOT / "results" / "mutbench" / "codex_wave1"

ALL_PATHOGENS = [
    "SARS-CoV-2", "H3N2", "Norovirus", "HIV-1", "Dengue",
    "RSV", "Influenza_B", "MERS", "HCV",
    "Zika", "Rabies", "EV-A71",
]
FEATURES = [
    "freq", "entropy", "rare_freq", "homoplasy", "esm2_llr",
    "plddt", "sasa", "grantham", "dnds_proxy", "semantic_change",
]
CORE_4 = ("freq", "entropy", "homoplasy", "plddt")
CORE_3 = ("freq", "entropy", "homoplasy")  # P3 dominant subset
TOP10_FRAC = 0.10
WINDOW_RADIUS = 10
N_BOOT = 1000
RANDOM_SEED = 42
BUDGETS = [20, 50, 80]
N_DECILES = 10


def load_data():
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
        data[p] = {"df": df, "y": y, "n": len(y), "base_rate": y.mean()}
    return data


def fit_signs(training_data: dict, features: list[str]) -> dict[str, float]:
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


def equalweight_score(held_df: pd.DataFrame, feature_subset: tuple[str, ...],
                       signs: dict[str, float]) -> np.ndarray:
    if not feature_subset:
        return np.zeros(len(held_df))
    F = np.nan_to_num(
        held_df[list(feature_subset)].values.astype(float),
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
        return np.zeros(len(held_df))
    w /= w.sum()
    return Z @ w


def window_indicator(y: np.ndarray, radius: int) -> np.ndarray:
    """For each position, 1 if any true positive lies within +/- radius."""
    n = len(y)
    idx = np.where(y == 1)[0]
    out = np.zeros(n, dtype=int)
    for i in idx:
        lo = max(0, i - radius)
        hi = min(n, i + radius + 1)
        out[lo:hi] = 1
    return out


def per_decile_metrics(scores: np.ndarray, y: np.ndarray, y_window: np.ndarray,
                        rng: np.random.Generator):
    n = len(scores)
    ranks = stats.rankdata(scores, method="average") / n  # 0..1
    decile = np.minimum(N_DECILES - 1, (ranks * N_DECILES).astype(int))
    base_rate = y.mean()
    rows = []
    for d in range(N_DECILES):
        mask = decile == d
        if mask.sum() == 0:
            rows.append({"decile": d, "n": 0, "prevalence": np.nan,
                         "prev_lo": np.nan, "prev_hi": np.nan,
                         "window_prev": np.nan, "enrichment": np.nan})
            continue
        prev = float(y[mask].mean())
        wprev = float(y_window[mask].mean())
        # bootstrap CI for prevalence within decile
        idx = np.where(mask)[0]
        boot = []
        for _ in range(N_BOOT):
            samp = rng.choice(idx, size=len(idx), replace=True)
            boot.append(y[samp].mean())
        lo, hi = np.percentile(boot, [2.5, 97.5])
        rows.append({
            "decile": d, "n": int(mask.sum()),
            "prevalence": prev,
            "prev_lo": float(lo), "prev_hi": float(hi),
            "window_prev": wprev,
            "enrichment": prev / base_rate if base_rate > 1e-12 else np.nan,
        })
    return rows, decile, base_rate


def isotonic_calibration_metrics(train_scores: np.ndarray, train_y: np.ndarray,
                                   held_scores: np.ndarray, held_y: np.ndarray):
    """Fit isotonic on training, evaluate on held-out: slope, ECE, Brier."""
    iso = IsotonicRegression(out_of_bounds="clip")
    iso.fit(train_scores, train_y)
    p_held = iso.predict(held_scores)
    # calibration slope: linear regression of y on p
    if p_held.std() < 1e-12:
        slope = np.nan
    else:
        slope = float(np.cov(p_held, held_y, ddof=0)[0, 1] / p_held.var())
    # ECE: 10-bin reliability error
    bins = np.linspace(0, 1, 11)
    ece = 0.0
    for b in range(10):
        m = (p_held >= bins[b]) & (p_held < bins[b + 1] if b < 9 else p_held <= bins[b + 1])
        if m.sum() == 0:
            continue
        conf = p_held[m].mean()
        acc = held_y[m].mean()
        ece += (m.sum() / len(p_held)) * abs(conf - acc)
    brier = float(brier_score_loss(held_y, p_held))
    return float(slope) if np.isfinite(slope) else np.nan, float(ece), brier


def expected_tp_at_budget(scores: np.ndarray, y: np.ndarray, budget: int) -> float:
    k = min(budget, len(scores))
    top_k_idx = np.argsort(-scores)[:k]
    return float(y[top_k_idx].sum())


def top_vs_bottom_ci(scores: np.ndarray, y: np.ndarray, rng: np.random.Generator):
    """Bootstrap CI for top-decile minus bottom-decile prevalence,
    plus Spearman trend across deciles."""
    n = len(scores)
    ranks = stats.rankdata(scores, method="average") / n
    decile = np.minimum(N_DECILES - 1, (ranks * N_DECILES).astype(int))
    top_idx = np.where(decile == N_DECILES - 1)[0]
    bot_idx = np.where(decile == 0)[0]
    if len(top_idx) == 0 or len(bot_idx) == 0:
        return np.nan, np.nan, np.nan, np.nan, np.nan
    obs_delta = float(y[top_idx].mean() - y[bot_idx].mean())
    boot = []
    for _ in range(N_BOOT):
        t_samp = rng.choice(top_idx, size=len(top_idx), replace=True)
        b_samp = rng.choice(bot_idx, size=len(bot_idx), replace=True)
        boot.append(y[t_samp].mean() - y[b_samp].mean())
    lo, hi = np.percentile(boot, [2.5, 97.5])
    # Spearman: decile index vs prevalence per decile
    decile_means = np.array([y[decile == d].mean() if (decile == d).any() else np.nan
                              for d in range(N_DECILES)])
    valid = ~np.isnan(decile_means)
    if valid.sum() < 3:
        rho, p = np.nan, np.nan
    else:
        rho, p = stats.spearmanr(np.where(valid)[0], decile_means[valid])
    return obs_delta, float(lo), float(hi), float(rho), float(p)


def lopo_score_method(data: dict, method_name: str, scoring_fn):
    """For each pathogen, return (held_scores, held_y) using LOPO sign-fitting where applicable.
    scoring_fn(training_data, held_df) -> array of scores."""
    out = {}
    for held_p in data:
        training = {k: v for k, v in data.items() if k != held_p}
        signs = fit_signs(training, FEATURES)
        scores = scoring_fn(training, signs, data[held_p]["df"])
        out[held_p] = scores
    return out


def main():
    print("MutBench P2: Rank reliability + decision curves")
    print("=" * 60)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(RANDOM_SEED)
    data = load_data()
    if not data:
        sys.exit("No usable pathogens.")
    pathogens = list(data.keys())
    print(f"Loaded {len(pathogens)} pathogens")

    # Methods: name -> scoring_fn(training, signs, held_df) -> scores
    def make_subset_fn(subset):
        return lambda training, signs, held_df: equalweight_score(held_df, subset, signs)
    def random_fn(training, signs, held_df):
        rng_local = np.random.default_rng(RANDOM_SEED + 7)
        return rng_local.standard_normal(len(held_df))

    methods = {
        "4-core": make_subset_fn(CORE_4),
        "3-core": make_subset_fn(CORE_3),
        "full-10": make_subset_fn(tuple(FEATURES)),
        "freq-only": make_subset_fn(("freq",)),
        "entropy-only": make_subset_fn(("entropy",)),
        "homoplasy-only": make_subset_fn(("homoplasy",)),
        "random": random_fn,
    }

    # Score each pathogen × method
    print("Scoring all pathogen × method combinations...")
    scored = {m: lopo_score_method(data, m, fn) for m, fn in methods.items()}

    # Per-decile prevalence
    print("Computing per-decile prevalence + bootstrap CI...")
    decile_rows = []
    tvb_rows = []
    for m in methods:
        for p in pathogens:
            scores = scored[m][p]
            y = data[p]["y"]
            y_win = window_indicator(y, WINDOW_RADIUS)
            drows, _, _ = per_decile_metrics(scores, y, y_win, rng)
            for r in drows:
                r.update({"method": m, "pathogen": p, "base_rate": data[p]["base_rate"]})
                decile_rows.append(r)
            obs, lo, hi, rho, p_spear = top_vs_bottom_ci(scores, y, rng)
            tvb_rows.append({
                "method": m, "pathogen": p,
                "top_minus_bottom_prev": obs,
                "ci_lo": lo, "ci_hi": hi,
                "spearman_rho": rho, "spearman_p": p_spear,
                "ci_excludes_zero": bool(np.isfinite(lo) and np.isfinite(hi) and (lo > 0 or hi < 0)),
            })

    pd.DataFrame(decile_rows).to_csv(OUT_DIR / "p2_decile_prevalence.csv", index=False)
    pd.DataFrame(tvb_rows).to_csv(OUT_DIR / "p2_top_vs_bottom.csv", index=False)

    # Calibration (isotonic on training pathogens, evaluated on each held-out)
    print("Fitting isotonic calibration per (method, fold)...")
    cal_rows = []
    for m in methods:
        for held_p in pathogens:
            train_scores, train_y = [], []
            for p in pathogens:
                if p == held_p:
                    continue
                train_scores.append(scored[m][p])
                train_y.append(data[p]["y"])
            ts = np.concatenate(train_scores)
            ty = np.concatenate(train_y)
            hs = scored[m][held_p]
            hy = data[held_p]["y"]
            slope, ece, brier = isotonic_calibration_metrics(ts, ty, hs, hy)
            cal_rows.append({
                "method": m, "pathogen": held_p,
                "calibration_slope": slope,
                "ece": ece, "brier": brier,
            })
    pd.DataFrame(cal_rows).to_csv(OUT_DIR / "p2_calibration.csv", index=False)

    # Decision curve
    print("Computing decision curves...")
    dec_rows = []
    for m in methods:
        for p in pathogens:
            scores = scored[m][p]
            y = data[p]["y"]
            for b in BUDGETS:
                tp = expected_tp_at_budget(scores, y, b)
                dec_rows.append({"method": m, "pathogen": p, "budget": b, "expected_tp": tp})
    pd.DataFrame(dec_rows).to_csv(OUT_DIR / "p2_decision_curve.csv", index=False)

    # Aggregate summaries
    print("\n=== Top-vs-bottom prevalence delta (positive = monotonic) ===")
    tvb = pd.DataFrame(tvb_rows)
    summary = tvb.groupby("method").agg(
        mean_delta=("top_minus_bottom_prev", "mean"),
        n_ci_excludes_zero=("ci_excludes_zero", "sum"),
        n_pathogens=("pathogen", "count"),
        mean_spearman=("spearman_rho", "mean"),
    ).reset_index()
    print(summary.to_string(index=False))
    summary.to_csv(OUT_DIR / "p2_method_summary.csv", index=False)

    # Reliability figure: deciles vs prevalence per pathogen for 4-core, faceted
    print("\nGenerating reliability figure...")
    fig, axes = plt.subplots(3, 4, figsize=(14, 8.5), sharey=True)
    dec_df = pd.DataFrame(decile_rows)
    for ax, p in zip(axes.flat, pathogens):
        for m, color in [("4-core", "red"), ("3-core", "darkblue"),
                          ("full-10", "gray"), ("random", "lightgray")]:
            sub = dec_df[(dec_df["method"] == m) & (dec_df["pathogen"] == p)]
            sub = sub.sort_values("decile")
            ax.plot(sub["decile"], sub["prevalence"], "o-", label=m, color=color,
                    alpha=0.85 if m in ("4-core", "3-core") else 0.5,
                    lw=1.8 if m in ("4-core", "3-core") else 1.0)
        ax.axhline(data[p]["base_rate"], ls=":", color="black", alpha=0.5)
        ax.set_title(p, fontsize=10)
        ax.set_xticks(range(0, N_DECILES, 2))
        ax.grid(alpha=0.3)
    axes[0, 0].legend(loc="upper left", fontsize=8)
    fig.suptitle("P2: Per-decile Layer A prevalence (12 pathogens; dotted = base rate)",
                 fontsize=12)
    fig.text(0.5, 0.02, "Score decile (0=lowest, 9=highest)", ha="center")
    fig.text(0.005, 0.5, "Layer A prevalence", va="center", rotation="vertical")
    fig.tight_layout(rect=[0.01, 0.03, 1.0, 0.96])
    fig.savefig(OUT_DIR / "p2_reliability.png", dpi=150)

    # Decision curve figure
    fig, axes = plt.subplots(3, 4, figsize=(14, 8.5), sharey=True)
    dec_curve_df = pd.DataFrame(dec_rows)
    for ax, p in zip(axes.flat, pathogens):
        for m, color in [("4-core", "red"), ("3-core", "darkblue"),
                          ("full-10", "gray"), ("random", "lightgray")]:
            sub = dec_curve_df[(dec_curve_df["method"] == m) & (dec_curve_df["pathogen"] == p)]
            sub = sub.sort_values("budget")
            ax.plot(sub["budget"], sub["expected_tp"], "o-", label=m, color=color,
                    alpha=0.85 if m in ("4-core", "3-core") else 0.5,
                    lw=1.8 if m in ("4-core", "3-core") else 1.0)
        ax.set_title(p, fontsize=10)
        ax.set_xticks(BUDGETS)
        ax.grid(alpha=0.3)
    axes[0, 0].legend(loc="upper left", fontsize=8)
    fig.suptitle("P2: Decision curves — TPs at screening budgets {20, 50, 80}", fontsize=12)
    fig.text(0.5, 0.02, "Screening budget (top-k positions)", ha="center")
    fig.text(0.005, 0.5, "Expected true positives", va="center", rotation="vertical")
    fig.tight_layout(rect=[0.01, 0.03, 1.0, 0.96])
    fig.savefig(OUT_DIR / "p2_decision_curve.png", dpi=150)

    # Headline numbers
    print("\n=== Headline numbers ===")
    for m in ["4-core", "3-core", "full-10"]:
        sub = tvb[tvb["method"] == m]
        excl = int(sub["ci_excludes_zero"].sum())
        mean_delta = float(sub["top_minus_bottom_prev"].mean())
        mean_rho = float(sub["spearman_rho"].mean())
        cal_sub = pd.DataFrame(cal_rows)
        cal_sub = cal_sub[cal_sub["method"] == m]
        ece = float(cal_sub["ece"].mean())
        # Decision curve at budget=50, sum across pathogens
        dec50 = float(dec_curve_df[(dec_curve_df["method"] == m) & (dec_curve_df["budget"] == 50)]["expected_tp"].sum())
        print(f"  {m:14s}: top-bot delta mean = {mean_delta:+.4f}, "
              f"CI excludes 0 in {excl}/{len(sub)} pathogens, "
              f"mean Spearman rho = {mean_rho:+.3f}, mean ECE = {ece:.3f}, "
              f"sum TP@budget=50 = {dec50:.0f}")

    print(f"\nDone. Outputs in {OUT_DIR}/p2_*")


if __name__ == "__main__":
    main()
