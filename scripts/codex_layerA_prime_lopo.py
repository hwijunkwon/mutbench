#!/usr/bin/env python3
"""Layer A' sensitivity-panel LOPO benchmark.

Mirrors the Wave 4 labeled-only 2-core machinery on the 10 UniProt-curated
Layer A' targets: median Pearson signs, signed z-score averaging, top-10%
thresholding, MCC, precision@20, and top-vs-bottom decile bootstrap.
"""

from __future__ import annotations

import math
import os
import warnings
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.stats as stats


RANDOM_SEED = 42
TOP10_FRAC = 0.10
PRECISION_K = 20
N_BOOTSTRAP = 1000
FEATURES = ("freq", "entropy")
ROOT = Path(__file__).resolve().parents[1]
IN_DIR = ROOT / "results" / "mutbench" / "feature_matrix_layerA_prime"
INVENTORY_CSV = ROOT / "results" / "mutbench" / "layerA_prime_inventory.csv"
OUT_DIR = ROOT / "results" / "mutbench" / "codex_layerA_prime"
REPORT_DIR = ROOT / "paper" / "dissertation" / "review" / "2026-05-02" / "wave5_replacement"
REPORT_PATH = REPORT_DIR / "lap_lopo_report.md"
W4_LOPO_CSV = ROOT / "results" / "mutbench" / "codex_wave4" / "w4_labeled_lopo_per_fold.csv"

TARGETS = [
    "lassa_gpc",
    "measles_virus_h",
    "mumps_virus_hn",
    "hcov-229e_spike",
    "hcov-nl63_spike",
    "yfv_e",
    "wnv_e",
    "japanese_encephalitis_virus_e",
    "tick-borne_encephalitis_virus_e",
    "eastern_equine_encephalitis_virus_e2",
]


warnings.filterwarnings("ignore", category=RuntimeWarning)


def require_columns(path: Path, df: pd.DataFrame, columns: list[str]) -> None:
    missing = [column for column in columns if column not in df.columns]
    if missing:
        raise ValueError(f"{path} missing required columns: {missing}")


def load_data() -> dict[str, dict]:
    inventory = pd.read_csv(INVENTORY_CSV)
    require_columns(INVENTORY_CSV, inventory, ["target", "n_layer_a_prime_positions"])
    inv = inventory.set_index("target", drop=False)
    data: dict[str, dict] = {}
    for slug in TARGETS:
        path = IN_DIR / f"{slug}.csv"
        df = pd.read_csv(path)
        require_columns(path, df, ["position", "freq", "entropy", "layer_a_prime"])
        df = df[["position", "freq", "entropy", "layer_a_prime"]].copy()
        df["position"] = df["position"].astype(int)
        df["layer_a_prime"] = df["layer_a_prime"].astype(int)
        y = df["layer_a_prime"].to_numpy(dtype=int)
        if y.sum() == 0 or y.sum() == len(y):
            raise ValueError(f"{slug} has degenerate layer_a_prime labels")
        inv_count = int(inv.loc[slug, "n_layer_a_prime_positions"]) if slug in inv.index else int(y.sum())
        if inv_count != int(y.sum()):
            raise ValueError(f"{slug} inventory count {inv_count} != matrix count {int(y.sum())}")
        data[slug] = {
            "df": df,
            "y": y,
            "n": int(len(df)),
            "n_pos": int(y.sum()),
            "prevalence": float(y.mean()),
        }
    return data


def pearson_r(df: pd.DataFrame, y: np.ndarray, feature: str) -> float:
    x = np.nan_to_num(df[feature].to_numpy(dtype=float), nan=0.0, posinf=0.0, neginf=0.0)
    yf = y.astype(float)
    if x.std() < 1e-12 or yf.std() < 1e-12:
        return np.nan
    return float(np.corrcoef(x, yf)[0, 1])


def pearson_sign_for_target(df: pd.DataFrame, y: np.ndarray, feature: str) -> float:
    r = pearson_r(df, y, feature)
    return -1.0 if np.isfinite(r) and r < 0 else 1.0


def fit_median_signs(training_data: dict[str, dict], features: tuple[str, ...] = FEATURES) -> dict[str, float]:
    signs = {}
    for feature in features:
        per_target_signs = [
            pearson_sign_for_target(d["df"], d["y"], feature)
            for d in training_data.values()
        ]
        median = float(np.median(per_target_signs))
        signs[feature] = -1.0 if median < 0 else 1.0
    return signs


def signed_zscore_average(df: pd.DataFrame, signs: dict[str, float], features: tuple[str, ...] = FEATURES) -> np.ndarray:
    parts = []
    for feature in features:
        x = np.nan_to_num(df[feature].to_numpy(dtype=float), nan=0.0, posinf=0.0, neginf=0.0)
        std = float(x.std())
        if std <= 1e-10:
            parts.append(np.zeros(len(df), dtype=float))
        else:
            parts.append(((x - x.mean()) / std) * signs.get(feature, 1.0))
    return np.vstack(parts).mean(axis=0)


def topk_pred(scores: np.ndarray, k: int) -> np.ndarray:
    k = max(1, min(int(k), len(scores)))
    pred = np.zeros(len(scores), dtype=int)
    order = np.lexsort((np.arange(len(scores)), -scores))
    pred[order[:k]] = 1
    return pred


def top_fraction_pred(scores: np.ndarray, fraction: float = TOP10_FRAC) -> np.ndarray:
    return topk_pred(scores, int(np.ceil(len(scores) * fraction)))


def safe_mcc(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    y_true = np.asarray(y_true, dtype=int)
    y_pred = np.asarray(y_pred, dtype=int)
    if y_pred.sum() == 0 or y_pred.sum() == len(y_pred):
        return 0.0
    if y_true.sum() == 0 or y_true.sum() == len(y_true):
        return 0.0
    tp = int(((y_true == 1) & (y_pred == 1)).sum())
    tn = int(((y_true == 0) & (y_pred == 0)).sum())
    fp = int(((y_true == 0) & (y_pred == 1)).sum())
    fn = int(((y_true == 1) & (y_pred == 0)).sum())
    denom = math.sqrt(float(tp + fp) * float(tp + fn) * float(tn + fp) * float(tn + fn))
    if denom < 1e-12:
        return 0.0
    return float((tp * tn - fp * fn) / denom)


def topk_tp(scores: np.ndarray, y: np.ndarray, k: int) -> int:
    k = min(k, len(scores))
    order = np.lexsort((np.arange(len(scores)), -scores))
    return int(y[order[:k]].sum())


def precision_at_k(scores: np.ndarray, y: np.ndarray, k: int = PRECISION_K) -> float:
    k = min(k, len(scores))
    return float(topk_tp(scores, y, k) / k) if k > 0 else 0.0


def top_bottom_decile_delta_with_ci(
    scores: np.ndarray,
    y: np.ndarray,
    rng: np.random.Generator,
    n_bootstrap: int = N_BOOTSTRAP,
) -> tuple[float, float, float]:
    n_top = max(1, int(np.ceil(len(scores) / 10)))
    top_idx = np.lexsort((np.arange(len(scores)), -scores))[:n_top]
    bottom_idx = np.lexsort((np.arange(len(scores)), scores))[:n_top]
    obs = float(y[top_idx].mean() - y[bottom_idx].mean())
    boot = np.empty(n_bootstrap, dtype=float)
    for i in range(n_bootstrap):
        t_samp = rng.choice(top_idx, size=len(top_idx), replace=True)
        b_samp = rng.choice(bottom_idx, size=len(bottom_idx), replace=True)
        boot[i] = y[t_samp].mean() - y[b_samp].mean()
    lo, hi = np.percentile(boot, [2.5, 97.5])
    return obs, float(lo), float(hi)


def stage1_per_target(data: dict[str, dict], rng: np.random.Generator) -> pd.DataFrame:
    rows = []
    for slug in TARGETS:
        d = data[slug]
        training = {k: v for k, v in data.items() if k != slug}
        signs = fit_median_signs(training)
        scores = signed_zscore_average(d["df"], signs)
        pred = top_fraction_pred(scores)
        rows.append(
            {
                "target": slug,
                "n_positions": d["n"],
                "n_layer_a_prime": d["n_pos"],
                "prevalence": d["prevalence"],
                "pearson_freq_layer_a_prime": pearson_r(d["df"], d["y"], "freq"),
                "pearson_entropy_layer_a_prime": pearson_r(d["df"], d["y"], "entropy"),
                "sign_freq_other9": int(signs["freq"]),
                "sign_entropy_other9": int(signs["entropy"]),
                "mcc_top10_other9_signed_2core": safe_mcc(d["y"], pred),
            }
        )
    return pd.DataFrame(rows)


def stage2_lopo(data: dict[str, dict], rng: np.random.Generator) -> tuple[pd.DataFrame, pd.DataFrame]:
    rows = []
    for held in TARGETS:
        training = {k: v for k, v in data.items() if k != held}
        signs = fit_median_signs(training)
        d = data[held]
        scores = signed_zscore_average(d["df"], signs)
        pred = top_fraction_pred(scores)
        delta, lo, hi = top_bottom_decile_delta_with_ci(scores, d["y"], rng)
        rows.append(
            {
                "heldout_target": held,
                "n_positions": d["n"],
                "n_layer_a_prime": d["n_pos"],
                "prevalence": d["prevalence"],
                "sign_freq": int(signs["freq"]),
                "sign_entropy": int(signs["entropy"]),
                "mcc_top10": safe_mcc(d["y"], pred),
                "precision_at_20": precision_at_k(scores, d["y"], PRECISION_K),
                "top_bottom_decile_delta": delta,
                "top_bottom_decile_delta_ci_lo": lo,
                "top_bottom_decile_delta_ci_hi": hi,
                "n_top10_predicted": int(pred.sum()),
                "tp_top10": int(d["y"][pred == 1].sum()),
            }
        )
    per_fold = pd.DataFrame(rows)
    summary = pd.DataFrame(
        [
            {
                "mean_mcc": float(per_fold["mcc_top10"].mean()),
                "median_mcc": float(per_fold["mcc_top10"].median()),
                "sd_mcc": float(per_fold["mcc_top10"].std(ddof=1)),
                "n_positive_folds": int((per_fold["mcc_top10"] > 0).sum()),
                "n_total_folds": int(per_fold.shape[0]),
                "mean_precision_at_20": float(per_fold["precision_at_20"].mean()),
                "mean_top_bottom_decile_delta": float(per_fold["top_bottom_decile_delta"].mean()),
                "random_seed": RANDOM_SEED,
            }
        ]
    )
    return per_fold, summary


def stage3_sign_bootstrap(data: dict[str, dict], n_bootstrap: int = N_BOOTSTRAP, seed: int = RANDOM_SEED) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    full_signs = fit_median_signs(data)
    targets = list(data.keys())
    signs = []
    for _ in range(n_bootstrap):
        sampled = rng.choice(targets, size=len(targets), replace=True).tolist()
        sampled_data = {f"{i}:{slug}": data[slug] for i, slug in enumerate(sampled)}
        signs.append(fit_median_signs(sampled_data))
    rows = []
    for feature in FEATURES:
        vals = np.array([s[feature] for s in signs], dtype=float)
        rows.append(
            {
                "feature": feature,
                "full_sample_sign": int(full_signs[feature]),
                "n_bootstrap": n_bootstrap,
                "fraction_preserve_full_sample_sign": float((vals == full_signs[feature]).mean()),
                "fraction_positive_sign": float((vals > 0).mean()),
                "fraction_negative_sign": float((vals < 0).mean()),
                "random_seed": seed,
            }
        )
    return pd.DataFrame(rows)


def stage4_cross_panel(per_fold: pd.DataFrame, summary: pd.DataFrame) -> pd.DataFrame:
    w4_mean = 0.077
    w4_sd = 0.136
    w4_n = 12
    lap = summary.iloc[0]
    test = stats.ttest_ind_from_stats(
        mean1=float(lap["mean_mcc"]),
        std1=float(lap["sd_mcc"]),
        nobs1=int(lap["n_total_folds"]),
        mean2=w4_mean,
        std2=w4_sd,
        nobs2=w4_n,
        equal_var=False,
    )
    return pd.DataFrame(
        [
            {
                "panel": "Wave4_labeled_12_target",
                "provenance": "literature_curated",
                "n_folds": w4_n,
                "mcc_mean": w4_mean,
                "mcc_sd": w4_sd,
                "n_positive_folds": 8,
                "welch_t_vs_other_panel": float(-test.statistic),
                "welch_p_two_sided": float(test.pvalue),
                "caveat": "Unpaired comparison; panels differ in provenance and target identity.",
            },
            {
                "panel": "LayerA_prime_10_target",
                "provenance": "UniProt_curated",
                "n_folds": int(lap["n_total_folds"]),
                "mcc_mean": float(lap["mean_mcc"]),
                "mcc_sd": float(lap["sd_mcc"]),
                "n_positive_folds": int(lap["n_positive_folds"]),
                "welch_t_vs_other_panel": float(test.statistic),
                "welch_p_two_sided": float(test.pvalue),
                "caveat": "Unpaired comparison; panels differ in provenance and target identity.",
            },
        ]
    )


def assign_branch(mean_mcc: float, n_positive: int) -> str:
    if mean_mcc >= 0.05 and n_positive >= 6:
        return "A"
    if mean_mcc < 0.0 or n_positive <= 3:
        return "C"
    return "B"


def write_figure(per_fold: pd.DataFrame, sign_boot: pd.DataFrame) -> None:
    fig, axes = plt.subplots(2, 2, figsize=(14, 10), dpi=200)
    ax = axes[0, 0]
    colors = ["#2b8cbe" if v > 0 else "#d95f0e" for v in per_fold["mcc_top10"]]
    ax.bar(range(len(per_fold)), per_fold["mcc_top10"], color=colors)
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_xticks(range(len(per_fold)))
    ax.set_xticklabels(per_fold["heldout_target"], rotation=45, ha="right", fontsize=8)
    ax.set_ylabel("MCC at top 10%")
    ax.set_title("A. Layer A' LOPO folds", loc="left")

    ax = axes[0, 1]
    ax.scatter(per_fold["prevalence"], per_fold["mcc_top10"], color="#2b8cbe")
    for row in per_fold.itertuples(index=False):
        ax.annotate(row.heldout_target, (row.prevalence, row.mcc_top10), fontsize=7, xytext=(3, 3), textcoords="offset points")
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_xlabel("Layer A' prevalence")
    ax.set_ylabel("MCC at top 10%")
    ax.set_title("B. Prevalence vs MCC", loc="left")

    ax = axes[1, 0]
    ax.bar(sign_boot["feature"], sign_boot["fraction_preserve_full_sample_sign"], color=["#2b8cbe", "#7b3294"])
    ax.set_ylim(0, 1.05)
    ax.set_ylabel("Bootstrap fraction")
    ax.set_title("C. Sign stability", loc="left")

    ax = axes[1, 1]
    layer_vals = per_fold["mcc_top10"].to_numpy(dtype=float)
    if W4_LOPO_CSV.exists():
        w4 = pd.read_csv(W4_LOPO_CSV)
        w4_col = "mcc_top10" if "mcc_top10" in w4.columns else "mcc"
        w4_vals = w4[w4_col].to_numpy(dtype=float)
        ax.boxplot([w4_vals, layer_vals], tick_labels=["Wave 4", "Layer A'"], showmeans=True)
    else:
        ax.errorbar([1], [0.077], yerr=[0.136], fmt="o", capsize=5, color="#4d4d4d", label="Wave 4 mean +/- SD")
        ax.boxplot([layer_vals], positions=[2], tick_labels=["Layer A'"], showmeans=True)
        ax.set_xticks([1, 2])
        ax.set_xticklabels(["Wave 4", "Layer A'"])
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_ylabel("MCC at top 10%")
    ax.set_title("D. Cross-panel MCC", loc="left")

    fig.tight_layout()
    fig.savefig(OUT_DIR / "summary_figure.png")
    plt.close(fig)


def markdown_table(df: pd.DataFrame) -> str:
    columns = [str(col) for col in df.columns]
    rows = [[str(value) for value in row] for row in df.itertuples(index=False, name=None)]
    widths = [
        max(len(columns[i]), *(len(row[i]) for row in rows))
        for i in range(len(columns))
    ]
    header = "| " + " | ".join(columns[i].ljust(widths[i]) for i in range(len(columns))) + " |"
    separator = "| " + " | ".join("-" * widths[i] for i in range(len(columns))) + " |"
    body = [
        "| " + " | ".join(row[i].ljust(widths[i]) for i in range(len(columns))) + " |"
        for row in rows
    ]
    return "\n".join([header, separator, *body])


def write_report(per_fold: pd.DataFrame, summary: pd.DataFrame, sign_boot: pd.DataFrame, cross: pd.DataFrame) -> str:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    s = summary.iloc[0]
    mean_mcc = float(s["mean_mcc"])
    sd_mcc = float(s["sd_mcc"])
    med_mcc = float(s["median_mcc"])
    n_positive = int(s["n_positive_folds"])
    branch = assign_branch(mean_mcc, n_positive)
    branch_text = {
        "A": "Layer A' sensitivity panel preserves the bounded directional signal under different label provenance.",
        "B": "weak signal preservation; sensitivity analysis bounded but inconclusive.",
        "C": "Layer A' label provenance does not preserve the signal - supports keeping 12-panel as primary and not extending.",
    }[branch]
    w4 = cross[cross["panel"] == "Wave4_labeled_12_target"].iloc[0]
    lap = cross[cross["panel"] == "LayerA_prime_10_target"].iloc[0]

    table = per_fold[["heldout_target", "prevalence", "mcc_top10", "precision_at_20", "top_bottom_decile_delta"]].copy()
    table["prevalence"] = table["prevalence"].map(lambda x: f"{100 * x:.1f}%")
    table["mcc_top10"] = table["mcc_top10"].map(lambda x: f"{x:.3f}")
    table["precision_at_20"] = table["precision_at_20"].map(lambda x: f"{x:.3f}")
    table["top_bottom_decile_delta"] = table["top_bottom_decile_delta"].map(lambda x: f"{x:.3f}")

    sign_lines = ", ".join(
        f"{row.feature}={row.fraction_preserve_full_sample_sign:.3f}"
        for row in sign_boot.itertuples(index=False)
    )

    report = f"""# Layer A' LOPO Sensitivity Benchmark

## Headline numbers

The 10-target Layer A' LOPO benchmark gives mean MCC={mean_mcc:.3f}, median MCC={med_mcc:.3f}, SD={sd_mcc:.3f}, with {n_positive}/10 positive folds. Precision@20 averages {s['mean_precision_at_20']:.3f}. The predeclared interpretation is **Branch {branch}**: {branch_text}

Sign stability under 1000 target-level bootstrap resamples preserves the full-sample sign at: {sign_lines}.

## Per-target results

{markdown_table(table)}

## Cross-panel comparison

The Wave 4 labeled 12-target baseline is MCC mean={w4.mcc_mean:.3f}, SD={w4.mcc_sd:.3f}, with {int(w4.n_positive_folds)}/12 positive folds. The Layer A' panel is MCC mean={lap.mcc_mean:.3f}, SD={lap.mcc_sd:.3f}, with {int(lap.n_positive_folds)}/10 positive folds. Because the panels differ in target identity and label provenance, paired Wilcoxon is not applicable. The unpaired Welch t-test is reported only as a descriptive cross-panel check: t={lap.welch_t_vs_other_panel:.3f}, two-sided p={lap.welch_p_two_sided:.3g}.

## Caveats

The four flavivirus targets yfv_e, wnv_e, japanese_encephalitis_virus_e, and tick-borne_encephalitis_virus_e share the same 98-111 fusion-peptide annotation, so their labels are correlated and should not be read as four fully independent biological replications.

The panel is small (n=10), so fold-count thresholds are intentionally coarse and the uncertainty around the mean MCC remains material.

The Layer A' labels come from UniProt feature-derived annotations. Feature-density and annotation-practice bias can inflate or suppress apparent signal depending on which proteins have detailed curated records.

The comparison to Wave 4 is cross-provenance: Wave 4 used literature-curated Layer A labels on a 12-target panel, while Layer A' is UniProt-curated and uses different target identities. The benchmark tests sensitivity to label provenance, not a clean replacement experiment.

## Recommendation for chapter 5 framing

Frame Layer A' as a bounded sensitivity analysis rather than as the primary evidence layer. The prose should state that the Wave 4 12-panel remains the primary labeled benchmark, while Layer A' checks whether the directional 2-core signal survives a stricter structured-database provenance. Use the Branch {branch} wording above as the main interpretive sentence, then immediately qualify it with the shared flavivirus annotation and provenance caveats.
"""
    REPORT_PATH.write_text(report, encoding="utf-8")
    return branch


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(RANDOM_SEED)
    data = load_data()

    per_target = stage1_per_target(data, rng)
    per_fold, summary = stage2_lopo(data, rng)
    sign_boot = stage3_sign_bootstrap(data)
    cross = stage4_cross_panel(per_fold, summary)

    per_target.to_csv(OUT_DIR / "per_target.csv", index=False)
    per_fold.to_csv(OUT_DIR / "lopo_per_fold.csv", index=False)
    summary.to_csv(OUT_DIR / "lopo_summary.csv", index=False)
    sign_boot.to_csv(OUT_DIR / "sign_bootstrap.csv", index=False)
    cross.to_csv(OUT_DIR / "cross_panel_comparison.csv", index=False)
    write_figure(per_fold, sign_boot)
    branch = write_report(per_fold, summary, sign_boot, cross)

    print(f"Wrote {OUT_DIR / 'per_target.csv'}")
    print(f"Wrote {OUT_DIR / 'lopo_per_fold.csv'}")
    print(f"Wrote {OUT_DIR / 'lopo_summary.csv'}")
    print(f"Wrote {OUT_DIR / 'sign_bootstrap.csv'}")
    print(f"Wrote {OUT_DIR / 'cross_panel_comparison.csv'}")
    print(f"Wrote {OUT_DIR / 'summary_figure.png'}")
    print(f"Wrote {REPORT_PATH}")
    print(
        f"RESULT: Branch={branch} "
        f"MCC_mean={summary.iloc[0]['mean_mcc']:.6f} "
        f"n_positive={int(summary.iloc[0]['n_positive_folds'])}/10"
    )


if __name__ == "__main__":
    main()
