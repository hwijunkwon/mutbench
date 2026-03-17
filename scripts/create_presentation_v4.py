#!/usr/bin/env python3
"""
MutBench PhD Defense Presentation v4 — ALL ENGLISH, Redesigned
Output: /proj/paper/paper/ppt/MutBench_Defense_v4.pptx
"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn
import os

# ── paths ──────────────────────────────────────────────────────
BASE = "/proj/paper"
OUT = os.path.join(BASE, "paper/ppt/MutBench_Defense_v4.pptx")
LOGO = os.path.join(BASE, "docs/presentation/knu_symbol_white.png")
LOGO_EMBLEM = os.path.join(BASE, "docs/presentation/knu_emblem_official.jpg")
FIG_DISS = os.path.join(BASE, "paper/dissertation/figures")
FIG_MAIN = os.path.join(BASE, "paper/figure")

# ── colors ─────────────────────────────────────────────────────
DARK_NAVY  = RGBColor(0x1B, 0x2A, 0x4A)
WHITE      = RGBColor(0xFF, 0xFF, 0xFF)
BLACK      = RGBColor(0x00, 0x00, 0x00)
GRAY       = RGBColor(0x88, 0x88, 0x88)
DARK_GRAY  = RGBColor(0x33, 0x33, 0x33)
LIGHT_GRAY = RGBColor(0xF5, 0xF5, 0xF5)
MID_GRAY   = RGBColor(0xE0, 0xE0, 0xE0)
PH_GRAY    = RGBColor(0xF0, 0xF0, 0xF0)   # placeholder fill
PH_BORDER  = RGBColor(0x99, 0x99, 0x99)   # placeholder border

# section colors
SEC_INTRO   = RGBColor(0x1B, 0x2A, 0x4A)  # navy
SEC_FRAME   = RGBColor(0x0D, 0x73, 0x77)  # teal
SEC_STAGE1  = RGBColor(0x2E, 0x7D, 0x32)  # green
SEC_STAGE2  = RGBColor(0xE6, 0x51, 0x00)  # orange
SEC_EXT     = RGBColor(0x6A, 0x1B, 0x9A)  # purple
SEC_CONCL   = RGBColor(0xC6, 0x28, 0x28)  # red

TEAL_ACCENT = RGBColor(0x0D, 0x73, 0x77)
RED_ACCENT  = RGBColor(0xC6, 0x28, 0x28)
GREEN       = RGBColor(0x2E, 0x7D, 0x32)
ORANGE      = RGBColor(0xE6, 0x51, 0x00)
PURPLE      = RGBColor(0x6A, 0x1B, 0x9A)
BLUE        = RGBColor(0x15, 0x65, 0xC0)

SLIDE_W = Inches(13.330)
SLIDE_H = Inches(7.500)

# ── helpers ────────────────────────────────────────────────────

def make_prs():
    prs = Presentation()
    prs.slide_width = SLIDE_W
    prs.slide_height = SLIDE_H
    return prs

def add_blank(prs):
    layout = prs.slide_layouts[6]  # blank
    return prs.slides.add_slide(layout)

def add_rect(slide, l, t, w, h, fill=None, border=None):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, l, t, w, h)
    shape.line.fill.background()
    if fill:
        shape.fill.solid()
        shape.fill.fore_color.rgb = fill
    else:
        shape.fill.background()
    if border:
        shape.line.fill.solid()
        shape.line.color.rgb = border
        shape.line.width = Pt(1)
    return shape

def add_rounded_rect(slide, l, t, w, h, fill=None, border=None):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, l, t, w, h)
    shape.line.fill.background()
    if fill:
        shape.fill.solid()
        shape.fill.fore_color.rgb = fill
    else:
        shape.fill.background()
    if border:
        shape.line.fill.solid()
        shape.line.color.rgb = border
        shape.line.width = Pt(1)
    return shape

def set_text(shape, text, size=14, bold=False, color=BLACK, align=PP_ALIGN.LEFT,
             font_name="Calibri", anchor=MSO_ANCHOR.TOP):
    tf = shape.text_frame
    tf.word_wrap = True
    tf.auto_size = None
    try:
        tf.vertical_anchor = anchor
    except:
        pass
    for i, line in enumerate(text.split("\n")):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.text = line
        p.font.size = Pt(size)
        p.font.bold = bold
        p.font.color.rgb = color
        p.font.name = font_name
        p.alignment = align

def add_textbox(slide, l, t, w, h, text, size=14, bold=False, color=BLACK,
                align=PP_ALIGN.LEFT, font_name="Calibri", anchor=MSO_ANCHOR.TOP):
    txBox = slide.shapes.add_textbox(l, t, w, h)
    set_text(txBox, text, size, bold, color, align, font_name, anchor)
    return txBox

def add_multiformat_textbox(slide, l, t, w, h, runs, align=PP_ALIGN.LEFT):
    """runs: list of (text, size, bold, color) tuples"""
    txBox = slide.shapes.add_textbox(l, t, w, h)
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = align
    for text, size, bold, color in runs:
        run = p.add_run()
        run.text = text
        run.font.size = Pt(size)
        run.font.bold = bold
        run.font.color.rgb = color
        run.font.name = "Calibri"
    return txBox

def content_slide(prs, title, section_color):
    """Create standard content slide with top bar, title, logo, bottom bar, footer."""
    slide = add_blank(prs)
    # top bar
    add_rect(slide, Inches(0), Inches(0), SLIDE_W, Inches(0.900), fill=section_color)
    # title
    add_textbox(slide, Inches(0.600), Inches(0.180), Inches(10.500), Inches(0.550),
                title, size=24, bold=True, color=WHITE, anchor=MSO_ANCHOR.MIDDLE)
    # KNU logo top-right (red emblem only)
    if os.path.exists(LOGO_EMBLEM):
        slide.shapes.add_picture(LOGO_EMBLEM, Inches(12.230), Inches(0.150),
                                 Inches(0.550), Inches(0.550))
    # bottom bar
    add_rect(slide, Inches(0), Inches(7.120), SLIDE_W, Inches(0.380), fill=DARK_NAVY)
    # footer text
    add_textbox(slide, Inches(0.400), Inches(7.140), Inches(10.0), Inches(0.340),
                "Kyungpook National University  |  Dept. of Computer Science  |  Hwijun Kwon",
                size=10, color=WHITE, anchor=MSO_ANCHOR.MIDDLE)
    return slide

def add_page_number(slide, num):
    add_textbox(slide, Inches(11.800), Inches(7.140), Inches(1.400), Inches(0.340),
                f"\u2014\u2014 {num}", size=10, color=WHITE, align=PP_ALIGN.RIGHT,
                anchor=MSO_ANCHOR.MIDDLE)

def add_card(slide, l, t, w, h, fill=WHITE, border=MID_GRAY):
    return add_rounded_rect(slide, l, t, w, h, fill=fill, border=border)

def add_accent_bar(slide, l, t, w, h, color):
    return add_rect(slide, l, t, w, h, fill=color)

def add_figure(slide, path, l, t, w, h):
    if os.path.exists(path):
        slide.shapes.add_picture(path, l, t, w, h)
    else:
        add_placeholder(slide, l, t, w, h, f"[Missing: {os.path.basename(path)}]")

def add_placeholder(slide, l, t, w, h, text="[Image Placeholder]"):
    """Gray rounded rectangle with dashed-style border and placeholder text."""
    shape = add_rounded_rect(slide, l, t, w, h, fill=PH_GRAY, border=PH_BORDER)
    shape.line.width = Pt(2)
    # Add dashed line via XML
    try:
        ln = shape.line._ln
        ln.set(qn('prstDash'), 'dash')
    except:
        pass
    set_text(shape, text, size=11, color=GRAY, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    return shape


# ══════════════════════════════════════════════════════════════
# BUILD PRESENTATION
# ══════════════════════════════════════════════════════════════

prs = make_prs()
slide_num = 0

# ── SLIDE 1: Title ─────────────────────────────────────────────
slide_num += 1
s = add_blank(prs)
# dark top area
add_rect(s, Inches(0), Inches(0), SLIDE_W, Inches(3.400), fill=DARK_NAVY)
# KNU emblem (red logo only, one per slide)
if os.path.exists(LOGO_EMBLEM):
    s.shapes.add_picture(LOGO_EMBLEM, Inches(0.600), Inches(0.250), Inches(0.650), Inches(0.650))
# university name (no "PhD Dissertation Defense")
add_textbox(s, Inches(1.400), Inches(0.300), Inches(8.0), Inches(0.300),
            "Graduate School, Kyungpook National University", size=14, color=WHITE)
# title
add_textbox(s, Inches(0.600), Inches(1.400), Inches(12.0), Inches(1.600),
            "MutBench: Systematic Benchmarking Framework\nfor Viral Mutation Hotspot Detection",
            size=34, bold=True, color=WHITE)
# author info (below dark area)
add_textbox(s, Inches(0.600), Inches(3.800), Inches(11.0), Inches(0.400),
            "Hwijun Kwon  |  Advisor: Prof. Inuk Jung", size=18, bold=True, color=DARK_GRAY)
add_textbox(s, Inches(0.600), Inches(4.250), Inches(11.0), Inches(0.350),
            "Dept. of Computer Science, KNU  |  March 2026", size=14, color=GRAY)
# bottom bar
add_rect(s, Inches(0), Inches(7.120), SLIDE_W, Inches(0.380), fill=DARK_NAVY)


# ── SLIDE 2: Table of Contents — clean vertical list ─────────────
slide_num += 1
s = content_slide(prs, "Table of Contents", SEC_INTRO)
add_page_number(s, slide_num)

toc_items = [
    ("1", "Introduction", "Prior work, biology background, problem definition", "S3 \u2013 S9", SEC_INTRO),
    ("2", "MutBench Framework", "Pipeline, scoring/detection, 3-layer ground truth, MCC", "S10 \u2013 S15", SEC_FRAME),
    ("3", "Stage 1: 4-Pathogen", "Method comparison, sensitivity, synthetic vs real gap", "S16 \u2013 S19", SEC_STAGE1),
    ("4", "Stage 2: 9-Pathogen", "ANOVA, per-pathogen best, Friedman, LOPO, ESM-2", "S20 \u2013 S25", SEC_STAGE2),
    ("5", "Extensions & PAHD", "PAHD algorithm, phylogenetic correction, baselines", "S26 \u2013 S28", SEC_EXT),
    ("6", "Conclusion", "Contributions, discussion, limitations, future work", "S29 \u2013 S33", SEC_CONCL),
]
for i, (num, title, desc, slides, color) in enumerate(toc_items):
    cy = Inches(1.200) + i * Inches(0.950)
    # number badge
    badge = add_rounded_rect(s, Inches(1.200), cy + Inches(0.050), Inches(0.550), Inches(0.550),
                              fill=color)
    set_text(badge, num, size=18, bold=True, color=WHITE, align=PP_ALIGN.CENTER,
             anchor=MSO_ANCHOR.MIDDLE)
    # title
    add_textbox(s, Inches(2.000), cy + Inches(0.020), Inches(5.500), Inches(0.400),
                title, size=17, bold=True, color=DARK_NAVY)
    # description + slide range
    add_textbox(s, Inches(2.000), cy + Inches(0.430), Inches(8.000), Inches(0.350),
                f"{desc}    ({slides})", size=11, color=DARK_GRAY)


# ── SLIDE 3: Prior Work — paper cards with figures ──────────────
slide_num += 1
s = content_slide(prs, "Prior Work: MOSD & MutClust", SEC_INTRO)
add_page_number(s, slide_num)

# MOSD card with accent bar
c1 = add_card(s, Inches(0.600), Inches(1.200), Inches(5.800), Inches(5.400), border=MID_GRAY)
add_accent_bar(s, Inches(0.600), Inches(1.200), Inches(0.100), Inches(5.400), TEAL_ACCENT)
add_textbox(s, Inches(0.900), Inches(1.300), Inches(5.300), Inches(0.350),
            "Paper 1  |  BMC Genomics 2025 (SCIE)", size=14, bold=True, color=TEAL_ACCENT)
add_textbox(s, Inches(0.900), Inches(1.700), Inches(5.300), Inches(0.350),
            "MOSD: Multi-Omics Subtyping with Deep learning", size=12, bold=True, color=DARK_NAVY)
add_textbox(s, Inches(0.900), Inches(2.150), Inches(5.300), Inches(1.200),
            "  Benchmarked 11 multi-omics integration methods\n"
            "  across 6 evaluation metrics for cancer subtyping\n\n"
            "  Key finding: No single method dominates\n"
            "  across all cancer datasets", size=11, color=DARK_GRAY)
# MOSD figure from dissertation
add_figure(s, os.path.join(FIG_DISS, "hotspot_score_comparison.png"),
           Inches(1.000), Inches(3.500), Inches(4.800), Inches(3.000))

# MutClust card with accent bar
c2 = add_card(s, Inches(6.900), Inches(1.200), Inches(5.800), Inches(5.400), border=MID_GRAY)
add_accent_bar(s, Inches(6.900), Inches(1.200), Inches(0.100), Inches(5.400), RED_ACCENT)
add_textbox(s, Inches(7.200), Inches(1.300), Inches(5.300), Inches(0.350),
            "Paper 2  |  BioData Mining 2025 (SCIE)", size=14, bold=True, color=RED_ACCENT)
add_textbox(s, Inches(7.200), Inches(1.700), Inches(5.300), Inches(0.350),
            "MutClust: Mutation Clustering for viral evolution", size=12, bold=True, color=DARK_NAVY)
add_textbox(s, Inches(7.200), Inches(2.150), Inches(5.300), Inches(1.200),
            "  H-score based mutation hotspot detection\n"
            "  with network propagation & bootstrap\n\n"
            "  Limitation: H-score founder bias (rho = -0.876)\n"
            "  Single-pathogen evaluation is insufficient", size=11, color=DARK_GRAY)
# MutClust figure from dissertation
add_figure(s, os.path.join(FIG_DISS, "method_comparison.png"),
           Inches(7.300), Inches(3.500), Inches(4.800), Inches(3.000))


# ── SLIDE 4: Biology — Central Dogma ──────────────────────────
slide_num += 1
s = content_slide(prs, "The Central Dogma: DNA \u2192 RNA \u2192 Protein", SEC_INTRO)
add_page_number(s, slide_num)

# Top center: large placeholder for Central Dogma overview diagram
add_placeholder(s, Inches(3.000), Inches(1.100), Inches(7.300), Inches(2.400),
                "[Central Dogma overview diagram]\nDNA \u2192 Transcription \u2192 mRNA \u2192 Translation \u2192 Protein")

# Left: key terms with SMALL placeholder boxes next to each
add_textbox(s, Inches(0.600), Inches(1.200), Inches(2.200), Inches(0.400),
            "Key Terms", size=16, bold=True, color=DARK_NAVY)

terms = [
    ("Genome", "Complete genetic information,\nencoded as DNA or RNA.", "[DNA double helix image]"),
    ("Gene", "Segment encoding a functional\nprotein or RNA molecule.", "[Gene segment image]"),
    ("Nucleotide", "Building blocks: A, T/U, G, C.", "[Nucleotide structure image]"),
    ("Amino Acid", "Protein building blocks.\n3 nucleotides = 1 codon = 1 AA.", "[Amino acid image]"),
]
for i, (term, desc, ph_label) in enumerate(terms):
    cy = Inches(3.700) + i * Inches(0.900)
    # term card
    card = add_card(s, Inches(0.600), cy, Inches(5.200), Inches(0.800), border=MID_GRAY)
    add_textbox(s, Inches(0.800), cy + Inches(0.050), Inches(1.400), Inches(0.300),
                term, size=12, bold=True, color=SEC_FRAME)
    add_textbox(s, Inches(0.800), cy + Inches(0.350), Inches(3.800), Inches(0.400),
                desc, size=9, color=DARK_GRAY)
    # small placeholder next to each term
    add_placeholder(s, Inches(4.700), cy + Inches(0.050), Inches(1.000), Inches(0.700), ph_label)

# Right side: DNA, RNA, Protein individual placeholders
cd_items = [
    ("DNA", SEC_FRAME, "[DNA double helix image]"),
    ("mRNA", ORANGE, "[mRNA transcription image]"),
    ("Protein", PURPLE, "[Protein folding image]"),
]
for i, (label, clr, ph_label) in enumerate(cd_items):
    cx = Inches(6.200) + i * Inches(2.400)
    cy = Inches(3.700)
    box = add_rounded_rect(s, cx, cy, Inches(2.100), Inches(0.550), fill=clr)
    set_text(box, label, size=13, bold=True, color=WHITE, align=PP_ALIGN.CENTER,
             anchor=MSO_ANCHOR.MIDDLE)
    # small placeholder below each term
    add_placeholder(s, cx + Inches(0.100), cy + Inches(0.650), Inches(1.900), Inches(1.500), ph_label)
    if i < 2:
        add_textbox(s, cx + Inches(2.100), cy + Inches(0.050), Inches(0.300), Inches(0.450),
                    "\u2192", size=20, bold=True, color=GRAY, align=PP_ALIGN.CENTER)

# note at bottom
note = add_card(s, Inches(6.200), Inches(6.100), Inches(6.300), Inches(0.700),
                fill=RGBColor(0xFF, 0xF3, 0xE0), border=ORANGE)
set_text(note, "RNA viruses use RNA (not DNA) as their genome.\nHigher mutation rate due to error-prone RNA polymerase.",
         size=11, color=DARK_GRAY, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)


# ── SLIDE 5: Mutations & Their Effects ──────────────────────────
slide_num += 1
s = content_slide(prs, "Mutations & Their Effects", SEC_INTRO)
add_page_number(s, slide_num)

# Large central placeholder for mutation types diagram
add_placeholder(s, Inches(2.650), Inches(1.100), Inches(8.000), Inches(4.000),
                "[Mutation types diagram: substitution, insertion, deletion with DNA sequence examples]")

# Left side: compact mutation type labels
mut_types = [
    ("Substitution", "One nucleotide replaced by another", SEC_FRAME),
    ("Insertion", "Extra nucleotide(s) added, shifts reading frame", ORANGE),
    ("Deletion", "Nucleotide(s) removed, disrupts structure", RED_ACCENT),
]
for i, (name, desc, clr) in enumerate(mut_types):
    cy = Inches(1.200) + i * Inches(1.300)
    add_accent_bar(s, Inches(0.500), cy, Inches(0.080), Inches(1.100), clr)
    add_textbox(s, Inches(0.700), cy + Inches(0.100), Inches(1.800), Inches(0.300),
                name, size=12, bold=True, color=clr)
    add_textbox(s, Inches(0.700), cy + Inches(0.420), Inches(1.800), Inches(0.550),
                desc, size=9, color=DARK_GRAY)

# Bottom: Effects on protein (compact row)
add_textbox(s, Inches(0.600), Inches(5.300), Inches(3.000), Inches(0.350),
            "Effects on Protein", size=14, bold=True, color=DARK_NAVY)

effects = [
    ("Silent", "No AA change", GRAY),
    ("Missense", "Different AA", BLUE),
    ("Nonsense", "Premature stop", RED_ACCENT),
]
for i, (name, desc, clr) in enumerate(effects):
    cx = Inches(0.600) + i * Inches(2.900)
    cy = Inches(5.750)
    card = add_card(s, cx, cy, Inches(2.700), Inches(0.800), border=MID_GRAY)
    add_accent_bar(s, cx, cy, Inches(0.060), Inches(0.800), clr)
    add_textbox(s, cx + Inches(0.200), cy + Inches(0.050), Inches(2.300), Inches(0.300),
                name, size=11, bold=True, color=clr)
    add_textbox(s, cx + Inches(0.200), cy + Inches(0.380), Inches(2.300), Inches(0.350),
                desc, size=9, color=DARK_GRAY)

# Link to hotspots
link_box = add_card(s, Inches(9.000), Inches(5.300), Inches(3.900), Inches(1.250),
                    fill=RGBColor(0xE8, 0xF5, 0xE9), border=GREEN)
set_text(link_box, "When mutations cluster at specific\npositions across many lineages,\nthey are called Mutation Hotspots.",
         size=11, bold=True, color=GREEN, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)


# ── SLIDE 6: Viral Evolution & Natural Selection ────────────────
slide_num += 1
s = content_slide(prs, "Viral Evolution & Natural Selection", SEC_INTRO)
add_page_number(s, slide_num)

# Three selection types with placeholders next to each
sel_types = [
    ("Positive Selection", "Mutations that increase viral fitness spread\nthrough the population.\n\n"
     "Examples:\n  Immune evasion mutations\n  Increased transmissibility\n  Drug resistance",
     GREEN, "[Positive selection diagram]"),
    ("Purifying Selection", "Mutations that damage essential functions\nare removed from the population.\n\n"
     "Examples:\n  Disruption of replication machinery\n  Loss of structural integrity\n  Impaired host entry",
     RED_ACCENT, "[Purifying selection diagram]"),
    ("Convergent Evolution", "The same mutation arises independently\nin different viral lineages.\n\n"
     "Examples:\n  N501Y in multiple SARS-CoV-2 variants\n  E484K across Alpha, Beta, Gamma\n  Strong signal of positive selection",
     PURPLE, "[Convergent evolution diagram]"),
]
for i, (ttl, desc, clr, ph_label) in enumerate(sel_types):
    cx = Inches(0.500) + i * Inches(4.200)
    card = add_card(s, cx, Inches(1.200), Inches(3.900), Inches(5.400), border=MID_GRAY)
    add_rect(s, cx, Inches(1.200), Inches(3.900), Inches(0.550), fill=clr)
    add_textbox(s, cx, Inches(1.220), Inches(3.900), Inches(0.510),
                ttl, size=15, bold=True, color=WHITE, align=PP_ALIGN.CENTER,
                anchor=MSO_ANCHOR.MIDDLE)
    add_textbox(s, cx + Inches(0.200), Inches(1.900), Inches(3.500), Inches(2.600),
                desc, size=11, color=DARK_GRAY)
    # small placeholder for each concept
    add_placeholder(s, cx + Inches(0.200), Inches(4.600), Inches(3.500), Inches(1.850), ph_label)


# ── SLIDE 7: Research Overview — real diagram ──────────────────
slide_num += 1
s = content_slide(prs, "Research Overview", SEC_INTRO)
add_page_number(s, slide_num)

# Horizontal flow with 5 connected boxes
flow_boxes = [
    ("Problem", "No benchmark for\nhotspot detection", RED_ACCENT),
    ("MutBench", "3-Layer GT\n9 Scoring\n39 Detection", BLUE),
    ("Stage 1", "SARS-CoV-2\ndepth analysis", GREEN),
    ("Stage 2", "9 pathogens\n2,544 evaluations", ORANGE),
    ("Finding", "No universal best\n\u03c9\u00b2 = 0.285", PURPLE),
]
box_w = Inches(2.200)
box_h = Inches(1.500)
start_x = Inches(0.400)
gap = Inches(0.400)
arrow_w = Inches(0.400)

for i, (ttl, desc, clr) in enumerate(flow_boxes):
    bx = start_x + i * (box_w + gap)
    by = Inches(1.300)
    box = add_rounded_rect(s, bx, by, box_w, box_h, fill=clr)
    set_text(box, f"{ttl}\n\n{desc}", size=11, bold=False, color=WHITE,
             align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    # Bold the title line via overlay
    add_textbox(s, bx, by + Inches(0.100), box_w, Inches(0.350),
                ttl, size=13, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    # arrow between boxes
    if i < len(flow_boxes) - 1:
        ax = bx + box_w
        add_textbox(s, ax, by + Inches(0.400), arrow_w, Inches(0.500),
                    "\u2192", size=24, bold=True, color=DARK_GRAY, align=PP_ALIGN.CENTER)

# Below the flow: summary arrow pointing to PAHD
# Arrow line
arrow_y = Inches(3.100)
add_rect(s, Inches(2.000), arrow_y, Inches(9.300), Inches(0.040), fill=DARK_NAVY)
# Down arrow from center
mid_x = Inches(6.150)
add_textbox(s, mid_x, arrow_y - Inches(0.100), Inches(1.000), Inches(0.500),
            "\u25bc", size=20, bold=True, color=DARK_NAVY, align=PP_ALIGN.CENTER)

# PAHD box below
pahd_box = add_rounded_rect(s, Inches(3.500), Inches(3.400), Inches(6.300), Inches(1.200),
                             fill=DARK_NAVY)
set_text(pahd_box, "PAHD: Pathogen-Adaptive Hotspot Detection\nAdaptive method selection based on pathogen profile",
         size=14, bold=True, color=WHITE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

# Key numbers below
nums = [
    ("9", "RNA Pathogens", SEC_FRAME),
    ("2,544", "Evaluations", SEC_STAGE2),
    ("351", "Method Combos", GREEN),
    ("3", "GT Layers", PURPLE),
    ("0.285", "Interaction \u03c9\u00b2", RED_ACCENT),
]
for i, (num, label, clr) in enumerate(nums):
    cx = Inches(0.400) + i * Inches(2.560)
    cy = Inches(5.000)
    card = add_card(s, cx, cy, Inches(2.350), Inches(1.600), border=MID_GRAY)
    add_textbox(s, cx, cy + Inches(0.150), Inches(2.350), Inches(0.700),
                num, size=28, bold=True, color=clr, align=PP_ALIGN.CENTER)
    add_textbox(s, cx, cy + Inches(0.900), Inches(2.350), Inches(0.500),
                label, size=11, color=DARK_GRAY, align=PP_ALIGN.CENTER)


# ── SLIDE 8: Mutation Hotspot Definition ────────────────────────
slide_num += 1
s = content_slide(prs, "What are Mutation Hotspots?", SEC_INTRO)
add_page_number(s, slide_num)

# definition box
defbox = add_card(s, Inches(0.600), Inches(1.200), Inches(12.100), Inches(1.200),
                  fill=RGBColor(0xE8, 0xF5, 0xE9), border=GREEN)
set_text(defbox, "Definition:  Genomic positions where mutations accumulate at significantly\n"
         "higher frequencies than expected by chance, indicating selective pressure.",
         size=14, color=DARK_GRAY, anchor=MSO_ANCHOR.MIDDLE)

# Left: placeholder for hotspot on Spike
add_placeholder(s, Inches(0.600), Inches(2.700), Inches(5.800), Inches(3.000),
                "[Image Placeholder]\nHotspot Visualization on Spike Protein\n"
                "e.g., N501Y, E484K, D614G positions highlighted\n(To be inserted)")

# Right: 3 cards
topics = [
    ("Why do they occur?", "Positive selection drives beneficial mutations\n"
     "(e.g., immune escape at receptor binding sites).\n"
     "Some regions tolerate mutations better than others."),
    ("Why are they important?", "Track viral evolution in real-time.\n"
     "Guide vaccine & drug target design.\n"
     "Predict emerging variants of concern."),
    ("Key Examples", "N501Y: Enhanced ACE2 binding affinity\n"
     "E484K: Immune escape from antibodies\n"
     "D614G: Founder effect vs true selection"),
]
for i, (ttl, desc) in enumerate(topics):
    cy = Inches(2.700) + i * Inches(1.050)
    card = add_card(s, Inches(6.700), cy, Inches(5.900), Inches(0.900), border=MID_GRAY)
    add_textbox(s, Inches(6.900), cy + Inches(0.050), Inches(2.000), Inches(0.300),
                ttl, size=12, bold=True, color=DARK_NAVY)
    add_textbox(s, Inches(6.900), cy + Inches(0.350), Inches(5.500), Inches(0.500),
                desc, size=9, color=DARK_GRAY)

# bottom note
note = add_card(s, Inches(0.600), Inches(5.950), Inches(12.100), Inches(0.700),
                fill=RGBColor(0xFF, 0xEB, 0xEE), border=RED_ACCENT)
set_text(note, "Current gap: No systematic way to compare hotspot detection methods across pathogens",
         size=13, bold=True, color=RED_ACCENT, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)


# ── SLIDE 9: Problem Definition ─────────────────────────────────
slide_num += 1
s = content_slide(prs, "Problem Definition", SEC_INTRO)
add_page_number(s, slide_num)

problems = [
    ("P1", "No Standardized Benchmark",
     "Existing methods evaluated on different datasets with different metrics, "
     "making fair comparison impossible.",
     "[Placeholder]\nIncompatible metrics"),
    ("P2", "Single-Pathogen Bias",
     "Methods tested on only 1-2 pathogens cannot generalize. "
     "Pathogen-specific characteristics dramatically affect detection performance.",
     "[Placeholder]\n1 vs 9 pathogens"),
    ("P3", "No Universal Best Method",
     "Our prior work (MOSD, MutClust) demonstrated that no single approach dominates "
     "across all settings, demanding systematic evaluation.",
     "[Placeholder]\nRanking reversal"),
]
for i, (pid, title, desc, ph_text) in enumerate(problems):
    cy = Inches(1.200) + i * Inches(1.850)
    card = add_card(s, Inches(0.600), cy, Inches(9.800), Inches(1.600), border=MID_GRAY)
    # problem id badge
    badge = add_rounded_rect(s, Inches(0.800), cy + Inches(0.300), Inches(0.600), Inches(0.500),
                             fill=DARK_NAVY)
    set_text(badge, pid, size=16, bold=True, color=WHITE, align=PP_ALIGN.CENTER,
             anchor=MSO_ANCHOR.MIDDLE)
    add_textbox(s, Inches(1.600), cy + Inches(0.200), Inches(8.500), Inches(0.400),
                title, size=16, bold=True, color=DARK_NAVY)
    add_textbox(s, Inches(1.600), cy + Inches(0.700), Inches(8.500), Inches(0.800),
                desc, size=12, color=DARK_GRAY)
    # placeholder icon on right
    add_placeholder(s, Inches(10.700), cy + Inches(0.150), Inches(2.000), Inches(1.300), ph_text)


# ── SLIDE 10: 9 Pathogens Overview ──────────────────────────────
slide_num += 1
s = content_slide(prs, "9 RNA Pathogens in MutBench", SEC_INTRO)
add_page_number(s, slide_num)

pathogens = [
    ("SARS-CoV-2", "~30 kb", "Spike protein", "COVID-19 pandemic"),
    ("Influenza", "~13.5 kb", "Hemagglutinin", "Seasonal epidemics, antigenic shift"),
    ("HIV", "~10 kb", "Env/Gag", "High mutation rate, chronic"),
    ("Dengue", "~11 kb", "E protein", "4 serotypes, tropical"),
    ("MERS-CoV", "~30 kb", "Spike protein", "Camel-origin, high fatality"),
    ("RSV", "~15 kb", "F protein", "Infant respiratory disease"),
    ("Norovirus", "~7.5 kb", "VP1 capsid", "Gastroenteritis, rapid evolution"),
    ("HCV", "~9.6 kb", "E1/E2 proteins", "Chronic hepatitis, high diversity"),
    ("Ebola", "~19 kb", "Glycoprotein", "Hemorrhagic fever, outbreaks"),
]

# Header row
add_rect(s, Inches(0.500), Inches(1.200), Inches(12.300), Inches(0.500), fill=DARK_NAVY)
headers = ["Pathogen", "Genome", "Target Protein", "Key Feature"]
h_widths = [Inches(2.200), Inches(1.400), Inches(2.600), Inches(6.100)]
hx = Inches(0.500)
for h, w in zip(headers, h_widths):
    add_textbox(s, hx, Inches(1.210), w, Inches(0.480),
                h, size=12, bold=True, color=WHITE, align=PP_ALIGN.CENTER,
                anchor=MSO_ANCHOR.MIDDLE)
    hx += w

# Data rows
for r, (name, genome, protein, feature) in enumerate(pathogens):
    ry = Inches(1.700) + r * Inches(0.580)
    fill = LIGHT_GRAY if r % 2 == 0 else WHITE
    add_rect(s, Inches(0.500), ry, Inches(12.300), Inches(0.580), fill=fill)
    vals = [name, genome, protein, feature]
    vx = Inches(0.500)
    for v, w in zip(vals, h_widths):
        bld = (v == name)
        clr = DARK_NAVY if bld else DARK_GRAY
        add_textbox(s, vx, ry, w, Inches(0.580), v, size=11, bold=bld, color=clr,
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        vx += w

# bottom note
add_textbox(s, Inches(0.600), Inches(6.950), Inches(12.100), Inches(0.300),
            "* All RNA viruses with publicly available sequence data from NCBI/GISAID",
            size=9, color=GRAY, align=PP_ALIGN.CENTER)


# ── SLIDE 11: MutBench Pipeline ─────────────────────────────────
slide_num += 1
s = content_slide(prs, "MutBench Pipeline Overview", SEC_FRAME)
add_page_number(s, slide_num)

# Pipeline flow — full-width boxes with arrows
flow_items = [
    ("Input\nSequences", SEC_FRAME),
    ("MSA\nAlignment", SEC_FRAME),
    ("Scoring\n(9 methods)", GREEN),
    ("Detection\n(39 methods)", GREEN),
    ("Ground\nTruth", ORANGE),
    ("Evaluation\n(MCC)", DARK_NAVY),
]
box_w = Inches(1.750)
box_h = Inches(1.050)
start_x = Inches(0.400)
for i, (item, fill_c) in enumerate(flow_items):
    bx = start_x + i * Inches(2.100)
    by = Inches(1.200)
    box = add_rounded_rect(s, bx, by, box_w, box_h, fill=fill_c)
    set_text(box, item, size=12, bold=True, color=WHITE, align=PP_ALIGN.CENTER,
             anchor=MSO_ANCHOR.MIDDLE)
    if i < len(flow_items) - 1:
        add_textbox(s, bx + box_w, by + Inches(0.250), Inches(0.350), Inches(0.500),
                    ">", size=20, bold=True, color=GRAY, align=PP_ALIGN.CENTER)

# Lower left: 9 Scoring Methods table
add_rect(s, Inches(0.400), Inches(2.600), Inches(6.000), Inches(0.450), fill=SEC_FRAME)
add_textbox(s, Inches(0.400), Inches(2.610), Inches(6.000), Inches(0.430),
            "9 Scoring Methods", size=13, bold=True, color=WHITE, align=PP_ALIGN.CENTER,
            anchor=MSO_ANCHOR.MIDDLE)
scoring_items = [
    ("Shannon Entropy", "Position variability"),
    ("Jensen-Shannon Div.", "Distribution divergence"),
    ("Mutation Frequency", "1 - dominant freq"),
    ("Wavelet (CWT)", "Multi-scale analysis"),
    ("Sliding Window", "Smoothed averages"),
    ("Phylo-aware Score", "Branch-weighted"),
    ("dN/dS Ratio", "Selection pressure"),
    ("Kabat Variability", "AA diversity index"),
    ("Property Entropy", "Physicochemical"),
]
for i, (name, desc) in enumerate(scoring_items):
    col = i % 3
    row = i // 3
    cx = Inches(0.500) + col * Inches(2.000)
    cy = Inches(3.150) + row * Inches(0.550)
    add_textbox(s, cx, cy, Inches(1.900), Inches(0.280),
                f"  {name}", size=9, bold=True, color=SEC_FRAME)
    add_textbox(s, cx, cy + Inches(0.250), Inches(1.900), Inches(0.250),
                f"    {desc}", size=8, color=GRAY)

# Lower right: Detection Families table
add_rect(s, Inches(6.700), Inches(2.600), Inches(6.000), Inches(0.450), fill=GREEN)
add_textbox(s, Inches(6.700), Inches(2.610), Inches(6.000), Inches(0.430),
            "Detection Families (39 methods)", size=13, bold=True, color=WHITE,
            align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
detect_items = [
    ("Z-score", "4 variants"),
    ("Percentile", "4 variants"),
    ("IQR Outlier", "2 variants"),
    ("DBSCAN", "6 variants"),
    ("HDBSCAN", "3 variants"),
    ("Gaussian Mix.", "4 variants"),
    ("Kernel Density", "4 variants"),
    ("Isolation Forest", "3 variants"),
    ("Wavelet Peaks", "3 variants"),
    ("LOF", "2 variants"),
    ("Threshold", "2 variants"),
    ("Bayesian CP", "2 variants"),
]
for i, (name, desc) in enumerate(detect_items):
    col = i % 3
    row = i // 3
    cx = Inches(6.800) + col * Inches(2.000)
    cy = Inches(3.150) + row * Inches(0.550)
    add_textbox(s, cx, cy, Inches(1.900), Inches(0.280),
                f"  {name}", size=9, bold=True, color=GREEN)
    add_textbox(s, cx, cy + Inches(0.250), Inches(1.900), Inches(0.250),
                f"    {desc}", size=8, color=GRAY)

# total count
add_textbox(s, Inches(3.500), Inches(5.500), Inches(6.300), Inches(0.400),
            "Total: 9 x 39 = 351 unique scoring-detection combinations per pathogen",
            size=12, bold=True, color=DARK_NAVY, align=PP_ALIGN.CENTER)


# ── SLIDE 12: Scoring Methods Detail ────────────────────────────
slide_num += 1
s = content_slide(prs, "Scoring Methods: 9 Approaches to Quantify Variability", SEC_FRAME)
add_page_number(s, slide_num)

scoring_detail = [
    ("Shannon Entropy", "H(x) = -Sum p(i) log2 p(i)", "Measures nucleotide uncertainty\nat each alignment position"),
    ("Jensen-Shannon Div.", "JSD(P||Q) = H(M) - [H(P)+H(Q)]/2", "Divergence from background\ndistribution"),
    ("Mutation Frequency", "f(x) = 1 - max(p(i))", "Simple: 1 minus dominant\nnucleotide frequency"),
    ("Wavelet (CWT)", "CWT with Ricker wavelet", "Multi-scale frequency analysis\ncaptures local + global patterns"),
    ("Sliding Window", "Mean score in window of size w", "Smoothed signal reduces noise\nparameter: window size"),
    ("Phylo-aware Score", "Branch-weighted mutations", "Weights by phylogenetic\nindependence of observations"),
    ("dN/dS Ratio", "omega = dN/dS", "Ratio of non-synonymous to\nsynonymous substitution rates"),
    ("Kabat Variability", "K = N_aa / (n * f_max)", "Wu-Kabat variability index\nfor amino acid diversity"),
    ("Property Entropy", "H based on AA properties", "Groups amino acids by\nphysicochemical properties"),
]
for i, (name, formula, desc) in enumerate(scoring_detail):
    col = i % 3
    row = i // 3
    cx = Inches(0.400) + col * Inches(4.200)
    cy = Inches(1.150) + row * Inches(1.900)
    card = add_card(s, cx, cy, Inches(3.950), Inches(1.700), border=MID_GRAY)
    add_accent_bar(s, cx, cy, Inches(0.080), Inches(1.700), SEC_FRAME)
    add_textbox(s, cx + Inches(0.200), cy + Inches(0.100), Inches(3.600), Inches(0.350),
                name, size=13, bold=True, color=SEC_FRAME)
    # formula box
    fbox = add_rect(s, cx + Inches(0.200), cy + Inches(0.500), Inches(3.500), Inches(0.400),
                    fill=RGBColor(0xF0, 0xF4, 0xF8), border=MID_GRAY)
    set_text(fbox, formula, size=9, color=DARK_NAVY, align=PP_ALIGN.CENTER,
             anchor=MSO_ANCHOR.MIDDLE)
    add_textbox(s, cx + Inches(0.200), cy + Inches(1.000), Inches(3.500), Inches(0.600),
                desc, size=9, color=DARK_GRAY)


# ── SLIDE 13: 3-Layer Ground Truth ──────────────────────────────
slide_num += 1
s = content_slide(prs, "3-Layer Ground Truth Design", SEC_FRAME)
add_page_number(s, slide_num)

add_figure(s, os.path.join(FIG_DISS, "multi_ground_truth_figure.png"),
           Inches(0.400), Inches(1.100), Inches(7.500), Inches(5.600))

layers = [
    ("Layer 1: Adaptive", "Entropy-based threshold auto-adjusted\nper pathogen. Captures high-variability\npositions relative to background."),
    ("Layer 2: Constrained", "Intersection of top-K positions across\nmultiple scoring methods. Reduces\nsingle-method bias."),
    ("Layer 3: DMS-based", "Deep mutational scanning data from\nexperimental fitness measurements.\nGold-standard biological validation."),
]
for i, (ttl, desc) in enumerate(layers):
    cy = Inches(1.200) + i * Inches(1.900)
    card = add_card(s, Inches(8.200), cy, Inches(4.500), Inches(1.650), border=MID_GRAY)
    add_textbox(s, Inches(8.400), cy + Inches(0.100), Inches(4.100), Inches(0.400),
                ttl, size=13, bold=True, color=SEC_FRAME)
    add_textbox(s, Inches(8.400), cy + Inches(0.550), Inches(4.100), Inches(1.000),
                desc, size=11, color=DARK_GRAY)


# ── SLIDE 14: MCC Metric ────────────────────────────────────────
slide_num += 1
s = content_slide(prs, "Evaluation Metric: Matthews Correlation Coefficient", SEC_FRAME)
add_page_number(s, slide_num)

# MCC formula in a proper box
fbox = add_card(s, Inches(0.600), Inches(1.200), Inches(6.200), Inches(1.400),
                fill=RGBColor(0xF3, 0xE5, 0xF5), border=PURPLE)
add_textbox(s, Inches(0.800), Inches(1.250), Inches(5.800), Inches(0.350),
            "MCC Formula", size=15, bold=True, color=PURPLE)
add_textbox(s, Inches(0.800), Inches(1.650), Inches(5.800), Inches(0.400),
            "MCC = (TP*TN - FP*FN) / sqrt((TP+FP)(TP+FN)(TN+FP)(TN+FN))",
            size=12, bold=True, color=DARK_NAVY)
add_textbox(s, Inches(0.800), Inches(2.100), Inches(5.800), Inches(0.400),
            "Range: [-1, +1]   |   0 = random   |   +1 = perfect agreement",
            size=11, color=DARK_GRAY)

# Confusion matrix diagram area
add_textbox(s, Inches(0.600), Inches(2.900), Inches(3.000), Inches(0.350),
            "Confusion Matrix", size=13, bold=True, color=DARK_NAVY)
# Draw simple confusion matrix
cm_x, cm_y = Inches(0.600), Inches(3.300)
cm_s = Inches(1.300)
labels = [("TP", GREEN), ("FP", RED_ACCENT), ("FN", ORANGE), ("TN", SEC_FRAME)]
for i, (lbl, clr) in enumerate(labels):
    col = i % 2
    row = i // 2
    bx = cm_x + col * cm_s
    by = cm_y + row * cm_s
    box = add_rect(s, bx, by, cm_s, cm_s, fill=clr)
    set_text(box, lbl, size=18, bold=True, color=WHITE, align=PP_ALIGN.CENTER,
             anchor=MSO_ANCHOR.MIDDLE)

# Why MCC > F1 comparison
add_textbox(s, Inches(3.500), Inches(2.900), Inches(3.300), Inches(0.350),
            "Why MCC over F1?", size=13, bold=True, color=DARK_NAVY)
why_items = [
    "Balanced even with severe class imbalance\n(hotspots are rare: ~5% of positions)",
    "Uses all 4 confusion matrix quadrants\n(F1 ignores true negatives)",
    "Random baseline: mean = 0.001, std = 0.003\n(verified empirically)",
]
for i, item in enumerate(why_items):
    cy = Inches(3.350) + i * Inches(0.900)
    card = add_card(s, Inches(3.500), cy, Inches(3.300), Inches(0.800), border=MID_GRAY)
    add_textbox(s, Inches(3.650), cy + Inches(0.080), Inches(3.000), Inches(0.650),
                item, size=9, color=DARK_GRAY)

# MCC vs F1 figure on right
add_figure(s, os.path.join(FIG_MAIN, "mcc_vs_f1_fairness.png"),
           Inches(7.100), Inches(1.200), Inches(5.600), Inches(5.400))


# ── SLIDE 15: Two-Stage Design ──────────────────────────────────
slide_num += 1
s = content_slide(prs, "Two-Stage Experimental Design", SEC_FRAME)
add_page_number(s, slide_num)

# Stage 1 card
s1 = add_card(s, Inches(0.600), Inches(1.200), Inches(5.800), Inches(4.200),
              fill=RGBColor(0xE8, 0xF5, 0xE9), border=GREEN)
add_rect(s, Inches(0.600), Inches(1.200), Inches(5.800), Inches(0.600), fill=GREEN)
add_textbox(s, Inches(0.800), Inches(1.220), Inches(5.400), Inches(0.560),
            "Stage 1: Controlled Comparison", size=18, bold=True, color=WHITE,
            anchor=MSO_ANCHOR.MIDDLE)
add_textbox(s, Inches(0.800), Inches(2.000), Inches(5.400), Inches(3.200),
            "4 pathogens\n"
            "  SARS-CoV-2, Influenza, HIV, Dengue\n\n"
            "351 scoring-detection combinations\n"
            "  9 scoring x 39 detection methods\n\n"
            "Focus areas:\n"
            "  Method comparison & ranking\n"
            "  Parameter sensitivity analysis\n"
            "  Synthetic vs real data gap\n"
            "  Initial ranking reversal observation",
            size=13, color=DARK_GRAY)

# Stage 2 card
s2 = add_card(s, Inches(6.900), Inches(1.200), Inches(5.800), Inches(4.200),
              fill=RGBColor(0xFF, 0xF3, 0xE0), border=ORANGE)
add_rect(s, Inches(6.900), Inches(1.200), Inches(5.800), Inches(0.600), fill=ORANGE)
add_textbox(s, Inches(7.100), Inches(1.220), Inches(5.400), Inches(0.560),
            "Stage 2: Large-Scale Validation", size=18, bold=True, color=WHITE,
            anchor=MSO_ANCHOR.MIDDLE)
add_textbox(s, Inches(7.100), Inches(2.000), Inches(5.400), Inches(3.200),
            "9 pathogens (+5 more)\n"
            "  + MERS, RSV, Norovirus, HCV, Ebola\n\n"
            "2,544 evaluations\n"
            "  9 scoring x 39 detection x 9 pathogens\n\n"
            "Focus areas:\n"
            "  Two-way ANOVA (interaction effects)\n"
            "  Per-pathogen best combination\n"
            "  Friedman test + LOPO CV\n"
            "  PAHD proof of concept",
            size=13, color=DARK_GRAY)

# Stage transition arrow area
arrow_box = add_card(s, Inches(2.500), Inches(5.650), Inches(8.300), Inches(1.000),
                     fill=DARK_NAVY)
set_text(arrow_box,
         "Stage 1 (discovery)  >>>  Stage 2 (validation at scale)  >>>  PAHD (algorithm)",
         size=14, bold=True, color=WHITE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)


# ── SLIDE 16: Method Comparison Results ─────────────────────────
slide_num += 1
s = content_slide(prs, "Stage 1: Method Comparison Results", SEC_STAGE1)
add_page_number(s, slide_num)

add_figure(s, os.path.join(FIG_DISS, "new_methodology_comparison.png"),
           Inches(0.300), Inches(1.100), Inches(8.200), Inches(5.600))

add_textbox(s, Inches(8.800), Inches(1.200), Inches(4.000), Inches(0.400),
            "Key Findings", size=16, bold=True, color=SEC_STAGE1)
findings = [
    "Wavelet scoring achieves highest\nmean MCC across 4 pathogens",
    "HDBSCAN-based detection outperforms\ntraditional threshold methods",
    "Large variance across pathogens\nsuggests generalization limits",
    "Top combination differs between\nSARS-CoV-2 and HIV",
]
for i, f in enumerate(findings):
    cy = Inches(1.800) + i * Inches(1.200)
    card = add_card(s, Inches(8.800), cy, Inches(3.900), Inches(1.000), border=MID_GRAY)
    add_accent_bar(s, Inches(8.800), cy, Inches(0.060), Inches(1.000), SEC_STAGE1)
    add_textbox(s, Inches(9.000), cy + Inches(0.100), Inches(3.600), Inches(0.800),
                f, size=11, color=DARK_GRAY)


# ── SLIDE 17: Parameter Sensitivity ─────────────────────────────
slide_num += 1
s = content_slide(prs, "Parameter Sensitivity Analysis", SEC_STAGE1)
add_page_number(s, slide_num)

add_figure(s, os.path.join(FIG_DISS, "sensitivity_heatmap.png"),
           Inches(0.300), Inches(1.100), Inches(7.500), Inches(5.600))

add_textbox(s, Inches(8.100), Inches(1.200), Inches(4.600), Inches(0.400),
            "Sensitivity Findings", size=16, bold=True, color=SEC_STAGE1)

# findings as table
sens_data = [
    ("Parameter", "Sensitivity", "Note"),
    ("Window size", "Moderate", "Optimal varies by pathogen"),
    ("Epsilon (DBSCAN)", "High", "Requires per-pathogen tuning"),
    ("Min-cluster (HDBSCAN)", "Low", "Robust across wide range"),
    ("Threshold percentile", "Moderate", "Pathogen-dependent optima"),
]
for r, row_data in enumerate(sens_data):
    ry = Inches(1.750) + r * Inches(0.550)
    fill = DARK_NAVY if r == 0 else (LIGHT_GRAY if r % 2 == 1 else WHITE)
    clr = WHITE if r == 0 else DARK_GRAY
    bld = (r == 0)
    add_rect(s, Inches(8.100), ry, Inches(4.600), Inches(0.550), fill=fill)
    ws = [Inches(1.800), Inches(1.200), Inches(1.600)]
    vx = Inches(8.100)
    for v, w in zip(row_data, ws):
        add_textbox(s, vx, ry, w, Inches(0.550), v, size=10, bold=bld, color=clr,
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        vx += w

# Bottom note
note = add_card(s, Inches(8.100), Inches(4.800), Inches(4.600), Inches(1.500),
                fill=RGBColor(0xE8, 0xF5, 0xE9), border=GREEN)
set_text(note, "HDBSCAN is the most robust detection\nmethod across parameter variations.\n\n"
         "This supports its use as a default\nchoice when pathogen characteristics\nare unknown.",
         size=10, color=DARK_GRAY, anchor=MSO_ANCHOR.TOP)


# ── SLIDE 18: Synthetic vs Real Gap ─────────────────────────────
slide_num += 1
s = content_slide(prs, "Synthetic vs Real Data Gap", SEC_STAGE1)
add_page_number(s, slide_num)

# Left header
add_rect(s, Inches(0.600), Inches(1.300), Inches(5.500), Inches(0.500), fill=BLUE)
add_textbox(s, Inches(0.600), Inches(1.310), Inches(5.500), Inches(0.480),
            "Synthetic Data", size=15, bold=True, color=WHITE, align=PP_ALIGN.CENTER,
            anchor=MSO_ANCHOR.MIDDLE)
# Right header
add_rect(s, Inches(6.500), Inches(1.300), Inches(6.200), Inches(0.500), fill=RED_ACCENT)
add_textbox(s, Inches(6.500), Inches(1.310), Inches(6.200), Inches(0.480),
            "Real Pathogen Data", size=15, bold=True, color=WHITE, align=PP_ALIGN.CENTER,
            anchor=MSO_ANCHOR.MIDDLE)

# Comparison rows
comp_rows = [
    ("Mutation Distribution", "Uniform / Poisson", "Highly skewed, founder effects"),
    ("Selection Pressure", "None (neutral)", "Complex positive + purifying"),
    ("Ground Truth", "Known by construction", "Approximate (DMS / literature)"),
    ("Phylogenetic Structure", "Independent samples", "Strong non-independence"),
    ("Best Method", "Threshold-based wins", "Clustering-based wins"),
]
for i, (aspect, syn, real) in enumerate(comp_rows):
    cy = Inches(2.000) + i * Inches(0.900)
    # aspect label
    add_textbox(s, Inches(0.600), cy, Inches(2.200), Inches(0.350),
                aspect, size=11, bold=True, color=DARK_NAVY)
    # Synthetic
    card_l = add_card(s, Inches(2.900), cy, Inches(3.200), Inches(0.750), border=MID_GRAY)
    set_text(card_l, syn, size=11, color=DARK_GRAY, align=PP_ALIGN.CENTER,
             anchor=MSO_ANCHOR.MIDDLE)
    # vs label
    add_textbox(s, Inches(6.100), cy, Inches(0.400), Inches(0.750),
                "vs", size=10, bold=True, color=GRAY, align=PP_ALIGN.CENTER,
                anchor=MSO_ANCHOR.MIDDLE)
    # Real
    card_r = add_card(s, Inches(6.500), cy, Inches(6.200), Inches(0.750),
                      fill=RGBColor(0xFF, 0xF3, 0xE0), border=ORANGE)
    set_text(card_r, real, size=11, bold=True, color=DARK_GRAY, align=PP_ALIGN.CENTER,
             anchor=MSO_ANCHOR.MIDDLE)

# Conclusion
msg = add_card(s, Inches(1.500), Inches(6.600), Inches(10.300), Inches(0.600),
               fill=RGBColor(0xFF, 0xEB, 0xEE), border=RED_ACCENT)
set_text(msg, "Ranking reversals between synthetic and real data demonstrate the need for real-pathogen benchmarking",
         size=12, bold=True, color=RED_ACCENT, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)


# ── SLIDE 19: H3N2 Ranking Reversal ─────────────────────────────
slide_num += 1
s = content_slide(prs, "Cross-Pathogen Ranking Reversal", SEC_STAGE1)
add_page_number(s, slide_num)

add_figure(s, os.path.join(FIG_MAIN, "detection_ranking.png"),
           Inches(0.300), Inches(1.100), Inches(7.800), Inches(5.600))

# big number
big = add_card(s, Inches(8.500), Inches(1.300), Inches(4.100), Inches(2.400), fill=DARK_NAVY)
add_textbox(s, Inches(8.500), Inches(1.500), Inches(4.100), Inches(1.000),
            "9 / 9", size=52, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
add_textbox(s, Inches(8.500), Inches(2.600), Inches(4.100), Inches(0.800),
            "unique best\ncombinations", size=18, color=RGBColor(0xBB, 0xDE, 0xFB),
            align=PP_ALIGN.CENTER)

add_textbox(s, Inches(8.500), Inches(4.000), Inches(4.100), Inches(2.800),
            "Every pathogen has a different\noptimal scoring + detection pair.\n\n"
            "No single method can be\n\"recommended\" universally.\n\n"
            "This motivates the need for\npathogen-adaptive selection (PAHD).",
            size=12, color=DARK_GRAY)


# ── SLIDE 20: 9-Pathogen Scale ──────────────────────────────────
slide_num += 1
s = content_slide(prs, "Stage 2: Scaling to 9 Pathogens", SEC_STAGE2)
add_page_number(s, slide_num)

bignums = [
    ("9", "Pathogens", "SARS-CoV-2, Influenza, HIV,\nDengue, MERS, RSV,\nNorovirus, HCV, Ebola"),
    ("2,544", "Evaluations", "9 scoring methods\nx 39 detection methods\nx 9 pathogens (multilayer GT)"),
    ("4", "Statistical Tests", "Two-way ANOVA\nPermutation test\nFriedman test\nLOPO cross-validation"),
]
for i, (num, label, desc) in enumerate(bignums):
    cx = Inches(0.600) + i * Inches(4.200)
    cy = Inches(1.500)
    card = add_card(s, cx, cy, Inches(3.900), Inches(4.800), border=MID_GRAY)
    add_textbox(s, cx, cy + Inches(0.300), Inches(3.900), Inches(1.200),
                num, size=54, bold=True, color=SEC_STAGE2, align=PP_ALIGN.CENTER)
    add_textbox(s, cx, cy + Inches(1.500), Inches(3.900), Inches(0.500),
                label, size=20, bold=True, color=DARK_NAVY, align=PP_ALIGN.CENTER)
    add_textbox(s, cx + Inches(0.300), cy + Inches(2.200), Inches(3.300), Inches(2.400),
                desc, size=12, color=DARK_GRAY, align=PP_ALIGN.CENTER)


# ── SLIDE 21: ANOVA ─────────────────────────────────────────────
slide_num += 1
s = content_slide(prs, "Two-Way ANOVA: Variance Decomposition", SEC_STAGE2)
add_page_number(s, slide_num)

add_figure(s, os.path.join(FIG_MAIN, "variance_decomposition.png"),
           Inches(0.300), Inches(1.100), Inches(7.200), Inches(5.600))

# omega-squared cards
anova_cards = [
    ("Detection", "~35%", "Largest effect:\nchoice of detection\nmethod matters most"),
    ("Interaction", "28.5%", "Scoring x Pathogen\ninteraction is strong:\nno universal best"),
    ("Scoring", "~8.3%", "Scoring method\ncontributes less than\ndetection or interaction"),
]
for i, (ttl, val, desc) in enumerate(anova_cards):
    cy = Inches(1.200) + i * Inches(1.900)
    card = add_card(s, Inches(7.900), cy, Inches(4.800), Inches(1.650), border=MID_GRAY)
    add_accent_bar(s, Inches(7.900), cy, Inches(0.080), Inches(1.650), SEC_STAGE2)
    add_textbox(s, Inches(8.200), cy + Inches(0.100), Inches(1.500), Inches(0.400),
                ttl, size=12, bold=True, color=SEC_STAGE2)
    add_textbox(s, Inches(8.200), cy + Inches(0.500), Inches(1.500), Inches(0.800),
                val, size=28, bold=True, color=SEC_STAGE2)
    add_textbox(s, Inches(9.900), cy + Inches(0.200), Inches(2.600), Inches(1.200),
                desc, size=11, color=DARK_GRAY)


# ── SLIDE 22: Per-Pathogen Best ──────────────────────────────────
slide_num += 1
s = content_slide(prs, "Per-Pathogen Best Combinations", SEC_STAGE2)
add_page_number(s, slide_num)

add_figure(s, os.path.join(FIG_MAIN, "cross_pathogen_top5.png"),
           Inches(0.300), Inches(1.100), Inches(8.500), Inches(5.600))

# highlight box
big = add_card(s, Inches(9.100), Inches(1.300), Inches(3.600), Inches(2.200), fill=SEC_STAGE2)
add_textbox(s, Inches(9.100), Inches(1.450), Inches(3.600), Inches(1.000),
            "9 / 9", size=48, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
add_textbox(s, Inches(9.100), Inches(2.400), Inches(3.600), Inches(0.800),
            "unique best\ncombinations", size=16, color=WHITE, align=PP_ALIGN.CENTER)

add_textbox(s, Inches(9.100), Inches(3.800), Inches(3.600), Inches(2.800),
            "High entropy-function divergence\n(Norovirus r=0.39 vs\nSARS-CoV-2 r=0.03)\n\n"
            "H-score founder bias\n(rho = -0.876)\n\n"
            "E-R correlation:\nrho=0.517, p=0.154 (n.s.)",
            size=11, color=DARK_GRAY)


# ── SLIDE 23: Friedman + LOPO ────────────────────────────────────
slide_num += 1
s = content_slide(prs, "Friedman Test & Leave-One-Pathogen-Out CV", SEC_STAGE2)
add_page_number(s, slide_num)

# Friedman card — left
fc = add_card(s, Inches(0.600), Inches(1.200), Inches(5.800), Inches(5.400), border=MID_GRAY)
add_rect(s, Inches(0.600), Inches(1.200), Inches(5.800), Inches(0.600), fill=SEC_STAGE2)
add_textbox(s, Inches(0.800), Inches(1.220), Inches(5.400), Inches(0.560),
            "Friedman Rank Test (Top-20)", size=18, bold=True, color=WHITE,
            anchor=MSO_ANCHOR.MIDDLE)
add_textbox(s, Inches(0.800), Inches(2.000), Inches(5.400), Inches(1.800),
            "Question:\n"
            "  Are top-20 method rankings consistent\n"
            "  across pathogens?\n\n"
            "Result:\n"
            "  chi-squared = 42.44\n"
            "  p-value = 0.0015 (significant at p < 0.01)",
            size=13, color=DARK_GRAY)

# Friedman placeholder for rank chart
add_placeholder(s, Inches(0.800), Inches(4.100), Inches(5.400), Inches(2.200),
                "[Image Placeholder]\nFriedman Rank Distribution Chart\n(To be inserted)")

# LOPO card — right
lc = add_card(s, Inches(6.900), Inches(1.200), Inches(5.800), Inches(5.400), border=MID_GRAY)
add_rect(s, Inches(6.900), Inches(1.200), Inches(5.800), Inches(0.600), fill=RED_ACCENT)
add_textbox(s, Inches(7.100), Inches(1.220), Inches(5.400), Inches(0.560),
            "LOPO Cross-Validation", size=18, bold=True, color=WHITE,
            anchor=MSO_ANCHOR.MIDDLE)
add_textbox(s, Inches(7.100), Inches(2.000), Inches(5.400), Inches(1.800),
            "Protocol:\n"
            "  Train on 8 pathogens, test on held-out 1\n\n"
            "Result:\n"
            "  0 / 9 correct predictions\n"
            "  Simple majority voting fails completely",
            size=13, color=DARK_GRAY)

# LOPO placeholder for hit/miss table
add_placeholder(s, Inches(7.100), Inches(4.100), Inches(5.400), Inches(2.200),
                "[Image Placeholder]\nLOPO Prediction Results Table\n(To be inserted)")


# ── SLIDE 24: ESM-2 Validation ──────────────────────────────────
slide_num += 1
s = content_slide(prs, "ESM-2 Protein Language Model Validation", SEC_STAGE2)
add_page_number(s, slide_num)

# table
add_rect(s, Inches(1.200), Inches(1.400), Inches(10.900), Inches(0.500), fill=DARK_NAVY)
esm_cols = ["Metric", "Without ESM-2", "With ESM-2", "Change"]
esm_ws = [Inches(3.000), Inches(2.600), Inches(2.600), Inches(2.700)]
cx = Inches(1.200)
for c, w in zip(esm_cols, esm_ws):
    add_textbox(s, cx, Inches(1.410), w, Inches(0.480),
                c, size=13, bold=True, color=WHITE, align=PP_ALIGN.CENTER,
                anchor=MSO_ANCHOR.MIDDLE)
    cx += w

esm_rows = [
    ("Mean MCC (top-20)", "0.347", "0.352", "+0.005"),
    ("Median MCC (top-20)", "0.338", "0.341", "+0.003"),
    ("Best single combo", "0.390", "0.393", "+0.003"),
    ("Coverage (>0.3 MCC)", "12/20", "13/20", "+1"),
    ("Rank correlation", "--", "rho = 0.94", "High agreement"),
]
for r, (m, wo, wi, ch) in enumerate(esm_rows):
    ry = Inches(1.900) + r * Inches(0.650)
    fill = LIGHT_GRAY if r % 2 == 0 else WHITE
    add_rect(s, Inches(1.200), ry, Inches(10.900), Inches(0.650), fill=fill)
    cx = Inches(1.200)
    for val, w in zip([m, wo, wi, ch], esm_ws):
        clr = GREEN if val.startswith("+") or val == "High agreement" else DARK_GRAY
        add_textbox(s, cx, ry, w, Inches(0.650), val, size=12, color=clr,
                    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
        cx += w

# Key finding box
msg = add_card(s, Inches(1.200), Inches(5.200), Inches(10.900), Inches(0.900),
               fill=RGBColor(0xE8, 0xF5, 0xE9), border=GREEN)
set_text(msg, "ESM-2 embeddings provide marginal improvement, confirming that\n"
         "sequence-based scoring already captures most of the relevant signal.\n"
         "The benchmark rankings remain stable (rho = 0.94).",
         size=12, color=DARK_GRAY, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

# ESM-2 placeholder
add_placeholder(s, Inches(3.500), Inches(6.300), Inches(6.300), Inches(0.600),
                "[Placeholder] ESM-2 Architecture Concept Diagram (To be inserted)")


# ── SLIDE 25: KEY FINDING ────────────────────────────────────────
slide_num += 1
s = content_slide(prs, "KEY FINDING: No Universal Best Method", SEC_STAGE2)
add_page_number(s, slide_num)

# central message
central = add_card(s, Inches(1.500), Inches(1.200), Inches(10.300), Inches(1.200), fill=DARK_NAVY)
set_text(central, "No single scoring + detection combination works best for all pathogens",
         size=18, bold=True, color=WHITE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

# 4 evidence cards
evidence = [
    ("ANOVA Interaction", "omega-sq = 0.285", "Scoring x Pathogen interaction\nexplains 28.5% of variance", SEC_STAGE2),
    ("Unique Best Combos", "9 / 9", "Every pathogen has a different\noptimal method pair", GREEN),
    ("Friedman Test", "p = 0.0015", "Rankings differ significantly\nacross pathogens", PURPLE),
    ("LOPO CV", "0 / 9 correct", "Majority voting fails completely\nfor unseen pathogens", RED_ACCENT),
]
for i, (ttl, val, desc, clr) in enumerate(evidence):
    col = i % 2
    row = i // 2
    cx = Inches(0.600) + col * Inches(6.300)
    cy = Inches(2.700) + row * Inches(2.200)
    card = add_card(s, cx, cy, Inches(5.800), Inches(1.950), border=MID_GRAY)
    add_accent_bar(s, cx, cy, Inches(0.080), Inches(1.950), clr)
    add_textbox(s, cx + Inches(0.250), cy + Inches(0.100), Inches(5.300), Inches(0.350),
                ttl, size=13, bold=True, color=clr)
    add_textbox(s, cx + Inches(0.250), cy + Inches(0.500), Inches(5.300), Inches(0.600),
                val, size=28, bold=True, color=DARK_NAVY)
    add_textbox(s, cx + Inches(0.250), cy + Inches(1.150), Inches(5.300), Inches(0.700),
                desc, size=11, color=DARK_GRAY)


# ── SLIDE 26: PAHD ──────────────────────────────────────────────
slide_num += 1
s = content_slide(prs, "PAHD: Pathogen-Adaptive Hotspot Detection", SEC_EXT)
add_page_number(s, slide_num)

# 3-step flow
steps = [
    ("Step 1: Profile", "Extract pathogen profile\n(entropy distribution, genome\nlength, mutation rate, diversity)"),
    ("Step 2: Match", "Compare profile against\nMutBench knowledge base\n(similarity-based retrieval)"),
    ("Step 3: Select", "Recommend optimal scoring +\ndetection combination based\non matched pathogen results"),
]
for i, (ttl, desc) in enumerate(steps):
    cx = Inches(0.600) + i * Inches(4.200)
    cy = Inches(1.200)
    card = add_card(s, cx, cy, Inches(3.900), Inches(2.300), border=MID_GRAY)
    add_rect(s, cx, cy, Inches(3.900), Inches(0.500), fill=PURPLE)
    add_textbox(s, cx, cy + Inches(0.050), Inches(3.900), Inches(0.400),
                ttl, size=14, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    add_textbox(s, cx + Inches(0.200), cy + Inches(0.600), Inches(3.500), Inches(1.500),
                desc, size=12, color=DARK_GRAY)
    if i < 2:
        add_textbox(s, cx + Inches(3.900), cy + Inches(0.650), Inches(0.300), Inches(0.500),
                    ">", size=24, bold=True, color=PURPLE, align=PP_ALIGN.CENTER)

# Results with figure
add_figure(s, os.path.join(FIG_DISS, "new_methodology_comparison.png"),
           Inches(0.400), Inches(3.800), Inches(6.500), Inches(2.800))

# Baseline comparison bars
add_textbox(s, Inches(7.200), Inches(3.700), Inches(5.500), Inches(0.400),
            "MCC Baseline Comparison", size=14, bold=True, color=PURPLE)
bars = [
    ("MutBench Best", "0.390", GREEN),
    ("FreqThresh", "0.248", BLUE),
    ("SWAN", "0.193", ORANGE),
    ("MutClust-Orig", "0.138", RED_ACCENT),
    ("Random", "0.001", GRAY),
]
for i, (name, val, color) in enumerate(bars):
    cy = Inches(4.200) + i * Inches(0.470)
    add_textbox(s, Inches(7.200), cy, Inches(1.800), Inches(0.250),
                name, size=10, bold=True, color=color)
    bar_w = float(val) / 0.4 * 4.5
    add_rect(s, Inches(9.100), cy, Inches(bar_w), Inches(0.250), fill=color)
    add_textbox(s, Inches(9.100) + Inches(bar_w) + Inches(0.100), cy,
                Inches(0.800), Inches(0.250), val, size=9, bold=True, color=color,
                anchor=MSO_ANCHOR.MIDDLE)


# ── SLIDE 27: Phylo + Region-overlap ────────────────────────────
slide_num += 1
s = content_slide(prs, "Phylogenetic Correction & Region Overlap", SEC_EXT)
add_page_number(s, slide_num)

# Phylo card — left
pc = add_card(s, Inches(0.600), Inches(1.200), Inches(5.800), Inches(5.400), border=MID_GRAY)
add_rect(s, Inches(0.600), Inches(1.200), Inches(5.800), Inches(0.600), fill=PURPLE)
add_textbox(s, Inches(0.800), Inches(1.220), Inches(5.400), Inches(0.560),
            "Phylogenetic Non-Independence", size=16, bold=True, color=WHITE,
            anchor=MSO_ANCHOR.MIDDLE)
add_textbox(s, Inches(0.800), Inches(2.000), Inches(5.400), Inches(2.000),
            "Problem:\n"
            "  Closely related sequences share mutations\n"
            "  by descent, not independent selection.\n"
            "  e.g., D614G spread by founder effect.\n\n"
            "Approach:\n"
            "  TreeTime phylogenetic reconstruction\n"
            "  Branch-weighted mutation scoring",
            size=12, color=DARK_GRAY)

# Phylo placeholder
add_placeholder(s, Inches(0.800), Inches(4.200), Inches(5.200), Inches(2.100),
                "[Image Placeholder]\nPhylogenetic Tree Diagram\n(To be inserted)")

# Region overlap card — right
rc = add_card(s, Inches(6.900), Inches(1.200), Inches(5.800), Inches(5.400), border=MID_GRAY)
add_rect(s, Inches(6.900), Inches(1.200), Inches(5.800), Inches(0.600), fill=TEAL_ACCENT)
add_textbox(s, Inches(7.100), Inches(1.220), Inches(5.400), Inches(0.560),
            "Region-Level Overlap Analysis", size=16, bold=True, color=WHITE,
            anchor=MSO_ANCHOR.MIDDLE)
add_textbox(s, Inches(7.100), Inches(2.000), Inches(5.400), Inches(2.000),
            "Motivation:\n"
            "  Position-level MCC may be too strict.\n"
            "  Methods may detect the right region\n"
            "  but miss exact positions.\n\n"
            "Results:\n"
            "  MCC improves from 0.289 to 0.712\n"
            "  with region-level evaluation.",
            size=12, color=DARK_GRAY)

# Region overlap figure
add_figure(s, os.path.join(FIG_MAIN, "lopo_region_precision.png"),
           Inches(7.100), Inches(4.200), Inches(5.200), Inches(2.100))


# ── SLIDE 28: Baseline Comparison ────────────────────────────────
slide_num += 1
s = content_slide(prs, "Scoring-Detection Heatmap & Baseline Comparison", SEC_EXT)
add_page_number(s, slide_num)

add_figure(s, os.path.join(FIG_MAIN, "scoring_detection_heatmap.png"),
           Inches(0.300), Inches(1.100), Inches(7.800), Inches(5.600))

# MCC comparison bars
add_textbox(s, Inches(8.500), Inches(1.200), Inches(4.200), Inches(0.400),
            "MCC Comparison", size=16, bold=True, color=SEC_EXT)
bars = [
    ("MutBench Best", "0.390", GREEN),
    ("FreqThresh", "0.248", BLUE),
    ("SWAN", "0.193", ORANGE),
    ("MutClust-Orig", "0.138", RED_ACCENT),
    ("Random", "0.001", GRAY),
]
for i, (name, val, color) in enumerate(bars):
    cy = Inches(1.800) + i * Inches(1.000)
    add_textbox(s, Inches(8.500), cy, Inches(2.500), Inches(0.350),
                name, size=12, bold=True, color=color)
    bar_w = float(val) / 0.4 * 4.0
    add_rect(s, Inches(8.500), cy + Inches(0.380), Inches(bar_w), Inches(0.350), fill=color)
    add_textbox(s, Inches(8.500) + Inches(bar_w) + Inches(0.100), cy + Inches(0.380),
                Inches(1.000), Inches(0.350), val, size=11, bold=True, color=color,
                anchor=MSO_ANCHOR.MIDDLE)


# ── SLIDE 29: Research Contributions (MOVED after results) ──────
slide_num += 1
s = content_slide(prs, "Research Contributions", SEC_CONCL)
add_page_number(s, slide_num)

contribs = [
    ("C1: MutBench Framework",
     "First systematic benchmark for viral\nmutation hotspot detection with\n"
     "standardized pipeline & evaluation",
     "See S10-S15", SEC_FRAME),
    ("C2: 3-Layer Ground Truth",
     "Adaptive threshold + constrained +\nDMS-based ground truth design\n"
     "reduces single-reference bias",
     "See S13", GREEN),
    ("C3: Cross-Pathogen Evidence",
     "9 pathogens, 2,544 evaluations prove\n"
     "no universal best method exists\n"
     "(interaction omega-sq = 0.285)",
     "See S20-S25", SEC_STAGE2),
    ("C4: PAHD Proof of Concept",
     "Pathogen-Adaptive Hotspot Detection:\n"
     "profile-based method selection\n"
     "outperforms any single approach",
     "See S26", PURPLE),
]
for i, (ttl, desc, ref, clr) in enumerate(contribs):
    col = i % 2
    row = i // 2
    cx = Inches(0.600) + col * Inches(6.300)
    cy = Inches(1.200) + row * Inches(2.700)
    card = add_card(s, cx, cy, Inches(5.800), Inches(2.400), border=MID_GRAY)
    add_accent_bar(s, cx, cy, Inches(0.080), Inches(2.400), clr)
    add_textbox(s, cx + Inches(0.250), cy + Inches(0.150), Inches(5.300), Inches(0.400),
                ttl, size=16, bold=True, color=clr)
    add_textbox(s, cx + Inches(0.250), cy + Inches(0.650), Inches(5.300), Inches(1.300),
                desc, size=12, color=DARK_GRAY)
    # slide reference
    add_textbox(s, cx + Inches(0.250), cy + Inches(1.950), Inches(5.300), Inches(0.300),
                ref, size=9, color=GRAY)


# ── SLIDE 30: Discussion ────────────────────────────────────────
slide_num += 1
s = content_slide(prs, "Discussion", SEC_CONCL)
add_page_number(s, slide_num)

disc = [
    ("Benchmarking Matters",
     "Without standardized evaluation, published methods appear to perform well in isolation "
     "but fail under cross-pathogen comparison. MutBench provides the missing infrastructure "
     "for fair, reproducible comparison of hotspot detection methods."),
    ("Method Selection is Pathogen-Dependent",
     "The strong interaction effect (omega-sq = 0.285) means that recommending a single method "
     "is fundamentally flawed. Pathogen-specific characteristics (genome structure, mutation rate, "
     "selection landscape) determine which approach works best."),
    ("From Benchmark to Algorithm",
     "MutBench is not just a benchmark but a knowledge base. The systematic evaluation across "
     "9 pathogens enables PAHD: data-driven, profile-based method selection that outperforms "
     "any fixed approach."),
]
for i, (ttl, desc) in enumerate(disc):
    cy = Inches(1.200) + i * Inches(1.850)
    card = add_card(s, Inches(0.600), cy, Inches(12.100), Inches(1.650), border=MID_GRAY)
    colors = [SEC_FRAME, SEC_STAGE2, PURPLE]
    add_accent_bar(s, Inches(0.600), cy, Inches(0.080), Inches(1.650), colors[i])
    add_textbox(s, Inches(0.900), cy + Inches(0.120), Inches(11.500), Inches(0.400),
                ttl, size=16, bold=True, color=colors[i])
    add_textbox(s, Inches(0.900), cy + Inches(0.580), Inches(11.500), Inches(0.950),
                desc, size=12, color=DARK_GRAY)


# ── SLIDE 31: Limitations & Future Work ──────────────────────────
slide_num += 1
s = content_slide(prs, "Limitations & Future Work", SEC_CONCL)
add_page_number(s, slide_num)

# 2-column layout
col_data = [
    ("Limitations", RED_ACCENT, [
        "Ground truth approximation\n(no perfect gold standard exists)",
        "Phylogenetic non-independence\nnot fully corrected (TreeTime partial)",
        "Limited to substitution mutations\n(no indels, recombination)",
        "PAHD is proof-of-concept only,\nnot production-ready system",
    ]),
    ("Future Work", BLUE, [
        "Full PAHD implementation with\nlearned pathogen profiles",
        "Integrate phylogenetic correction\n(TreeTime branch weighting)",
        "Extend to indels, recombination,\nand structural variants",
        "Real-time surveillance integration\nfor emerging pathogens",
    ]),
]
for ci, (ttl, color, items) in enumerate(col_data):
    cx = Inches(0.500) + ci * Inches(6.400)
    add_rect(s, cx, Inches(1.200), Inches(6.000), Inches(0.500), fill=color)
    add_textbox(s, cx, Inches(1.210), Inches(6.000), Inches(0.480),
                ttl, size=16, bold=True, color=WHITE, align=PP_ALIGN.CENTER,
                anchor=MSO_ANCHOR.MIDDLE)
    for j, item in enumerate(items):
        iy = Inches(1.850) + j * Inches(1.250)
        card = add_card(s, cx, iy, Inches(6.000), Inches(1.050), border=MID_GRAY)
        add_accent_bar(s, cx, iy, Inches(0.060), Inches(1.050), color)
        add_textbox(s, cx + Inches(0.200), iy + Inches(0.100), Inches(5.600), Inches(0.850),
                    item, size=11, color=DARK_GRAY)


# ── SLIDE 32: Key Takeaway ──────────────────────────────────────
slide_num += 1
s = content_slide(prs, "Key Takeaway", SEC_CONCL)
add_page_number(s, slide_num)

# central message
central = add_card(s, Inches(1.200), Inches(1.300), Inches(10.900), Inches(1.800), fill=DARK_NAVY)
set_text(central,
         "MutBench transforms viral hotspot detection from\n"
         "ad-hoc single-virus evaluation to systematic cross-pathogen benchmarking",
         size=20, bold=True, color=WHITE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

# 4 evidence boxes
evidences = [
    ("9 Pathogens", "Largest cross-pathogen\nbenchmark for hotspot\ndetection", SEC_FRAME),
    ("2,544 Evaluations", "Comprehensive coverage\nof scoring x detection\ncombinations", SEC_STAGE2),
    ("omega-sq = 0.285", "Strong interaction proves\npathogen-adaptive\nselection is needed", PURPLE),
    ("PAHD Concept", "From benchmark insight\nto actionable algorithm\nfor method selection", GREEN),
]
for i, (ttl, desc, clr) in enumerate(evidences):
    cx = Inches(0.500) + i * Inches(3.200)
    cy = Inches(3.500)
    card = add_card(s, cx, cy, Inches(2.900), Inches(3.100), border=MID_GRAY)
    add_accent_bar(s, cx, cy, Inches(0.080), Inches(3.100), clr)
    add_textbox(s, cx, cy + Inches(0.250), Inches(2.900), Inches(0.500),
                ttl, size=16, bold=True, color=clr, align=PP_ALIGN.CENTER)
    add_textbox(s, cx + Inches(0.200), cy + Inches(0.900), Inches(2.500), Inches(2.000),
                desc, size=12, color=DARK_GRAY, align=PP_ALIGN.CENTER)


# ── SLIDE 33: Thank You ─────────────────────────────────────────
slide_num += 1
s = add_blank(prs)
# dark top area
add_rect(s, Inches(0), Inches(0), SLIDE_W, Inches(3.500), fill=DARK_NAVY)
# KNU logo (red emblem)
if os.path.exists(LOGO_EMBLEM):
    s.shapes.add_picture(LOGO_EMBLEM, Inches(0.600), Inches(0.300), Inches(0.650), Inches(0.650))
add_textbox(s, Inches(0.600), Inches(1.200), Inches(12.0), Inches(1.200),
            "Thank You", size=44, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
add_textbox(s, Inches(0.600), Inches(2.400), Inches(12.0), Inches(0.600),
            "Questions & Discussion", size=20, color=RGBColor(0xBB, 0xDE, 0xFB),
            align=PP_ALIGN.CENTER)

# contact info
add_textbox(s, Inches(3.000), Inches(4.200), Inches(7.300), Inches(0.400),
            "Hwijun Kwon", size=22, bold=True, color=DARK_NAVY, align=PP_ALIGN.CENTER)
add_textbox(s, Inches(3.000), Inches(4.700), Inches(7.300), Inches(0.350),
            "Dept. of Computer Science, Kyungpook National University",
            size=14, color=DARK_GRAY, align=PP_ALIGN.CENTER)
add_textbox(s, Inches(3.000), Inches(5.200), Inches(7.300), Inches(0.350),
            "Advisor: Prof. Inuk Jung", size=14, color=DARK_GRAY, align=PP_ALIGN.CENTER)
add_textbox(s, Inches(3.000), Inches(5.700), Inches(7.300), Inches(0.350),
            "March 2026", size=14, color=GRAY, align=PP_ALIGN.CENTER)

# GitHub placeholder
add_placeholder(s, Inches(5.000), Inches(6.200), Inches(3.300), Inches(0.600),
                "[QR Code Placeholder] GitHub Repository")

# bottom bar
add_rect(s, Inches(0), Inches(7.120), SLIDE_W, Inches(0.380), fill=DARK_NAVY)
add_textbox(s, Inches(0.400), Inches(7.140), Inches(10.0), Inches(0.340),
            "Kyungpook National University  |  Dept. of Computer Science  |  Hwijun Kwon",
            size=10, color=WHITE, anchor=MSO_ANCHOR.MIDDLE)


# ══════════════════════════════════════════════════════════════
# SAVE
# ══════════════════════════════════════════════════════════════
os.makedirs(os.path.dirname(OUT), exist_ok=True)
prs.save(OUT)
print(f"Saved: {OUT}")
print(f"Total slides: {len(prs.slides)}")
