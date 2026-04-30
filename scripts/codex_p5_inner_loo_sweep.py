#!/usr/bin/env python3
"""P5 predeclared threshold sensitivity sweep.

Per codex Wave 2 review §Q3: sweep D1 quorum and D2 lower bound only.
DO NOT sweep D3 thresholds, D4 prevalence band, or inversion-count
threshold (would multiply researcher degrees of freedom).

Reuses raw diagnostic counts from p5_callable_decisions.csv (the
columns d1_n_pass, d2_boot_lo, d3_pass, d4_pass, inversion_pass
are independent of the swept thresholds). For each
(quorum in {5, 6, 7, 8}) × (lower_bound in {1.05, 1.10, 1.20, 1.50})
× (method in {3-core, 4-core}) = 32 configs:
  callable_pass = (d1_n_pass >= quorum) AND (d2_boot_lo > lower_bound)
                  AND d3_pass AND d4_pass AND inversion_pass
  Aggregate: count of callable, mean MCC, sum TP@50, identity.

This is a SENSITIVITY analysis, not threshold selection — defaults
(7/11, 1.10) remain the pre-registered rule. The sweep reports
robustness only.

Output: results/mutbench/codex_wave2/p5_threshold_sensitivity_sweep.csv
"""
from __future__ import annotations
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = PROJECT_ROOT / "results" / "mutbench" / "codex_wave2"

QUORUM_GRID = [5, 6, 7, 8]
LOWER_GRID = [1.05, 1.10, 1.20, 1.50]
METHODS = ["3-core", "4-core"]


def main():
    df = pd.read_csv(OUT_DIR / "p5_callable_decisions.csv")
    rows = []
    for method in METHODS:
        sub = df[df["method"] == method].copy()
        for q in QUORUM_GRID:
            for t in LOWER_GRID:
                d1_eff = (sub["d1_n_pass"] >= q).astype(int)
                d2_eff = (sub["d2_boot_lo"] > t).astype(int)
                # Other diagnostics fixed
                callable_eff = (
                    d1_eff
                    * d2_eff
                    * sub["d3_pass"]
                    * sub["d4_pass"]
                    * sub["inversion_pass"]
                ).astype(int)
                callable_subset = sub[callable_eff == 1]
                n_call = len(callable_subset)
                if n_call > 0:
                    mean_mcc = float(callable_subset["observed_mcc"].mean())
                    sum_tp50 = int(callable_subset["observed_tp50"].sum())
                    sum_tp20 = int(callable_subset["observed_tp20"].sum())
                    sum_tp80 = int(callable_subset["observed_tp80"].sum())
                    callable_ids = ";".join(callable_subset["pathogen"])
                else:
                    mean_mcc = float("nan")
                    sum_tp20 = sum_tp50 = sum_tp80 = 0
                    callable_ids = ""
                rows.append({
                    "method": method,
                    "d1_quorum": q,
                    "d2_lower_bound": t,
                    "n_callable": n_call,
                    "n_total": len(sub),
                    "callable_fraction": n_call / max(1, len(sub)),
                    "mean_mcc_callable": mean_mcc,
                    "sum_tp20_callable": sum_tp20,
                    "sum_tp50_callable": sum_tp50,
                    "sum_tp80_callable": sum_tp80,
                    "callable_pathogens": callable_ids,
                })
    out = pd.DataFrame(rows)
    out.to_csv(OUT_DIR / "p5_threshold_sensitivity_sweep.csv", index=False)
    # Print summary table
    print("Predeclared threshold sensitivity sweep (D1 quorum × D2 lower bound)")
    print("=" * 78)
    for method in METHODS:
        print(f"\n--- {method} ---")
        sub = out[out["method"] == method]
        pivot = sub.pivot_table(index="d1_quorum", columns="d2_lower_bound",
                                 values="n_callable")
        print("n_callable (rows: D1 quorum, cols: D2 lower bound)")
        print(pivot.to_string())
        # Best (highest n_callable) configuration
        best = sub.loc[sub["n_callable"].idxmax()] if sub["n_callable"].max() > 0 else None
        if best is not None:
            print(f"\n  Best config: quorum={best['d1_quorum']}, "
                  f"lower={best['d2_lower_bound']:.2f}: "
                  f"{int(best['n_callable'])}/{int(best['n_total'])} callable, "
                  f"mean MCC = {best['mean_mcc_callable']:.4f}, "
                  f"sum TP@50 = {int(best['sum_tp50_callable'])}, "
                  f"callable: {best['callable_pathogens']}")
        else:
            print("  No configuration in sweep yields any callable folds.")
    print(f"\nWrote {OUT_DIR}/p5_threshold_sensitivity_sweep.csv")


if __name__ == "__main__":
    main()
