# Risk-3 Deep Panel: Panel-Size Threshold Wording

Scope: `abstract.tex`, `ch1_introduction.tex`, `ch3_methods.tex`, `ch4_results.tex`, `ch5_discussion.tex`. Literal search terms: `20-30`, `20--30`, `Bolker`, `panel size`, `rule of thumb`, `20 to 30`, `twenty`, `Bolker minimum`.

No matches were found in `front_en/abstract.tex`.

## Canonical Wording

Use this phrase wherever adaptive-selection limitations are discussed:

> Adaptive method selection is not learnable at `n=11`, under the tested regime; a `20--30+` pathogen panel is a design target/rule-of-thumb for more stable estimation and validation, not a phase transition or sufficiency guarantee.

This satisfies the Risk-1 guardrails by pairing "not learnable" with "at `n=11`, under tested regime" and treating `20--30` as a design target rather than a guaranteed threshold.

## Occurrences and Recommendations

1. `ch1_introduction.tex:170`

Quote: "11 pathogen clusters places the design near the small-cluster regime---above the Bolker rule-of-thumb minimum of 5--6 but below the typical recommendation of 20--30 for stable random-effects estimation"

Classification: bound. It says the present `n=11` design is below a random-effects stability recommendation; it does not claim `20--30` suffices for adaptive selection.

Recommended edit: keep, but soften "typical recommendation" to "commonly cited rule-of-thumb target" if desired.

2. `ch3_methods.tex:135`

Quote: "Twenty scoring types organized into six categories"

Classification: bound/irrelevant. This is a count of scoring types, not panel-size threshold language.

Recommended edit: none.

3. `ch3_methods.tex:498`

Quote: "Twenty scoring types organized into six categories"

Classification: bound/irrelevant. This is a count of scoring types.

Recommended edit: none.

4. `ch3_methods.tex:503`

Quote: "Twenty scoring types used in the MutBench Stage~2 benchmark"

Classification: bound/irrelevant. This is a table caption count.

Recommended edit: none.

5. `ch4_results.tex:704`

Quote: "at $n = 11$ reference pathogens the 13-dimensional pathogen-profile space is severely undersampled"

Classification: bound. This appropriately binds the failure to the current `n=11` tested regime.

Recommended edit: keep.

6. `ch4_results.tex:704`

Quote: "adaptive gains are possible in principle but require $20$--$30$+ pathogens for reliable selection"

Classification: overstrong. "require" plus "for reliable selection" implies `20--30+` will be sufficient or is a formal operating threshold.

Recommended edit: replace with: "adaptive gains are possible in principle, but were not learnable at $n=11$ under the tested regime; a $20$--$30$+ pathogen panel is a design target for testing whether reliable selection emerges."

7. `ch4_results.tex:708`

Quote: "on the search-space-reduction task this Tier~1 recipe narrows ${\sim}1{,}000$ alignment positions to $20$--$80$"

Classification: bound/irrelevant. This is candidate-position budget, not pathogen panel size.

Recommended edit: none.

8. `ch4_results.tex:708`

Quote: "Validation of Tier 2 on held-out families is reserved as a Priority-3 deliverable contingent on the benchmark expanding beyond the current 11-pathogen Bolker-minimum panel"

Classification: bound but risky. It binds validation to expansion beyond `n=11`, but "Bolker-minimum panel" is imprecise and may sound like `n=11` already meets the `20--30` target.

Recommended edit: "Validation of Tier 2 on held-out families is reserved as a Priority-3 deliverable contingent on expansion beyond the current 11-pathogen small-panel regime."

9. `ch4_results.tex:752`

Quote: "does $n\approx30$ help?"

Classification: bound. The table frames `n≈30` as an empirical question, and the interpretation says "panel-size limit not relaxed".

Recommended edit: keep; optionally change to "does expansion toward $n\approx30$ help?" to avoid threshold framing.

10. `ch4_results.tex:755`

Quote: "constraint = panel size, not algorithm"

Classification: bound. It attributes the negative result to current panel size without promising that a specific expansion will solve it.

Recommended edit: add "`at n=11`" if space permits: "constraint = panel size at $n=11$, not algorithm".

11. `ch4_results.tex:890`

Quote: "the failure is most consistent with panel size"

Classification: bound. It ties the adaptive failure to `n=11` and says "most consistent", not proven.

Recommended edit: keep; optionally "the failure is most consistent with the $n=11$ panel-size limit".

12. `ch5_discussion.tex:218`

Quote: "$n = 11$ is below Bolker's $\geq$20--30 stable-random-effects regime"

Classification: bound. This is the safest form: `n=11` is below a rule-of-thumb stable random-effects regime.

Recommended edit: replace "regime" with "rule-of-thumb target" to avoid phase-transition wording.

13. `ch5_discussion.tex:218`

Quote: "expansion to 20--30+ pathogens is future work"

Classification: bound. This frames expansion as future work, not sufficiency.

Recommended edit: "expansion toward a 20--30+ pathogen design target is future work."

14. `ch5_discussion.tex:277`

Quote: "20--30+ pathogen validation"

Classification: bound. This is a future validation label.

Recommended edit: "20--30+ pathogen design-target validation."

15. `ch5_discussion.tex:284`

Quote: "a 20--30+ pathogen expansion with curated external labels, time-forward validation, and the same paired nested-LOPO/callability gates"

Classification: bound. It presents expansion as the next test and explicitly requires gates before deployment.

Recommended edit: "an expansion toward a 20--30+ pathogen design target..." for consistency.

16. `ch5_discussion.tex:312`

Quote: "11-pathogen panel below the Bolker $20$--$30$ threshold for stable random effects"

Classification: bound but risky. It does not claim adaptive sufficiency, but "threshold" suggests a phase transition.

Recommended edit: "11-pathogen panel below the Bolker $20$--$30$ rule-of-thumb target for stable random-effects estimation."

## Summary

Only one occurrence is substantively overstrong: `ch4_results.tex:704`, where `20--30+` is described as required "for reliable selection." The rest are acceptable if edited to avoid "threshold/regime/minimum" language where it might imply a formal phase transition.

RESULT_R3_DEEP_PANEL: occurrences=16 overstrong=1 canonical="not learnable at n=11, under the tested regime; 20--30+ is a design target/rule-of-thumb, not a phase transition"
