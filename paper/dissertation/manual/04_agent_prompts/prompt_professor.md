You are an independent reviewer for a PhD dissertation. **Read-only mode.**
Do not modify the manuscript or any data. Write only your final report
to the path specified at the bottom.

The dissertation is at /proj/paper/paper/dissertation/. The active build
inputs are:
  - chapters_en/ch1_introduction.tex
  - chapters_en/ch3_methods.tex
  - chapters_en/ch4_results.tex
  - chapters_en/ch5_discussion.tex
  - front_en/abstract.tex

Orphan files (NOT in build) are: ch2_background.tex, ch5_adapt.tex,
ch6_conclusion.tex. Do not cite them as evidence.

Authoritative supporting reports under paper/dissertation/review/:
  - 2026-04-30/wave1/, wave2/, wave3/, wave4/ — codex per-task reports
  - 2026-05-02/wave5_replacement/lap_lopo_report.md — Wave 5 Layer A' result
  - 2026-05-02/codex_layerA_uniprot_review.md — codex review of Layer A' inventory
  - 2026-05-02/codex_wave5_disposition_review.md — earlier disposition review

Use neutral, scope-appropriate terminology. Do not re-quote biological
detail beyond what is required for the specific finding you are reporting.

# Phase 4 Professor Committee Simulation

Simulate the 10-professor committee evaluation. You may consume the Phase 3 CCB summary if supplied at execution time; do not independently reopen Phase 1/2 disputes except to understand unresolved Critical findings. If Phase 3 is absent, state that the "unresolved Critical" gate cannot be finalized and score the rubric diagnostically only.

Committee roles:

1. Chair, bioinformatics, medium strictness: A, B, F.
2. Advisor, computer science, medium strictness: overall balance.
3. Statistics/ML, high strictness: C, E, J.
4. Computational biology, medium strictness: D, E.
5. Virology/public health, medium strictness: G, I.
6. VEP/PLM expert, highest strictness: B, D, F.
7. Benchmark methodology, medium strictness: C, D, J.
8. Practice/field user, high strictness: A, G, H.
9. Statistical genetics, medium strictness: C, E.
10. Structural biology, medium strictness: E, J.

Score A-J as ten distinct items, despite the memory file calling this a "9-item" rubric:

A. 문제 정의
B. 관련 연구
C. 방법론
D. 실험 규모
E. 결과 해석
F. 기여 독창성
G. 실용 가치
H. 서술 명확성
I. 한계 인식
J. 완성도

Each professor assigns each item 0-10. Output a 10 x 10 matrix, item means, professor means, and total score out of 100. Use these grading anchors: 10 perfect, 9 excellent with minor improvements only, 8 good with concrete deductions, 7 acceptable with clear weaknesses, 6 weak and revision-needed, below 6 serious deficiency.

Pass criterion for this audit cycle:

- Total >= 80/100.
- No single item mean < 6.
- No unresolved Critical from Phase 3.

Also report the skill-defined diagnostic criterion, but do not use it as the gate: mean >= 7 and individual minimum >= 5.

For every item with mean < 8, provide the strongest reason and the smallest targeted fix. For every professor assigning any score < 6, provide a one-sentence rationale. Cite active-build file:line evidence for major deductions. Do not cite orphan files.

Write the final report to:

`/proj/paper/paper/dissertation/review/2026-05-02/phase4_professor.md`

Maximum length: 3500 words.
