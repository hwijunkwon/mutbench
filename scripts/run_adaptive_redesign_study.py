#!/usr/bin/env python3
"""Adaptive PAHD redesign study.

This script compares several redesign directions for pathogen-adaptive method
selection under leave-one-pathogen-out evaluation.

The key distinction is intentional:
  * exact-combo selectors are deployable single-choice policies;
  * coarse selectors and shortlist@K are diagnostic ceilings that show where
    adaptive signal exists before committing to a detector calibration policy.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler


PROJECT_ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = PROJECT_ROOT / "results" / "mutbench"
INPUT = RESULTS_DIR / "multilayer_9pathogen_results.csv"


def load_results() -> pd.DataFrame:
    df = pd.read_csv(INPUT)
    required = {
        "pathogen", "score", "detector", "family", "n_sequences", "n_unique",
        "seq_length", "mcc_adaptive", "n_detected",
    }
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    return df


def build_no_gt_profiles(df: pd.DataFrame) -> pd.DataFrame:
    """Build target-usable profiles without Layer A/GT size leakage."""
    scores = sorted(df["score"].unique())
    families = sorted(df["family"].unique())
    profiles: dict[str, dict[str, float]] = {}

    for pathogen, group in df.groupby("pathogen"):
        first = group.iloc[0]
        seq_len = float(first["seq_length"])
        nd_ratio = group["n_detected"].astype(float) / max(seq_len, 1.0)

        row: dict[str, float] = {
            "log_seq_length": float(np.log1p(seq_len)),
            "log_n_sequences": float(np.log1p(first["n_sequences"])),
            "log_n_unique": float(np.log1p(first["n_unique"])),
            "diversity_ratio": float(first["n_unique"] / max(first["n_sequences"], 1)),
            "det_mean": float(nd_ratio.mean()),
            "det_std": float(nd_ratio.std()),
            "det_q10": float(nd_ratio.quantile(0.10)),
            "det_q50": float(nd_ratio.quantile(0.50)),
            "det_q90": float(nd_ratio.quantile(0.90)),
            "det_sparse_frac": float((nd_ratio < 0.05).mean()),
            "det_dense_frac": float((nd_ratio > 0.30).mean()),
        }

        for family in families:
            fam_ratio = (
                group.loc[group["family"] == family, "n_detected"].astype(float)
                / max(seq_len, 1.0)
            )
            row[f"family_{family}_det_mean"] = float(fam_ratio.mean()) if len(fam_ratio) else 0.0
            row[f"family_{family}_sparse_frac"] = (
                float((fam_ratio < 0.05).mean()) if len(fam_ratio) else 0.0
            )

        for score in scores:
            score_ratio = (
                group.loc[group["score"] == score, "n_detected"].astype(float)
                / max(seq_len, 1.0)
            )
            row[f"score_{score}_det_mean"] = float(score_ratio.mean()) if len(score_ratio) else 0.0

        profiles[pathogen] = row

    return pd.DataFrame(profiles).T.fillna(0.0)


def profile_similarity(profiles: pd.DataFrame) -> pd.DataFrame:
    x = StandardScaler().fit_transform(profiles.values)
    sim = cosine_similarity(x)
    return pd.DataFrame(sim, index=profiles.index, columns=profiles.index)


def _target_combo_set(df: pd.DataFrame, target: str) -> set[tuple[str, str]]:
    target_df = df[df["pathogen"] == target]
    return set(map(tuple, target_df[["score", "detector"]].drop_duplicates().values))


def _combo_mcc(df: pd.DataFrame, pathogen: str, score: str, detector: str) -> float | None:
    rows = df[(df["pathogen"] == pathogen) & (df["score"] == score) & (df["detector"] == detector)]
    if len(rows) == 0:
        return None
    return float(rows.iloc[0]["mcc_adaptive"])


def _combo_ranking(
    df: pd.DataFrame,
    sim: pd.DataFrame,
    target: str,
    strategy: str,
) -> list[tuple[tuple[str, str], float]]:
    pathogens = sorted(df["pathogen"].unique())
    train_pathogens = [p for p in pathogens if p != target]
    target_combos = _target_combo_set(df, target)

    train = df[df["pathogen"].isin(train_pathogens)].copy()
    train = train[train[["score", "detector"]].apply(tuple, axis=1).isin(target_combos)]

    weights = {p: max(0.01, float(sim.loc[target, p])) for p in train_pathogens}
    ranked: list[tuple[tuple[str, str], float]] = []

    for combo, group in train.groupby(["score", "detector"]):
        if strategy == "global_mean":
            value = float(group["mcc_adaptive"].mean())
        elif strategy == "robust_mean":
            value = float(group["mcc_adaptive"].mean() - 0.5 * group["mcc_adaptive"].std(ddof=0))
        elif strategy == "sim_weighted":
            num = 0.0
            den = 0.0
            for pathogen, p_group in group.groupby("pathogen"):
                w = weights[pathogen]
                num += w * float(p_group.iloc[0]["mcc_adaptive"])
                den += w
            value = num / den if den else -np.inf
        elif strategy == "sim_rank":
            rank_num = 0.0
            rank_den = 0.0
            for pathogen in train_pathogens:
                p_df = train[train["pathogen"] == pathogen].copy()
                p_rows = p_df[(p_df["score"] == combo[0]) & (p_df["detector"] == combo[1])]
                if len(p_rows) == 0:
                    continue
                ranks = p_df["mcc_adaptive"].rank(ascending=False, method="average")
                w = weights[pathogen]
                rank_num += w * float(ranks.loc[p_rows.index[0]])
                rank_den += w
            value = -(rank_num / rank_den) if rank_den else -np.inf
        else:
            raise ValueError(f"Unknown strategy: {strategy}")

        ranked.append((combo, value))

    return sorted(ranked, key=lambda item: item[1], reverse=True)


def evaluate_exact_selectors(df: pd.DataFrame, sim: pd.DataFrame) -> pd.DataFrame:
    rows = []
    strategies = ["global_mean", "robust_mean", "sim_weighted", "sim_rank"]

    for target in sorted(df["pathogen"].unique()):
        target_df = df[df["pathogen"] == target]
        oracle = float(target_df["mcc_adaptive"].max())
        oracle_idx = target_df["mcc_adaptive"].idxmax()
        oracle_row = target_df.loc[oracle_idx]

        for strategy in strategies:
            ranking = _combo_ranking(df, sim, target, strategy)
            score, detector = ranking[0][0]
            test_mcc = _combo_mcc(df, target, score, detector)
            rows.append({
                "pathogen": target,
                "strategy": strategy,
                "selected_score": score,
                "selected_detector": detector,
                "test_mcc": test_mcc,
                "oracle_mcc": oracle,
                "oracle_score": oracle_row["score"],
                "oracle_detector": oracle_row["detector"],
                "pct_oracle": 100.0 * test_mcc / oracle if oracle > 0 and test_mcc is not None else 0.0,
            })

        train_pathogens = [p for p in sorted(df["pathogen"].unique()) if p != target]
        nn = sim.loc[target, train_pathogens].idxmax()
        nn_df = df[df["pathogen"] == nn]
        nn_df = nn_df[nn_df[["score", "detector"]].apply(tuple, axis=1).isin(_target_combo_set(df, target))]
        nn_best = nn_df.loc[nn_df["mcc_adaptive"].idxmax()]
        test_mcc = _combo_mcc(df, target, nn_best["score"], nn_best["detector"])
        rows.append({
            "pathogen": target,
            "strategy": "nearest_neighbor_best",
            "selected_score": nn_best["score"],
            "selected_detector": nn_best["detector"],
            "test_mcc": test_mcc,
            "oracle_mcc": oracle,
            "oracle_score": oracle_row["score"],
            "oracle_detector": oracle_row["detector"],
            "pct_oracle": 100.0 * test_mcc / oracle if oracle > 0 and test_mcc is not None else 0.0,
        })

    return pd.DataFrame(rows)


def evaluate_coarse_ceilings(df: pd.DataFrame, sim: pd.DataFrame) -> pd.DataFrame:
    """Evaluate adaptive signal at family/scoring granularity.

    achieved_mcc is the best held-out combo inside the predicted class. This is
    not a deployable single-combo policy; it measures whether the adaptive class
    choice is useful enough to justify a second-stage calibration method.
    """
    rows = []
    pathogens = sorted(df["pathogen"].unique())

    for target in pathogens:
        target_df = df[df["pathogen"] == target]
        train = df[df["pathogen"] != target]
        oracle = float(target_df["mcc_adaptive"].max())
        training = [p for p in pathogens if p != target]
        weights = {p: max(0.01, float(sim.loc[target, p])) for p in training}
        nearest = sim.loc[target, training].idxmax()

        for level in ["score", "family"]:
            actual_class = target_df.groupby(level)["mcc_adaptive"].max().idxmax()

            nn_class = (
                df[df["pathogen"] == nearest]
                .groupby(level)["mcc_adaptive"]
                .max()
                .idxmax()
            )

            weighted_values = []
            for class_name, class_df in train.groupby(level):
                num = 0.0
                den = 0.0
                for pathogen, p_df in class_df.groupby("pathogen"):
                    w = weights[pathogen]
                    num += w * float(p_df["mcc_adaptive"].max())
                    den += w
                weighted_values.append((class_name, num / den if den else -np.inf))
            weighted_class = max(weighted_values, key=lambda item: item[1])[0]

            for strategy, predicted_class in [
                (f"{level}_nearest_neighbor_ceiling", nn_class),
                (f"{level}_weighted_ceiling", weighted_class),
            ]:
                achieved = float(target_df[target_df[level] == predicted_class]["mcc_adaptive"].max())
                rows.append({
                    "pathogen": target,
                    "strategy": strategy,
                    "level": level,
                    "predicted_class": predicted_class,
                    "actual_best_class": actual_class,
                    "class_match": predicted_class == actual_class,
                    "achieved_mcc": achieved,
                    "oracle_mcc": oracle,
                    "pct_oracle": 100.0 * achieved / oracle if oracle > 0 else 0.0,
                })

    return pd.DataFrame(rows)


def evaluate_shortlists(df: pd.DataFrame, sim: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for target in sorted(df["pathogen"].unique()):
        target_df = df[df["pathogen"] == target]
        oracle = float(target_df["mcc_adaptive"].max())

        for strategy in ["global_mean", "robust_mean", "sim_weighted", "sim_rank"]:
            ranking = _combo_ranking(df, sim, target, strategy)
            scored = []
            for combo, rank_score in ranking:
                score, detector = combo
                mcc = _combo_mcc(df, target, score, detector)
                if mcc is not None:
                    scored.append((combo, rank_score, mcc))

            oracle_rank = next(
                (i + 1 for i, (_, _, mcc) in enumerate(scored) if abs(mcc - oracle) < 1e-12),
                len(scored) + 1,
            )
            for k in [1, 3, 5, 10, 20, 50]:
                top = scored[:k]
                best_mcc = max(mcc for _, _, mcc in top)
                rows.append({
                    "pathogen": target,
                    "strategy": strategy,
                    "k": k,
                    "best_mcc_in_shortlist": best_mcc,
                    "oracle_mcc": oracle,
                    "pct_oracle": 100.0 * best_mcc / oracle if oracle > 0 else 0.0,
                    "oracle_rank": oracle_rank,
                    "oracle_in_shortlist": oracle_rank <= k,
                })

    return pd.DataFrame(rows)


def summarize(exact: pd.DataFrame, coarse: pd.DataFrame, shortlist: pd.DataFrame) -> pd.DataFrame:
    rows = []

    for strategy, group in exact.groupby("strategy"):
        rows.append({
            "category": "deployable_exact_combo",
            "strategy": strategy,
            "mean_mcc": group["test_mcc"].mean(),
            "median_mcc": group["test_mcc"].median(),
            "mean_pct_oracle": group["pct_oracle"].mean(),
            "positive_pathogens": int((group["test_mcc"] > 0).sum()),
            "n_pathogens": group["pathogen"].nunique(),
            "extra": "",
        })

    for strategy, group in coarse.groupby("strategy"):
        rows.append({
            "category": "coarse_ceiling",
            "strategy": strategy,
            "mean_mcc": group["achieved_mcc"].mean(),
            "median_mcc": group["achieved_mcc"].median(),
            "mean_pct_oracle": group["pct_oracle"].mean(),
            "positive_pathogens": int((group["achieved_mcc"] > 0).sum()),
            "n_pathogens": group["pathogen"].nunique(),
            "extra": f"class_match={int(group['class_match'].sum())}/{group['pathogen'].nunique()}",
        })

    for (strategy, k), group in shortlist.groupby(["strategy", "k"]):
        rows.append({
            "category": "shortlist_ceiling",
            "strategy": f"{strategy}@{k}",
            "mean_mcc": group["best_mcc_in_shortlist"].mean(),
            "median_mcc": group["best_mcc_in_shortlist"].median(),
            "mean_pct_oracle": group["pct_oracle"].mean(),
            "positive_pathogens": int((group["best_mcc_in_shortlist"] > 0).sum()),
            "n_pathogens": group["pathogen"].nunique(),
            "extra": f"oracle_hit={int(group['oracle_in_shortlist'].sum())}/{group['pathogen'].nunique()}",
        })

    return (
        pd.DataFrame(rows)
        .sort_values(["category", "mean_mcc"], ascending=[True, False])
        .reset_index(drop=True)
    )


def write_report(summary: pd.DataFrame, exact: pd.DataFrame, coarse: pd.DataFrame) -> Path:
    report_path = RESULTS_DIR / "adaptive_redesign_study.md"
    best_exact = summary[summary["category"] == "deployable_exact_combo"].iloc[0]
    best_coarse = summary[summary["category"] == "coarse_ceiling"].iloc[0]
    best_short = summary[summary["category"] == "shortlist_ceiling"].iloc[0]

    def markdown_table(frame: pd.DataFrame) -> str:
        text_frame = frame.copy()
        for col in text_frame.columns:
            if pd.api.types.is_float_dtype(text_frame[col]):
                text_frame[col] = text_frame[col].map(lambda value: f"{value:.4f}")
            else:
                text_frame[col] = text_frame[col].astype(str)
        headers = list(text_frame.columns)
        lines = [
            "| " + " | ".join(headers) + " |",
            "| " + " | ".join(["---"] * len(headers)) + " |",
        ]
        for _, row in text_frame.iterrows():
            lines.append("| " + " | ".join(str(row[col]) for col in headers) + " |")
        return "\n".join(lines)

    lines = [
        "# Adaptive Algorithm Redesign Study",
        "",
        "Primary metric: Layer A MCC under leave-one-pathogen-out evaluation.",
        "",
        "## Main Finding",
        "",
        (
            "Exact combo selection remains unstable, but adaptive signal is strong at "
            "the scoring-formula/family and shortlist levels. This supports a "
            "two-stage redesign: first adaptively restrict the search space, then "
            "calibrate detector thresholds inside the selected class."
        ),
        "",
        "## Best Results",
        "",
        (
            f"- Best deployable exact selector: `{best_exact['strategy']}` "
            f"mean MCC={best_exact['mean_mcc']:.4f}, "
            f"median MCC={best_exact['median_mcc']:.4f}."
        ),
        (
            f"- Best coarse adaptive ceiling: `{best_coarse['strategy']}` "
            f"mean MCC={best_coarse['mean_mcc']:.4f}, "
            f"median MCC={best_coarse['median_mcc']:.4f}, "
            f"{best_coarse['extra']}."
        ),
        (
            f"- Best shortlist ceiling: `{best_short['strategy']}` "
            f"mean MCC={best_short['mean_mcc']:.4f}, "
            f"median MCC={best_short['median_mcc']:.4f}, "
            f"{best_short['extra']}."
        ),
        "",
        "## Interpretation",
        "",
        (
            "The negative result is important: directly predicting one exact "
            "score-detector pair is too high-variance for nine pathogens. The "
            "positive result is that adaptive selection can recover much of the "
            "oracle when it is used to choose a scoring formula, detector family, "
            "or a short candidate list."
        ),
        "",
        "## Recommended Redesign",
        "",
        "1. Stage 1: predict a coarse class (`score` first, `family` second) from non-GT pathogen profiles.",
        "2. Stage 2: generate a top-20 robust shortlist inside that class.",
        "3. Stage 3: calibrate the detector with label-free stability criteria such as sparse-hit stability, bootstrap consistency, and constrained-site FPR.",
        "4. Report exact-combo performance separately from coarse/shortlist ceilings.",
        "",
        "## Top Summary Rows",
        "",
        markdown_table(summary.head(18)),
        "",
        "## Per-Pathogen Best Coarse Rows",
        "",
        markdown_table(coarse.sort_values(["strategy", "pathogen"])),
        "",
        "## Exact Selector Rows",
        "",
        markdown_table(exact.sort_values(["strategy", "pathogen"])),
        "",
    ]
    report_path.write_text("\n".join(lines), encoding="utf-8")
    return report_path


def main() -> None:
    df = load_results()
    profiles = build_no_gt_profiles(df)
    sim = profile_similarity(profiles)

    exact = evaluate_exact_selectors(df, sim)
    coarse = evaluate_coarse_ceilings(df, sim)
    shortlist = evaluate_shortlists(df, sim)
    summary = summarize(exact, coarse, shortlist)

    profiles.to_csv(RESULTS_DIR / "adaptive_redesign_profiles_no_gt.csv")
    sim.to_csv(RESULTS_DIR / "adaptive_redesign_similarity_no_gt.csv")
    exact.to_csv(RESULTS_DIR / "adaptive_redesign_exact_results.csv", index=False)
    coarse.to_csv(RESULTS_DIR / "adaptive_redesign_coarse_results.csv", index=False)
    shortlist.to_csv(RESULTS_DIR / "adaptive_redesign_shortlist_results.csv", index=False)
    summary.to_csv(RESULTS_DIR / "adaptive_redesign_summary.csv", index=False)
    report_path = write_report(summary, exact, coarse)

    print("Adaptive redesign study complete")
    print(f"Input pathogens: {df['pathogen'].nunique()}")
    print(f"Detailed exact results: {RESULTS_DIR / 'adaptive_redesign_exact_results.csv'}")
    print(f"Coarse results: {RESULTS_DIR / 'adaptive_redesign_coarse_results.csv'}")
    print(f"Shortlist results: {RESULTS_DIR / 'adaptive_redesign_shortlist_results.csv'}")
    print(f"Summary: {RESULTS_DIR / 'adaptive_redesign_summary.csv'}")
    print(f"Report: {report_path}")
    print()
    print(summary.head(12).to_string(index=False))


if __name__ == "__main__":
    main()
