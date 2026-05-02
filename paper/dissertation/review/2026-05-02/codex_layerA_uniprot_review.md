# Public-Database Layer A' Review

## Verdict

I recommend **R4 -- Hybrid**. Keep the 12-target literature-curated benchmark as the dissertation headline. Add any UniProt-derived expansion only as a separately labelled **public-database functional-annotation sensitivity panel (Layer A')**, after fixing the feature filter and the coordinate checks. The v2 output is useful as a triage inventory, but it is not yet label-equivalent to the original Layer A table.

The strongest reasons are:

- The v2 rule counts any `Region` as Layer A-relevant. That pulls in weak or non-positive annotations such as `Disordered`, `Mucin-like region`, full-domain `S1`/`S2`, `Stalk`, and `Head`.
- The alphavirus E2 targets are materially overcounted: `chain_label` is set to `Envelope protein E2`, but `chain_start` and `chain_end` are empty in the v2 inventory, so capsid, 6K, and E1 annotations remain in the E2 candidate set.
- The flavivirus position-score files do not match the UniProt mature-chain lengths exactly, and cleavage-site rows map to position 0 or beyond the chain boundary. These cannot be used as positive labels without a coordinate repair step.
- The original 12-target labels are denser and have different provenance: the local `layer_a_tags.csv` has 308 data rows across 12 targets, mean 25.7 positions/target, whereas the 16-target v2 UniProt inventory has 163 relevant rows, mean 10.2 rows/target before refinement.

## 1. Classification Audit

The current A/B/C classifier reproduces the stated v2 split: Class A=10, B=5, C=1. As a triage score, it is directionally useful. As an automatic label-construction rule, it is too permissive.

Spot-checked Class A targets:

- `lassa_gpc`: mostly defensible. It includes binding sites and fusion/cleavage annotations. Strong examples include (`lassa_gpc`, `Binding site`, 455, 455, empty description) and (`lassa_gpc`, `Site`, 33, 33, `Important for GP-C-mediated membrane fusion`). Cleavage rows such as (`lassa_gpc`, `Site`, 259, 260, `Cleavage; by host MBTPS1`) are biologically functional but weaker as positive labels for adaptive/immune relevance.
- `marburg_virus_gp`: mixed. (`marburg_virus_gp`, `Region`, 38, 188, `Receptor-binding`) and (`marburg_virus_gp`, `Region`, 529, 549, `Fusion peptide`) are good candidates. But (`marburg_virus_gp`, `Region`, 223, 427, `Disordered`) and (`marburg_virus_gp`, `Region`, 277, 455, `Mucin-like region`) should not count as positive labels by default.
- `measles_virus_h`: mostly defensible after dropping broad structural rows. (`measles_virus_h`, `Region`, 458, 543, `Interaction with host NECTIN4 receptor`) and the SLAMF1 receptor interaction sites, e.g. (`measles_virus_h`, `Site`, 483, 483, `Interaction with host SLAMF1 receptor`), are strong positives. (`measles_virus_h`, `Region`, 1, 154, `Stalk`) is structural and should be excluded.
- `mumps_virus_hn`: defensible. (`mumps_virus_hn`, `Active site`, 429, 429, `Nucleophile`), (`mumps_virus_hn`, `Active site`, 484, 484, `Proton donor`), and (`mumps_virus_hn`, `Site`, 553, 553, `Transition state stabilizer`) are exactly the kind of functional residues suitable for Layer A'.
- `chikungunya_virus_e2` and the equine encephalitis E2 targets are not clean Class A calls in v2. Their relevant rows include capsid functions and E1 features because the chain mapping did not resolve. Examples include (`chikungunya_virus_e2`, `Region`, 1, 104, `Disordered`), (`chikungunya_virus_e2`, `Active site`, 139, 139, `Charge relay system`), and (`chikungunya_virus_e2`, `Region`, 893, 910, `E1 fusion peptide loop`). These are not E2 mature-protein labels.

Spot-checked Class B targets:

- `yfv_e`: one strong row, two weak/boundary rows. (`yfv_e`, `Region`, 98, 111, `Fusion peptide loop`) is a strong positive. (`yfv_e`, `Site`, 0, 1, `Cleavage; by host signal peptidase`) is invalid in mature coordinates and should not be used. (`yfv_e`, `Site`, 493, 494, `Cleavage; by host signal peptidase`) crosses the UniProt E chain boundary.
- `nipah_virus_g`: should not be B under a functional-label criterion. (`nipah_virus_g`, `Region`, 96, 163, `Stalk`) and (`nipah_virus_g`, `Region`, 177, 602, `Head`) are broad structural domains, not positive position-level functional labels.

Recommendation: refine `Region` by description text. Exclude at least `Disordered`, `Mucin-like region`, `Stalk`, `Head`, bare `S1`, bare `S2`, broad heptad-repeat domains, transient transmembrane/signal-peptide regions, and full-domain bands. Keep `Region` rows only when the description names a specific functional interaction or mechanism, such as receptor binding, host receptor interaction, fusion peptide/fusion loop, viral RNA binding, ribosome binding, capsid interaction, or membrane fusion. Also exclude mature coordinates `<1` and rows that exceed the mature chain length unless a separate reference-length reconciliation justifies them.

## 2. Coordinate-Frame Check

The three flavivirus position-score files use 1-based mature-style indexing, but their ranges do not match the v2 UniProt chain lengths exactly.

| target | first positions in score file | score range | UniProt chain | chain length | flag |
|---|---:|---:|---:|---:|---|
| `yfv_e` | 1-5 | 1-499 | 286-778 | 493 | mismatch +6 |
| `wnv_e` | 1-5 | 1-501 | 291-787 | 497 | mismatch +4 |
| `japanese_encephalitis_virus_e` | 1-5 | 1-506 | 295-794 | 500 | mismatch +6 |

This is not a harmless display issue. The fusion-loop row maps consistently to 98-111 for all three targets, but the cleavage rows reveal a frame/boundary problem: YFV and WNV/JEV have N-terminal cleavage annotations mapped to 0-1, and C-terminal cleavage annotations extend to 494/498/501 while the UniProt mature chains are 493/497/500 aa. The score files likely come from alternative reference sequences or include residues outside the exact UniProt chain definition. Before labels are written, require a per-target sequence-length assertion and drop boundary cleavage rows from the positive set.

## 3. Comparability to the 12-Target Labels

The 12-target `layer_a_tags.csv` is not comparable to v2 UniProt rows as-is. The local file has 308 data rows, not 309 by my count, across 12 pathogens:

- HCV 54, Rabies 39, Zika 27, EV-A71 27, HIV-1 26, H3N2 25, SARS-CoV-2 25, Dengue 24, RSV 20, Influenza_B 17, Norovirus 15, MERS 9.
- Mean density: 25.7 labelled positions/target.
- New v2 UniProt density: 163 rows across 16 targets, mean 10.2 rows/target before filtering. After dropping structural-only regions and failed chain mappings, the effective density would fall further.

This argues against mixing the labels in a single benchmark fold as though they share provenance. The original panel labels are literature-curated immune/functional/convergent sites. The new labels are structured public-database functional annotations, with no guarantee that absence from UniProt means a true negative.

For the requested 12-target sanity check: the local feature matrices do not contain `accession` or `organism` fields, so I could not reproduce the exact UniProt query offline. Using standard offline accession knowledge, SARS-CoV-2 spike (`P0DTC2`) would almost certainly classify as A under the same broad UniProt-feature rule because it has many region, binding, cleavage, fusion, and motif annotations. Norovirus VP1 is less certain: VP1 has shell/P domains and receptor/antigenic-region annotations in public resources, but likely fewer precise residue-level UniProt features than SARS-CoV-2 spike. This asymmetry reinforces the main point: UniProt feature density is partly database-curation density, not just biological label density.

## 4. Dissertation Framing

The most defensible language is:

> We retained the 12-pathogen literature-curated Layer A benchmark as the primary evaluation set. Separately, we constructed a public-database functional-annotation sensitivity panel, denoted Layer A', from reviewed UniProtKB feature annotations. Layer A' labels were treated as distinct provenance rather than merged with literature-curated immune-relevance labels, because UniProt feature density reflects structured database curation and includes functional annotations that are not equivalent to adaptive or immune-escape evidence.

I would not call the new set simply an "extended panel" without an asterisk, because that implies label equivalence. I also would not reject it entirely: receptor-binding, active-site, fusion-peptide, and host-interaction annotations are useful sensitivity labels once the coordinate and description filters are fixed.

Suggested replacement for the current "pilot 3" future-work reference in `chapters_en/ch5_discussion.tex`:

> A next step is to evaluate a public-database functional-annotation sensitivity panel (Layer A') built from reviewed UniProtKB features for additional surface proteins. These labels should remain separate from the literature-curated Layer A benchmark: receptor-binding, catalytic, fusion, and host-interaction annotations provide useful structured positives, but broad structural domains, disordered regions, mucin-like regions, and chain-boundary cleavage annotations are not equivalent to curated immune-relevance evidence. The sensitivity panel would therefore test whether the ranking signal persists under a different label provenance, not replace the 12-pathogen benchmark.

## 5. Final Recommendation

**Pick R4 -- Hybrid.**

Do not adopt the full 12+10 Class-A extension yet. The 10 v2 Class A targets are `lassa_gpc`, `marburg_virus_gp`, `measles_virus_h`, `mumps_virus_hn`, `chikungunya_virus_e2`, `eastern_equine_encephalitis_virus_e2`, `venezuelan_equine_encephalitis_virus_e2`, `western_equine_encephalitis_virus_e2`, `hcov-229e_spike`, and `hcov-nl63_spike`; however, at least four of these are inflated by failed mature-chain mapping, and two coronavirus spikes are inflated by broad S1/S2/HR regions. The safer near-term Layer A' sensitivity subset is: `lassa_gpc`, `marburg_virus_gp`, `measles_virus_h`, `mumps_virus_hn`, `hcov-229e_spike`, and `hcov-nl63_spike`, with the coronavirus labels restricted to receptor-interaction/fusion/motif rows rather than whole S1/S2/HR bands. Add flaviviruses only after the length mismatch is reconciled; add alphavirus E2 only after chain remapping excludes capsid/6K/E1 rows.

## Next Steps

1. Write a Layer A' label-construction script that reads `layerA_alternative_sources_features_v2.csv`, not UniProt directly.
2. Add a description filter for `Region`: exclude `Disordered`, `Mucin-like region`, `Stalk`, `Head`, bare `S1`, bare `S2`, `Heptad repeat`, `Transient transmembrane`, and signal-peptide/propeptide bands.
3. Add coordinate guards: require `start_mature >= 1`, `end_mature <= mature_length`, and score-file maximum position equal to the accepted reference length or explicitly mapped by an accession-specific offset.
4. Fix alphavirus mature-chain mapping before using `chikungunya_virus_e2`, `eastern_equine_encephalitis_virus_e2`, `venezuelan_equine_encephalitis_virus_e2`, or `western_equine_encephalitis_virus_e2`.
5. Reclassify targets after filtering and report both raw v2 class and refined Layer A' class.
6. Run the 12-target benchmark as the primary result and the refined Layer A' targets as a separate sensitivity panel with separate tables.
7. Paste the Chapter 5 paragraph above into the future-work section, replacing the current pilot-3 language.
8. Remove any claim that the 16-target extension validates Layer A performance until the refined Layer A' panel has been evaluated separately.
