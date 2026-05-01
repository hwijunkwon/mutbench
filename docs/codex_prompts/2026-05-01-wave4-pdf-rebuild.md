# Codex task — Rebuild thesis_en.pdf and report

You are at `/proj/paper`.

## Task

Run `cd paper/dissertation && bash build.sh digital` (digital only — no print spine).
Stream the full xelatex output to `paper/dissertation/build_v206.log` and watch
for fatal errors.

## Pre-build baseline (already known)

- Latest committed version is v205. Wave 4 prose (just landed in the working tree
  by the previous codex task) is uncommitted and adds 3 insertions to
  `chapters_en/ch4_results.tex` and `chapters_en/ch5_discussion.tex`. A new
  `\label{para:w4_tier2_lopo}` is referenced from two ch5 paragraphs.
- Pre-Wave-4 PDF baseline: 232 pages, 0 errors, 0 undefined refs.

## Deliverable

After the build, print exactly:

```
=== W4 PDF REBUILD ===
build_status: <ok|fail>
errors_count: <n>          # grep -c "^! " build_v206.log
undefined_refs: <n>         # grep -c "Reference .* undefined" build_v206.log
multiply_defined: <n>       # grep -c "multiply defined" build_v206.log
warnings_count: <n>         # grep -c "Warning:" build_v206.log
page_count: <n>             # pdfinfo paper/dissertation/thesis_en.pdf | awk '/^Pages/{print $2}'
para_w4_resolves: <yes|no>  # grep para:w4_tier2_lopo paper/dissertation/thesis_en.aux must show \newlabel{para:w4_tier2_lopo}
log_path: paper/dissertation/build_v206.log
```

If `build_status == fail`, also print the first 30 lines of any `! LaTeX Error`
or `! Undefined control sequence` block from the log.

## Constraints

- Do not edit chapter files. The prose is already in place.
- Do not commit.
- Do not run the print build (`bash build.sh print` or `both`) — only the digital
  build is needed for verification.
- If xelatex is missing or the build dies on environment, report `build_status: fail`
  with the relevant log line and stop.
