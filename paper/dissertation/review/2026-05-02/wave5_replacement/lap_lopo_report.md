# Layer A' LOPO Sensitivity Benchmark

## Headline numbers

The 10-target Layer A' LOPO benchmark gives mean MCC=-0.055, median MCC=-0.057, SD=0.068, with 2/10 positive folds. Precision@20 averages 0.005. The predeclared interpretation is **Branch C**: Layer A' label provenance does not preserve the signal - supports keeping 12-panel as primary and not extending.

Sign stability under 1000 target-level bootstrap resamples preserves the full-sample sign at: freq=1.000, entropy=1.000.

## Per-target results

| heldout_target                       | prevalence | mcc_top10 | precision_at_20 | top_bottom_decile_delta |
| ------------------------------------ | ---------- | --------- | --------------- | ----------------------- |
| lassa_gpc                            | 2.0%       | 0.047     | 0.050           | 0.040                   |
| measles_virus_h                      | 14.5%      | -0.137    | 0.000           | -0.081                  |
| mumps_virus_hn                       | 2.4%       | -0.053    | 0.000           | -0.017                  |
| hcov-229e_spike                      | 13.4%      | -0.131    | 0.000           | -0.102                  |
| hcov-nl63_spike                      | 11.6%      | -0.121    | 0.000           | -0.074                  |
| yfv_e                                | 2.8%       | -0.057    | 0.000           | 0.000                   |
| wnv_e                                | 2.8%       | -0.057    | 0.000           | 0.000                   |
| japanese_encephalitis_virus_e        | 2.8%       | 0.064     | 0.000           | 0.000                   |
| tick-borne_encephalitis_virus_e      | 2.8%       | -0.057    | 0.000           | 0.000                   |
| eastern_equine_encephalitis_virus_e2 | 2.4%       | -0.052    | 0.000           | 0.000                   |

## Cross-panel comparison

The Wave 4 labeled 12-target baseline is MCC mean=0.077, SD=0.136, with 8/12 positive folds. The Layer A' panel is MCC mean=-0.055, SD=0.068, with 2/10 positive folds. Because the panels differ in target identity and label provenance, paired Wilcoxon is not applicable. The unpaired Welch t-test is reported only as a descriptive cross-panel check: t=-2.961, two-sided p=0.00886.

## Caveats

The four flavivirus targets yfv_e, wnv_e, japanese_encephalitis_virus_e, and tick-borne_encephalitis_virus_e share the same 98-111 fusion-peptide annotation, so their labels are correlated and should not be read as four fully independent biological replications.

The panel is small (n=10), so fold-count thresholds are intentionally coarse and the uncertainty around the mean MCC remains material.

The Layer A' labels come from UniProt feature-derived annotations. Feature-density and annotation-practice bias can inflate or suppress apparent signal depending on which proteins have detailed curated records.

The comparison to Wave 4 is cross-provenance: Wave 4 used literature-curated Layer A labels on a 12-target panel, while Layer A' is UniProt-curated and uses different target identities. The benchmark tests sensitivity to label provenance, not a clean replacement experiment.

## Recommendation for chapter 5 framing

Frame Layer A' as a bounded sensitivity analysis rather than as the primary evidence layer. The prose should state that the Wave 4 12-panel remains the primary labeled benchmark, while Layer A' checks whether the directional 2-core signal survives a stricter structured-database provenance. Use the Branch C wording above as the main interpretive sentence, then immediately qualify it with the shared flavivirus annotation and provenance caveats.
