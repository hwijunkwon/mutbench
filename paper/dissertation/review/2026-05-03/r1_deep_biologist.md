# Risk-1 Deep Archetype 2 -- Biologist / Wet-Lab User Rebuttal

## Opening question

**Biologist:** "If 0/12 folds are callable and you cannot deploy this prospectively, why should a wet-lab group invest pipette time on MutBench predictions?"

**Defense script:** I would not ask a wet-lab group to deploy MutBench as a prospective escape alarm. The defensible claim is narrower: MutBench is a retrospective triage instrument that can reduce an experimentally expensive residue search from a whole glycoprotein to a short candidate list. The strongest evidence is HIV-1 Env gp120, where the best audit gives 7.19x enrichment over 45 antibody-escape positions, 82% of that escape set is Layer-A-disjoint, 37/45 positions are novel relative to Layer A, and the novel-only enrichment remains Bonferroni-significant at about p_adj = 3.9e-9 (ch4 lines 941-972, 976-987; ch5 lines 125-149, 242). That does not prove prospective deployment; it says that when a lab has budget for 10-50 residues rather than hundreds to about 1,000 mutation/neutralization experiments, MutBench can be a rational prioritization heuristic.

## Three hard follow-up questions

### 1. Retrospective value versus operational value

**Quote:** "You are calling this practical, but the prospective/callability audit refuses all folds. Isn't this only a retrospective curve-fitting exercise?"

**Why hard:** A wet-lab reviewer will distinguish a tool that directs current surveillance from a tool that explains old biology. The 0/12 callable result blocks any claim that a user can run MutBench tomorrow and treat a call as an operational warning.

**Best rebuttal:** Correct: it is not an operational warning system. The practical value is lower in the stack: retrospective residue prioritization for experiments, with HIV-1 as the least circular anchor because only 18% of the escape list overlaps Layer A and 37/45 escape positions are Layer-A-disjoint, yet the novel-only signal remains 7.16-8.24x enriched after 780-test correction (ch4 lines 941-972; ch5 lines 144-149). For lab economics, that converts "screen the whole envelope/glycoprotein" into "start with a 10-50 residue list," which is exactly how limited pipette time is usually allocated before DMS, neutralization, or structural validation (ch4 lines 986-987; ch5 lines 132-134, 157-160, 242).

### 2. False discovery and wasted experiments

**Quote:** "If the positive predictive value is not high, why should I spend antibody panels, pseudovirus assays, or mutagenesis budget on these calls?"

**Why hard:** Enrichment is not the same as precision. Even a 7x enriched list may contain many false positives, and false positives cost real labor, reagents, assay time, and opportunity cost.

**Best rebuttal:** I would present MutBench as a first-pass enrichment filter, not a definitive biological annotation. In HIV-1, the key point is not that every detected residue is an escape residue; it is that the candidate pool is materially enriched for independently curated antibody-escape positions, including a mostly Layer-A-disjoint subset, so the expected yield per assayed residue rises compared with exhaustive or unguided selection (ch4 lines 941-972, 976-987; ch5 lines 141-149). The right wet-lab workflow is to treat the output as a ranked candidate set to cross-check against exposure, glycan context, antibody footprint, and construct feasibility before committing assays.

### 3. Interpretability and structural biology

**Quote:** "A ranked site list is not enough. Can you tell me why a position matters biologically, or is this just a black-box hotspot score?"

**Why hard:** Virologists and structural biologists need mechanistic plausibility: surface exposure, conformational epitope context, glycosylation, receptor-binding effects, and fitness constraints. A position-only signal can be unconvincing if it cannot be mapped to a structure or epitope hypothesis.

**Best rebuttal:** The current claim is position triage, not mechanism discovery. MutBench integrates interpretable signal families--frequency/entropy, phylogenetic selection, homoplasy, PLM scores, and structural features--and Chapter 4 explicitly reports that pathogen-specific best features differ, which is why the thesis avoids a universal mechanistic story (ch4 lines 927-936; ch5 lines 123-134, 157-181). For HIV-1, the defense should say: the audit identifies an enriched set of Env gp120 antibody-escape candidates, including novel-to-Layer-A positions; wet-lab and structural follow-up must then decide whether those residues are directly antibody-contacting, allosteric, glycan-mediated, or fitness-linked.

## Two trap questions

### Trap 1

**Quote:** "H3N2 has 69% Layer-A overlap. Isn't MutBench just rediscovering known antigenic sites?"

**Why weak:** For H3N2, yes, mostly. Chapter 4 says H3N2 is a self-consistency check: 20/29 escape positions overlap Layer A, 8 of the 9 top captured drift sites are already in Layer A, and the novel-only H3N2 test is not significant (p = 0.132) (ch4 lines 970-984; ch5 lines 131, 144-149, 242).

**Scope-narrowing honest response:** I would not lead with H3N2 as external validation. H3N2 shows that the scoring system can recover canonical antigenic site A/B biology and that EqualWeight can add site-B positions 160 and 186 beyond frequency-only top-5, but it does not carry the novelty claim (ch4 lines 979-984; ch5 lines 131-132). The practical-value claim should lead with HIV-1, where the escape audit is mostly Layer-A-disjoint and the novel-only enrichment remains significant.

### Trap 2

**Quote:** "If MutBench prioritizes positions, isn't DMS already the gold-standard prioritization?"

**Why weak:** DMS is the stronger experimental assay when a relevant library, phenotype, strain background, and antibody/serum context exist. MutBench should not be framed as replacing DMS.

**Scope-narrowing honest response:** DMS is a downstream or parallel gold standard; MutBench is a cheaper computational prefilter for cases where DMS is unavailable, incomplete, too expensive, or not matched to the antibody/virus context. Chapter 5 explicitly says users should complement low-recall or difficult pathogens with DMS or epitope mapping and that task-aligned comparison with DMS/fitness benchmarks remains future work (ch5 lines 120, 151-154). The defensible role is to choose which residues deserve first experimental attention, not to adjudicate final escape biology.

### Trap 3

**Quote:** "Most viral hotspot 'discoveries' are sites already known from immune-evasion literature. Why is this not literature mining with extra computation?"

**Why weak:** Layer A partly includes immune-escape evidence, so circularity is a real concern. The dissertation already concedes this for H3N2 and SARS-CoV-2 and labels them self-consistency/exploratory rather than primary external validation (ch4 lines 941-984; ch5 lines 141-149).

**Scope-narrowing honest response:** The claim should not be "MutBench discovers all-new viral immunology across pathogens." The narrower defensible statement is: in HIV-1, the external escape list is largely independent of the Layer-A construction--82% disjoint, 37/45 novel positions--and still shows 7.16-8.24x novel-only enrichment after correction (ch4 lines 970-977; ch5 lines 144-149, 242). That makes HIV-1 the evidence for nontrivial triage value; H3N2 is retained as a sanity check, not as novelty evidence.

## Strongest deduction

The biologist most likely deducts for overstated practical deployment because 0/12 callable and the prospective validation gap mean MutBench cannot yet be used as a surveillance decision rule; the discussion must lead with **HIV-1 novel-only escape enrichment, not H3N2**, because H3N2's 69% Layer-A overlap invites the circularity objection.

RESULT_R1_DEEP_BIO: anticipated_score=7.2/10 anchor_to_lead="HIV-1 7.19x full-set enrichment with 82% Layer-A-disjoint escape set, 37/45 novel positions, and novel-only p_adj=3.9e-9" trap_count=3
