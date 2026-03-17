#!/usr/bin/env python3
"""
Comprehensive dissertation verification script.

Performs 7 categories of checks on the MutBench dissertation:
  1. Forbidden pattern scan
  2. Key statistics consistency
  3. CSV data vs table verification
  4. LaTeX structure integrity
  5. Scoring formula vs code verification
  6. Permutation test formula check
  7. MOSD/MutClust weight analysis

Usage:
    python3 verify_dissertation.py
"""

import os
import re
import csv
import sys
from pathlib import Path
from collections import defaultdict

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

SCRIPT_DIR = Path(__file__).resolve().parent
CHAPTERS_DIR = SCRIPT_DIR / "chapters"
CHAPTERS_EN_DIR = SCRIPT_DIR / "chapters_en"
FRONT_DIR = SCRIPT_DIR / "front"
BACK_DIR = SCRIPT_DIR / "back"
FRONT_EN_DIR = SCRIPT_DIR / "front_en"
BIB_FILE = SCRIPT_DIR / "references.bib"
RESULTS_DIR = SCRIPT_DIR.parent.parent / "results" / "mutbench"
SCRIPTS_DIR = SCRIPT_DIR.parent.parent / "scripts"
TOOLS_DIR = SCRIPT_DIR.parent.parent / "tools"

BENCHMARK_SCRIPT = SCRIPTS_DIR / "run_extended_benchmark.py"
METRICS_SCRIPT = TOOLS_DIR / "mutbench" / "evaluation" / "metrics.py"

# Counters
PASS_COUNT = 0
FAIL_COUNT = 0
WARN_COUNT = 0


def log_pass(msg):
    global PASS_COUNT
    PASS_COUNT += 1
    print(f"  [PASS] {msg}")


def log_fail(msg):
    global FAIL_COUNT
    FAIL_COUNT += 1
    print(f"  [FAIL] {msg}")


def log_warn(msg):
    global WARN_COUNT
    WARN_COUNT += 1
    print(f"  [WARN] {msg}")


def gather_tex_files():
    """Collect all .tex files from chapters/, front/, back/, front_en/, chapters_en/."""
    tex_files = []
    for d in [CHAPTERS_DIR, CHAPTERS_EN_DIR, FRONT_DIR, BACK_DIR, FRONT_EN_DIR]:
        if d.exists():
            for f in sorted(d.glob("*.tex")):
                tex_files.append(f)
    return tex_files


def read_file_lines(path):
    """Read file lines, returning empty list if file not found."""
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            return f.readlines()
    except FileNotFoundError:
        return []


def read_file_text(path):
    """Read entire file as text."""
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            return f.read()
    except FileNotFoundError:
        return ""


# ===================================================================
# CHECK 1: Forbidden Pattern Scan
# ===================================================================

def check1_forbidden_patterns():
    print("\n" + "=" * 70)
    print("CHECK 1: Forbidden Pattern Scan")
    print("=" * 70)

    tex_files = gather_tex_files()
    if not tex_files:
        log_fail("No .tex files found")
        return

    forbidden_patterns = [
        (r"세\s*연구|세\s*가지\s*연구|세\s*가지\s*기여", "Three studies (Korean)"),
        (r"three\s+studies|three\s+interconnected|three\s+research", "Three studies (English)"),
        (r"First.*Second.*Third", "First/Second/Third listing (check context)"),
        (r"starr2020deep", "Removed duplicate citation key"),
        (r"근영", "Should be '0에 가까운 값'"),
        (r"MOSD.*를\s*통해.*MutClust.*를\s*통해.*MutBench.*를\s*통해",
         "MOSD/MutClust/MutBench parallel listing"),
    ]

    for pattern_str, desc in forbidden_patterns:
        found_any = False
        pat = re.compile(pattern_str, re.IGNORECASE if "three" in pattern_str.lower() or "First" in pattern_str else 0)
        for tf in tex_files:
            lines = read_file_lines(tf)
            for i, line in enumerate(lines, 1):
                if pat.search(line):
                    log_fail(f"'{desc}' found in {tf.name}:{i}: {line.strip()[:100]}")
                    found_any = True
        if not found_any:
            log_pass(f"No '{desc}' found in any .tex file")

    # MOSD/MutClust count in ch1
    print()
    ch1_files = []
    for d in [CHAPTERS_DIR, CHAPTERS_EN_DIR]:
        p = d / "ch1_introduction.tex"
        if p.exists():
            ch1_files.append(p)

    for ch1 in ch1_files:
        lines = read_file_lines(ch1)
        mosd_count = sum(1 for line in lines if "MOSD" in line)
        mutclust_count = sum(1 for line in lines if "MutClust" in line)
        if mosd_count > 5:
            log_fail(f"{ch1.name}: MOSD appears {mosd_count} times (> 5 limit)")
        else:
            log_pass(f"{ch1.name}: MOSD appears {mosd_count} times (<= 5)")
        if mutclust_count > 5:
            log_fail(f"{ch1.name}: MutClust appears {mutclust_count} times (> 5 limit)")
        else:
            log_pass(f"{ch1.name}: MutClust appears {mutclust_count} times (<= 5)")


# ===================================================================
# CHECK 2: Key Statistics Consistency
# ===================================================================

def check2_statistics_consistency():
    print("\n" + "=" * 70)
    print("CHECK 2: Key Statistics Consistency")
    print("=" * 70)

    tex_files = gather_tex_files()

    # Helper: find all occurrences of a pattern in all tex files
    def find_all_occurrences(pattern, description, flags=0):
        pat = re.compile(pattern, flags)
        results = []
        for tf in tex_files:
            lines = read_file_lines(tf)
            for i, line in enumerate(lines, 1):
                m = pat.search(line)
                if m:
                    results.append((tf.name, i, m.group(0), line.strip()[:120]))
        return results

    # --- omega^2 / eta^2 for family x pathogen interaction ---
    print("\n  --- omega^2 / eta^2 values ---")
    eta_patterns = [
        r"\\omega\^?\{?2\}?\s*[=≈]\s*([0-9.]+)",
        r"omega\^?\{?2\}?\s*[=≈]\s*([0-9.]+)",
        r"\\eta\^?\{?2\}?\s*[=≈]\s*([0-9.]+)",
        r"eta\^?\{?2\}?\s*[=≈]\s*([0-9.]+)",
        r"η²?\s*[=≈]\s*([0-9.]+)",
        r"ω²?\s*[=≈]\s*([0-9.]+)",
        r"0\.285",  # direct value
        r"0\.31",   # old value from memory
    ]
    found_eta = []
    seen_eta = set()
    for pat_str in eta_patterns:
        occs = find_all_occurrences(pat_str, "eta/omega squared")
        for file, line, match, ctx in occs:
            key = (file, line)
            if key not in seen_eta:
                seen_eta.add(key)
                found_eta.append((file, line, match, ctx))
    if found_eta:
        for file, line, match, ctx in found_eta:
            print(f"    Found in {file}:{line}: {ctx[:100]}")
    else:
        log_warn("No omega^2 or eta^2 values found in .tex files")

    # --- Friedman chi-squared ---
    print("\n  --- Friedman chi-squared ---")
    friedman_occs = find_all_occurrences(r"(?:chi|\\chi)\^?\{?2\}?\s*[=≈]\s*([0-9.]+)", "Friedman chi2")
    friedman_occs += find_all_occurrences(r"603\.81|42\.44", "Friedman chi2 value")
    if friedman_occs:
        for file, line, match, ctx in friedman_occs:
            if "42.44" in match:
                log_pass(f"Friedman chi2=42.44 found in {file}:{line}")
            elif "603.81" in match:
                log_warn(f"Old Friedman chi2=603.81 found in {file}:{line} - verify if this is the right test")
            else:
                print(f"    Friedman-related in {file}:{line}: {ctx[:100]}")
    else:
        log_warn("No Friedman chi-squared values found")

    # --- Friedman p-value ---
    print("\n  --- Friedman p-value ---")
    friedman_p_occs = find_all_occurrences(r"0\.0015|0\.987|p\s*[=<]\s*0\.00[0-9]+", "Friedman p-value")
    if friedman_p_occs:
        for file, line, match, ctx in friedman_p_occs:
            if "0.987" in match:
                log_fail(f"Friedman p=0.987 (old value) found in {file}:{line}: {ctx[:80]}")
            elif "0.0015" in match:
                log_pass(f"Friedman p=0.0015 found in {file}:{line}")
            else:
                print(f"    p-value in {file}:{line}: {ctx[:100]}")
    else:
        log_warn("No Friedman p-values found")

    # --- LOPO match rate ---
    print("\n  --- LOPO match rate ---")
    lopo_occs = find_all_occurrences(r"0/9|0\s*/\s*9|0에서\s*9|일치율.*0", "LOPO 0/9")
    if lopo_occs:
        for file, line, match, ctx in lopo_occs:
            print(f"    LOPO ref in {file}:{line}: {ctx[:100]}")
    else:
        log_warn("No LOPO 0/9 match rate found")

    # --- Total evaluations ---
    print("\n  --- Total evaluations (3,321 and 2,544) ---")
    eval_3321 = find_all_occurrences(r"3[,.]?321", "3321 evaluations")
    eval_2544 = find_all_occurrences(r"2[,.]?544", "2544 evaluations")
    if eval_3321:
        log_pass(f"3,321 evaluations found {len(eval_3321)} time(s)")
        for file, line, match, ctx in eval_3321:
            print(f"      {file}:{line}: {ctx[:100]}")
    else:
        log_fail("3,321 evaluations not found")
    if eval_2544:
        log_pass(f"2,544 evaluations found {len(eval_2544)} time(s)")
        for file, line, match, ctx in eval_2544:
            print(f"      {file}:{line}: {ctx[:100]}")
    else:
        log_warn("2,544 evaluations not found (may not be used)")
    # Check arithmetic: 3321 - 2544 = 777
    if eval_3321 and eval_2544:
        diff_occs = find_all_occurrences(r"777", "3321-2544=777")
        if diff_occs:
            log_pass("Difference 777 (3321-2544) found in text")
        else:
            log_warn("3321-2544=777 not explicitly mentioned (may be OK)")

    # --- hotspot-score best value ---
    print("\n  --- hotspot-score best value (0.778) ---")
    hs_occs = find_all_occurrences(r"0\.778", "hotspot-score 0.778")
    if hs_occs:
        for file, line, match, ctx in hs_occs:
            log_pass(f"hotspot-score 0.778 found in {file}:{line}")
    else:
        log_warn("hotspot-score 0.778 not found")

    # --- Oracle MCC ---
    print("\n  --- Oracle MCC (0.298) ---")
    oracle_occs = find_all_occurrences(r"0\.298", "Oracle MCC 0.298")
    if oracle_occs:
        for file, line, match, ctx in oracle_occs:
            log_pass(f"Oracle MCC 0.298 found in {file}:{line}")
    else:
        log_warn("Oracle MCC 0.298 not found")

    # --- Random baseline std ---
    print("\n  --- Random baseline std (0.002 vs 0.003) ---")
    rand_002 = find_all_occurrences(r"0\.002", "Random std 0.002")
    rand_003 = find_all_occurrences(r"0\.003", "Random std 0.003")
    # Filter to only those near "random" or "baseline" or "std"
    rand_002_ctx = [(f, l, m, c) for f, l, m, c in rand_002
                    if any(kw in c.lower() for kw in ["random", "baseline", "std", "표준편차"])]
    rand_003_ctx = [(f, l, m, c) for f, l, m, c in rand_003
                    if any(kw in c.lower() for kw in ["random", "baseline", "std", "표준편차"])]
    if rand_002_ctx and rand_003_ctx:
        log_fail("Both 0.002 and 0.003 found for random baseline std — inconsistency!")
        for f, l, m, c in rand_002_ctx:
            print(f"      0.002 in {f}:{l}: {c[:100]}")
        for f, l, m, c in rand_003_ctx:
            print(f"      0.003 in {f}:{l}: {c[:100]}")
    elif rand_002_ctx:
        log_pass("Random baseline std consistently 0.002")
    elif rand_003_ctx:
        log_pass("Random baseline std consistently 0.003")
    else:
        # Just report all occurrences
        if rand_002 or rand_003:
            log_warn("Found 0.002/0.003 but not in random baseline context")
        else:
            log_warn("No random baseline std value found")

    # --- H-score founder bias rho ---
    print("\n  --- H-score founder bias rho (-0.876) ---")
    rho_occs = find_all_occurrences(r"-?0\.876", "rho -0.876")
    if rho_occs:
        for file, line, match, ctx in rho_occs:
            log_pass(f"rho -0.876 found in {file}:{line}")
    else:
        log_warn("rho -0.876 not found")

    # --- Enrichment ratio 5.94 vs correct 5.918 ---
    print("\n  --- Enrichment ratio 5.94 (verify: 5.80/0.98 = 5.918) ---")
    er_594 = find_all_occurrences(r"5\.94", "enrichment 5.94")
    er_591 = find_all_occurrences(r"5\.91[0-9]*", "enrichment ~5.918")
    if er_594:
        log_warn(f"Enrichment 5.94 found (note: 5.80/0.98 = {5.80/0.98:.3f}, so 5.94 may be inaccurate)")
        for f, l, m, c in er_594:
            print(f"      {f}:{l}: {c[:100]}")
    if er_591:
        for f, l, m, c in er_591:
            print(f"      ~5.918 in {f}:{l}: {c[:100]}")
    if not er_594 and not er_591:
        log_warn("No enrichment ratio 5.94 or 5.918 found")


# ===================================================================
# CHECK 3: CSV Data vs Table Verification
# ===================================================================

def check3_csv_vs_tables():
    print("\n" + "=" * 70)
    print("CHECK 3: CSV Data vs Table Verification")
    print("=" * 70)

    # (a) extended_9pathogen_results.csv row count
    print("\n  --- (a) extended_9pathogen_results.csv row count ---")
    ext_csv = RESULTS_DIR / "extended_9pathogen_results.csv"
    if ext_csv.exists():
        with open(ext_csv, "r") as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = list(reader)
        n_rows = len(rows)
        if n_rows == 3321:
            log_pass(f"extended_9pathogen_results.csv has {n_rows} data rows (expected 3,321)")
        else:
            log_fail(f"extended_9pathogen_results.csv has {n_rows} data rows (expected 3,321)")
    else:
        log_fail(f"File not found: {ext_csv}")

    # (b) multilayer_9pathogen_results.csv or anova row count
    print("\n  --- (b) multilayer/ANOVA n=2,544 ---")
    multi_csv = RESULTS_DIR / "multilayer_9pathogen_results.csv"
    if multi_csv.exists():
        with open(multi_csv, "r") as f:
            reader = csv.reader(f)
            header = next(reader)
            rows = list(reader)
        n_rows = len(rows)
        if n_rows == 2544:
            log_pass(f"multilayer_9pathogen_results.csv has {n_rows} data rows (expected 2,544)")
        else:
            log_fail(f"multilayer_9pathogen_results.csv has {n_rows} data rows (expected 2,544)")
    else:
        log_warn(f"multilayer_9pathogen_results.csv not found, checking anova_9pathogen.csv")
        anova_csv = RESULTS_DIR / "anova_9pathogen.csv"
        if anova_csv.exists():
            with open(anova_csv, "r") as f:
                reader = csv.reader(f)
                header = next(reader)
                rows = list(reader)
            # Check the 'n' column in combined row
            n_col_idx = header.index("n") if "n" in header else -1
            if n_col_idx >= 0:
                for row in rows:
                    if len(row) > n_col_idx and row[0] == "Combined":
                        n_val = int(row[n_col_idx])
                        if n_val == 3321:
                            log_pass(f"ANOVA Combined n={n_val}")
                        else:
                            log_warn(f"ANOVA Combined n={n_val} (expected 3321 or 2544)")
                # Check per-pathogen n
                for row in rows:
                    if len(row) > n_col_idx and row[0] != "Combined":
                        n_val = int(row[n_col_idx])
                        if n_val != 369:
                            log_warn(f"ANOVA {row[0]} n={n_val} (expected 369 per pathogen)")
            else:
                log_warn("No 'n' column in anova_9pathogen.csv")
        else:
            log_fail("Neither multilayer nor anova CSV found")

    # (c) Best combos per pathogen
    print("\n  --- (c) Best combos per pathogen from multilayer CSV ---")
    if multi_csv.exists():
        import csv as csv_mod
        with open(multi_csv, "r") as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        # Find best composite_score per pathogen
        best_combos = {}
        for row in rows:
            pathogen = row.get("pathogen", "")
            try:
                score_val = float(row.get("composite_score", 0))
            except (ValueError, TypeError):
                continue
            combo = f"{row.get('score', '')} + {row.get('detector', '')}"
            if pathogen not in best_combos or score_val > best_combos[pathogen][1]:
                best_combos[pathogen] = (combo, score_val)

        print("    Best combo per pathogen (from CSV):")
        unique_combos = set()
        for pathogen in sorted(best_combos.keys()):
            combo, score = best_combos[pathogen]
            print(f"      {pathogen}: {combo} (composite={score:.4f})")
            unique_combos.add(combo)
        n_unique = len(unique_combos)
        print(f"    Unique best combos: {n_unique}/9")
        if n_unique == 9:
            log_pass("All 9 pathogens have unique best combos (9/9)")
        else:
            log_warn(f"Only {n_unique}/9 unique best combos")

        # Try to compare with ch4 table
        ch4_path = CHAPTERS_DIR / "ch4_results.tex"
        if ch4_path.exists():
            ch4_text = read_file_text(ch4_path)
            missing_in_ch4 = []
            for pathogen in best_combos:
                if pathogen not in ch4_text:
                    missing_in_ch4.append(pathogen)
            if missing_in_ch4:
                log_warn(f"Pathogens not mentioned in ch4: {missing_in_ch4}")
            else:
                log_pass("All 9 pathogens mentioned in ch4_results.tex")
    else:
        log_warn("Cannot verify best combos without multilayer_9pathogen_results.csv")

    # (d) LOPO 0/9 match, generalization ratio
    print("\n  --- (d) LOPO verification ---")
    lopo_csv = RESULTS_DIR / "lopo_9pathogen_cv.csv"
    if lopo_csv.exists():
        with open(lopo_csv, "r") as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        n_match = sum(1 for r in rows if r.get("combo_match", "").strip().lower() in ["true", "1"])
        n_total = len(rows)
        if n_match == 0 and n_total == 9:
            log_pass(f"LOPO match rate: {n_match}/{n_total} (expected 0/9)")
        else:
            log_fail(f"LOPO match rate: {n_match}/{n_total} (expected 0/9)")

        # Generalization ratio
        gen_ratios = []
        for r in rows:
            try:
                gr = float(r.get("generalization_ratio", 0))
                gen_ratios.append(gr)
            except (ValueError, TypeError):
                pass
        if gen_ratios:
            mean_gr = sum(gen_ratios) / len(gen_ratios)
            print(f"    Mean generalization ratio: {mean_gr:.4f} ({mean_gr*100:.1f}%)")
            if abs(mean_gr - 0.049) < 0.01:
                log_pass(f"Generalization ratio ~4.9% (actual: {mean_gr*100:.1f}%)")
            else:
                log_warn(f"Generalization ratio {mean_gr*100:.1f}% (expected ~4.9%)")
    else:
        log_fail(f"File not found: {lopo_csv}")

    # (e) Arithmetic checks
    print("\n  --- (e) Arithmetic verification ---")
    # 3321 - 2544 = 777
    diff = 3321 - 2544
    if diff == 777:
        log_pass(f"3321 - 2544 = {diff} (correct)")
    else:
        log_fail(f"3321 - 2544 = {diff} (expected 777)")

    # 5.80 / 0.98 check
    ratio = 5.80 / 0.98
    print(f"    5.80 / 0.98 = {ratio:.4f}")
    if abs(ratio - 5.94) > 0.03:
        log_warn(f"5.80/0.98 = {ratio:.3f}, not 5.94 — if text claims 5.94, the arithmetic is inaccurate (actual ≈ {ratio:.2f})")
    else:
        log_pass(f"5.80/0.98 ≈ 5.94")

    # 9 * 41 * 9 = 3321
    product = 9 * 41 * 9
    if product == 3321:
        log_pass(f"9 scoring × 41 detectors × 9 pathogens = {product} (matches 3,321)")
    else:
        log_fail(f"9 × 41 × 9 = {product} (expected 3,321)")


# ===================================================================
# CHECK 4: LaTeX Structure Integrity
# ===================================================================

def check4_latex_structure():
    print("\n" + "=" * 70)
    print("CHECK 4: LaTeX Structure Integrity")
    print("=" * 70)

    tex_files = gather_tex_files()

    # (a) Labels and refs
    print("\n  --- (a) Label/Ref cross-reference ---")
    all_labels = set()
    all_refs = defaultdict(list)  # ref_key -> [(file, line)]

    label_pat = re.compile(r"\\label\{([^}]+)\}")
    ref_pat = re.compile(r"\\(?:ref|eqref|autoref|cref|Cref|pageref)\{([^}]+)\}")

    for tf in tex_files:
        lines = read_file_lines(tf)
        for i, line in enumerate(lines, 1):
            for m in label_pat.finditer(line):
                all_labels.add(m.group(1))
            for m in ref_pat.finditer(line):
                all_refs[m.group(1)].append((tf.name, i))

    # Also check main thesis.tex and thesis_en.tex for labels
    for main_tex in [SCRIPT_DIR / "thesis.tex", SCRIPT_DIR / "thesis_en.tex"]:
        if main_tex.exists():
            lines = read_file_lines(main_tex)
            for i, line in enumerate(lines, 1):
                for m in label_pat.finditer(line):
                    all_labels.add(m.group(1))
                for m in ref_pat.finditer(line):
                    all_refs[m.group(1)].append((main_tex.name, i))

    undefined_refs = {k: v for k, v in all_refs.items() if k not in all_labels}
    if undefined_refs:
        log_fail(f"{len(undefined_refs)} undefined \\ref{{}} found:")
        for ref_key, locations in sorted(undefined_refs.items()):
            locs_str = ", ".join(f"{f}:{l}" for f, l in locations[:3])
            print(f"      \\ref{{{ref_key}}} used in {locs_str}")
    else:
        log_pass(f"All {len(all_refs)} \\ref{{}} have matching \\label{{}}")

    print(f"    Total labels: {len(all_labels)}, Total unique refs: {len(all_refs)}")

    # (b) Citation keys vs bib
    print("\n  --- (b) Citation key verification ---")
    bib_keys = set()
    if BIB_FILE.exists():
        bib_text = read_file_text(BIB_FILE)
        bib_key_pat = re.compile(r"@\w+\{([^,\s]+),")
        for m in bib_key_pat.finditer(bib_text):
            bib_keys.add(m.group(1))
        print(f"    Bib entries found: {len(bib_keys)}")
    else:
        log_fail("references.bib not found")
        return

    cite_pat = re.compile(r"\\(?:cite|citep|citet|citeauthor|citeyear|parencite|textcite)\{([^}]+)\}")
    all_cite_keys = defaultdict(list)
    for tf in tex_files:
        lines = read_file_lines(tf)
        for i, line in enumerate(lines, 1):
            for m in cite_pat.finditer(line):
                # Multiple keys can be in one \cite{a,b,c}
                keys = [k.strip() for k in m.group(1).split(",")]
                for k in keys:
                    if k:
                        all_cite_keys[k].append((tf.name, i))

    undefined_cites = {k: v for k, v in all_cite_keys.items() if k not in bib_keys}
    if undefined_cites:
        log_fail(f"{len(undefined_cites)} citation key(s) not in references.bib:")
        for cite_key, locations in sorted(undefined_cites.items()):
            locs_str = ", ".join(f"{f}:{l}" for f, l in locations[:3])
            print(f"      \\cite{{{cite_key}}} used in {locs_str}")
    else:
        log_pass(f"All {len(all_cite_keys)} citation keys found in references.bib")

    # (c) Section hierarchy: flag subsubsection directly under section
    print("\n  --- (c) Section hierarchy ---")
    section_pat = re.compile(r"\\(chapter|section|subsection|subsubsection)\*?\{")
    hierarchy_issues = []

    for tf in tex_files:
        lines = read_file_lines(tf)
        last_level = None
        for i, line in enumerate(lines, 1):
            m = section_pat.search(line)
            if m:
                cmd = m.group(1)
                level_map = {"chapter": 0, "section": 1, "subsection": 2, "subsubsection": 3}
                level = level_map.get(cmd, -1)
                if last_level is not None and level - last_level > 1:
                    hierarchy_issues.append(
                        (tf.name, i, f"\\{cmd} follows \\{['chapter','section','subsection','subsubsection'][last_level]} (skipped level)")
                    )
                last_level = level

    if hierarchy_issues:
        for f, l, msg in hierarchy_issues:
            log_warn(f"Section hierarchy skip in {f}:{l}: {msg}")
    else:
        log_pass("No section hierarchy skips found")

    # (d) Count tables and figures per chapter
    print("\n  --- (d) Tables and figures per chapter ---")
    table_pat = re.compile(r"\\begin\{(?:table|longtable)\}")
    figure_pat = re.compile(r"\\begin\{figure\}")

    for tf in sorted(tex_files):
        if "ch" not in tf.name:
            continue
        text = read_file_text(tf)
        n_tables = len(table_pat.findall(text))
        n_figures = len(figure_pat.findall(text))
        print(f"    {tf.name}: {n_tables} tables, {n_figures} figures")


# ===================================================================
# CHECK 5: Scoring Formula vs Code Verification
# ===================================================================

def check5_scoring_vs_code():
    print("\n" + "=" * 70)
    print("CHECK 5: Scoring Formula vs Code Verification")
    print("=" * 70)

    # --- Read benchmark script ---
    print("\n  --- (a) Scoring formulas from code ---")
    if not BENCHMARK_SCRIPT.exists():
        log_fail(f"Benchmark script not found: {BENCHMARK_SCRIPT}")
        return

    bench_text = read_file_text(BENCHMARK_SCRIPT)

    # Extract score names from compute_scores function
    code_score_names = []
    score_pat = re.compile(r"scores\['([^']+)'\]")
    for m in score_pat.finditer(bench_text):
        name = m.group(1)
        if name not in code_score_names:
            code_score_names.append(name)
    print(f"    Code scoring formulas ({len(code_score_names)}): {code_score_names}")

    expected_scores = ['E*rare', 'P*E*rare', 'minority_E', 'P*minority_E',
                       'P*E', 'H-score', 'E_only', 'P*E^2', 'rank(P*E)']
    if set(code_score_names) == set(expected_scores):
        log_pass(f"All 9 scoring formulas present in code")
    else:
        missing = set(expected_scores) - set(code_score_names)
        extra = set(code_score_names) - set(expected_scores)
        if missing:
            log_fail(f"Missing from code: {missing}")
        if extra:
            log_warn(f"Extra in code: {extra}")

    # --- Extract detector families ---
    print("\n  --- (b) Detector families from code ---")
    # Count detectors in get_detectors()
    detector_section = bench_text[bench_text.find("def get_detectors"):]
    detector_lines = detector_section.split("\n")
    detector_instances = []
    family_names = set()

    # Parse get_detectors function
    in_func = False
    bracket_depth = 0
    for line in detector_lines:
        stripped = line.strip()
        if "def get_detectors" in stripped:
            in_func = True
            continue
        if in_func:
            if "return [" in stripped:
                bracket_depth = 1
                continue
            if bracket_depth > 0:
                bracket_depth += stripped.count("[") - stripped.count("]")
                # Look for detector instantiations (any class with parentheses)
                det_match = re.match(r"([A-Z]\w+)\s*\(", stripped)
                if det_match:
                    detector_instances.append(stripped.rstrip(",").strip())
                if bracket_depth <= 0:
                    break

    n_detectors = len(detector_instances)
    print(f"    Detectors in get_detectors(): {n_detectors}")

    # Extract family names from class definitions
    family_pat = re.compile(r'return\s+"([^"]+)"', re.MULTILINE)
    # Better: look for family property returns
    class_families = set()
    for m in re.finditer(r"class\s+(\w+)\(BaseDetector\)", bench_text):
        class_name = m.group(1)
    # Use the family properties
    for m in re.finditer(r'def family\(self\):\s*\n\s*return\s+"([^"]+)"', bench_text):
        class_families.add(m.group(1))
    # Also check single-quote returns
    for m in re.finditer(r"def family\(self\):\s*\n\s*return\s+'([^']+)'", bench_text):
        class_families.add(m.group(1))

    print(f"    Detector families ({len(class_families)}): {sorted(class_families)}")

    if n_detectors == 41:
        log_pass(f"Detector count = {n_detectors} (expected 41)")
    else:
        log_fail(f"Detector count = {n_detectors} (expected 41)")

    if len(class_families) == 15:
        log_pass(f"15 detector families found")
    else:
        log_warn(f"{len(class_families)} detector families found (expected 15)")

    # --- Check ch3 for matching names ---
    print("\n  --- (c) Verify ch3_methods.tex matches code ---")
    ch3_files = []
    for d in [CHAPTERS_DIR, CHAPTERS_EN_DIR]:
        p = d / "ch3_methods.tex"
        if p.exists():
            ch3_files.append(p)

    for ch3 in ch3_files:
        ch3_text = read_file_text(ch3)

        # Check scoring names
        missing_scores = []
        for s in expected_scores:
            # Escape special chars for searching in LaTeX
            search_name = s.replace("*", r"\*").replace("^", r"\^")
            # Also try LaTeX-friendly versions
            variants = [s, s.replace("*", r"$\times$"), s.replace("*", r"\cdot"),
                        s.replace("^", r"\textasciicircum")]
            found = any(v in ch3_text for v in variants)
            # Also check without special chars
            if not found:
                simple = s.replace("*", "").replace("^", "").replace("(", "").replace(")", "")
                found = simple in ch3_text or s in ch3_text
            if not found:
                missing_scores.append(s)

        if missing_scores:
            log_warn(f"{ch3.name}: Scoring formulas not found in text: {missing_scores}")
        else:
            log_pass(f"{ch3.name}: All 9 scoring formulas referenced")

        # Check detector families
        missing_families = []
        for fam in sorted(class_families):
            if fam not in ch3_text:
                missing_families.append(fam)
        if missing_families:
            log_warn(f"{ch3.name}: Detector families not found: {missing_families}")
        else:
            log_pass(f"{ch3.name}: All {len(class_families)} detector families referenced")

        # Check detector count
        if "41" in ch3_text:
            log_pass(f"{ch3.name}: Detector count 41 mentioned")
        else:
            log_warn(f"{ch3.name}: Detector count 41 not found")

    # --- minority_E formula check ---
    print("\n  --- (d) minority_E formula description ---")
    # In code: minority_E = minority_freq * E, where minority = second most common allele freq
    for ch3 in ch3_files:
        ch3_text = read_file_text(ch3)
        if "minority" in ch3_text.lower():
            # Check for correct description
            if any(phrase in ch3_text for phrase in ["second most common", "두 번째로 빈번한",
                                                      "f_{2nd}", "f_2", "second-most"]):
                log_pass(f"{ch3.name}: minority_E correctly described as second most common allele")
            elif "1-f_max" in ch3_text or "1 - f_{max}" in ch3_text:
                log_fail(f"{ch3.name}: minority_E described as 1-f_max (should be second most common allele freq)")
            else:
                log_warn(f"{ch3.name}: minority_E mentioned but description unclear")
        else:
            log_warn(f"{ch3.name}: No mention of minority_E")


# ===================================================================
# CHECK 6: Permutation Test Formula Check
# ===================================================================

def check6_permutation_formula():
    print("\n" + "=" * 70)
    print("CHECK 6: Permutation Test Formula Check")
    print("=" * 70)

    # Read metrics.py for permutation p-value
    if not METRICS_SCRIPT.exists():
        log_fail(f"Metrics script not found: {METRICS_SCRIPT}")
        return

    metrics_text = read_file_text(METRICS_SCRIPT)

    # Find p-value computation in circular_permutation_test
    # Expected: p_value = float(np.mean(null_values >= observed))  i.e., count/n
    if "np.mean(null_values >= observed)" in metrics_text:
        code_formula = "count/n (np.mean of boolean)"
        log_pass(f"Code p-value formula: {code_formula}")
    elif "(count + 1)" in metrics_text or "(count+1)" in metrics_text:
        code_formula = "(count+1)/(n+1)"
        log_warn(f"Code uses conservative p-value formula: {code_formula}")
    else:
        code_formula = "unknown"
        log_warn(f"Could not determine p-value formula from code")

    # Check ch3 for the formula description
    ch3_files = []
    for d in [CHAPTERS_DIR, CHAPTERS_EN_DIR]:
        p = d / "ch3_methods.tex"
        if p.exists():
            ch3_files.append(p)

    for ch3 in ch3_files:
        ch3_text = read_file_text(ch3)
        ch3_lines = read_file_lines(ch3)

        # Search for permutation p-value formula
        found_pval_formula = False
        for i, line in enumerate(ch3_lines, 1):
            if "p" in line.lower() and ("permut" in line.lower() or "null" in line.lower()):
                # Check nearby lines for formula
                context = "".join(ch3_lines[max(0, i - 3):min(len(ch3_lines), i + 3)])
                if "count" in context.lower() or "frac" in context.lower() or "n_perm" in context.lower():
                    found_pval_formula = True
                    # Check if it's count/n or (count+1)/(n+1)
                    if "+1" in context:
                        tex_formula = "(count+1)/(n+1)"
                        if code_formula == "count/n (np.mean of boolean)":
                            log_fail(f"{ch3.name}: p-value formula is {tex_formula} but code uses count/n")
                        else:
                            log_pass(f"{ch3.name}: p-value formula matches code ({tex_formula})")
                    else:
                        tex_formula = "count/n"
                        if "count/n" in code_formula:
                            log_pass(f"{ch3.name}: p-value formula matches code (count/n)")

        if not found_pval_formula:
            # Look for any frac patterns with permutation context
            perm_sections = re.findall(r"(?:permutation|순열|원형).*?(?:\n.*?){0,10}", ch3_text, re.IGNORECASE)
            if perm_sections:
                log_warn(f"{ch3.name}: Permutation section found but p-value formula not clearly identified")
            else:
                log_warn(f"{ch3.name}: No permutation test formula section found")


# ===================================================================
# CHECK 7: MOSD/MutClust Weight Analysis
# ===================================================================

def check7_mosd_mutclust_weight():
    print("\n" + "=" * 70)
    print("CHECK 7: MOSD/MutClust Weight Analysis")
    print("=" * 70)

    chapter_dirs = [CHAPTERS_DIR, CHAPTERS_EN_DIR]
    chapter_files = []
    for d in chapter_dirs:
        if d.exists():
            for f in sorted(d.glob("ch*.tex")):
                chapter_files.append(f)

    for cf in chapter_files:
        lines = read_file_lines(cf)
        total_lines = len(lines)
        mosd_lines = sum(1 for line in lines if "MOSD" in line)
        mutclust_lines = sum(1 for line in lines if "MutClust" in line)
        either_lines = sum(1 for line in lines if "MOSD" in line or "MutClust" in line)
        pct = (either_lines / total_lines * 100) if total_lines > 0 else 0

        print(f"\n    {cf.name} ({total_lines} lines):")
        print(f"      MOSD: {mosd_lines} lines")
        print(f"      MutClust: {mutclust_lines} lines")
        print(f"      Either: {either_lines} lines ({pct:.1f}%)")

        # Flag if > 15% (except ch2 which is background)
        is_background = "ch2" in cf.name
        if pct > 15 and not is_background:
            log_fail(f"{cf.name}: MOSD/MutClust mentions = {pct:.1f}% of lines (> 15% threshold)")
        elif pct > 15 and is_background:
            log_warn(f"{cf.name} (background chapter): MOSD/MutClust mentions = {pct:.1f}% — OK for background")
        else:
            log_pass(f"{cf.name}: MOSD/MutClust mentions = {pct:.1f}% (<= 15%)")


# ===================================================================
# Main
# ===================================================================

def main():
    global PASS_COUNT, FAIL_COUNT, WARN_COUNT

    print("=" * 70)
    print("DISSERTATION VERIFICATION SCRIPT")
    print(f"Base directory: {SCRIPT_DIR}")
    print("=" * 70)

    # Verify base directory exists
    if not SCRIPT_DIR.exists():
        print("[FATAL] Dissertation directory not found!")
        sys.exit(1)

    check1_forbidden_patterns()
    check2_statistics_consistency()
    check3_csv_vs_tables()
    check4_latex_structure()
    check5_scoring_vs_code()
    check6_permutation_formula()
    check7_mosd_mutclust_weight()

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    total = PASS_COUNT + FAIL_COUNT + WARN_COUNT
    print(f"  [PASS] {PASS_COUNT}")
    print(f"  [FAIL] {FAIL_COUNT}")
    print(f"  [WARN] {WARN_COUNT}")
    print(f"  Total checks: {total}")
    print("=" * 70)

    if FAIL_COUNT > 0:
        print(f"\n  {FAIL_COUNT} FAILURE(s) detected — review required.")
    else:
        print("\n  No failures detected.")

    return FAIL_COUNT


if __name__ == "__main__":
    sys.exit(main())
