# Layer A Curation Philosophy Catalog

## Summary table (12 pathogens)

| Pathogen | n | sources | curation method | year span | evidence types | implicit feature bias |
|---|---:|---|---|---|---|---|
| HCV | 54 | no paper tag; HVR1/HVR2 protocol | region-based | NA | immune 54/54 | Very high: whole hypervariable regions make frequency/entropy-like signals win by construction. |
| HIV-1 | 26 | single paper: Moore & Williamson | V-loop region-based | 2015 | immune 26/26 | Very high: variable-loop inclusion privileges entropy/diversity. |
| H3N2 | 25 | single paper: Koel | antigenic-site / cluster-transition | 2013 | immune 25/25 | High: antigenic HA sites overlap known selected epitopes; phylogenetic selection is advantaged. |
| Influenza_B | 17 | Wang; Ni | antigenic-loop based | 2008-2013 | immune 17/17 | High: drift-loop sites privilege frequency and entropy in HA surface loops. |
| RSV | 20 | Sullender; Mas | antigenic-site based | 2000-2018 | immune 20/20 | High: named F antigenic sites privilege surface/PLM/epitope accessibility. |
| EV-A71 | 27 | Foo; Plevka; Lim; Huang; NikNadia | loop/epitope hybrid | 2007-2018 | immune 25/27; functional 2/27 | Moderate-high: capsid loop labels privilege surface semantic/structural change. |
| Rabies | 39 | Lafon; Dietzschold; Benmansour; Guo; Aditham | antigenic-site plus DMS hybrid | 1983-2025 | immune 38/39; functional 1/39 | Moderate: legacy antigenic sites plus DMS escape can privilege local structural stability/escape effects. |
| SARS-CoV-2 | 25 | Korber; Carabelli; Cao | position-by-position multi-VOC | 2020-2023 | immune 22/25; functional 3/25 | Lower: curated individual VOC mutations, not whole regions; less automatic feature bias. |
| Dengue | 24 | Twiddy; Holmes | domain/position hybrid | 2002-2003 | immune 17/24; convergent 7/24 | Moderate: EDIII and serotype-diversifying positions privilege entropy/indel diversity. |
| MERS | 9 | Tang; Kim | sparse RBD point/region hybrid | 2014-2016 | immune 7/9; functional 2/9 | Moderate: receptor-interface escape labels privilege frequency in RBD mutations. |
| Norovirus | 15 | Lindesmith 2012/2013 | P2 epochal-position hybrid | 2012-2013 | immune 15/15 | High: epochal variant/blockade sites privilege homoplasy and convergent replacement signals. |
| Zika | 27 | Keeffe; Long; Sourisseau | epitope plus DMS/convergence hybrid | 2018-2019 | immune 25/27; convergent 2/27 | Moderate-high: DIII epitope/DMS labels privilege surface semantic change and entropy. |

## Per-pathogen detail

### HCV (n=54)
**Curation method**: Pure region inclusion: every position in HVR1 (1-27) and HVR2 (77-103).  
**Sources**: No explicit paper/year in the tag file; single curation protocol.  
**Implicit bias**: Extreme. The positive set is literally hypervariable antibody-escape sequence, so frequency, rarity, entropy, and window methods are advantaged.  
**Effect on Stage 2 best scoring**: Matches expectation. Observed best is `freq` (MCC 0.660), consistent with protocol-driven high-frequency-region labels.

### HIV-1 (n=26)
**Curation method**: Region-based inclusion of Env variable-loop positions (V1/V2/V3/V4/V5) from Moore & Williamson 2015.  
**Sources**: Single paper, 2015.  
**Implicit bias**: Extreme. Variable loops are high-entropy by definition.  
**Effect on Stage 2 best scoring**: Matches expectation. Observed best is `entropy` (MCC 0.275). The curation protocol almost pre-specifies this information type.

### H3N2 (n=25)
**Curation method**: Single-paper antigenic-site/cluster-transition list from Koel 2013, concentrated in HA sites A/B/D/E.  
**Sources**: Single paper, 2013.  
**Implicit bias**: High. Antigenic-site positions are historically drifted and epitope-exposed, so codon positive-selection scores can rediscover them.  
**Effect on Stage 2 best scoring**: Matches expectation. Observed best is FUBAR Bayes factor (MCC 0.534).

### Influenza_B (n=17)
**Curation method**: Antigenic-loop regions: 120-loop, 140/150-loop, 160-loop, 190-helix, and drift positions.  
**Sources**: Two papers, 2008-2013.  
**Implicit bias**: High. Loop/drift labels favor frequency and entropy signals in surface HA.  
**Effect on Stage 2 best scoring**: Matches expectation. Observed best is `freq` (MCC 0.392).

### RSV (n=20)
**Curation method**: Antigenic-site inclusion on F protein: site II, IV, 0, and I.  
**Sources**: Two papers across 2000-2018.  
**Implicit bias**: High, but not toward MSA variability alone; named prefusion/surface sites can privilege structure-aware or PLM signals.  
**Effect on Stage 2 best scoring**: Partial/non-match. Expected surface/epitope accessibility; observed best is ESM-2 masked-marginal (MCC 0.196), plausible but not directly protocol-predicted.

### EV-A71 (n=27)
**Curation method**: Hybrid loop/epitope protocol: BC, DE, and GH loop regions plus a few specific escape/functional mutations.  
**Sources**: Five papers, 2007-2018.  
**Implicit bias**: Moderate-high. Surface capsid loops privilege semantic-change and structural accessibility features; two functional labels add a non-immune component.  
**Effect on Stage 2 best scoring**: Plausible match. Observed best is `semantic_change` (MCC 0.260), consistent with loop/epitope residue replacement sensitivity.

### Rabies (n=39)
**Curation method**: Hybrid. Legacy antigenic sites I-IV are region-defined, while 2025 DMS escape sites and G349 are position-specific.  
**Sources**: Five papers across 1983-2025.  
**Implicit bias**: Moderate. Region labels favor surface antigenic patches; DMS labels favor functional escape/stability effects.  
**Effect on Stage 2 best scoring**: Weak match. Observed best is `stability` (MCC 0.248). That fits DMS/functional additions better than the older antigenic-site blocks.

### SARS-CoV-2 (n=25)
**Curation method**: Position-by-position multi-VOC curation: RBD/NTD escape and functional mutations, not whole-region inclusion.  
**Sources**: Three papers, 2020-2023.  
**Implicit bias**: Lower than most. It favors known VOC/escape mutations, but does not automatically select high-entropy regions.  
**Effect on Stage 2 best scoring**: Non-match. Observed best is Tranception (MCC 0.211). The protocol does not obviously pre-select a PLM feature winner.

### Dengue (n=24)
**Curation method**: Hybrid: EDIII immune positions plus Holmes serotype-diversifying positions in domains I/II.  
**Sources**: Two papers, 2002-2003.  
**Implicit bias**: Moderate. Serotype-diversifying labels bias toward entropy/indel-aware diversity; EDIII labels bias toward surface epitopes.  
**Effect on Stage 2 best scoring**: Matches expectation. Observed best is `entropy_with_indel` (MCC 0.274).

### MERS (n=9)
**Curation method**: Sparse RBD interface curation with escape and receptor-binding/positive-selection positions.  
**Sources**: Two papers, 2014-2016.  
**Implicit bias**: Moderate. Small RBD set may privilege recurrent/frequency signals, but n is too small for stable inference.  
**Effect on Stage 2 best scoring**: Plausible match. Observed best is `freq` (MCC 0.196), but this is fragile because Layer A has only 9 positives.

### Norovirus (n=15)
**Curation method**: P2-domain epochal/blockade positions, selected one-by-one but within a domain/epochal evolution frame.  
**Sources**: Two related papers, 2012-2013.  
**Implicit bias**: High. Epochal replacement and blockade escape should favor homoplasy/convergence signals.  
**Effect on Stage 2 best scoring**: Matches expectation. Observed best is `homoplasy` (MCC 0.510).

### Zika (n=27)
**Curation method**: Hybrid DIII/DII epitope, DMS-escape, and convergent/diversifying positions.  
**Sources**: Three papers, 2018-2019.  
**Implicit bias**: Moderate-high. DIII lateral-ridge and DMS escape labels favor surface semantic-change/entropy signals.  
**Effect on Stage 2 best scoring**: Not applicable: Zika is present in `layer_a_tags.csv` but absent from Table 4.1 / `stage3_full_results.csv`.

## Cross-pathogen patterns

- **Region-based curation** (HCV, HIV-1): These are the clearest protocol-dependence cases. The target definition embeds hypervariability, so frequency/entropy winners should not be interpreted as independent pathogen biology.
- **Position-based curation** (SARS-CoV-2, MERS, Norovirus, Rabies): These sets are less mechanically biased, but still inherit the literature's attention bias toward VOCs, receptor interfaces, antibody escape, or epochal variants.
- **Antigenic-site definition** (H3N2, RSV, Influenza_B): These labels are biologically meaningful, but not neutral. They favor surface-exposed epitope, drift, phylogenetic-selection, and PLM/structure signals.
- **DMS-supplemented** (EV-A71, Rabies, Zika): These are hybrid ground truths. They are stronger experimentally, but mix immune escape and functional effects, which can shift winners toward semantic-change or stability features.

## Implicit feature bias assessment

Expected best feature from protocol alone: HCV frequency; HIV-1 entropy; H3N2 FUBAR/selection; Influenza_B frequency/entropy; Dengue entropy-with-indel; Norovirus homoplasy; MERS frequency; EV-A71 semantic/structure; Rabies stability/structure; RSV surface/PLM; SARS-CoV-2 no strong protocol prediction; Zika semantic/entropy, unobserved.

Against the 11 observed Stage 2 pathogens, clear or plausible matches are HCV, HIV-1, H3N2, Influenza_B, Dengue, Norovirus, MERS, and EV-A71: 8/11. Rabies is partial, RSV is plausible but weak, and SARS-CoV-2 is the cleanest non-match. Zika cannot be compared because it lacks a Stage 2 winner in the archived table.

## Risk verdict

The reviewer concern is materially valid. Layer A is not a single measurement instrument: it is a mixture of whole-region definitions, antigenic-site definitions, position-by-position VOC curation, and DMS-supplemented escape curation. Because 9/12 pathogens are evidence-homogeneous by tag type and roughly 8/11 Stage 2 winners can be predicted from curation philosophy alone, a large share of the scoring x pathogen interaction likely reflects protocol-dependence.

Quantitative estimate: I would attribute about 55-65% of the reported omega-squared interaction to curation-protocol-dependence rather than pathogen biology alone, with a point estimate of 60%. That does not make the result invalid; it changes the claim. The safer interpretation is "Layer-A operational hotspot definitions are pathogen/protocol dependent, and scoring methods track those operational definitions" rather than "pathogen biology alone determines the optimal information source."

RESULT_CURATION_AGENT1: region_based=8/12 position_based=4/12 single_paper=2/12 evidence_homogeneous=9/12 expected_protocol_omega_share=60.0%
