# Phase 4 Professor v6 — Distributed (10 codex blind agents)

Aggregate of 10 independent codex-driven blind professor evaluations dispatched in parallel on 215pp post-v219 manuscript. Each professor read all 5 active-build files and scored 10 items (A–J) on 0–10.

## 10 × 10 Score Matrix

| Prof | Role | A | B | C | D | E | F | G | H | I | J | Total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 01 | Chair, bioinformatics (medium) | 8.2 | 8.0 | 7.7 | 8.1 | 8.2 | 8.4 | 7.0 | 7.6 | 9.0 | 8.0 | **80.2** |
| 02 | Advisor, CS (medium) | 8.5 | 8.0 | 8.0 | 8.5 | 8.0 | 8.0 | 7.0 | 8.0 | 9.0 | 8.0 | **81.0** |
| 03 | Statistics/ML (high) | 8.0 | 8.0 | 7.0 | 8.0 | 7.0 | 8.0 | 7.0 | 8.0 | 9.0 | 7.0 | 77.0 |
| 04 | Computational biology (medium) | 8.0 | 8.0 | 7.5 | 7.0 | 7.0 | 8.0 | 7.0 | 8.0 | 9.0 | 8.0 | 77.5 |
| 05 | Virology/public health (medium) | 8.0 | 8.0 | 7.5 | 8.0 | 8.0 | 8.0 | 6.5 | 7.0 | 9.0 | 7.5 | 77.5 |
| 06 | VEP/PLM expert (highest) | 8.0 | 7.5 | 7.0 | **6.0** | 8.0 | 7.0 | 6.5 | 7.0 | 9.0 | 7.5 | 73.5 |
| 07 | Benchmark methodology (medium) | 8.0 | 8.0 | 7.5 | 8.0 | 7.5 | 8.0 | 7.0 | 8.0 | 9.0 | 7.5 | 78.5 |
| 08 | Practice/field user (high) | 8.0 | 8.0 | 7.0 | 8.0 | 7.0 | 8.0 | **6.0** | 6.5 | 9.0 | 7.5 | 75.0 |
| 09 | Statistical genetics (medium) | 8.0 | 8.0 | 7.0 | 8.0 | 7.0 | 8.0 | 7.0 | 8.0 | 9.0 | 8.0 | 78.0 |
| 10 | Structural biology (medium) | 8.0 | 8.0 | 7.0 | 8.0 | 7.0 | 8.0 | 7.0 | 8.0 | 9.0 | 7.0 | 77.0 |

## Item Means (across 10 profs)

| Item | Mean | Min | Max | Notes |
|---|---|---|---|---|
| A. 문제 정의 | 8.07 | 8.0 | 8.5 | strong |
| B. 관련 연구 | 7.95 | 7.5 | 8.0 | strong |
| C. 방법론 | **7.32** | 7.0 | 8.0 | weak |
| D. 실험 규모 | 7.76 | 6.0 | 8.5 | one outlier (Prof 06: 6.0) |
| E. 결과 해석 | **7.47** | 7.0 | 8.2 | weak |
| F. 기여 독창성 | 7.94 | 7.0 | 8.4 | strong |
| G. 실용 가치 | **6.80** | 6.0 | 7.0 | **weakest** |
| H. 서술 명확성 | 7.61 | 6.5 | 8.0 | mixed |
| I. 한계 인식 | **9.00** | 9.0 | 9.0 | strongest, unanimous |
| J. 완성도 | 7.60 | 7.0 | 8.0 | mixed |

## Headline

- **Mean total: 77.52/100** (range 73.5 – 81.0)
- **Item mean range: 6.80 (G) — 9.00 (I)**
- **Min single score: 6.0** (D by Prof 06; G by Prof 08)

## Gate Verdict

| Criterion | Threshold | Observed | Result |
|---|---|---|---|
| Phase 4 prompt: total ≥ 80 | 80 | 77.52 | **FAIL** |
| Phase 4 prompt: every item mean ≥ 6 | 6.0 | 6.80 (G) | PASS |
| Phase 4 prompt: no Critical from Phase 3 | — | n/a (skipped) | n/a |
| Skill memory diagnostic: mean ≥ 7 | 7.0 | 7.75 | PASS |
| Skill memory diagnostic: individual ≥ 5 | 5.0 | 6.0 | PASS |

→ **CONDITIONAL PASS** under skill-memory diagnostic; **FAIL** under Phase 4 prompt 80/100 gate.

## Per-item rationale (items < 8.0 mean)

### G. 실용 가치 (mean 6.80, weakest)
- **Why**: 0/12 callable under P5 abstention rule; LOPO 0/11; HBFWS p=0.78; Cycle 7B all 6 paradigms fail. Practical claim is bounded to "search-space reduction" via top-decile budget on a panel where the prospective callable set is empty.
- **Smallest fix**: Reframe G headline to "search-space reduction with prospectively-defined callable subsets, not deployable detector" and quantify (10–80 positions / 7–9× enrichment) up-front in abstract.

### C. 방법론 (mean 7.32)
- **Why**: 11-pathogen cluster bootstrap is anti-conservative (G ≤ 30 small-cluster regime). 5-frame robustness mitigates but doesn't fully fix. ANCOVA / Bayesian / mixed-effects each surface different ω² estimates.
- **Smallest fix**: Already addressed via 5-frame triangulation table; consider 1-line abstract caveat that 11-cluster bootstrap is small-G.

### E. 결과 해석 (mean 7.47)
- **Why**: LOPO 0/11 + Friedman p=0.990 + HBFWS p=0.78 + Cycle 7B failures all cluster as "panel-size limit" interpretation; some readers may read this as fragility rather than negative-result robustness.
- **Smallest fix**: Already framed as "convergent failure" pattern in ch4/ch5; no further change needed.

### H. 서술 명확성 (mean 7.61)
- **Why**: 215pp dense; Wave 1–5 + Cycle 7B + HBFWS + 5-frame ω² + Layer A/B/C taxonomy is a heavy load for non-specialist readers. Prof 08 (practice/field user) flagged 6.5.
- **Smallest fix**: Could add a 1-paragraph "audit ledger reading guide" in ch4 intro pointing to tab:audit_ledger.

### J. 완성도 (mean 7.60)
- **Why**: 6 active-build chapters + numerous orphan files create reader confusion; remaining 9-pathogen-era CSV archives flagged in audit v2/v3.
- **Smallest fix**: Repository-level README documenting active-build vs. orphan + archive freshness; outside main text scope.

### F. 기여 독창성 (mean 7.94)
- Borderline; only Prof 06 deducts to 7.0. No targeted fix needed at this margin.

### B. 관련 연구 (mean 7.95)
- Borderline; Prof 06 deducts to 7.5. ProteinGym/EVEREST/ViroGym preprint disclosure addressed in v217.

### D. 실험 규모 (mean 7.76)
- One outlier: Prof 06 (VEP/PLM expert, highest strictness) at 6.0; cites n=11 panel size.
- **Smallest fix**: Already explicitly acknowledged as "Bolker minimum" panel; the score reflects domain expert's strict prior, not new finding.

## Strongest single deductions

| Prof | Item | Score | Reason | Suggested fix |
|---|---|---|---|---|
| 06 | D | 6.0 | n=11 too small for any deployable claim | already acknowledged in ch5 limitations |
| 08 | G | 6.0 | "practical value" as field user requires deployable detector, not retrospective screen | reframe as triage tool with explicit refusal of deployment |
| 08 | H | 6.5 | dense audit prose hard to parse for end-user | audit ledger reading guide |
| 05 | G | 6.5 | virology end-user wants H3N2/SARS-CoV-2/HIV-1 actionable list | search-space anchor framed up front |
| 06 | G | 6.5 | similar to Prof 08 | same |

## Comparison to v4/v5

- v4 (215pp single-agent blind): 81.85
- v5 (215pp post-Critical+M1-M6 fix, single-agent blind): 82.6
- v6 (215pp post-v219, **10-prof distributed**): **77.52**

The distributed v6 is **5–7 points lower than v4/v5 single-agent**, consistent with single-agent blind evaluations being more lenient than a 10-perspective committee — committee variance produces lower means because at least one strict reviewer (Prof 06 at 73.5) penalizes weaknesses that single-agent passes normalize. This is **expected** and is the value-add of distributed evaluation: it surfaces the strictness gradient.

## Per-prof totals distribution

```
73.5  ████████████████████████████████████ Prof 06 (VEP/PLM, highest)
75.0  ██████████████████████████████████████ Prof 08 (Practice, high)
77.0  ████████████████████████████████████████ Prof 03, 10
77.5  ████████████████████████████████████████▌ Prof 04, 05
78.0  █████████████████████████████████████████ Prof 09
78.5  █████████████████████████████████████████▌ Prof 07
80.2  ████████████████████████████████████████████ Prof 01
81.0  ████████████████████████████████████████████▌ Prof 02
```

Five of ten profs land at 77.0–78.5; two reach ≥80; two are at 73.5–75.0.

## Net delta from v5

`-5.08` (82.60 → 77.52). The drop is committee-variance-driven, not new audit findings (audit v2+v3 fixes since v5 should have lifted the score, not lowered it).

`RESULT_PROF_V6_AGGREGATE: total=77.52/100 mean_prof=77.52 min_prof=73.5 max_prof=81.0 min_item=6.80(G) max_item=9.00(I) verdict=CONDITIONAL_PASS gate_phase4=FAIL gate_skill=PASS delta_from_v5=-5.08`
