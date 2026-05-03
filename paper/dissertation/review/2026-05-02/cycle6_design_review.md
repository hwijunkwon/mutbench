# Cycle 6 Design Review -- User-Intent-Aligned Content Review

Scope: design of a next dissertation review cycle aligned to the user's stated intent: content, length, method, argument focus, flow, and data appropriateness. Prior work includes cycle 1--3 paper-plan reviews and cycle 4 perspectives A--I. The active English PDF is 242 pages (`thesis_en.pdf`, built 2026-05-03).

## 1. Coverage Assessment

### Axis 1 -- Content Appropriateness

Well-defined: mostly yes, but it needs a rubric. "PhD-level depth" and "engineering-vs-science balance" should be operationalized as contribution novelty, biological interpretation, benchmark artifact value, and limits.

Overlap: overlaps with blue/red/professor reviews and cycle 4 falsifiability/generalisation. Differentiating angle: judge whether each chapter contains the right kind of material for a dissertation, not whether each claim survives adversarial attack.

Concrete checks: dissertation-scale problem, contribution necessity, Ch2 prerequisite coverage, Ch3 reproducibility detail, Ch4 evidence priority, Ch5 interpretation, and mature treatment of negative results.

Usefulness: high. This directly matches "내용의 적절성" and is not fully duplicated by prior adversarial reviews.

### Axis 2 -- Length Appropriateness

Well-defined: yes if measured using page count, chapter share, float density, table density, and prose compression targets.

Overlap: low. Earlier reviews discuss dense Wave sections, but not dissertation length as its own design problem.

Concrete checks: 242-page total, chapter-line balance, chapter role bloat, figure/table yield, equation placement, Wave 1--5 compression, and front/back matter proportionality.

Usefulness: high. This is the clearest new axis.

### Axis 3 -- Method Appropriateness

Well-defined: yes, but it should separate statistical appropriateness, benchmark-design appropriateness, and method-complexity appropriateness.

Overlap: substantial with cycle 4 F statistical alternatives, cycle 4 E reproducibility, and phase 2 statistics. Differentiating angle: ask whether the methods are appropriate for the dissertation question and defense readability, not whether more robustness tests exist.

Concrete checks: ANOVA/omega estimand fit, Friedman use, LOPO calibration, bootstrap unit alignment, Bayesian-check usefulness, simpler blocked-permutation value, and Ch3 pre-specification.

Usefulness: medium-high. It duplicates some statistical review, but the "method fit to thesis purpose" angle is still valuable.

### Axis 4 -- Argument Focus

Well-defined: yes if anchored to a single thesis sentence and contribution dependency map.

Overlap: medium with cycle 4 I flow and phase 4 professor. Differentiating angle: coherence of thesis identity, not local chapter ordering.

Concrete checks: one-sentence thesis, contribution dependency, main-thesis identity, case-study roles, Wave integration, and terminology stability.

Usefulness: high. This matches "주장하는 내용이 산만하지 않고 하나로 집중되는지".

### Axis 5 -- Flow

Well-defined: yes, but cycle 4 I already did a content-flow audit.

Overlap: high with cycle 4 I. Differentiating angle: make it user-intent-oriented and decision-oriented: would a committee reader experience the dissertation as motivation -> method -> result -> interpretation?

Concrete checks: roadmap accuracy, Ch2 preparation, Ch3 pre-specification, Ch4 central-first ordering, Ch5 implication order, Wave integration, and conclusion closure.

Usefulness: medium. Needed for the user, but should be combined with argument focus to avoid repeating cycle 4 I.

### Axis 6 -- Data Appropriateness

Well-defined: yes if split into panel design, sequence provenance, label provenance, and external validation.

Overlap: high with cycle 4 B curation, G HIV-1 cherry-pick, H generalisation, and E reproducibility. Differentiating angle: judge whether the dataset is appropriate for the dissertation's intended claims, not whether every data source is perfectly curated.

Concrete checks: 11-pathogen panel fit, 12-pathogen Stage 3 separation, sequence provenance, Layer A defensibility, Layer B/C role fit, HIV-1 validation independence, and missing-dataset disclosure.

Usefulness: high, but must be framed as "appropriateness for claim" to avoid duplicating curation/reproducibility audits.

## 2. Missing Axes

Recommend adding two axes.

### Added Axis 7 -- Claim-Evidence Calibration

Rationale: the user asks whether the argument is focused and data/methods are appropriate. The missing bridge is whether each claim's strength matches its evidence tier: proven, retrospective, suggestive, deferred, or negative.

Checks should classify headline claims across abstract, Ch1, Ch4, Ch5, and conclusion. This is distinct from red-team review because it produces a defense-facing claim register.

### Added Axis 8 -- Defense Readability and Q&A Robustness

Rationale: prior phase 4 simulated professor scoring, but this axis asks whether a human committee can verbally follow and challenge the dissertation without getting lost in terminology, panel sizes, and late-cycle audits.

Checks should focus on one-minute thesis, expected objections, figure/table explainability, and whether Ch4 can be explained without opening scripts or CSVs.

Do not add editorial polish as a full separate axis for this cycle. It is useful, but lower priority than content/method/data/focus and can be folded into flow and defense readability.

## 3. Check-Item Refinement

### Axis 1 -- Content Appropriateness

Check items:
- C1. Does Ch1 define a PhD-scale research gap, not only a software/tool gap? Verdict: strong / partial / weak.
- C2. Are the stated contributions individually necessary and collectively sufficient for the thesis? Verdict: sufficient / redundant / missing.
- C3. Does Ch2 cover all conceptual prerequisites used in Ch3--Ch5? Verdict: complete / minor gaps / major gaps.
- C4. Does Ch3 contain enough method detail for reproducibility without excessive implementation noise? Verdict: balanced / too thin / bloated.
- C5. Does Ch4 prioritize the main empirical findings before secondary audits? Verdict: clear / mixed / audit-dominated.
- C6. Does Ch5 synthesize implications and limitations rather than restating Ch4? Verdict: interpretive / mixed / repetitive.
- C7. Are negative/null results positioned as scope boundaries? Verdict: mature / defensive / buried.

### Axis 2 -- Length Appropriateness

Check items:
- L1. Total page count vs dissertation norm: current 242 pages. Verdict: appropriate / over / under.
- L2. Chapter balance by source size: Ch3 940 lines, Ch4 957, Ch5 Adapt 312, Ch5 Discussion 348. Verdict: balanced / methods-results heavy / discussion thin.
- L3. Are any sections longer than their defense value warrants? Verdict: no / moderate trimming / major trimming.
- L4. Does each figure/table support a claim that would be weaker without it? Verdict: high-yield / mixed / redundant.
- L5. Are equations and statistical details placed in the minimum necessary location? Verdict: efficient / some duplication / excessive.
- L6. Should Wave 1--5 details be compressed into a table plus appendix/provenance? Verdict: keep / compress / move.
- L7. Are abstract, introduction, and conclusion proportionate to the technical core? Verdict: proportionate / too dense / too thin.

### Axis 3 -- Method Appropriateness

Check items:
- M1. Is omega/ANOVA the right estimand for "pathogen-dependent optimality"? Verdict: appropriate / qualified / inappropriate.
- M2. Is Friedman used for the correct rank-level question? Verdict: appropriate / overclaimed / unnecessary.
- M3. Is LOPO interpreted correctly as corroborative evidence, not standalone proof? Verdict: calibrated / mixed / overclaimed.
- M4. Are bootstrap and cluster-bootstrap units defensible for the uncertainty claim? Verdict: defensible / limited / mismatched.
- M5. Do Bayesian checks clarify robustness, or create unnecessary method sprawl? Verdict: useful / optional / distracting.
- M6. Would a simpler blocked-permutation result be more defense-useful than additional complex models? Verdict: yes / no / already enough.
- M7. Are all analyses reported in Ch4 sufficiently specified in Ch3? Verdict: complete / minor missing / major missing.

### Axis 4 -- Argument Focus

Check items:
- F1. Is the central thesis visible on page 1/abstract? Verdict: explicit / inferable / absent.
- F2. Can the thesis be stated as one sentence without losing the three contributions? Verdict: yes / needs rewrite / no.
- F3. Do all major sections serve the same thesis rather than separate project identities? Verdict: focused / mixed / scattered.
- F4. Is the practical contribution subordinate to the benchmark/pathogen-dependence thesis? Verdict: aligned / competing / confusing.
- F5. Are pathogen case studies assigned stable roles: sanity check, main panel, external anchor, exploratory? Verdict: stable / partially stable / unstable.
- F6. Are 11/12 pathogen, 3-core/4-core, and Layer A/A' distinctions handled without fragmenting the argument? Verdict: clear / demanding / confusing.

### Axis 5 -- Flow

Check items:
- W1. Does the chapter sequence match motivation -> benchmark design -> evidence -> interpretation? Verdict: clean / usable / broken.
- W2. Does Ch1's roadmap match the actual current chapter contents? Verdict: current / partly stale / stale.
- W3. Does Ch3 prepare every major Ch4 analysis before results appear? Verdict: yes / partial / no.
- W4. Does Ch4 order results from central to supporting evidence? Verdict: clear / mixed / scattered.
- W5. Does Ch5 discuss limitations after the relevant result has been established? Verdict: aligned / delayed / disconnected.
- W6. Are Wave 1--5 presented as an integrated robustness arc? Verdict: integrated / log-like / orphaned.
- W7. Does the conclusion close the argument without introducing new claims? Verdict: clean / minor drift / major drift.

### Axis 6 -- Data Appropriateness

Check items:
- D1. Is the 11-pathogen panel adequate for the stated RNA-virus single-position scope? Verdict: adequate / limited but defensible / inadequate.
- D2. Is the 12-pathogen Stage 3 panel clearly separated from 11-pathogen claims? Verdict: clear / mixed / confusing.
- D3. Are sequence sources, filters, deduplication, alignment, and date scope verifiable from methods? Verdict: complete / partial / insufficient.
- D4. Is Layer A appropriate for positive labels despite heterogeneous evidence types? Verdict: defensible / limited / not defensible.
- D5. Are Layer B and Layer C used only for claims they can support? Verdict: calibrated / mixed / overused.
- D6. Is HIV-1 external validation independent and strong enough for the practical anchor role? Verdict: strong / limited / weak.
- D7. Are missing alternative datasets and unavailable validation panels acknowledged? Verdict: explicit / partial / absent.

### Axis 7 -- Claim-Evidence Calibration

Check items:
- E1. Are all abstract headline claims classified as proven, retrospective, suggestive, negative, or future work? Verdict: classified / partly / not.
- E2. Does every "demonstrates/shows/confirms" verb match the evidence tier? Verdict: calibrated / some overstatement / major overstatement.
- E3. Are retrospective benchmark findings distinguished from prospective deployment claims? Verdict: clear / mixed / blurred.
- E4. Are null/negative results included in the claim register? Verdict: included / partial / omitted.
- E5. Are confidence intervals and p-values used only where the inferential unit supports them? Verdict: calibrated / overprecise / misleading.
- E6. Does the conclusion avoid upgrading suggestive evidence into established fact? Verdict: yes / minor drift / no.

### Axis 8 -- Defense Readability and Q&A Robustness

Check items:
- Q1. Can a committee member understand the one-sentence thesis without knowing MutBench internals? Verdict: yes / partly / no.
- Q2. Can the candidate answer "what is your main contribution?" in three ordered bullets? Verdict: clear / too many / unclear.
- Q3. Can Ch4 be explained verbally using 3--5 core figures/tables? Verdict: yes / difficult / no.
- Q4. Are likely objections to Layer A, LOPO, HIV-1, and 11 pathogens answered in the main text? Verdict: yes / partial / no.
- Q5. Are terminology switches likely to derail Q&A? Verdict: low / moderate / high.
- Q6. Does the dissertation provide enough "why this matters" language for non-specialist committee members? Verdict: enough / thin / missing.

## 4. Execution Plan Recommendation

Minimum recommended job count: 4 codex jobs.

Job 1: Content + Length. These axes both judge chapter fit and dissertation proportions. They can share chapter/page/float inventory.

Job 2: Method + Data. These axes overlap on whether analyses and datasets support the stated claims. The reviewer should explicitly avoid repeating cycle 4 F/B/H and instead produce an appropriateness verdict.

Job 3: Argument Focus + Flow + Claim-Evidence Calibration. These are tightly coupled: one central thesis, chapter progression, and claim strength should be judged together.

Job 4: Defense Readability/Q&A. Keep separate because it should simulate oral committee comprehension rather than written manuscript structure.

Parallelism: run Jobs 1, 2, and 3 in parallel after giving them the prior review index and active manuscript files. Run Job 4 after Jobs 1--3, because it should use their findings to build a Q&A-focused risk map.

Do not run eight independent jobs. That would duplicate prior cycle 4 work and produce overlapping recommendations.

## 5. User Confirmation Prompt

Proposed prompt:

"Cycle 6 will review whether the dissertation matches your intended concerns: content appropriateness, length, method fit, focused argument, flow, and data appropriateness. I recommend adding two axes: (7) claim-evidence calibration and (8) defense readability/Q&A robustness. I would execute this as four jobs: (1) Content+Length, (2) Method+Data, (3) Focus+Flow+Claim Calibration, and (4) Defense Readability after the first three finish. Please confirm:

1. Use the six original axes as listed?
2. Add Axis 7 Claim-Evidence Calibration and Axis 8 Defense Readability/Q&A Robustness?
3. Proceed with the four-job plan: first three in parallel, fourth sequential after synthesis?"

Recommended default if the user wants the shortest path: approve all three.
