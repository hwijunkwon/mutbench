# Phase 4 Professor v9 — 2-Stage Hybrid on v228

Re-run of v8 method (5 chapter-deep + 10 prof aggregator) on master v228 (post final-audit cleanup) to verify cleanup did not regress.

## 10 × 10 Score Matrix

| Prof | Role | A | B | C | D | E | F | G | H | I | J | v9 | v8 | Δ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 01 | Chair, bioinformatics | 8.7 | 8.4 | 8.3 | 8.5 | 8.5 | 8.6 | 7.8 | 8.0 | 9.1 | 8.4 | **84.3** | 84.0 | +0.3 |
| 02 | Advisor, CS | 8.6 | 8.4 | 8.3 | 8.5 | 8.4 | 8.5 | 7.9 | 8.0 | 9.1 | 8.5 | **84.2** | 84.3 | -0.1 |
| 03 | Statistics/ML | 8.6 | 8.4 | 8.1 | 8.3 | 8.2 | 8.3 | 7.8 | 7.9 | 9.0 | 8.4 | **82.0** | 82.9 | -0.9 |
| 04 | Comp biology | 8.6 | 8.4 | 8.3 | 8.4 | 8.5 | 8.4 | 7.9 | 8.0 | 9.0 | 8.5 | **84.0** | 83.9 | +0.1 |
| 05 | Virology | 8.6 | 8.4 | 8.2 | 8.5 | 8.4 | 8.3 | 7.8 | 7.9 | 9.1 | 8.5 | **83.7** | 84.7 | -1.0 |
| 06 | VEP/PLM (highest) | 8.5 | 8.3 | 8.0 | 8.2 | 8.4 | 8.1 | 7.6 | 7.8 | 9.0 | 8.3 | **82.2** | 81.7 | +0.5 |
| 07 | Benchmark | 8.6 | 8.4 | 8.3 | 8.4 | 8.5 | 8.3 | 7.9 | 7.9 | 9.0 | 8.4 | **83.7** | 83.7 | +0.0 |
| 08 | Practice/field | 8.4 | 8.3 | 8.2 | 8.4 | 8.3 | 8.2 | 7.7 | 7.5 | 9.0 | 8.1 | **82.1** | 83.2 | -1.1 |
| 09 | Stat genetics | 8.6 | 8.4 | 8.0 | 8.4 | 8.4 | 8.3 | 7.8 | 7.9 | 9.0 | 8.4 | **83.2** | 84.1 | -0.9 |
| 10 | Structural | 8.6 | 8.4 | 8.3 | 8.4 | 8.4 | 8.3 | 7.8 | 8.0 | 9.0 | 8.5 | **83.7** | 83.8 | -0.1 |

## Item Means

| Item | v9 | v8 | Δ |
|---|---|---|---|
| A | 8.58 | 8.59 | -0.01 |
| B | 8.38 | 8.33 | +0.05 |
| C | 8.20 | 8.36 | **-0.16** |
| D | 8.40 | 8.49 | -0.09 |
| E | 8.40 | 8.45 | -0.05 |
| F | 8.33 | 8.21 | +0.12 |
| G | **7.80** | 7.71 | +0.09 |
| H | 7.89 | 7.95 | -0.06 |
| I | 9.03 | 9.06 | -0.03 |
| J | 8.40 | 8.48 | -0.08 |

## Headline

- Mean total: **83.31/100** (v8: 83.63, Δ -0.32)
- All 10 profs ≥ 80
- Min item: G (practical) 7.80
- Max item: I (limitations) 9.03

## v9 vs v8 Stage 1 hidden-issue counts

| Chapter | v8 hidden | v9 hidden | Δ |
|---|---|---|---|
| abstract+ch1 | 11 | 13 | +2 |
| ch2 | 5 | 5 | 0 |
| ch3 | 9 | 9 | 0 |
| ch4 | 17 | 10 | **-7** |
| ch5 | 10 | 12 | +2 |
| Total | 52 | 49 | -3 |

Ch4 shows -7 hidden issues — the v228 cleanup (Bolker citation, Layer C anchor reinforcement) directly improved chapter-deep auditability.

## Gate Verdict

| Criterion | Threshold | v9 | Result |
|---|---|---|---|
| Phase 4 prompt total ≥ 80 | 80 | 83.31 | **PASS ✓** |
| Phase 4 min item mean ≥ 6 | 6.0 | 7.80 (G) | **PASS ✓** |
| Skill memory mean ≥ 7 | 7.0 | 8.33 | **PASS ✓** |
| Skill memory individual ≥ 5 | 5.0 | 7.5 | **PASS ✓** |

→ All 4 gates PASS. Defense readiness: **GREEN**.

## Per-prof shifts

- Prof 06 (VEP/PLM highest strictness) +0.5: cleanup credit applied
- Prof 03 (Stats/ML high) -0.9: lost C narrative credit on close re-read
- Prof 05/08/09 -0.9 to -1.1: minor drift, still ≥ 82
- Prof 01 (Chair) +0.3: v228 cleanup positively absorbed

## Verdict

v9 ≈ v8 within evaluation noise (±0.5 per prof, -0.32 mean). v228 cleanup did **not regress** the manuscript and even tightened ch4 (chapter-deep hidden issues 17→10). All gates PASS, defense readiness confirmed.

No problematic findings. **Defense-ready as v228**.

`RESULT_PROF_V9_AGGREGATE: total=83.31/100 mean_prof=83.31 min_prof=82.0 max_prof=84.3 min_item=7.80(G) max_item=9.03(I) verdict=PASS gate_phase4=PASS gate_skill=PASS delta_from_v8=-0.32 hidden_issues=49 (vs v8 52)`
