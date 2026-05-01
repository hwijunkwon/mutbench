#!/usr/bin/env python3
"""Wave 4 Tier-2 feature/LOPO scaffold.

Task 1 implements only --audit-only. Modeling modes are reserved for later
Wave 4 tasks and intentionally raise NotImplementedError.
"""

from __future__ import annotations

import argparse
import json
import math
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import scipy.stats as stats
from sklearn.metrics import matthews_corrcoef


random_seed = 42
RANDOM_SEED = random_seed
RNG = np.random.default_rng(42)
warnings.filterwarnings("ignore", category=RuntimeWarning)

ROOT = Path(__file__).resolve().parents[1]
FEATURE_DIR = ROOT / "results" / "mutbench" / "feature_analysis"
CROSS_DIR = ROOT / "data" / "cross_pathogen"
OUT_DIR = ROOT / "results" / "mutbench" / "codex_wave4"

INVENTORY_CSV = OUT_DIR / "w4_input_inventory.csv"
SCHEMA_AUDIT_CSV = OUT_DIR / "w4_feature_schema_audit.csv"
LABELED_LOPO_PER_FOLD_CSV = OUT_DIR / "w4_labeled_lopo_per_fold.csv"
LABELED_LOPO_SUMMARY_CSV = OUT_DIR / "w4_labeled_lopo_summary.csv"
LABELED_CALLABILITY_RECHECK_CSV = OUT_DIR / "w4_labeled_callability_recheck.csv"
EXPANDED_TARGET_SCORES_CSV = OUT_DIR / "w4_expanded_target_scores.csv"
EXPANDED_STABILITY_PER_TARGET_CSV = OUT_DIR / "w4_expanded_stability_per_target.csv"
EXPANDED_QUORUM_REACHABILITY_CSV = OUT_DIR / "w4_expanded_quorum_reachability.csv"
OVERLAP_SCHEMA_DRIFT_CSV = OUT_DIR / "w4_overlap_schema_drift.csv"

OVERLAP_SLUGS = {"dengue_e", "hiv1_gp120", "norovirus_vp1"}
OVERLAP_PAIRS = {
    "Dengue": "dengue_e",
    "HIV-1": "hiv1_gp120",
    "Norovirus": "norovirus_vp1",
}
ALL_PATHOGENS = [
    "SARS-CoV-2",
    "H3N2",
    "Norovirus",
    "HIV-1",
    "Dengue",
    "RSV",
    "Influenza_B",
    "MERS",
    "HCV",
    "Zika",
    "Rabies",
    "EV-A71",
]
TWO_CORE_FEATURES = ("freq", "entropy")
HISTORICAL_4CORE_FEATURES = ("freq", "entropy", "homoplasy", "plddt")
TOP10_FRAC = 0.10
WINDOW_RADIUS = 10
PRECISION_K = 20
N_DECILES = 10
D1_QUORUM = 7
D1_LOWER_CI_MIN = 0.02
D1_POINT_MIN = 0.05
D1_BOOT = 1000
EXPANDED_BOOT = 1000


def slug_label(slug: str) -> str:
    return slug.replace("_", " ").replace("-", " ").title()


def clean_values(values: pd.Series) -> str:
    cleaned = []
    for value in sorted(values.dropna().unique().tolist()):
        if isinstance(value, (np.integer, int)):
            cleaned.append(int(value))
        elif isinstance(value, (np.floating, float)) and float(value).is_integer():
            cleaned.append(int(value))
        elif isinstance(value, (np.floating, float)):
            cleaned.append(float(value))
        else:
            cleaned.append(value)
    return json.dumps(cleaned, separators=(",", ":"))


def require_columns(path: Path, df: pd.DataFrame, columns: list[str]) -> None:
    missing = [column for column in columns if column not in df.columns]
    if missing:
        raise ValueError(f"{path} missing required columns: {missing}")


def build_inventory() -> pd.DataFrame:
    rows = []

    feature_paths = sorted(FEATURE_DIR.glob("feature_matrix_*.csv"))
    cross_paths = sorted(CROSS_DIR.glob("*_position_scores.csv"))

    for path in feature_paths:
        pathogen = path.stem.removeprefix("feature_matrix_")
        df = pd.read_csv(path)
        require_columns(path, df, ["position", "freq", "entropy", "layer_a"])
        rows.append(
            {
                "slug": pathogen,
                "pathogen_label": pathogen,
                "source_type": "feature_matrix",
                "is_labeled": True,
                "is_overlap": False,
                "audit_only": False,
                "unique_target_inclusion": True,
                "n_positions": int(df.shape[0]),
                "has_freq": "freq" in df.columns,
                "has_entropy": "entropy" in df.columns,
                "has_hscore": "hscore" in df.columns,
                "has_layer_a": "layer_a" in df.columns,
                "ground_truth_values": clean_values(df["layer_a"]),
            }
        )

    for path in cross_paths:
        slug = path.stem.removesuffix("_position_scores")
        is_overlap = slug in OVERLAP_SLUGS
        df = pd.read_csv(path)
        require_columns(path, df, ["position", "frequency", "entropy", "hscore", "ground_truth"])
        rows.append(
            {
                "slug": slug,
                "pathogen_label": slug_label(slug),
                "source_type": "cross_pathogen",
                "is_labeled": False,
                "is_overlap": is_overlap,
                "audit_only": is_overlap,
                "unique_target_inclusion": not is_overlap,
                "n_positions": int(df.shape[0]),
                "has_freq": "frequency" in df.columns,
                "has_entropy": "entropy" in df.columns,
                "has_hscore": "hscore" in df.columns,
                "has_layer_a": "layer_a" in df.columns,
                "ground_truth_values": clean_values(df["ground_truth"]),
            }
        )

    return pd.DataFrame(
        rows,
        columns=[
            "slug",
            "pathogen_label",
            "source_type",
            "is_labeled",
            "is_overlap",
            "audit_only",
            "unique_target_inclusion",
            "n_positions",
            "has_freq",
            "has_entropy",
            "has_hscore",
            "has_layer_a",
            "ground_truth_values",
        ],
    )


def top_fraction_positions(df: pd.DataFrame, score_col: str, fraction: float = 0.10) -> set[int]:
    n_top = max(1, int(np.ceil(df.shape[0] * fraction)))
    ranked = df.sort_values([score_col, "position"], ascending=[False, True], kind="mergesort")
    return set(ranked.head(n_top)["position"].astype(int).tolist())


def build_schema_audit() -> pd.DataFrame:
    rows = []
    for pathogen, cross_slug in OVERLAP_PAIRS.items():
        labeled_path = FEATURE_DIR / f"feature_matrix_{pathogen}.csv"
        cross_path = CROSS_DIR / f"{cross_slug}_position_scores.csv"

        labeled = pd.read_csv(labeled_path)
        cross = pd.read_csv(cross_path)
        require_columns(labeled_path, labeled, ["position", "freq", "entropy"])
        require_columns(cross_path, cross, ["position", "hscore"])

        labeled_work = labeled[["position", "freq", "entropy"]].copy()
        labeled_work["hscore_labeled"] = labeled_work["freq"] * labeled_work["entropy"]
        cross_work = cross[["position", "hscore"]].rename(columns={"hscore": "hscore_cross"})

        aligned = labeled_work.merge(cross_work, on="position", how="inner")
        if aligned.shape[0] < 2:
            rho = np.nan
            pvalue = np.nan
        else:
            result = stats.spearmanr(aligned["hscore_labeled"], aligned["hscore_cross"])
            rho = float(result.statistic)
            pvalue = float(result.pvalue)

        top_labeled = top_fraction_positions(aligned, "hscore_labeled")
        top_cross = top_fraction_positions(aligned, "hscore_cross")
        intersection = top_labeled & top_cross
        union = top_labeled | top_cross
        jaccard = float(len(intersection) / len(union)) if union else np.nan
        harmonizable = bool(rho >= 0.70 and jaccard >= 0.50)

        rows.append(
            {
                "pathogen_pair": f"{pathogen}:{cross_slug}",
                "n_positions_labeled": int(labeled.shape[0]),
                "n_positions_cross": int(cross.shape[0]),
                "n_positions_aligned": int(aligned.shape[0]),
                "spearman_rho": rho,
                "spearman_p": pvalue,
                "top10pct_jaccard": jaccard,
                "top10pct_overlap_count": int(len(intersection)),
                "harmonizable_per_threshold": harmonizable,
            }
        )

    return pd.DataFrame(
        rows,
        columns=[
            "pathogen_pair",
            "n_positions_labeled",
            "n_positions_cross",
            "n_positions_aligned",
            "spearman_rho",
            "spearman_p",
            "top10pct_jaccard",
            "top10pct_overlap_count",
            "harmonizable_per_threshold",
        ],
    )


def print_invariants(inventory: pd.DataFrame) -> bool:
    checks = [
        ("unique_target_inclusion == 28", inventory[inventory.unique_target_inclusion].shape[0] == 28),
        ("audit_only == 3", inventory[inventory.audit_only].shape[0] == 3),
        (
            "source_type feature_matrix == 12",
            inventory[inventory.source_type == "feature_matrix"].shape[0] == 12,
        ),
        (
            "source_type cross_pathogen == 19",
            inventory[inventory.source_type == "cross_pathogen"].shape[0] == 19,
        ),
    ]
    all_passed = True
    print("Inventory invariants:")
    for label, passed in checks:
        print(f"  {'PASS' if passed else 'FAIL'} {label}")
        all_passed = all_passed and passed
    return all_passed


def print_schema_summary(schema_audit: pd.DataFrame) -> None:
    print("Schema hscore overlap audit:")
    for row in schema_audit.itertuples(index=False):
        verdict = "PASS" if row.harmonizable_per_threshold else "FAIL"
        print(
            "  "
            f"{verdict} {row.pathogen_pair}: "
            f"aligned={row.n_positions_aligned}, "
            f"rho={row.spearman_rho:.4f}, "
            f"p={row.spearman_p:.4g}, "
            f"top10_jaccard={row.top10pct_jaccard:.4f}, "
            f"top10_overlap={row.top10pct_overlap_count}"
        )

    n_harmonizable = int(schema_audit["harmonizable_per_threshold"].sum())
    if n_harmonizable < 2:
        verdict = "2-core fallback recommended"
    else:
        verdict = "hscore harmonization gate passes"
    print(f"Overall hscore harmonizable pairs: {n_harmonizable}/3; {verdict}.")


def run_audit_only() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    inventory = build_inventory()
    schema_audit = build_schema_audit()

    inventory.to_csv(INVENTORY_CSV, index=False)
    schema_audit.to_csv(SCHEMA_AUDIT_CSV, index=False)

    print(f"Wrote {INVENTORY_CSV}")
    print(f"Wrote {SCHEMA_AUDIT_CSV}")
    all_invariants_passed = print_invariants(inventory)
    print_schema_summary(schema_audit)
    if not all_invariants_passed:
        raise AssertionError("One or more Wave 4 Task 1 inventory invariants failed.")


def safe_mcc(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    y_true = np.asarray(y_true, dtype=int)
    y_pred = np.asarray(y_pred, dtype=int)
    if y_pred.sum() == 0 or y_pred.sum() == len(y_pred):
        return 0.0
    if y_true.sum() == 0 or y_true.sum() == len(y_true):
        return 0.0
    return float(matthews_corrcoef(y_true, y_pred))


def window_mcc(y_true: np.ndarray, y_pred: np.ndarray, radius: int = WINDOW_RADIUS) -> float:
    y_true = np.asarray(y_true, dtype=int)
    y_pred = np.asarray(y_pred, dtype=int)
    n = len(y_true)
    if y_pred.sum() == 0 or y_pred.sum() == n or y_true.sum() == 0 or y_true.sum() == n:
        return 0.0

    def dilate(v: np.ndarray) -> np.ndarray:
        idx = np.where(v == 1)[0]
        out = np.zeros(n, dtype=int)
        for i in idx:
            lo = max(0, i - radius)
            hi = min(n, i + radius + 1)
            out[lo:hi] = 1
        return out

    pred_window = dilate(y_pred)
    true_window = dilate(y_true)
    tp = int(((y_pred == 1) & (true_window == 1)).sum())
    fp = int(((y_pred == 1) & (true_window == 0)).sum())
    fn = int(((y_true == 1) & (pred_window == 0)).sum())
    tn = int(((y_pred == 0) & (y_true == 0)).sum())
    denom = math.sqrt(float(tp + fp) * float(tp + fn) * float(tn + fp) * float(tn + fn))
    if denom < 1e-12:
        return 0.0
    return float((tp * tn - fp * fn) / denom)


def load_labeled_data() -> dict[str, dict]:
    data = {}
    for pathogen in ALL_PATHOGENS:
        path = FEATURE_DIR / f"feature_matrix_{pathogen}.csv"
        df = pd.read_csv(path)
        require_columns(path, df, ["position", "freq", "entropy", "homoplasy", "plddt", "layer_a"])
        y = df["layer_a"].values.astype(int)
        if y.sum() == 0 or y.sum() == len(y):
            raise ValueError(f"{pathogen} has degenerate layer_a labels")
        data[pathogen] = {"df": df, "y": y, "n": len(df), "base_rate": float(y.mean())}
    return data


def pearson_sign_for_pathogen(df: pd.DataFrame, y: np.ndarray, feature: str) -> float:
    x = np.nan_to_num(df[feature].values.astype(float), nan=0.0, posinf=0.0, neginf=0.0)
    y_float = y.astype(float)
    if x.std() < 1e-12 or y_float.std() < 1e-12:
        return 1.0
    r = np.corrcoef(x, y_float)[0, 1]
    return -1.0 if np.isfinite(r) and r < 0 else 1.0


def fit_median_signs(training_data: dict[str, dict], features: tuple[str, ...]) -> dict[str, float]:
    signs = {}
    for feature in features:
        per_pathogen_signs = [
            pearson_sign_for_pathogen(d["df"], d["y"], feature)
            for d in training_data.values()
        ]
        median = float(np.median(per_pathogen_signs))
        signs[feature] = -1.0 if median < 0 else 1.0
    return signs


def fit_median_signs_for_sample(
    labeled_data: dict[str, dict],
    sampled_pathogens: list[str],
    features: tuple[str, ...],
) -> dict[str, float]:
    signs = {}
    for feature in features:
        sampled_signs = [
            pearson_sign_for_pathogen(labeled_data[pathogen]["df"], labeled_data[pathogen]["y"], feature)
            for pathogen in sampled_pathogens
        ]
        median = float(np.median(sampled_signs))
        signs[feature] = -1.0 if median < 0 else 1.0
    return signs


def signed_zscore_average(df: pd.DataFrame, features: tuple[str, ...], signs: dict[str, float]) -> np.ndarray:
    if not features:
        return np.zeros(len(df))
    score_parts = []
    for feature in features:
        col = np.nan_to_num(df[feature].values.astype(float), nan=0.0, posinf=0.0, neginf=0.0)
        std = col.std()
        if std <= 1e-10:
            score_parts.append(np.zeros(len(df)))
        else:
            z = (col - col.mean()) / std
            score_parts.append(z * signs.get(feature, 1.0))
    return np.vstack(score_parts).mean(axis=0)


def topk_pred(scores: np.ndarray, k: int) -> np.ndarray:
    k = max(1, min(int(k), len(scores)))
    pred = np.zeros(len(scores), dtype=int)
    order = np.lexsort((np.arange(len(scores)), -scores))
    pred[order[:k]] = 1
    return pred


def top_fraction_pred(scores: np.ndarray, fraction: float = TOP10_FRAC) -> np.ndarray:
    return topk_pred(scores, int(np.ceil(len(scores) * fraction)))


def topk_tp(scores: np.ndarray, y: np.ndarray, k: int) -> int:
    k = min(k, len(scores))
    order = np.lexsort((np.arange(len(scores)), -scores))
    return int(y[order[:k]].sum())


def precision_at_k(scores: np.ndarray, y: np.ndarray, k: int = PRECISION_K) -> float:
    k = min(k, len(scores))
    if k <= 0:
        return 0.0
    return float(topk_tp(scores, y, k) / k)


def decile_stats(scores: np.ndarray, y: np.ndarray) -> tuple[float, float]:
    n = len(scores)
    order = np.lexsort((np.arange(n), scores))
    decile = np.zeros(n, dtype=int)
    for rank, idx in enumerate(order):
        decile[idx] = min(N_DECILES - 1, int(rank * N_DECILES / n))
    means = np.array([
        y[decile == d].mean() if (decile == d).any() else np.nan
        for d in range(N_DECILES)
    ])
    top_bottom_delta = float(means[-1] - means[0]) if np.isfinite(means[-1]) and np.isfinite(means[0]) else np.nan
    valid = np.isfinite(means)
    if valid.sum() < 3:
        rho = np.nan
    else:
        rho = float(stats.spearmanr(np.where(valid)[0], means[valid]).statistic)
    return top_bottom_delta, rho


def top_bottom_delta_with_ci(scores: np.ndarray, y: np.ndarray, rng: np.random.Generator) -> tuple[float, float, float]:
    pred_top = top_fraction_pred(scores, TOP10_FRAC).astype(bool)
    n_top = int(pred_top.sum())
    order_low = np.lexsort((np.arange(len(scores)), scores))
    bot_idx = order_low[:n_top]
    top_idx = np.where(pred_top)[0]
    if len(top_idx) == 0 or len(bot_idx) == 0:
        return np.nan, np.nan, np.nan
    obs = float(y[top_idx].mean() - y[bot_idx].mean())
    boot = []
    for _ in range(D1_BOOT):
        t_samp = rng.choice(top_idx, size=len(top_idx), replace=True)
        b_samp = rng.choice(bot_idx, size=len(bot_idx), replace=True)
        boot.append(y[t_samp].mean() - y[b_samp].mean())
    lo, hi = np.percentile(boot, [2.5, 97.5])
    return obs, float(lo), float(hi)


def d1_recheck_for_fold(
    held: str,
    training_data: dict[str, dict],
    features: tuple[str, ...],
    signs: dict[str, float],
    rng: np.random.Generator,
) -> tuple[dict, list[dict]]:
    detail_rows = []
    n_pass = 0
    n_total = 0
    for pathogen, d in training_data.items():
        scores = signed_zscore_average(d["df"], features, signs)
        obs, lo, hi = top_bottom_delta_with_ci(scores, d["y"], rng)
        passed = bool(np.isfinite(obs) and np.isfinite(lo) and obs > D1_POINT_MIN and lo > D1_LOWER_CI_MIN)
        n_total += int(np.isfinite(obs))
        n_pass += int(passed)
        detail_rows.append(
            {
                "heldout_pathogen": held,
                "training_pathogen": pathogen,
                "method": "2-core",
                "d1_top_bottom_delta": obs,
                "d1_ci_lo": lo,
                "d1_ci_hi": hi,
                "d1_training_pathogen_pass": int(passed),
            }
        )
    aggregate = {
        "heldout_pathogen": held,
        "method": "2-core",
        "d1_n_pass": n_pass,
        "d1_n_total": n_total,
        "callability_d1_pass": bool(n_pass >= D1_QUORUM),
        "d1_quorum": D1_QUORUM,
        "d1_lower_ci_min": D1_LOWER_CI_MIN,
        "d1_point_min": D1_POINT_MIN,
        "training_pathogens_d1_passed": ";".join(
            row["training_pathogen"] for row in detail_rows if row["d1_training_pathogen_pass"]
        ),
        "training_pathogens_d1_failed": ";".join(
            row["training_pathogen"] for row in detail_rows if not row["d1_training_pathogen_pass"]
        ),
    }
    return aggregate, detail_rows


def evaluate_scores(scores: np.ndarray, y: np.ndarray, base_rate: float) -> dict[str, float]:
    pred10 = top_fraction_pred(scores, TOP10_FRAC)
    precision10 = float(y[pred10 == 1].mean()) if pred10.sum() else 0.0
    top_bottom_delta, decile_rho = decile_stats(scores, y)
    return {
        "mcc_top10": safe_mcc(y, pred10),
        "mcc_window10": window_mcc(y, pred10, WINDOW_RADIUS),
        "precision_at_20": precision_at_k(scores, y, PRECISION_K),
        "tp_at_20": topk_tp(scores, y, 20),
        "tp_at_50": topk_tp(scores, y, 50),
        "tp_at_80": topk_tp(scores, y, 80),
        "enrichment_top10": precision10 / base_rate if base_rate > 1e-12 else np.nan,
        "top_bottom_decile_delta": top_bottom_delta,
        "spearman_decile_rho": decile_rho,
    }


def fold_hypergeom_p(scores: np.ndarray, y: np.ndarray) -> float:
    pred = top_fraction_pred(scores, TOP10_FRAC)
    tp = int(y[pred == 1].sum())
    return float(stats.hypergeom.sf(tp - 1, len(y), int(y.sum()), int(pred.sum())))


def run_labeled_only(smoke: bool = False) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(RANDOM_SEED)
    data = load_labeled_data()
    pathogens = ALL_PATHOGENS[:2] if smoke else ALL_PATHOGENS
    rows = []
    d1_rows = []

    print("Wave 4 Task 2: labeled-only shared-feature LOPO")
    print(f"random_seed={RANDOM_SEED}")
    print("2-core fallback active: features=freq,entropy; hscore dropped")
    if smoke:
        print(f"SMOKE mode: held-out folds={pathogens}")

    for held in pathogens:
        training = {p: d for p, d in data.items() if p != held}
        held_d = data[held]
        two_core_signs = fit_median_signs(training, TWO_CORE_FEATURES)
        four_core_signs = fit_median_signs(training, HISTORICAL_4CORE_FEATURES)
        two_scores = signed_zscore_average(held_d["df"], TWO_CORE_FEATURES, two_core_signs)
        four_scores = signed_zscore_average(held_d["df"], HISTORICAL_4CORE_FEATURES, four_core_signs)
        metrics = evaluate_scores(two_scores, held_d["y"], held_d["base_rate"])
        four_metrics = evaluate_scores(four_scores, held_d["y"], held_d["base_rate"])
        d1_agg, d1_detail = d1_recheck_for_fold(held, training, TWO_CORE_FEATURES, two_core_signs, rng)
        d1_rows.append(d1_agg)
        notes = f"D1 {d1_agg['d1_n_pass']}/{d1_agg['d1_n_total']} training pathogens pass; quorum={D1_QUORUM}/11"
        row = {
            "pathogen": held,
            "n_positions": int(held_d["n"]),
            "n_layer_a_pos": int(held_d["y"].sum()),
            "layer_a_prev": held_d["base_rate"],
            "sign_freq": int(two_core_signs["freq"]),
            "sign_entropy": int(two_core_signs["entropy"]),
            **metrics,
            "callability_d1_pass": int(d1_agg["callability_d1_pass"]),
            "callability_like_notes": notes,
            "historical_4core_mcc_top10": four_metrics["mcc_top10"],
            "delta_2core_minus_4core": metrics["mcc_top10"] - four_metrics["mcc_top10"],
            "historical_4core_source": "recomputed in Wave 4",
            "fold_hypergeom_p_top10": fold_hypergeom_p(two_scores, held_d["y"]),
        }
        rows.append(row)
        print(
            f"{held}: 2-core MCC={metrics['mcc_top10']:.4f}, "
            f"4-core MCC={four_metrics['mcc_top10']:.4f}, "
            f"delta={row['delta_2core_minus_4core']:.4f}, D1={d1_agg['d1_n_pass']}/{d1_agg['d1_n_total']}"
        )

    per_fold = pd.DataFrame(rows)
    callability = pd.DataFrame(d1_rows)
    if not smoke:
        wilcoxon = stats.wilcoxon(
            per_fold["mcc_top10"],
            per_fold["historical_4core_mcc_top10"],
            alternative="greater",
            zero_method="wilcox",
        )
        wilcoxon_p = float(wilcoxon.pvalue)
    else:
        wilcoxon_p = np.nan

    summary = pd.DataFrame(
        [
            {
                "n_folds": int(per_fold.shape[0]),
                "mean_mcc_top10": float(per_fold["mcc_top10"].mean()),
                "std_mcc_top10": float(per_fold["mcc_top10"].std(ddof=1)) if per_fold.shape[0] > 1 else 0.0,
                "min_mcc_top10": float(per_fold["mcc_top10"].min()),
                "max_mcc_top10": float(per_fold["mcc_top10"].max()),
                "n_positive_mcc": int((per_fold["mcc_top10"] > 0).sum()),
                "mean_precision_at_20": float(per_fold["precision_at_20"].mean()),
                "fold_significance_count_hypergeom_p_lt_0_05": int((per_fold["fold_hypergeom_p_top10"] < 0.05).sum()),
                "paired_wilcoxon_2core_vs_4core_greater_p": wilcoxon_p,
                "d1_callability_recheck_pass_count": int(per_fold["callability_d1_pass"].sum()),
                "historical_4core_source": "recomputed in Wave 4",
                "random_seed": RANDOM_SEED,
            }
        ]
    )

    if smoke:
        print("Smoke run complete; output files not overwritten.")
    else:
        per_fold_out = per_fold[
            [
                "pathogen",
                "n_positions",
                "n_layer_a_pos",
                "layer_a_prev",
                "sign_freq",
                "sign_entropy",
                "mcc_top10",
                "mcc_window10",
                "precision_at_20",
                "tp_at_20",
                "tp_at_50",
                "tp_at_80",
                "enrichment_top10",
                "top_bottom_decile_delta",
                "spearman_decile_rho",
                "callability_d1_pass",
                "callability_like_notes",
                "historical_4core_mcc_top10",
                "delta_2core_minus_4core",
                "historical_4core_source",
            ]
        ]
        per_fold_out.to_csv(LABELED_LOPO_PER_FOLD_CSV, index=False)
        summary.to_csv(LABELED_LOPO_SUMMARY_CSV, index=False)
        callability.to_csv(LABELED_CALLABILITY_RECHECK_CSV, index=False)
        print(f"Wrote {LABELED_LOPO_PER_FOLD_CSV}")
        print(f"Wrote {LABELED_LOPO_SUMMARY_CSV}")
        print(f"Wrote {LABELED_CALLABILITY_RECHECK_CSV}")

    s = summary.iloc[0]
    print(
        "2-core MCC across folds: "
        f"mean={s.mean_mcc_top10:.6f}, std={s.std_mcc_top10:.6f}, "
        f"min={s.min_mcc_top10:.6f}, max={s.max_mcc_top10:.6f}"
    )
    print(f"Positive-MCC folds: {int(s.n_positive_mcc)}/{int(s.n_folds)}")
    print(f"Paired Wilcoxon one-sided greater p (2-core vs 4-core): {s.paired_wilcoxon_2core_vs_4core_greater_p}")
    print(f"D1 callability recheck pass count: {int(s.d1_callability_recheck_pass_count)}/{int(s.n_folds)}")
    if not smoke:
        print("TASK 2 DONE")


def load_expanded_targets(inventory: pd.DataFrame) -> dict[str, dict]:
    targets = {}
    included = inventory[inventory["unique_target_inclusion"]].copy()
    for row in included.itertuples(index=False):
        if row.source_type == "feature_matrix":
            path = FEATURE_DIR / f"feature_matrix_{row.slug}.csv"
            df = pd.read_csv(path)
            require_columns(path, df, ["position", "freq", "entropy", "layer_a"])
            work = df[["position", "freq", "entropy", "layer_a"]].copy()
            work = work.rename(columns={"layer_a": "ground_truth"})
            is_labeled = True
        elif row.source_type == "cross_pathogen":
            path = CROSS_DIR / f"{row.slug}_position_scores.csv"
            df = pd.read_csv(path)
            require_columns(path, df, ["position", "frequency", "entropy", "ground_truth"])
            if row.slug in OVERLAP_SLUGS:
                raise ValueError(f"Audit-only overlap target leaked into expanded panel: {row.slug}")
            work = df[["position", "frequency", "entropy"]].copy()
            work = work.rename(columns={"frequency": "freq"})
            work["ground_truth"] = -1
            is_labeled = False
        else:
            raise ValueError(f"Unknown source_type for {row.slug}: {row.source_type}")

        work["position"] = work["position"].astype(int)
        work = work.sort_values("position", kind="mergesort").reset_index(drop=True)
        targets[row.slug] = {
            "slug": row.slug,
            "pathogen_label": row.pathogen_label,
            "source_type": row.source_type,
            "is_labeled": bool(is_labeled),
            "df": work,
            "n_positions_inventory": int(row.n_positions),
        }

    if len(targets) != 28:
        raise AssertionError(f"Expanded panel expected 28 unique targets, found {len(targets)}")
    n_unlabeled = sum(1 for target in targets.values() if not target["is_labeled"])
    if n_unlabeled != 16:
        raise AssertionError(f"Expanded panel expected 16 unlabeled cross-pathogen targets, found {n_unlabeled}")
    return targets


def bootstrap_sign_table(
    labeled_data: dict[str, dict],
    n_bootstrap: int = EXPANDED_BOOT,
    seed: int = RANDOM_SEED,
) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    pathogens = list(labeled_data.keys())
    rows = []
    for bootstrap_id in range(n_bootstrap):
        sampled = rng.choice(pathogens, size=len(pathogens), replace=True).tolist()
        signs = fit_median_signs_for_sample(labeled_data, sampled, TWO_CORE_FEATURES)
        rows.append(
            {
                "bootstrap_id": bootstrap_id,
                "sign_freq": int(signs["freq"]),
                "sign_entropy": int(signs["entropy"]),
            }
        )
    return pd.DataFrame(rows)


def ordered_top_set_and_ranks(df: pd.DataFrame, scores: np.ndarray) -> tuple[set[int], np.ndarray, bool]:
    positions = df["position"].to_numpy(dtype=int)
    constant = bool(np.nanstd(scores) <= 1e-12)
    order = np.lexsort((positions, -scores))
    n_top = max(1, int(np.ceil(len(scores) * TOP10_FRAC)))
    top_set = set(positions[order[:n_top]].tolist())
    ranks = np.empty(len(scores), dtype=float)
    ranks[order] = np.arange(1, len(scores) + 1, dtype=float)
    return top_set, ranks, constant


def weighted_percentile(values: list[float], weights: list[int], percentile: float) -> float:
    if not values:
        return np.nan
    order = np.argsort(values)
    sorted_values = np.asarray(values, dtype=float)[order]
    sorted_weights = np.asarray(weights, dtype=float)[order]
    cutoff = (percentile / 100.0) * sorted_weights.sum()
    cumulative = np.cumsum(sorted_weights)
    idx = int(np.searchsorted(cumulative, cutoff, side="left"))
    idx = min(idx, len(sorted_values) - 1)
    return float(sorted_values[idx])


def weighted_median(values: list[float], weights: list[int]) -> float:
    return weighted_percentile(values, weights, 50.0)


def jaccard(a: set[int], b: set[int]) -> float:
    union = a | b
    return float(len(a & b) / len(union)) if union else np.nan


def spearman_from_ranks(a: np.ndarray, b: np.ndarray) -> float:
    if np.nanstd(a) <= 1e-12 or np.nanstd(b) <= 1e-12:
        return np.nan
    return float(stats.spearmanr(a, b).statistic)


def expanded_stability_for_target(
    target: dict,
    sign_counts: pd.DataFrame,
    full_sample_signs: dict[str, float],
) -> tuple[dict, dict]:
    df = target["df"]
    variants = []
    for row in sign_counts.itertuples(index=False):
        signs = {"freq": float(row.sign_freq), "entropy": float(row.sign_entropy)}
        scores = signed_zscore_average(df, TWO_CORE_FEATURES, signs)
        top_set, ranks, constant = ordered_top_set_and_ranks(df, scores)
        variants.append(
            {
                "sign_freq": int(row.sign_freq),
                "sign_entropy": int(row.sign_entropy),
                "n_bootstraps": int(row.n_bootstraps),
                "scores": scores,
                "top_set": top_set,
                "ranks": ranks,
                "constant": constant,
            }
        )

    jaccard_values = []
    jaccard_weights = []
    spearman_values = []
    spearman_weights = []
    n_constant = 0
    for i, left in enumerate(variants):
        if left["constant"]:
            n_constant += left["n_bootstraps"]
        n_same_pairs = left["n_bootstraps"] * (left["n_bootstraps"] - 1) // 2
        if n_same_pairs:
            jaccard_values.append(1.0)
            jaccard_weights.append(n_same_pairs)
            if not left["constant"]:
                spearman_values.append(1.0)
                spearman_weights.append(n_same_pairs)
        for right in variants[i + 1 :]:
            n_cross_pairs = left["n_bootstraps"] * right["n_bootstraps"]
            jaccard_values.append(jaccard(left["top_set"], right["top_set"]))
            jaccard_weights.append(n_cross_pairs)
            rho = spearman_from_ranks(left["ranks"], right["ranks"])
            if np.isfinite(rho):
                spearman_values.append(rho)
                spearman_weights.append(n_cross_pairs)

    median_jaccard = weighted_median(jaccard_values, jaccard_weights)
    p10_jaccard = weighted_percentile(jaccard_values, jaccard_weights, 10.0)
    spearman_median = weighted_median(spearman_values, spearman_weights)
    no_result_constant_rank = bool(n_constant > (EXPANDED_BOOT / 2))
    target_pass_stability = bool(median_jaccard >= 0.60 and p10_jaccard >= 0.40)

    full_scores = signed_zscore_average(df, TWO_CORE_FEATURES, full_sample_signs)
    n_top = max(1, int(np.ceil(len(df) * TOP10_FRAC)))
    target_scores_row = {
        "target": target["slug"],
        "pathogen_label": target["pathogen_label"],
        "source_type": target["source_type"],
        "is_labeled": int(target["is_labeled"]),
        "n_positions": int(len(df)),
        "top10pct_count": int(n_top),
        "score_mean_full_sample_sign": float(np.mean(full_scores)),
        "score_std_full_sample_sign": float(np.std(full_scores)),
        "score_min_full_sample_sign": float(np.min(full_scores)),
        "score_max_full_sample_sign": float(np.max(full_scores)),
        "score_constant_full_sample_sign": int(np.std(full_scores) <= 1e-12),
        "ground_truth_available": int(target["is_labeled"]),
    }
    stability_row = {
        "target": target["slug"],
        "pathogen_label": target["pathogen_label"],
        "source_type": target["source_type"],
        "is_labeled": int(target["is_labeled"]),
        "n_positions": int(len(df)),
        "median_pairwise_jaccard": median_jaccard,
        "p10_pairwise_jaccard": p10_jaccard,
        "spearman_rank_corr_median": spearman_median,
        "n_constant_score_drop": int(n_constant),
        "no_result_constant_rank": int(no_result_constant_rank),
        "target_pass_stability": int(target_pass_stability),
    }
    return target_scores_row, stability_row


def feature_spread_rows(targets: dict[str, dict]) -> tuple[list[dict], dict[str, bool]]:
    base_rows = []
    for target in targets.values():
        df = target["df"]
        freq = df["freq"].astype(float)
        entropy = df["entropy"].astype(float)
        base_rows.append(
            {
                "target": target["slug"],
                "pathogen_label": target["pathogen_label"],
                "source_type": target["source_type"],
                "is_labeled": int(target["is_labeled"]),
                "n_positions": int(len(df)),
                "mean_freq": float(freq.mean()),
                "std_freq": float(freq.std(ddof=1)) if len(freq) > 1 else 0.0,
                "mean_entropy": float(entropy.mean()),
                "std_entropy": float(entropy.std(ddof=1)) if len(entropy) > 1 else 0.0,
                "variable_pos_frac": float(((freq > 0) | (entropy > 0)).mean()),
                "top10pct_count": int(max(1, np.ceil(len(df) * TOP10_FRAC))),
            }
        )

    labeled_rows = [row for row in base_rows if row["is_labeled"]]
    min_freq = min(row["mean_freq"] for row in labeled_rows)
    max_freq = max(row["mean_freq"] for row in labeled_rows)
    min_entropy = min(row["mean_entropy"] for row in labeled_rows)
    max_entropy = max(row["mean_entropy"] for row in labeled_rows)
    inside_by_target = {}
    for row in base_rows:
        if row["is_labeled"]:
            row["inside_labeled_envelope"] = ""
            inside_by_target[row["target"]] = True
        else:
            inside = bool(
                min_freq <= row["mean_freq"] <= max_freq
                and min_entropy <= row["mean_entropy"] <= max_entropy
            )
            row["inside_labeled_envelope"] = int(inside)
            inside_by_target[row["target"]] = inside
    return base_rows, inside_by_target


def run_expanded() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    if INVENTORY_CSV.exists():
        inventory = pd.read_csv(INVENTORY_CSV)
    else:
        inventory = build_inventory()
        inventory.to_csv(INVENTORY_CSV, index=False)

    if not SCHEMA_AUDIT_CSV.exists():
        build_schema_audit().to_csv(SCHEMA_AUDIT_CSV, index=False)
    if SCHEMA_AUDIT_CSV.exists() and not OVERLAP_SCHEMA_DRIFT_CSV.exists():
        pd.read_csv(SCHEMA_AUDIT_CSV).to_csv(OVERLAP_SCHEMA_DRIFT_CSV, index=False)

    labeled_data = load_labeled_data()
    targets = load_expanded_targets(inventory)
    full_sample_signs = fit_median_signs(labeled_data, TWO_CORE_FEATURES)
    sign_table = bootstrap_sign_table(labeled_data, EXPANDED_BOOT, RANDOM_SEED)
    sign_counts = (
        sign_table.groupby(["sign_freq", "sign_entropy"], as_index=False)
        .size()
        .rename(columns={"size": "n_bootstraps"})
    )

    spread_rows, inside_by_target = feature_spread_rows(targets)
    spread_by_target = {row["target"]: row for row in spread_rows}
    target_score_rows = []
    stability_rows = []
    for target in targets.values():
        target_row, stability_row = expanded_stability_for_target(target, sign_counts, full_sample_signs)
        target_row.update(spread_by_target[target["slug"]])
        target_score_rows.append(target_row)
        stability_rows.append(stability_row)

    target_scores = pd.DataFrame(target_score_rows).sort_values("target", kind="mergesort")
    stability = pd.DataFrame(stability_rows).sort_values("target", kind="mergesort")

    stable_targets = set(stability.loc[stability["target_pass_stability"] == 1, "target"])
    unlabeled_targets = {target["slug"] for target in targets.values() if not target["is_labeled"]}
    inside_unlabeled = {target for target in unlabeled_targets if inside_by_target[target]}
    stable_inside_unlabeled = stable_targets & inside_unlabeled
    stable_or_inside_unlabeled = (stable_targets & unlabeled_targets) | inside_unlabeled
    n_usable_targets = int(len(stable_targets))
    n_inside_envelope = int(len(inside_unlabeled))
    same_targets_quorum = int(len(stable_inside_unlabeled))
    union_quorum = int(len(stable_or_inside_unlabeled))
    quorum_pass = bool(n_usable_targets >= 20 and n_usable_targets >= 7 and n_inside_envelope >= 7)

    sign_match = {}
    for feature in TWO_CORE_FEATURES:
        full_sign = int(full_sample_signs[feature])
        sign_match[feature] = float((sign_table[f"sign_{feature}"] == full_sign).mean() * 100.0)

    quorum = pd.DataFrame(
        [
            {
                "n_total_targets": 28,
                "n_labeled_targets": 12,
                "n_unlabeled_targets": 16,
                "n_usable_targets": n_usable_targets,
                "n_inside_envelope": n_inside_envelope,
                "same_targets_quorum": same_targets_quorum,
                "union_quorum": union_quorum,
                "quorum_pass": int(quorum_pass),
                "random_seed": RANDOM_SEED,
                "n_bootstrap": EXPANDED_BOOT,
                "full_sample_sign_freq": int(full_sample_signs["freq"]),
                "full_sample_sign_entropy": int(full_sample_signs["entropy"]),
                "n_bootstrap_sign_freq_pos": int((sign_table["sign_freq"] == 1).sum()),
                "n_bootstrap_sign_freq_neg": int((sign_table["sign_freq"] == -1).sum()),
                "n_bootstrap_sign_entropy_pos": int((sign_table["sign_entropy"] == 1).sum()),
                "n_bootstrap_sign_entropy_neg": int((sign_table["sign_entropy"] == -1).sum()),
                "pct_bootstrap_sign_freq_matches_full": sign_match["freq"],
                "pct_bootstrap_sign_entropy_matches_full": sign_match["entropy"],
                "features": "freq,entropy",
                "notes": "2-core fallback active; no Layer A claim or evaluation metrics computed for unlabeled targets",
            }
        ]
    )

    target_scores.to_csv(EXPANDED_TARGET_SCORES_CSV, index=False)
    stability.to_csv(EXPANDED_STABILITY_PER_TARGET_CSV, index=False)
    quorum.to_csv(EXPANDED_QUORUM_REACHABILITY_CSV, index=False)

    print("Wave 4 Task 3: expanded 28-target stability diagnostics")
    print(f"random_seed={RANDOM_SEED}; n_bootstrap={EXPANDED_BOOT}")
    print("2-core fallback active: features=freq,entropy")
    print(f"Wrote {EXPANDED_TARGET_SCORES_CSV}")
    print(f"Wrote {EXPANDED_STABILITY_PER_TARGET_CSV}")
    print(f"Wrote {EXPANDED_QUORUM_REACHABILITY_CSV}")
    if OVERLAP_SCHEMA_DRIFT_CSV.exists():
        print(f"Wrote {OVERLAP_SCHEMA_DRIFT_CSV}")
    print(f"28-target stability summary: {n_usable_targets}/28 target_pass_stability=True")
    print(f"16-unlabeled envelope count: {n_inside_envelope}/16")
    print(
        "Quorum diagnostics: "
        f"n_usable_targets={n_usable_targets}, "
        f"same_targets_quorum={same_targets_quorum}, "
        f"union_quorum={union_quorum}, "
        f"quorum_pass={quorum_pass}"
    )
    print(
        "Sign-fitting stability: "
        f"freq={sign_match['freq']:.1f}% match full-sample sign, "
        f"entropy={sign_match['entropy']:.1f}% match full-sample sign"
    )
    print("TASK 3 DONE")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Wave 4 Tier-2 feature/LOPO scaffold")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--audit-only", action="store_true", help="write Task 1 inventory/schema audit CSVs")
    mode.add_argument("--labeled-only", action="store_true", help="run Task 2 labeled 12-fold LOPO")
    mode.add_argument("--expanded", action="store_true", help="reserved for Task 3")
    mode.add_argument("--full", action="store_true", help="reserved for Tasks 2-3")
    parser.add_argument("--smoke", action="store_true", help="run a two-heldout-pathogen smoke subset")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.audit_only:
        run_audit_only()
        return
    if args.labeled_only:
        run_labeled_only(smoke=args.smoke)
        return
    if args.expanded:
        run_expanded()
        return
    raise NotImplementedError("--full is reserved for a later Wave 4 task.")


if __name__ == "__main__":
    main()
