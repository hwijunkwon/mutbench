#!/usr/bin/env python3
"""Submission-readiness checks for the dissertation PDF and LaTeX sources."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DISS = ROOT / "paper" / "dissertation"
CHAPTERS = DISS / "chapters_en"
FIGURES = DISS / "figures"
LOG = DISS / "thesis_en.log"
DIGITAL = DISS / "thesis_digital.pdf"
PRINT = DISS / "thesis_print.pdf"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def tex_files() -> list[Path]:
    files = sorted(CHAPTERS.glob("*.tex"))
    files.extend([DISS / "thesis_en.tex", DISS / "front_en" / "abstract.tex", DISS / "front" / "abstract_kr.tex"])
    return [p for p in files if p.exists()]


def run(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)


def pdf_pages(path: Path) -> int | None:
    proc = run(["pdfinfo", str(path.relative_to(ROOT))])
    match = re.search(r"^Pages:\s+(\d+)", proc.stdout, re.M)
    return int(match.group(1)) if match else None


def audit_figures(text: str) -> tuple[bool, list[str]]:
    images = re.findall(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}", text)
    missing = []
    for image in images:
        candidates = [DISS / image, FIGURES / image]
        if not any(path.exists() for path in candidates):
            missing.append(image)
    messages = [
        f"includegraphics={len(images)}",
        f"unique_includegraphics={len(set(images))}",
        f"missing_includegraphics={len(missing)}",
    ]
    messages.extend(f"missing image: {name}" for name in missing)
    return not missing, messages


def audit_labels_and_floats(files: list[Path]) -> tuple[bool, list[str]]:
    labels: dict[str, Path] = {}
    duplicate_labels: list[str] = []
    refs: list[str] = []
    floats = 0
    captions = 0
    floats_without_label: list[str] = []

    for path in files:
        text = read_text(path)
        for match in re.finditer(r"\\label\{([^}]+)\}", text):
            label = match.group(1)
            if label in labels:
                duplicate_labels.append(f"{label} in {path.relative_to(ROOT)} and {labels[label].relative_to(ROOT)}")
            labels[label] = path
        refs.extend(re.findall(r"\\(?:ref|autoref|pageref)\{([^}]+)\}", text))

        for env in ("figure", "table"):
            pattern = re.compile(rf"\\begin\{{{env}\}}(.+?)\\end\{{{env}\}}", re.S)
            for match in pattern.finditer(text):
                floats += 1
                block = match.group(1)
                captions += len(re.findall(r"\\caption(?:\[[^\]]*\])?\{", block))
                if "\\label{" not in block:
                    line = text[: match.start()].count("\n") + 1
                    floats_without_label.append(f"{env} without label: {path.relative_to(ROOT)}:{line}")

    missing_refs = sorted(set(ref for ref in refs if ref not in labels))
    messages = [
        f"labels={len(labels)}",
        f"refs={len(refs)}",
        f"unique_refs={len(set(refs))}",
        f"missing_refs={len(missing_refs)}",
        f"duplicate_labels={len(duplicate_labels)}",
        f"floats={floats}",
        f"captions={captions}",
        f"floats_without_label={len(floats_without_label)}",
    ]
    messages.extend(f"missing ref: {ref}" for ref in missing_refs)
    messages.extend(f"duplicate label: {item}" for item in duplicate_labels)
    messages.extend(floats_without_label)
    return not missing_refs and not duplicate_labels and not floats_without_label, messages


def audit_log() -> tuple[bool, list[str]]:
    text = read_text(LOG)
    fatal_patterns = [
        "undefined references",
        "undefined citations",
        "Citation `",
        "Reference `",
        "There were undefined",
        "Rerun to get cross-references right",
    ]
    fatal_hits = [pattern for pattern in fatal_patterns if pattern in text]
    overfull = len(re.findall(r"Overfull \\hbox", text))
    underfull = len(re.findall(r"Underfull \\hbox", text))
    severe = []
    for match in re.finditer(r"Overfull \\hbox \(([0-9.]+)pt too wide\) in paragraph at lines ([0-9-]+)", text):
        width = float(match.group(1))
        if width >= 25:
            severe.append(f"{width:.2f}pt at source lines {match.group(2)}")
    messages = [
        f"fatal_reference_or_citation_hits={len(fatal_hits)}",
        f"overfull_hbox={overfull}",
        f"underfull_hbox={underfull}",
        f"severe_overfull_ge_25pt={len(severe)}",
    ]
    messages.extend(f"fatal log hit: {hit}" for hit in fatal_hits)
    messages.extend(f"severe overfull: {item}" for item in severe)
    return not fatal_hits, messages


def audit_pdf_text() -> tuple[bool, list[str]]:
    proc = run(["pdftotext", str(DIGITAL.relative_to(ROOT)), "-"])
    text = proc.stdout
    unresolved = len(re.findall(r"\?\?", text))
    return unresolved == 0, [f"pdf_text_unresolved_question_marks={unresolved}"]


def main() -> int:
    files = tex_files()
    text = "\n".join(read_text(path) for path in files)
    checks = [
        ("figures", *audit_figures(text)),
        ("labels_floats", *audit_labels_and_floats(files)),
        ("latex_log", *audit_log()),
        ("pdf_text", *audit_pdf_text()),
    ]

    digital_pages = pdf_pages(DIGITAL)
    print_pages = pdf_pages(PRINT)
    print(f"digital_pages={digital_pages}")
    print(f"print_pages={print_pages}")
    print(f"expected_print_extra_page={print_pages == digital_pages + 1}")

    ok = print_pages == digital_pages + 1
    for name, passed, messages in checks:
        status = "PASS" if passed else "FAIL"
        print(f"\n[{status}] {name}")
        for message in messages:
            print(f"  {message}")
        ok = ok and passed

    print(f"\noverall={'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
