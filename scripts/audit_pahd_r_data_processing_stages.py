#!/usr/bin/env python3
"""Stage-wise PAHD-R data-processing audit.

This audit asks whether each data-processing stage has measurable data
properties that should change the algorithm design.  It intentionally uses
already-produced PAHD-R experiment files plus the feature matrices, so the
output is a synthesis layer rather than another model sweep.
"""

from __future__ import annotations

from pathlib import Path
import sys

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = PROJECT_ROOT / "results" / "mutbench"
FEATURE_DIR = RESULTS_DIR / "feature_analysis"

sys.path.insert(0, str(PROJECT_ROOT / "scripts"))
import run_pahd_r_multi_hypothesis as pahd  # noqa: E402


OUT_REPORT = RESULTS_DIR / "pahd_r_data_processing_stage_audit.md"
OUT_ISSUES = RESULTS_DIR / "pahd_r_data_processing_stage_issues.csv"
OUT_FEATURE_STATS = RESULTS_DIR / "pahd_r_data_processing_feature_stats.csv"
OUT_PATHOGEN_SUMMARY = RESULTS_DIR / "pahd_r_data_processing_pathogen_summary.csv"


def read_csv_optional(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


def markdown_table(frame: pd.DataFrame, max_rows: int | None = None) -> str:
    if frame.empty:
        return "_No rows._"
    text = frame.head(max_rows).copy() if max_rows else frame.copy()
    for col in text.columns:
        if pd.api.types.is_float_dtype(text[col]):
            text[col] = text[col].map(lambda x: "" if pd.isna(x) else f"{x:.4f}")
        else:
            text[col] = text[col].astype(str)
    lines = [
        "| " + " | ".join(text.columns) + " |",
        "| " + " | ".join(["---"] * len(text.columns)) + " |",
    ]
    for _, row in text.iterrows():
        lines.append("| " + " | ".join(row[col] for col in text.columns) + " |")
    return "\n".join(lines)


def primary_pathogens(data: dict[str, pd.DataFrame]) -> list[str]:
    benchmark = read_csv_optional(RESULTS_DIR / "multilayer_9pathogen_results.csv")
    if benchmark.empty or "pathogen" not in benchmark:
        return sorted(data)
    return sorted(set(benchmark["pathogen"].unique()) & set(data))


def numeric_feature_stats(data: dict[str, pd.DataFrame], pathogens: list[str]) -> pd.DataFrame:
    rows = []
    for pathogen in pathogens:
        df = data[pathogen]
        y = df["layer_a"].astype(int).values
        for feature in pahd.FEATURES:
            x = pd.to_numeric(df[feature], errors="coerce")
            valid = x.dropna()
            auc = np.nan
            if y.sum() >= 2 and (len(y) - y.sum()) >= 2 and valid.nunique() > 1:
                try:
                    auc = roc_auc_score(y, x.fillna(0.0).values)
                except ValueError:
                    auc = np.nan
            q01 = valid.quantile(0.01) if len(valid) else np.nan
            q50 = valid.quantile(0.50) if len(valid) else np.nan
            q99 = valid.quantile(0.99) if len(valid) else np.nan
            mad = (valid - q50).abs().median() if len(valid) else np.nan
            outlier_frac = np.nan
            if pd.notna(mad) and mad > 1e-12:
                outlier_frac = float(((valid - q50).abs() > 8.0 * mad).mean())
            rows.append(
                {
                    "pathogen": pathogen,
                    "feature": feature,
                    "n_positions": len(df),
                    "n_layer_a": int(y.sum()),
                    "prevalence": float(y.mean()),
                    "missing_frac": float(x.isna().mean()),
                    "unique_values": int(valid.nunique()),
                    "zero_frac": float((valid == 0).mean()) if len(valid) else np.nan,
                    "std": float(valid.std(ddof=0)) if len(valid) else np.nan,
                    "skew": float(valid.skew()) if len(valid) > 2 else np.nan,
                    "q01": float(q01) if pd.notna(q01) else np.nan,
                    "q50": float(q50) if pd.notna(q50) else np.nan,
                    "q99": float(q99) if pd.notna(q99) else np.nan,
                    "mad_outlier_frac": outlier_frac,
                    "auc": auc,
                }
            )
    return pd.DataFrame(rows)


def pathogen_summary(stats: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for pathogen, group in stats.groupby("pathogen"):
        labels = group.iloc[0]
        usable_auc = group["auc"].dropna()
        inverted = group.loc[group["auc"] < 0.40, "feature"].tolist()
        strong = group.loc[group["auc"] >= 0.75, "feature"].tolist()
        weak = group.loc[(group["auc"] >= 0.40) & (group["auc"] <= 0.60), "feature"].tolist()
        rows.append(
            {
                "pathogen": pathogen,
                "n_positions": int(labels["n_positions"]),
                "n_layer_a": int(labels["n_layer_a"]),
                "prevalence": float(labels["prevalence"]),
                "max_feature_auc": float(usable_auc.max()) if len(usable_auc) else np.nan,
                "median_feature_auc": float(usable_auc.median()) if len(usable_auc) else np.nan,
                "n_inverted_features": len(inverted),
                "inverted_features": ", ".join(inverted),
                "n_strong_features": len(strong),
                "strong_features": ", ".join(strong),
                "n_weak_features": len(weak),
            }
        )
    return pd.DataFrame(rows).sort_values(["prevalence", "pathogen"])


def add_issue(
    rows: list[dict[str, str]],
    severity: str,
    stage: str,
    finding: str,
    evidence: str,
    method_modification: str,
    status: str,
) -> None:
    rows.append(
        {
            "severity": severity,
            "stage": stage,
            "finding": finding,
            "evidence": evidence,
            "method_modification": method_modification,
            "status": status,
        }
    )


def build_issues(stats: pd.DataFrame, summary: pd.DataFrame) -> pd.DataFrame:
    issues: list[dict[str, str]] = []
    raw = read_csv_optional(RESULTS_DIR / "pahd_r_raw_sequence_stability_summary.csv")
    dedup = read_csv_optional(RESULTS_DIR / "pahd_r_dedup_sequence_sensitivity_summary.csv")
    temporal = read_csv_optional(RESULTS_DIR / "pahd_r_temporal_design_coverage.csv")
    failures = read_csv_optional(RESULTS_DIR / "pahd_r_pathogen_failure_audit.csv")
    corr = read_csv_optional(FEATURE_DIR / "feature_correlation_mean.csv")
    final_decisions = read_csv_optional(RESULTS_DIR / "pahd_r_calibrated_core_final_decision_table.csv")

    if not raw.empty:
        flagged = raw.loc[
            (raw["duplicate_rate"] >= 0.50)
            | (raw["p05_top_jaccard"] < 0.70)
            | (raw["raw_sequence_stability_status"].astype(str).str.contains("review"))
        ]
        if not flagged.empty:
            evidence = "; ".join(
                f"{r.pathogen}: dup={r.duplicate_rate:.2f}, p05J={r.p05_top_jaccard:.2f}, {r.raw_sequence_stability_status}"
                for r in flagged.itertuples()
            )
            add_issue(
                issues,
                "medium",
                "raw_sequence_sampling",
                "원시 서열 표본의 중복률과 top-site 안정성이 병원체별로 다르다.",
                evidence,
                "raw-count 기반 recurrence를 절대증거로 쓰지 말고 dedup/sequence-bootstrap 민감도 표를 기본 검수에 포함한다.",
                "implemented_audit_gate",
            )

    if not dedup.empty:
        changed = dedup.loc[dedup["dedup_decision"].astype(str).str.contains("changes")]
        if not changed.empty:
            evidence = "; ".join(
                f"{r.pathogen}: original-vs-dedup J={r.original_vs_dedup_top_jaccard:.2f}"
                for r in changed.itertuples()
            )
            add_issue(
                issues,
                "medium",
                "dedup_preprocessing",
                "일부 병원체는 dedup 여부가 상위 후보 위치를 바꾼다.",
                evidence,
                "dedup을 새 기본값으로 고정하지 않고, 민감한 병원체에는 review caveat와 보수적 calibration을 적용한다.",
                "candidate_only",
            )

    sparse = summary.loc[(summary["n_layer_a"] < 10) | (summary["prevalence"] < 0.01)]
    if not sparse.empty:
        evidence = "; ".join(
            f"{r.pathogen}: nA={int(r.n_layer_a)}, prev={r.prevalence:.4f}"
            for r in sparse.itertuples()
        )
        add_issue(
            issues,
            "high",
            "label_layer_construction",
            "Layer-A 양성 라벨이 너무 희소한 병원체가 있어 exact MCC가 불안정하다.",
            evidence,
            "병원체별 전용 알고리즘으로 단정하지 말고, sparse target은 review/diagnostic 모드와 window metric을 함께 보고한다.",
            "claim_limited",
        )

    inverted_rows = summary.loc[summary["n_inverted_features"] > 0]
    if not inverted_rows.empty:
        evidence = "; ".join(
            f"{r.pathogen}: {r.inverted_features}"
            for r in inverted_rows.itertuples()
            if r.inverted_features
        )
        add_issue(
            issues,
            "high",
            "feature_direction",
            "feature의 유효 방향이 병원체마다 뒤집히는 경우가 있다.",
            evidence,
            "전역 고정 부호 대신 LOPO 학습 부호와 병원체별 reliability gate를 유지한다. PLM/structure feature는 보조증거로 제한한다.",
            "implemented_in_core_design",
        )

    weak_signal = summary.loc[summary["max_feature_auc"] < 0.60]
    if not weak_signal.empty:
        evidence = "; ".join(
            f"{r.pathogen}: maxAUC={r.max_feature_auc:.2f}"
            for r in weak_signal.itertuples()
        )
        add_issue(
            issues,
            "medium",
            "feature_signal_strength",
            "단일 feature가 충분히 강하지 않은 병원체가 있다.",
            evidence,
            "단일 feature 선택이나 AI feature 단독 주장을 피하고, evidence-fusion 결과도 null/decoy 검수를 통과해야 채택한다.",
            "guardrail",
        )

    high_outliers = stats.loc[stats["mad_outlier_frac"] >= 0.08]
    if not high_outliers.empty:
        by_path = (
            high_outliers.groupby("pathogen")["feature"]
            .apply(lambda x: ", ".join(sorted(set(x))))
            .reset_index()
        )
        evidence = "; ".join(f"{r.pathogen}: {r.feature}" for r in by_path.itertuples())
        add_issue(
            issues,
            "medium",
            "feature_scaling_outliers",
            "일부 feature는 heavy-tail/outlier 비율이 높아 rank가 과도하게 흔들릴 수 있다.",
            evidence,
            "winsorization은 후보 전처리로 유지하고, 기본 주장은 raw와 winsorized 민감도 차이를 같이 제시한다.",
            "candidate_only",
        )

    if not corr.empty:
        corr = corr.set_index(corr.columns[0]) if corr.columns[0] == "Unnamed: 0" else corr
        redundant = []
        for i, a in enumerate(pahd.FEATURES):
            for b in pahd.FEATURES[i + 1 :]:
                if a in corr.index and b in corr.columns:
                    val = float(corr.loc[a, b])
                    if abs(val) >= 0.80:
                        redundant.append(f"{a}-{b}={val:.2f}")
        if redundant:
            add_issue(
                issues,
                "medium",
                "feature_redundancy",
                "recurrence/diversity/selection proxy가 강하게 상관되어 evidence double-count 위험이 있다.",
                "; ".join(redundant),
                "모듈 평균, learned weight, reliability calibration을 유지하고, 다음 후보는 empirical-Bayes shrinkage로 중복 증거를 줄인다.",
                "partially_addressed",
            )

    if not temporal.empty:
        sufficient = temporal.loc[temporal.get("collection_year_coverage", 0) >= 0.80]
        if not sufficient.empty:
            evidence = "; ".join(
                f"{r.pathogen}: coverage={r.collection_year_coverage:.2f}"
                for r in sufficient.itertuples()
            )
            add_issue(
                issues,
                "low",
                "temporal_metadata",
                "일부 추가 수집 데이터는 temporal control 실험에 충분한 metadata coverage가 있다.",
                evidence,
                "시간 feature는 독립 증거가 아니라 robustness/control feature로만 사용한다. resampling 실패로 기본 반영은 보류한다.",
                "diagnostic_only",
            )

    if not failures.empty:
        broad = failures.loc[failures["flags"].astype(str).str.contains("broad_region|high_constrained_fpr|not_above_null")]
        if not broad.empty:
            counts = broad["flags"].str.get_dummies(sep=";").sum().sort_values(ascending=False)
            evidence = "; ".join(f"{k}={int(v)}" for k, v in counts.head(5).items())
            add_issue(
                issues,
                "high",
                "postprocessing_and_reporting",
                "window MCC만 보면 broad-region 또는 high-FPR 후보를 과대평가할 수 있다.",
                evidence,
                "exact MCC, P@20, constrained FPR, coverage, null exceedance를 동시 채택 기준으로 둔다. Core-Calibrated도 후보로만 둔다.",
                "implemented_guardrail",
            )

    if not final_decisions.empty:
        candidate = final_decisions.loc[final_decisions["entry"] == "PAHD-R-Core-Calibrated"]
        if not candidate.empty:
            row = candidate.iloc[0]
            add_issue(
                issues,
                "low",
                "algorithm_revision",
                "negative-control-aware calibration은 성능을 올리지만 병원체별 null 약점이 남는다.",
                (
                    f"Core-Calibrated exact={row.exact_mcc:.4f}, "
                    f"window10={row.mcc_window_10:.4f}, FPR={row.constrained_fpr:.4f}; "
                    f"decision={row.decision}"
                ),
                "새 기본값이 아니라 optional review/calibrated candidate로 유지한다.",
                "candidate_not_default",
            )

    return pd.DataFrame(issues)


def write_report(
    stats: pd.DataFrame,
    summary: pd.DataFrame,
    issues: pd.DataFrame,
) -> None:
    severity_order = {"high": 0, "medium": 1, "low": 2}
    severe = issues.copy()
    severe["_severity_order"] = severe["severity"].map(severity_order).fillna(9)
    severe = severe.sort_values(["_severity_order", "stage"]).drop(columns=["_severity_order"])
    feature_snapshot = summary[
        [
            "pathogen",
            "n_layer_a",
            "prevalence",
            "max_feature_auc",
            "median_feature_auc",
            "n_inverted_features",
            "inverted_features",
            "n_strong_features",
            "strong_features",
        ]
    ]
    report = f"""# PAHD-R data-processing stage audit

This audit checks which statistical properties should be inspected at each
data-processing stage and how those observations should modify PAHD-R.

## Stage conclusions

1. Raw sequence sampling and deduplication are not neutral for every pathogen.
   They should remain mandatory sensitivity checks, not hidden preprocessing.
2. Layer-A label sparsity is the largest hard limit for MERS-like targets.
   This limits exact-site claims and argues for review/diagnostic reporting.
3. Feature direction is pathogen-dependent.  Fixed global signs or single
   feature rules are unsafe; LOPO sign learning and reliability gating remain
   necessary.
4. Several features are redundant or heavy-tailed.  Module-level fusion,
   winsorized sensitivity checks, and future shrinkage are statistically
   justified.
5. Postprocessing must penalize broad calls.  Window MCC alone is insufficient;
   constrained FPR, coverage, precision@20, and null controls must stay in the
   decision rule.

## Issues and method modifications

{markdown_table(severe)}

## Pathogen-level feature diagnostics

{markdown_table(feature_snapshot)}

## Stage-by-stage action plan

| Stage | What to inspect | Method change |
| --- | --- | --- |
| Raw sequence collection | duplicate rate, usable length coverage, bootstrap top-site Jaccard | keep raw sampling and dedup sensitivity as audit gates |
| Alignment / coordinate mapping | feature length match, coordinate provenance, decoy coordinate controls | do not claim location signal unless provenance and decoy controls pass |
| Label construction | n Layer-A sites, prevalence, window sensitivity | sparse labels use review/diagnostic language and paired/null tests |
| Feature generation | missingness, variance, skew/outliers, per-feature AUC, AUC inversion | use LOPO signs, module fusion, winsorized candidate checks |
| Feature fusion | cross-feature correlation, module ablation, decoy margins | shrink or gate redundant evidence; keep Core-Calibrated as candidate |
| Candidate calling | prediction fraction, coverage, constrained FPR, P@20 | reject methods that improve only broad window MCC |
| External/additional data | temporal coverage, year-bin size, resampling stability | use temporal metadata as control/robustness evidence only |

## Highest-impact next design changes

1. Implement an empirical-Bayes or correlation-aware module shrinkage candidate
   to reduce double-counting among freq, entropy, and dnds_proxy.
2. Add a sparse-label policy: if n_layer_a < 10 or prevalence < 1%, report
   only review-mode candidate lists unless external validation exists.
3. Extend reliability calibration with a per-pathogen uncertainty score derived
   from raw bootstrap Jaccard, dedup sensitivity, feature inversion count, and
   null margin.
4. Keep PLM/AI-derived features as auxiliary evidence.  They are useful for
   some pathogens but fail directionality checks on others.

## Machine-readable outputs

- `{OUT_ISSUES.name}`
- `{OUT_FEATURE_STATS.name}`
- `{OUT_PATHOGEN_SUMMARY.name}`
"""
    OUT_REPORT.write_text(report, encoding="utf-8")


def main() -> None:
    data = pahd.load_feature_matrices()
    pathogens = primary_pathogens(data)
    stats = numeric_feature_stats(data, pathogens)
    summary = pathogen_summary(stats)
    issues = build_issues(stats, summary)

    stats.to_csv(OUT_FEATURE_STATS, index=False)
    summary.to_csv(OUT_PATHOGEN_SUMMARY, index=False)
    issues.to_csv(OUT_ISSUES, index=False)
    write_report(stats, summary, issues)

    print(f"Wrote {OUT_REPORT}")
    print(f"Wrote {OUT_ISSUES}")
    print(f"Wrote {OUT_FEATURE_STATS}")
    print(f"Wrote {OUT_PATHOGEN_SUMMARY}")


if __name__ == "__main__":
    main()
