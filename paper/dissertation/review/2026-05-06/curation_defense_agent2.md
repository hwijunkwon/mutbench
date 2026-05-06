# Dissertation Defense Audit: Layer A Curation Heterogeneity

## 1. Existing defenses (quoted from manuscript)

### Defense 1: Explicit Layer A heterogeneity disclosure in methods
**Location**: `ch3_methods.tex`, Section `Layer A: Adaptive Positive Selection`, lines 214-219.

**Quote**: "The operational contract is therefore evidence-based rather than algorithmic: Layer A is the union of literature-curated positive/diversifying-selection positions per the references in Table~\ref{tab:gt_positions}."

**Quote**: "SARS-CoV-2 and H3N2 use phylogenetically confirmed convergent evolution sites ($\geq$3 independent lineages); Norovirus uses epochal-variant positions; HCV uses the hypervariable regions HVR1/HVR2; and the remaining seven pathogens use literature-reported immune-escape position lists. This heterogeneous adaptive-selection union (convergent evolution $\cup$ immune escape $\cup$ HVR membership) is a limitation rather than a single computational construct..."

**Strength**: MEDIUM because it directly admits the concern and distinguishes the label logics. It is not a statistical defense; it tells the examiner the benchmark is intentionally evidence-based and heterogeneous.

### Defense 2: Layer A source/provenance table
**Location**: `ch3_methods.tex`, Table `tab:gt_positions`, lines 284-318; `ch5_discussion.tex`, Table `tab:layer_a_provenance`, lines 21-46.

**Quote**: "Table~\ref{tab:gt_positions} summarizes the amino acid position counts and sources for each pathogen's 3-layer ground truth."

**Quote**: "Layer~A provenance summary, one row per pathogen. ``Dominant source'' is the most-cited paper string in \texttt{layer\_a\_tags.csv}; tag mix shows the qualitative evidence type."

**Quote**: "Layer~A source heterogeneity is summarized above and treated as a limitation in Chapter~\ref{ch:discussion}."

**Strength**: LOW because it is descriptive provenance, not a correction. It lets the candidate identify HCV/HVR1-HVR2, Koel 2013 H3N2, Moore-Williamson 2015 HIV-1, etc., but it does not show that omega-squared survives within matched source types or curation philosophies.

### Defense 3: HCV-excluded sensitivity
**Location**: `ch4_results.tex`, ANOVA diagnostics / leave-one-out sensitivity, lines 481-502.

**Quote**: "Excluding HCV gives $\omega^2_{\text{scoring}\times\text{pathogen}}=0.246$, so the interaction is not driven only by HCV's HVR-based Layer~A; the caveat remains that Layer~A mixes convergent-evolution, immune-escape, and HVR-membership evidence."

**Quote**: "All 11 LOO values lie inside the 11-pathogen cluster-bootstrap 95\% interval $[0.201, 0.346]$ and above Cohen's large threshold (0.14)."

**Strength**: HIGH for the narrow claim "not all HCV." HCV is the most obvious protocol outlier because it uses region/HVR labels and has the largest leverage. Removing it leaves a large interaction. This does not prove biology over curation, but it blocks the simplest HCV-only artifact critique.

### Defense 4: Immune-escape-only Layer A subset audit
**Location**: `ch4_results.tex`, Ground Truth Heterogeneity, lines 861-893; `ch4_results.tex`, selective-reporting paragraph, line 427; `ch5_discussion.tex`, limitations matrix, line 217.

**Quote**: "A potential confound in interpreting the pathogen-dependent performance patterns is that the Layer~A ground truth definitions may themselves differ across pathogens."

**Quote**: "Despite homogeneous ground truth composition (immune\_escape $\geq 71\%$ for all 12 pathogens), 5 different best features emerge, and 10/12 pathogens retain the same best feature when restricting to immune\_escape-only positions."

**Quote**: "$\omega^2$ on Layer-A immune-escape-only subsets ($n = 10/9/4$, $\omega^2 = 0.199/0.187/0.137$; Chapter~\ref{ch:discussion}, Section~\ref{sec:gt_heterogeneity}). Each carries a small-sample caveat."

**Quote**: "Subset refits remain medium or larger: $\omega^2 = 0.199$ ($n = 10$), $0.187$ ($n = 9$), $0.137$ ($n = 4$); 6-category aggregation gives $0.103$."

**Strength**: MEDIUM. This is the closest direct answer to "same label type." It shows the interaction does not vanish after restricting to immune-escape-heavy labels, and feature rankings remain diverse. But immune_escape tag homogeneity is not the same as homogeneous curation protocol: HCV HVR-region entries can be tagged immune_escape, and antibody escape lists can still differ in assay granularity, review-source aggregation, coordinate mapping, and region-vs-position extraction.

### Defense 5: Frequency/Layer A circularity audit
**Location**: `ch5_discussion.tex`, Section `Independence of Ground Truth and Detection Methods`, lines 16-19.

**Quote**: "A per-pathogen audit of the point-biserial correlation between Layer~A membership and per-position frequency finds a mean $|\rho| = 0.12$ across the 11 pathogens (range $[-0.06, +0.33]$)."

**Quote**: "The effect is therefore pathogen-specific rather than uniform, and is driven by ground-truth curation style: pathogens whose Layer~A uses hypervariable/epochal-variant criteria (HCV, Influenza~B, Norovirus) couple more strongly with frequency than pathogens whose Layer~A uses phylogenetically-confirmed convergent positions (SARS-CoV-2, H3N2)."

**Quote**: "HCV's frequency-best ranking and Norovirus's epochal-variant Layer~A coupling with frequency scoring should be read as partly structural rather than purely mechanistic..."

**Strength**: MEDIUM. It directly acknowledges protocol-induced signal, especially for frequency scoring. It is convincing as a caveat and partial diagnostic, but it tests only one scoring signal's circularity, not whether the full scoring x pathogen omega-squared is protocol-driven.

### Defense 6: Curation reproducibility limitations paragraph
**Location**: `ch5_discussion.tex`, paragraph `Layer A curation-reproducibility limitations`, lines 48-49.

**Quote**: "Three structural limitations of the Layer~A curation procedure are not measured by the position-level circularity audit above and remain disclosed as bounding caveats rather than resolved failure modes."

**Quote**: "No duplicate independent recuration subset, inter-annotator agreement statistic, or adjudicated disagreement log is available, so label reproducibility is not directly measured against an alternate curator."

**Quote**: "A source-selection sensitivity check that swapped one dominant source for an alternative same-topic publication could plausibly alter both Layer~A membership and prevalence; this dissertation does not measure that source-selection sensitivity directly."

**Quote**: "For entries derived from source-reported regions rather than residue-specific assays, the labels should be interpreted as region-supported position annotations rather than as residue-equivalent experimental evidence..."

**Strength**: HIGH as disclosure, LOW as defense. It is admirably candid and names the exact reproducibility gaps, but it concedes rather than resolves the strict reviewer's concern.

### Defense 7: Limitations matrix frames the claim under real curation heterogeneity
**Location**: `ch5_discussion.tex`, limitations section and matrix, lines 193 and 217.

**Quote**: "Layer~A is intentionally heterogeneous across pathogens (Table~\ref{tab:gt_positions}); the interaction claim is therefore a claim about relative method rankings under real curation heterogeneity, not directly comparable absolute MCC across viruses."

**Quote**: "Layer~A heterogeneity & HCV, Norovirus, SARS-CoV-2, H3N2, and immune-escape-led pathogens use different label logics, so absolute MCC is not cross-pathogen comparable."

**Strength**: MEDIUM. This is defense by reframing: the dissertation does not claim absolute MCC comparability across viruses, only pathogen-dependent method ranking under the available benchmark. That is defensible for a benchmark thesis, but partial if the examiner asks whether the biology, independent of curation, causes the omega-squared.

## 2. Defense gaps

What's NOT in the manuscript:

- No explicit region-based vs position-based curation philosophy variable. HCV HVR1/HVR2, Norovirus epochal/loop-like positions, and residue-level antibody escape lists are discussed, but not encoded as a separate curation-protocol factor.
- No "same curation philosophy subset" omega-squared recalculation. The immune_escape-only subset is helpful, but it is evidence-type homogeneous, not protocol homogeneous.
- No direct test of whether $\omega^2_{\text{scoring}\times\text{pathogen}}$ drops substantially within homogeneous-curation subsets such as residue-level antibody escape only, non-region labels only, single-anchor lists only, or excluding all region-derived labels.
- No interaction model that includes curation protocol as a factor or covariate, e.g. scoring x pathogen after absorbing scoring x curation_type.
- No duplicate independent recuration or inter-annotator agreement. The manuscript explicitly says this is absent.
- No source-swap sensitivity analysis, e.g. replacing dominant Layer A sources with alternate same-topic publications and re-running the ANOVA.
- No per-position audit trail sufficient to distinguish original residue assay, review-derived residue, domain/region expansion, coordinate conversion, and curator judgment across every Layer A position.
- The candidate cannot yet quantify "how much of 0.296 is biology versus curation protocol"; the manuscript only shows that some signal remains after HCV exclusion and immune_escape filtering.

## 3. Defense readiness verdict

If asked: "Is your $\omega^2=0.296$ measuring biology or curation protocol?"

**Current best answer (from manuscript)**: "Excluding HCV gives $\omega^2_{\text{scoring}\times\text{pathogen}}=0.246$, so the interaction is not driven only by HCV's HVR-based Layer~A; the caveat remains that Layer~A mixes convergent-evolution, immune-escape, and HVR-membership evidence." Plus: "Subset refits remain medium or larger: $\omega^2 = 0.199$ ($n = 10$), $0.187$ ($n = 9$), $0.137$ ($n = 4$)."

**Adequacy**: PARTIAL. The candidate can point to specific paragraphs and numbers. The answer is enough to say "not purely HCV and not erased by immune-escape restriction." It is not enough to say "biology rather than curation protocol," because the manuscript itself states that curation protocol, auxiliary input quality, and biology are not isolated causally.

## 4. Suggested manuscript additions

To convert PARTIAL/WEAK to ADEQUATE, add:

- Add a curation-protocol annotation column to `layer_a_tags.csv`: `evidence_type`, `curation_unit` (`residue_assay`, `residue_review`, `region_membership`, `convergent_lineage`, `epochal_variant`), `dominant_source`, `source_count`, `coordinate_mapping_confidence`.
- Refit omega-squared on protocol-homogeneous subsets: residue-level immune escape only; non-region labels only; excluding HCV/Norovirus/Influenza B region/epochal definitions; single-anchor-only vs multi-source labels. Report whether scoring x pathogen remains large and how much it attenuates.
- Add a direct decomposition: model MCC as `scoring + family + pathogen + curation_protocol + scoring:curation_protocol + scoring:pathogen`, then report whether scoring:pathogen remains large after protocol terms.
- Insert after `ch4_results.tex` Ground Truth Heterogeneity paragraph: "This immune_escape-only audit controls evidence type but not curation protocol; region-derived and residue-derived immune_escape labels remain mixed. A protocol-homogeneous refit is deferred unless the per-position curation-unit tags are completed."
- Insert in `ch5_discussion.tex` limitations matrix, Layer A heterogeneity row: "The current dissertation cannot partition the 0.296 interaction into biological versus curation-protocol components; HCV-excluded and immune_escape-only refits bound the concern but do not eliminate it."

RESULT_CURATION_AGENT2: existing_defenses=7 gap_count=8 adequacy=PARTIAL suggested_additions=5
