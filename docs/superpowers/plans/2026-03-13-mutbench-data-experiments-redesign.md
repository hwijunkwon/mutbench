# MutBench Data & Experiments Redesign Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace unreliable data, add DMS ground truth for multiple pathogens, redesign GT framework, and add meaningful experiments using real data.

**Architecture:** Phase 1 downloads/prepares data (FASTA sequences + DMS datasets). Phase 2 redesigns ground truth into a 3-layer framework (Adaptive/Constrained/DMS). Phase 3 re-runs the 9-pathogen benchmark and adds new experiments (LOPO CV, multi-DMS validation, subsampling robustness, pathogen-level bootstrap). Phase 4 updates the statistical framework and dissertation chapters.

**Tech Stack:** Python 3.12, BioPython, scipy, statsmodels, scikit-learn, NCBI Datasets CLI, matplotlib

---

## Chunk 1: Data Acquisition

### Task 1: Replace H3N2 HA sequences (anonymous headers → real NCBI data)

**Files:**
- Create: `scripts/download_ncbi_sequences.py`
- Replace: `data/influenza/h3n2_ha_sequences.fasta`

- [ ] **Step 1: Write download script with NCBI Datasets or Entrez**

```python
#!/usr/bin/env python3
"""Download viral protein sequences from NCBI for MutBench benchmark."""

import os
import subprocess
import sys
from pathlib import Path
from Bio import Entrez, SeqIO

Entrez.email = "mutbench@example.com"

DATA_DIR = Path(__file__).parent.parent / "data"

PATHOGEN_QUERIES = {
    "h3n2_ha": {
        "term": (
            '"Influenza A virus" AND "H3N2"[Subtype] AND "HA"[Gene] '
            'AND "Homo sapiens"[Host] AND 500:600[Sequence Length] '
            'AND 2010:2024[Collection Date]'
        ),
        "db": "protein",
        "output": DATA_DIR / "influenza" / "h3n2_ha_sequences.fasta",
        "max_seqs": 3000,
        "min_length": 540,
        "max_length": 570,
    },
    "influenza_b_ha": {
        "term": (
            '"Influenza B virus" AND "HA"[Gene] '
            'AND "Homo sapiens"[Host] AND 500:600[Sequence Length] '
            'AND 2010:2024[Collection Date]'
        ),
        "db": "protein",
        "output": DATA_DIR / "influenza" / "influenza_b_ha_sequences.fasta",
        "max_seqs": 3000,
        "min_length": 560,
        "max_length": 590,
    },
    "rsv_f": {
        "term": (
            '"Human respiratory syncytial virus" AND "fusion"[Gene] '
            'AND "Homo sapiens"[Host] AND 500:600[Sequence Length]'
        ),
        "db": "protein",
        "output": DATA_DIR / "rsv" / "rsv_f_sequences.fasta",
        "max_seqs": 3000,
        "min_length": 550,
        "max_length": 580,
    },
}


def download_sequences(name: str, config: dict) -> None:
    """Download and deduplicate sequences from NCBI."""
    print(f"\n{'='*60}")
    print(f"Downloading {name}...")

    # Search
    handle = Entrez.esearch(
        db=config["db"], term=config["term"],
        retmax=config["max_seqs"], usehistory="y"
    )
    results = Entrez.read(handle)
    handle.close()

    count = int(results["Count"])
    print(f"  Found {count} sequences, fetching up to {config['max_seqs']}...")

    webenv = results["WebEnv"]
    query_key = results["QueryKey"]
    ids = results["IdList"]

    # Fetch in batches
    batch_size = 500
    records = []
    for start in range(0, min(len(ids), config["max_seqs"]), batch_size):
        end = min(start + batch_size, len(ids))
        print(f"  Fetching {start+1}-{end}...")
        fetch_handle = Entrez.efetch(
            db=config["db"], rettype="fasta", retmode="text",
            webenv=webenv, query_key=query_key,
            retstart=start, retmax=batch_size
        )
        for record in SeqIO.parse(fetch_handle, "fasta"):
            seq_len = len(record.seq)
            if config["min_length"] <= seq_len <= config["max_length"]:
                records.append(record)
        fetch_handle.close()

    # Deduplicate by sequence
    seen = set()
    unique = []
    for r in records:
        s = str(r.seq)
        if s not in seen:
            seen.add(s)
            unique.append(r)

    print(f"  Total: {len(records)}, Unique: {len(unique)}")

    # Save
    config["output"].parent.mkdir(parents=True, exist_ok=True)
    SeqIO.write(unique, config["output"], "fasta")
    print(f"  Saved to {config['output']}")


def main():
    targets = sys.argv[1:] if len(sys.argv) > 1 else list(PATHOGEN_QUERIES.keys())
    for name in targets:
        if name in PATHOGEN_QUERIES:
            download_sequences(name, PATHOGEN_QUERIES[name])
        else:
            print(f"Unknown target: {name}")

if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Back up current data and run download for H3N2**

```bash
cp data/influenza/h3n2_ha_sequences.fasta data/influenza/h3n2_ha_sequences.fasta.bak
python scripts/download_ncbi_sequences.py h3n2_ha
```

Expected: New FASTA with real NCBI accession headers, 1000+ unique sequences.

- [ ] **Step 3: Verify downloaded data quality**

```bash
grep -c ">" data/influenza/h3n2_ha_sequences.fasta
head -2 data/influenza/h3n2_ha_sequences.fasta  # Should show real accession
```

Expected: Real accession IDs (e.g., `>ABCxxxxx.1 hemagglutinin [Influenza A virus (A/...)]`), 1000+ sequences.

- [ ] **Step 4: Commit**

```bash
git add scripts/download_ncbi_sequences.py
git commit -m "feat: add NCBI sequence download script for reproducible data"
```

---

### Task 2: Replace Influenza B HA sequences

- [ ] **Step 1: Run download**

```bash
cp data/influenza/influenza_b_ha_sequences.fasta data/influenza/influenza_b_ha_sequences.fasta.bak
python scripts/download_ncbi_sequences.py influenza_b_ha
```

- [ ] **Step 2: Verify**

```bash
grep -c ">" data/influenza/influenza_b_ha_sequences.fasta
head -2 data/influenza/influenza_b_ha_sequences.fasta
```

---

### Task 3: Replace RSV F sequences (too many duplicates)

- [ ] **Step 1: Run download**

```bash
cp data/rsv/rsv_f_sequences.fasta data/rsv/rsv_f_sequences.fasta.bak
python scripts/download_ncbi_sequences.py rsv_f
```

- [ ] **Step 2: Verify unique count is higher than current 685**

```bash
grep -c ">" data/rsv/rsv_f_sequences.fasta
```

---

### Task 4: Download DMS data for HIV-1 and H3N2

**Files:**
- Create: `scripts/download_dms_datasets.py`
- Create: `data/dms/hiv1_env_fitness.csv`
- Create: `data/dms/h3n2_ha_fitness.csv`
- Create: `data/dms/rsv_f_fitness.csv`

- [ ] **Step 1: Write DMS download script**

```python
#!/usr/bin/env python3
"""Download DMS fitness datasets from published studies for multi-pathogen GT."""

import os
import urllib.request
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data" / "dms"

DMS_SOURCES = {
    # HIV-1 Env BG505: Haddox et al. 2018 (eLife)
    # Amino acid preferences for each position
    "hiv1_env": {
        "url": "https://raw.githubusercontent.com/jbloomlab/EnvMutationalShiftsPaper/master/results/BG505/BG505_prefs.csv",
        "output": "hiv1_env_prefs_BG505.csv",
        "description": "HIV-1 BG505 Env amino acid preferences (Haddox et al. 2018)",
        "paper": "Haddox et al. 2018 eLife doi:10.7554/eLife.34420",
    },
    # HIV-1 Env BF520: Haddox et al. 2018
    "hiv1_env_bf520": {
        "url": "https://raw.githubusercontent.com/jbloomlab/EnvMutationalShiftsPaper/master/results/BF520/BF520_prefs.csv",
        "output": "hiv1_env_prefs_BF520.csv",
        "description": "HIV-1 BF520 Env amino acid preferences (Haddox et al. 2018)",
        "paper": "Haddox et al. 2018 eLife doi:10.7554/eLife.34420",
    },
    # H3N2 HA Perth/2009: Lee et al. 2018 (PNAS)
    "h3n2_ha": {
        "url": "https://raw.githubusercontent.com/jbloomlab/Perth2009-DMS-Manuscript/master/results/prefs/avgprefs.csv",
        "output": "h3n2_ha_prefs_Perth2009.csv",
        "description": "H3N2 Perth/2009 HA amino acid preferences (Lee et al. 2018)",
        "paper": "Lee et al. 2018 PNAS doi:10.1073/pnas.1806133115",
    },
    # SARS-CoV-2 Spike: already have bloom_fitness/aamut_fitness_all.csv
    # RSV F: dms-vep (2025) - check availability
    "rsv_f": {
        "url": "https://raw.githubusercontent.com/dms-vep/RSV_Long_F_DMS/main/results/summaries/phenotypes_per_mutation.csv",
        "output": "rsv_f_mutation_effects.csv",
        "description": "RSV Long F protein DMS mutation effects (Simonich et al. 2025)",
        "paper": "Simonich et al. 2025 bioRxiv",
    },
}


def download_dms_data():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    for name, config in DMS_SOURCES.items():
        output_path = DATA_DIR / config["output"]
        if output_path.exists():
            print(f"  [SKIP] {name}: {output_path} already exists")
            continue

        print(f"\nDownloading {name}...")
        print(f"  Source: {config['url']}")
        print(f"  Paper: {config['paper']}")
        try:
            urllib.request.urlretrieve(config["url"], output_path)
            # Verify
            with open(output_path) as f:
                lines = f.readlines()
            print(f"  Saved: {output_path} ({len(lines)} lines)")
            print(f"  Header: {lines[0].strip()[:100]}")
        except Exception as e:
            print(f"  [ERROR] Failed to download {name}: {e}")
            # Try alternative URL or log for manual download
            if output_path.exists():
                output_path.unlink()


if __name__ == "__main__":
    download_dms_data()
```

- [ ] **Step 2: Run download**

```bash
python scripts/download_dms_datasets.py
```

Expected: CSV files in `data/dms/` for HIV-1, H3N2, and RSV.

- [ ] **Step 3: Verify downloaded DMS data**

```bash
wc -l data/dms/*.csv
head -3 data/dms/hiv1_env_prefs_BG505.csv
head -3 data/dms/h3n2_ha_prefs_Perth2009.csv
```

- [ ] **Step 4: If RSV URL fails, note for manual download**

RSV DMS (dms-vep/RSV_Long_F_DMS) is very new (2025). If the URL structure has changed, manually check the GitHub repo and update the URL.

- [ ] **Step 5: Commit**

```bash
git add scripts/download_dms_datasets.py data/dms/
git commit -m "feat: download DMS fitness data for HIV-1, H3N2, RSV ground truth"
```

---

## Chunk 2: Ground Truth Redesign

### Task 5: Implement 3-layer ground truth framework

**Files:**
- Create: `tools/mutbench/ground_truth/multilayer_gt.py`
- Modify: `tools/mutbench/ground_truth/__init__.py`

- [ ] **Step 1: Write the 3-layer GT module**

```python
"""Three-layer ground truth framework for MutBench.

Layer A (Adaptive): Positions under positive/diversifying selection
  - Convergent evolution sites (documented independent emergence)
  - Sites with dN/dS > 1 from published analyses

Layer B (Constrained): Positions under strong purifying selection
  - Conserved functional residues (fusion peptides, structural cysteines)
  - Sites with dN/dS < 0.1
  - TRUE NEGATIVES: should NOT be detected as hotspots

Layer C (DMS-functional): Experimentally validated functional sites
  - Deep mutational scanning fitness effects
  - Independent of sequence-based detection methods
"""

from typing import Dict, Set, Tuple


def get_gt_adaptive(pathogen: str, max_len: int) -> Set[int]:
    """Layer A: Positions with evidence of positive selection.

    These are TRUE HOTSPOTS — positions where mutations accumulate
    at elevated rates due to selection pressure.
    Returns 0-based positions.
    """
    gt = set()

    if pathogen == "SARS-CoV-2":
        # Convergent evolution positions across independent VOC lineages
        # Sources: Carabelli et al. 2023 Nat Rev Microbiol, Cao et al. 2023 Nature
        convergent = {
            484, 501, 452, 346, 417, 681,  # High-confidence convergent
            478, 614, 655, 156, 18, 19, 20,  # Recurrent across lineages
            371, 373, 375, 376, 405, 408,  # Omicron RBD convergent
            440, 446, 460, 490, 493, 498,  # BA.2/BA.5/XBB convergent
        }
        gt = {p for p in convergent if p < max_len}

    elif pathogen == "H3N2":
        # Koel et al. 2013 Science: cluster-transition positions
        # + Wolf et al. 2006: antigenic drift positions
        gt = {p for p in {
            145, 155, 156, 158, 159, 189, 193,  # Koel cluster transitions
            137, 142, 144, 186, 190, 192, 196,  # Additional antigenic drift
            131, 135, 138, 140, 147, 148,  # Site A positive selection
            157, 160, 163, 164, 165,  # Site B positive selection
        } if p < max_len}

    elif pathogen == "Norovirus":
        # Lindesmith et al. 2012, 2013: GII.4 epochal variant positions
        # Positions that change between pandemic variants
        gt = {p for p in {
            297, 298, 310, 333, 340, 373, 376,  # Blockade epitope A/B
            340, 341, 345, 372, 373, 376, 394, 395, 397,  # HBGA binding vicinity
            310, 333, 340, 356, 357, 368,  # Inter-variant divergent
        } if p < max_len}

    elif pathogen == "HIV-1":
        # Moore & Williamson 2015: sites under positive selection in Env
        # Pond & Frost: FUBAR/FEL identified sites
        gt = {p for p in {
            # V1/V2 loop: hypervariable
            132, 138, 141, 152, 155, 160, 165, 167, 169, 171,
            # V3 loop: tropism-determining, under selection
            301, 305, 308, 315, 317, 319, 321, 323, 325,
            # V4/V5: hypervariable
            385, 392, 395, 396, 460, 462, 463,
        } if p < max_len}

    elif pathogen == "Dengue":
        # Twiddy et al. 2002: inter-serotype positive selection
        # Holmes 2003: serotype-defining positions
        gt = {p for p in {
            # DIII: serotype-specific epitopes under immune selection
            305, 307, 310, 312, 329, 330, 332, 335,
            337, 339, 340, 360, 361, 364, 380, 383, 384,
            # Domain II: inter-serotype variable
            52, 71, 83, 120, 155, 157, 161,
        } if p < max_len}

    elif pathogen == "RSV":
        # Mas et al. 2018: antigenic site variability
        # Sullender 2000: escape mutation positions
        gt = {p for p in {
            # Site II: palivizumab escape
            255, 256, 259, 260, 262, 268, 272, 275, 276,
            # Site V: variable across subgroups
            148, 152, 155, 159, 163, 173, 174,
            # Site IV: partially variable
            422, 425, 427, 429,
        } if p < max_len}

    elif pathogen == "Influenza_B":
        # Ni et al. 2013: antigenic drift positions
        # Wang et al. 2008: HA antigenic characterization
        gt = {p for p in {
            122, 127, 129, 141, 147, 150, 151, 162, 163,
            164, 165, 175, 177, 179, 194, 196, 197,
        } if p < max_len}

    elif pathogen == "MERS":
        # Kim et al. 2016: RBD escape mutations
        # Tang et al. 2014: positively selected sites
        gt = {p for p in {
            484, 506, 510, 511, 530, 534, 537, 539, 542,
        } if p < max_len}

    elif pathogen == "HCV":
        # Sheridan et al.: HVR1 positions under host-driven selection
        # Dowd et al.: broadly neutralizing Ab escape
        gt = {p for p in {
            # HVR1: highly variable
            *range(1, 28),
            # HVR2: highly variable
            *range(77, 104),
        } if p < max_len}

    return gt


def get_gt_constrained(pathogen: str, max_len: int) -> Set[int]:
    """Layer B: Positions under strong purifying selection.

    TRUE NEGATIVES — should NOT be detected as hotspots.
    A good method should have LOW recall against this set.
    Returns 0-based positions.
    """
    gt = set()

    if pathogen == "SARS-CoV-2":
        # Fusion peptide, HR1/HR2: highly conserved structural elements
        gt = set()
        for start, end in [
            (816, 833),   # Fusion peptide
            (912, 984),   # HR1
            (1163, 1213), # HR2
        ]:
            gt.update(range(start, min(end + 1, max_len)))
        # Structural cysteines (invariant disulfide bonds)
        cysteines = {15, 136, 166, 291, 301, 336, 361, 379, 391, 432, 480, 488}
        gt.update(p for p in cysteines if p < max_len)

    elif pathogen == "H3N2":
        # Receptor binding site core (conserved for sialic acid binding)
        gt = {p for p in {98, 134, 136, 153, 183, 194, 195, 225, 226, 228} if p < max_len}

    elif pathogen == "Norovirus":
        # Shell domain (highly conserved)
        gt = {p for p in range(1, 230) if p < max_len}

    elif pathogen == "HIV-1":
        # Conserved CD4 binding site contact residues
        gt = {p for p in {124, 125, 126, 196, 198, 279, 280, 281, 282, 283, 365, 366, 367, 368, 370, 425, 426, 427, 428, 429, 430, 431, 432, 455, 456, 457, 458, 459, 469, 471, 473, 474, 476} if p < max_len}

    elif pathogen == "Dengue":
        # Fusion loop: extremely conserved across all flaviviruses
        gt = {p for p in range(98, 111) if p < max_len}
        # Structural disulfides
        gt.update(p for p in {3, 30, 60, 74, 92, 105, 116, 121, 137, 166, 176, 189} if p < max_len)

    elif pathogen == "RSV":
        # Fusion peptide: highly conserved
        gt = {p for p in range(137, 155) if p < max_len}

    elif pathogen == "Influenza_B":
        # Receptor binding site core
        gt = {p for p in {95, 141, 159, 190, 193, 194, 195, 225, 226, 228} if p < max_len}

    elif pathogen == "MERS":
        # Fusion peptide
        gt = {p for p in range(888, 912) if p < max_len}
        # HR1 and HR2
        gt.update(p for p in range(974, 1060) if p < max_len)

    elif pathogen == "HCV":
        # CD81 binding site: functionally constrained
        gt = {p for p in {418, 420, 422, 424, 436, 438, 441, 442, 503, 506, 528, 529, 530, 535} if p < max_len}

    return gt


def get_gt_dms(pathogen: str, dms_data: dict, threshold_percentile: float = 80) -> Set[int]:
    """Layer C: DMS-derived functional positions.

    Positions where mutations have high phenotypic effect (|fitness| > threshold).
    Only available for pathogens with published DMS data.

    Args:
        pathogen: pathogen name
        dms_data: dict mapping position (0-based) to mean absolute fitness effect
        threshold_percentile: percentile cutoff for "high effect" (default 80th)

    Returns: set of 0-based positions
    """
    if not dms_data:
        return set()

    import numpy as np
    values = list(dms_data.values())
    threshold = np.percentile(values, threshold_percentile)
    return {pos for pos, val in dms_data.items() if val >= threshold}


def get_all_gt_layers(
    pathogen: str, max_len: int, dms_data: dict = None
) -> Dict[str, Set[int]]:
    """Get all three GT layers for a pathogen.

    Returns dict with keys: 'adaptive', 'constrained', 'dms'
    """
    return {
        "adaptive": get_gt_adaptive(pathogen, max_len),
        "constrained": get_gt_constrained(pathogen, max_len),
        "dms": get_gt_dms(pathogen, dms_data) if dms_data else set(),
    }


def evaluate_multilayer(
    detected: Set[int], gt_layers: Dict[str, Set[int]], genome_length: int
) -> Dict[str, float]:
    """Evaluate detection against all GT layers.

    Returns dict with metrics per layer + composite score.
    """
    from tools.mutbench.evaluation.metrics import precision, recall, f1_score, enrichment_ratio

    results = {}

    # Layer A: Adaptive (primary — higher is better)
    gt_a = gt_layers["adaptive"]
    if gt_a:
        results["adaptive_precision"] = precision(detected, gt_a)
        results["adaptive_recall"] = recall(detected, gt_a)
        results["adaptive_f1"] = f1_score(detected, gt_a)
        results["adaptive_enrichment"] = enrichment_ratio(detected, gt_a, genome_length)

    # Layer B: Constrained (negative control — lower recall is better)
    gt_b = gt_layers["constrained"]
    if gt_b:
        results["constrained_recall"] = recall(detected, gt_b)
        results["constrained_false_positive_rate"] = (
            len(detected & gt_b) / len(gt_b) if gt_b else 0
        )

    # Layer C: DMS (supplementary)
    gt_c = gt_layers.get("dms", set())
    if gt_c:
        results["dms_precision"] = precision(detected, gt_c)
        results["dms_recall"] = recall(detected, gt_c)
        results["dms_f1"] = f1_score(detected, gt_c)

    # Composite: adaptive MCC penalized by constrained false positives
    if gt_a and gt_b:
        alpha = 0.3  # penalty weight for false positives on constrained sites
        adaptive_f1 = results.get("adaptive_f1", 0)
        constrained_fpr = results.get("constrained_false_positive_rate", 0)
        results["composite_score"] = adaptive_f1 - alpha * constrained_fpr

    return results
```

- [ ] **Step 2: Update `__init__.py` to export new GT functions**

Add to `tools/mutbench/ground_truth/__init__.py`:
```python
from .multilayer_gt import (
    get_gt_adaptive,
    get_gt_constrained,
    get_gt_dms,
    get_all_gt_layers,
    evaluate_multilayer,
)
```

- [ ] **Step 3: Commit**

```bash
git add tools/mutbench/ground_truth/multilayer_gt.py tools/mutbench/ground_truth/__init__.py
git commit -m "feat: add 3-layer ground truth framework (adaptive/constrained/DMS)"
```

---

### Task 6: Create DMS data loaders for HIV-1 and H3N2

**Files:**
- Modify: `tools/mutbench/ground_truth/dms_loader.py`

- [ ] **Step 1: Add loaders for HIV-1 and H3N2 DMS preference data**

The Bloom lab DMS preference files have format: `site, A, C, D, E, F, G, H, I, K, L, M, N, P, Q, R, S, T, V, W, Y` where values are amino acid preferences (higher = more tolerated).

Add functions to `dms_loader.py`:

```python
def load_bloom_preferences(filepath: str) -> dict:
    """Load Bloom lab amino acid preference CSV.

    Returns dict mapping 0-based position to mean preference diversity.
    High diversity = position tolerates many mutations = potential hotspot.
    Low diversity = position is constrained = not a hotspot.
    """
    import pandas as pd
    import numpy as np

    df = pd.read_csv(filepath)
    # Column 'site' is 1-based position
    # Remaining columns are AA preferences
    aa_cols = [c for c in df.columns if c != 'site' and len(c) == 1]

    position_scores = {}
    for _, row in df.iterrows():
        pos = int(row['site']) - 1  # Convert to 0-based
        prefs = [row[aa] for aa in aa_cols]
        # Shannon entropy of preferences as diversity measure
        prefs = np.array(prefs)
        prefs = prefs / prefs.sum()  # Normalize
        entropy = -np.sum(prefs * np.log2(prefs + 1e-10))
        position_scores[pos] = entropy

    return position_scores


def load_sars2_fitness(filepath: str) -> dict:
    """Load SARS-CoV-2 Bloom fitness data (aamut_fitness_all.csv).

    Returns dict mapping 0-based Spike AA position to mean absolute fitness effect.
    """
    import pandas as pd
    import numpy as np

    df = pd.read_csv(filepath)
    # Group by position, compute mean absolute fitness
    site_fitness = df.groupby('site')['fitness'].apply(
        lambda x: np.mean(np.abs(x))
    ).to_dict()

    # Convert to 0-based
    return {int(pos) - 1: val for pos, val in site_fitness.items()}
```

- [ ] **Step 2: Commit**

```bash
git add tools/mutbench/ground_truth/dms_loader.py
git commit -m "feat: add DMS preference loaders for HIV-1, H3N2, SARS-CoV-2"
```

---

## Chunk 3: Re-run Benchmark & New Experiments

### Task 7: Re-run 9-pathogen benchmark with new data

**Files:**
- Modify: `scripts/run_extended_benchmark.py` (update GT to use multilayer)
- Create: `scripts/run_multilayer_benchmark.py`

- [ ] **Step 1: Write multilayer benchmark script**

This script runs the 9-pathogen benchmark with the new 3-layer GT framework, using whatever FASTA files are currently in the data directories (including newly downloaded ones).

```python
#!/usr/bin/env python3
"""Run 9-pathogen benchmark with 3-layer ground truth framework."""

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from pathlib import Path
import pandas as pd
import numpy as np

# Reuse existing infrastructure
from scripts.run_extended_benchmark import (
    load_fasta, compute_features, compute_scores,
    get_all_detectors, postprocess, compute_mcc, compute_f1, compute_enrichment
)
from tools.mutbench.ground_truth.multilayer_gt import (
    get_gt_adaptive, get_gt_constrained, get_all_gt_layers, evaluate_multilayer
)
from tools.mutbench.ground_truth.dms_loader import (
    load_bloom_preferences, load_sars2_fitness
)

DATA_DIR = Path(__file__).parent.parent / "data"
RESULTS_DIR = Path(__file__).parent.parent / "results" / "mutbench"

PATHOGENS = {
    "SARS-CoV-2": DATA_DIR / "ncbi_temporal" / "spike_2020_H1.fasta",
    "H3N2": DATA_DIR / "influenza" / "h3n2_ha_sequences.fasta",
    "Norovirus": DATA_DIR / "norovirus" / "norovirus_vp1_sequences.fasta",
    "HIV-1": DATA_DIR / "cross_pathogen" / "hiv1_gp120_sequences.fasta",
    "Dengue": DATA_DIR / "dengue" / "dengue_e_sequences.fasta",
    "RSV": DATA_DIR / "rsv" / "rsv_f_sequences.fasta",
    "Influenza_B": DATA_DIR / "influenza" / "influenza_b_ha_sequences.fasta",
    "MERS": DATA_DIR / "mers" / "mers_spike_sequences.fasta",
    "HCV": DATA_DIR / "hcv" / "hcv_e2_sequences.fasta",
}

DMS_DATA_DIR = DATA_DIR / "dms"

DMS_FILES = {
    "SARS-CoV-2": DATA_DIR / "mutbench" / "aamut_fitness_all.csv",
    "HIV-1": DMS_DATA_DIR / "hiv1_env_prefs_BG505.csv",
    "H3N2": DMS_DATA_DIR / "h3n2_ha_prefs_Perth2009.csv",
}


def load_dms_for_pathogen(pathogen: str) -> dict:
    """Load DMS data if available for this pathogen."""
    if pathogen not in DMS_FILES:
        return {}
    path = DMS_FILES[pathogen]
    if not path.exists():
        print(f"  DMS file not found: {path}")
        return {}
    if pathogen == "SARS-CoV-2":
        return load_sars2_fitness(str(path))
    else:
        return load_bloom_preferences(str(path))


def main():
    all_results = []

    for pathogen, fasta_path in PATHOGENS.items():
        print(f"\n{'='*60}")
        print(f"Processing {pathogen}...")

        if not fasta_path.exists():
            print(f"  [SKIP] FASTA not found: {fasta_path}")
            continue

        # Load and compute
        sequences = load_fasta(str(fasta_path))
        min_len = min(len(s) for s in sequences)
        sequences = [s[:min_len] for s in sequences]
        print(f"  Sequences: {len(sequences)}, Length: {min_len}")

        # Unique count
        unique_count = len(set(sequences))
        print(f"  Unique: {unique_count}")

        features = compute_features(sequences)
        all_scores = compute_scores(features)

        # Load GT layers
        dms_data = load_dms_for_pathogen(pathogen)
        gt_layers = get_all_gt_layers(pathogen, min_len, dms_data)

        print(f"  GT Adaptive: {len(gt_layers['adaptive'])} positions")
        print(f"  GT Constrained: {len(gt_layers['constrained'])} positions")
        print(f"  GT DMS: {len(gt_layers['dms'])} positions")

        # Get detectors
        detectors = get_all_detectors()

        # Evaluate each scoring × detection combo against all GT layers
        for score_name, scores in all_scores.items():
            if np.all(scores == 0):
                continue
            for det_name, det_family, det_fn in detectors:
                try:
                    detected_raw, _ = det_fn(scores)
                    detected = postprocess(detected_raw, min_len)
                    detected_set = set(detected)
                except Exception:
                    continue

                # Evaluate against Layer A (adaptive) — primary metric
                gt_a = gt_layers["adaptive"]
                if not gt_a:
                    continue

                mcc = compute_mcc(detected, list(gt_a), min_len)
                p, r, f1 = compute_f1(detected, list(gt_a), min_len)
                enrich = compute_enrichment(detected, list(gt_a), min_len)

                # Evaluate against Layer B (constrained) — false positive check
                gt_b = gt_layers["constrained"]
                constrained_fpr = 0.0
                if gt_b and detected_set:
                    constrained_fpr = len(detected_set & gt_b) / len(gt_b)

                # Evaluate against Layer C (DMS) if available
                gt_c = gt_layers["dms"]
                dms_f1 = None
                if gt_c:
                    _, _, dms_f1 = compute_f1(detected, list(gt_c), min_len)

                row = {
                    "pathogen": pathogen,
                    "score": score_name,
                    "detector": det_name,
                    "family": det_family,
                    "n_sequences": len(sequences),
                    "n_unique": unique_count,
                    "seq_length": min_len,
                    "gt_adaptive_size": len(gt_a),
                    "gt_constrained_size": len(gt_b),
                    "gt_dms_size": len(gt_c) if gt_c else 0,
                    "mcc_adaptive": mcc,
                    "f1_adaptive": f1,
                    "precision_adaptive": p,
                    "recall_adaptive": r,
                    "enrichment_adaptive": enrich,
                    "constrained_fpr": constrained_fpr,
                    "dms_f1": dms_f1,
                    "n_detected": len(detected),
                }
                all_results.append(row)

    # Save
    df = pd.DataFrame(all_results)
    output_path = RESULTS_DIR / "multilayer_9pathogen_results.csv"
    df.to_csv(output_path, index=False)
    print(f"\nSaved {len(df)} evaluations to {output_path}")

    # Summary statistics
    print(f"\n{'='*60}")
    print("Summary by pathogen:")
    summary = df.groupby("pathogen").agg({
        "mcc_adaptive": "max",
        "constrained_fpr": "min",
        "n_sequences": "first",
        "n_unique": "first",
    }).round(4)
    print(summary)


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Run the multilayer benchmark**

```bash
cd /proj/paper && python scripts/run_multilayer_benchmark.py
```

Expected: `results/mutbench/multilayer_9pathogen_results.csv` with ~3,321 rows, new GT-based metrics.

- [ ] **Step 3: Commit**

```bash
git add scripts/run_multilayer_benchmark.py results/mutbench/multilayer_9pathogen_results.csv
git commit -m "feat: run 9-pathogen benchmark with 3-layer GT framework"
```

---

### Task 8: LOPO 9-pathogen cross-validation

**Files:**
- Create: `scripts/run_lopo_9pathogen.py`

- [ ] **Step 1: Write LOPO CV script**

```python
#!/usr/bin/env python3
"""Leave-One-Pathogen-Out cross-validation for 9 pathogens.

For each held-out pathogen:
  1. Select best combo (score+detector) based on mean MCC across 8 training pathogens
  2. Evaluate that combo on the held-out pathogen
  3. Compare with oracle (best possible MCC on held-out)
  4. The gap = oracle - LOPO shows how much performance is lost by generalizing
"""

import pandas as pd
import numpy as np
from pathlib import Path

RESULTS_DIR = Path(__file__).parent.parent / "results" / "mutbench"


def run_lopo():
    # Load multilayer results (or fall back to extended_9pathogen_results.csv)
    multilayer_path = RESULTS_DIR / "multilayer_9pathogen_results.csv"
    extended_path = RESULTS_DIR / "extended_9pathogen_results.csv"

    if multilayer_path.exists():
        df = pd.read_csv(multilayer_path)
        mcc_col = "mcc_adaptive"
    else:
        df = pd.read_csv(extended_path)
        mcc_col = "mcc"

    pathogens = sorted(df["pathogen"].unique())
    print(f"Pathogens: {pathogens}")
    print(f"Total evaluations: {len(df)}")

    # Create combo identifier
    df["combo"] = df["score"] + " + " + df["detector"]

    results = []

    for held_out in pathogens:
        train_pathogens = [p for p in pathogens if p != held_out]
        train_df = df[df["pathogen"].isin(train_pathogens)]
        test_df = df[df["pathogen"] == held_out]

        # Best combo by mean MCC across training pathogens
        combo_means = train_df.groupby("combo")[mcc_col].mean()
        best_combo = combo_means.idxmax()
        train_mcc = combo_means[best_combo]

        # Evaluate best combo on held-out
        test_row = test_df[test_df["combo"] == best_combo]
        test_mcc = test_row[mcc_col].values[0] if len(test_row) > 0 else 0.0

        # Oracle: best possible on held-out
        oracle_mcc = test_df[mcc_col].max()
        oracle_combo = test_df.loc[test_df[mcc_col].idxmax(), "combo"]

        gap = oracle_mcc - test_mcc
        ratio = test_mcc / oracle_mcc if oracle_mcc > 0 else 0

        results.append({
            "held_out": held_out,
            "best_train_combo": best_combo,
            "train_mean_mcc": round(train_mcc, 4),
            "test_mcc": round(test_mcc, 4),
            "oracle_mcc": round(oracle_mcc, 4),
            "oracle_combo": oracle_combo,
            "gap": round(gap, 4),
            "generalization_ratio": round(ratio, 4),
            "combo_match": best_combo == oracle_combo,
        })

        print(f"\n{held_out}:")
        print(f"  Train best: {best_combo} (mean MCC={train_mcc:.4f})")
        print(f"  Test MCC: {test_mcc:.4f}")
        print(f"  Oracle: {oracle_combo} (MCC={oracle_mcc:.4f})")
        print(f"  Gap: {gap:.4f}, Ratio: {ratio:.4f}")

    results_df = pd.DataFrame(results)
    output_path = RESULTS_DIR / "lopo_9pathogen_cv.csv"
    results_df.to_csv(output_path, index=False)

    # Summary
    print(f"\n{'='*60}")
    print(f"Mean generalization ratio: {results_df['generalization_ratio'].mean():.4f}")
    print(f"Mean gap: {results_df['gap'].mean():.4f}")
    print(f"Combo matches: {results_df['combo_match'].sum()}/{len(pathogens)}")
    print(f"\nSaved to {output_path}")


if __name__ == "__main__":
    run_lopo()
```

- [ ] **Step 2: Run LOPO**

```bash
python scripts/run_lopo_9pathogen.py
```

- [ ] **Step 3: Commit**

```bash
git add scripts/run_lopo_9pathogen.py results/mutbench/lopo_9pathogen_cv.csv
git commit -m "feat: add LOPO 9-pathogen cross-validation"
```

---

### Task 9: Subsampling robustness test

**Files:**
- Create: `scripts/run_subsampling_robustness.py`

- [ ] **Step 1: Write subsampling script**

```python
#!/usr/bin/env python3
"""Subsampling robustness: how stable are rankings under sequence sampling bias?

For each pathogen, subsample sequences at various rates and measure:
1. MCC stability (compared to full dataset)
2. Rank correlation of position scores (Spearman rho)
3. Which scoring/detection families are most robust
"""

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from pathlib import Path
import pandas as pd
import numpy as np
from scipy.stats import spearmanr

from scripts.run_extended_benchmark import (
    load_fasta, compute_features, compute_scores,
    get_all_detectors, postprocess, compute_mcc
)
from tools.mutbench.ground_truth.multilayer_gt import get_gt_adaptive

DATA_DIR = Path(__file__).parent.parent / "data"
RESULTS_DIR = Path(__file__).parent.parent / "results" / "mutbench"

PATHOGENS = {
    "SARS-CoV-2": DATA_DIR / "ncbi_temporal" / "spike_2020_H1.fasta",
    "H3N2": DATA_DIR / "influenza" / "h3n2_ha_sequences.fasta",
    "HIV-1": DATA_DIR / "cross_pathogen" / "hiv1_gp120_sequences.fasta",
    "Dengue": DATA_DIR / "dengue" / "dengue_e_sequences.fasta",
    "RSV": DATA_DIR / "rsv" / "rsv_f_sequences.fasta",
    "MERS": DATA_DIR / "mers" / "mers_spike_sequences.fasta",
    "HCV": DATA_DIR / "hcv" / "hcv_e2_sequences.fasta",
    "Norovirus": DATA_DIR / "norovirus" / "norovirus_vp1_sequences.fasta",
    "Influenza_B": DATA_DIR / "influenza" / "influenza_b_ha_sequences.fasta",
}

SUBSAMPLE_RATES = [0.1, 0.25, 0.5, 0.75, 1.0]
N_REPS = 10  # repetitions per rate
TOP_COMBOS = 5  # evaluate top N combos per pathogen


def main():
    rng = np.random.RandomState(42)
    all_results = []

    for pathogen, fasta_path in PATHOGENS.items():
        print(f"\n{'='*60}")
        print(f"{pathogen}...")

        if not fasta_path.exists():
            continue

        sequences = load_fasta(str(fasta_path))
        min_len = min(len(s) for s in sequences)
        sequences = [s[:min_len] for s in sequences]
        n_total = len(sequences)

        gt = get_gt_adaptive(pathogen, min_len)
        if not gt:
            continue

        # Full dataset reference
        features_full = compute_features(sequences)
        scores_full = compute_scores(features_full)
        detectors = get_all_detectors()

        # Pick a representative scoring + top detectors
        ref_score_name = "E*rare"
        ref_scores = scores_full[ref_score_name]

        for rate in SUBSAMPLE_RATES:
            n_sub = max(50, int(n_total * rate))

            for rep in range(N_REPS):
                if rate >= 1.0 and rep > 0:
                    break  # full dataset, no repetition needed

                # Subsample
                idx = rng.choice(n_total, size=min(n_sub, n_total), replace=False)
                sub_seqs = [sequences[i] for i in idx]

                features_sub = compute_features(sub_seqs)
                scores_sub = compute_scores(features_sub)

                # Score correlation with full dataset
                sub_score = scores_sub[ref_score_name]
                score_len = min(len(ref_scores), len(sub_score))
                rho, _ = spearmanr(ref_scores[:score_len], sub_score[:score_len])

                # MCC for a few detectors
                for det_name, det_family, det_fn in detectors[:10]:
                    try:
                        detected, _ = det_fn(sub_score)
                        detected = postprocess(detected, min_len)
                        mcc = compute_mcc(detected, list(gt), min_len)
                    except Exception:
                        mcc = 0.0

                    all_results.append({
                        "pathogen": pathogen,
                        "subsample_rate": rate,
                        "n_sequences": len(sub_seqs),
                        "rep": rep,
                        "score_rho": round(rho, 4),
                        "detector": det_name,
                        "family": det_family,
                        "mcc": round(mcc, 4),
                    })

        print(f"  Done ({n_total} seqs, {len(SUBSAMPLE_RATES)} rates)")

    df = pd.DataFrame(all_results)
    output_path = RESULTS_DIR / "subsampling_robustness.csv"
    df.to_csv(output_path, index=False)
    print(f"\nSaved {len(df)} rows to {output_path}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Run**

```bash
python scripts/run_subsampling_robustness.py
```

- [ ] **Step 3: Commit**

```bash
git add scripts/run_subsampling_robustness.py results/mutbench/subsampling_robustness.csv
git commit -m "feat: add subsampling robustness analysis for 9 pathogens"
```

---

### Task 10: Pathogen-level bootstrap CI (replace synthetic bootstrap)

**Files:**
- Create: `scripts/run_pathogen_bootstrap.py`

- [ ] **Step 1: Write pathogen-level bootstrap**

```python
#!/usr/bin/env python3
"""Pathogen-level bootstrap CI for method rankings.

Bootstrap resamples pathogens (not synthetic regions) to estimate
uncertainty of mean MCC across the 9-pathogen benchmark.
"""

import pandas as pd
import numpy as np
from pathlib import Path

RESULTS_DIR = Path(__file__).parent.parent / "results" / "mutbench"
N_BOOT = 10000
SEED = 42


def bca_ci(data, stat_fn, n_boot=10000, alpha=0.05, rng=None):
    """BCa bootstrap confidence interval."""
    if rng is None:
        rng = np.random.RandomState(SEED)

    n = len(data)
    theta_hat = stat_fn(data)

    # Bootstrap distribution
    boot_thetas = np.array([
        stat_fn(data[rng.choice(n, n, replace=True)])
        for _ in range(n_boot)
    ])

    # Bias correction (z0)
    z0 = np.percentile(boot_thetas, 50)
    from scipy.stats import norm
    z0 = norm.ppf(np.mean(boot_thetas < theta_hat))

    # Acceleration (a) via jackknife
    jack_thetas = np.array([
        stat_fn(np.delete(data, i)) for i in range(n)
    ])
    jack_mean = jack_thetas.mean()
    num = np.sum((jack_mean - jack_thetas) ** 3)
    den = 6 * (np.sum((jack_mean - jack_thetas) ** 2) ** 1.5)
    a = num / den if den != 0 else 0

    # Adjusted percentiles
    z_alpha = norm.ppf(alpha / 2)
    z_1alpha = norm.ppf(1 - alpha / 2)

    a1 = norm.cdf(z0 + (z0 + z_alpha) / (1 - a * (z0 + z_alpha)))
    a2 = norm.cdf(z0 + (z0 + z_1alpha) / (1 - a * (z0 + z_1alpha)))

    ci_lower = np.percentile(boot_thetas, 100 * a1)
    ci_upper = np.percentile(boot_thetas, 100 * a2)

    return theta_hat, ci_lower, ci_upper, z0, a


def main():
    # Load results
    multilayer_path = RESULTS_DIR / "multilayer_9pathogen_results.csv"
    extended_path = RESULTS_DIR / "extended_9pathogen_results.csv"

    if multilayer_path.exists():
        df = pd.read_csv(multilayer_path)
        mcc_col = "mcc_adaptive"
    else:
        df = pd.read_csv(extended_path)
        mcc_col = "mcc"

    df["combo"] = df["score"] + " + " + df["detector"]
    pathogens = sorted(df["pathogen"].unique())

    rng = np.random.RandomState(SEED)

    # For top-20 combos by mean MCC, compute bootstrap CI
    combo_means = df.groupby("combo")[mcc_col].mean().sort_values(ascending=False)
    top_combos = combo_means.head(20).index.tolist()

    results = []
    for combo in top_combos:
        combo_df = df[df["combo"] == combo]

        # Get MCC per pathogen
        mcc_per_pathogen = np.array([
            combo_df[combo_df["pathogen"] == p][mcc_col].values[0]
            if len(combo_df[combo_df["pathogen"] == p]) > 0 else 0.0
            for p in pathogens
        ])

        theta, ci_lo, ci_hi, z0, a = bca_ci(
            mcc_per_pathogen, np.mean, n_boot=N_BOOT, rng=rng
        )

        results.append({
            "combo": combo,
            "mean_mcc": round(theta, 4),
            "ci_lower": round(ci_lo, 4),
            "ci_upper": round(ci_hi, 4),
            "ci_width": round(ci_hi - ci_lo, 4),
            "z0": round(z0, 4),
            "acceleration": round(a, 4),
            "n_pathogens": len(pathogens),
            "n_bootstrap": N_BOOT,
        })

    results_df = pd.DataFrame(results)
    output_path = RESULTS_DIR / "pathogen_bootstrap_ci.csv"
    results_df.to_csv(output_path, index=False)
    print(results_df.to_string())
    print(f"\nSaved to {output_path}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Run**

```bash
python scripts/run_pathogen_bootstrap.py
```

- [ ] **Step 3: Commit**

```bash
git add scripts/run_pathogen_bootstrap.py results/mutbench/pathogen_bootstrap_ci.csv
git commit -m "feat: add pathogen-level BCa bootstrap CI (replaces synthetic bootstrap)"
```

---

## Chunk 4: Statistical Framework Update

### Task 11: Update ANOVA to three-way with omega-squared

**Files:**
- Create: `scripts/run_threeway_anova.py`

- [ ] **Step 1: Write three-way ANOVA script**

```python
#!/usr/bin/env python3
"""Three-way ANOVA: scoring × detection_family × pathogen.

Reports omega-squared (less biased than eta-squared) with 95% CI.
Treats the analysis as variance decomposition, not hypothesis testing,
since evaluations are deterministic function evaluations, not random samples.
"""

import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.formula.api import ols
from pathlib import Path

RESULTS_DIR = Path(__file__).parent.parent / "results" / "mutbench"


def omega_squared(aov_table, ss_total):
    """Compute omega-squared effect size (less biased than eta-squared)."""
    results = {}
    for idx in aov_table.index:
        if idx == "Residual":
            continue
        ss = aov_table.loc[idx, "sum_sq"]
        df_effect = aov_table.loc[idx, "df"]
        ms_resid = aov_table.loc["Residual", "sum_sq"] / aov_table.loc["Residual", "df"]
        omega2 = (ss - df_effect * ms_resid) / (ss_total + ms_resid)
        results[idx] = max(0, omega2)  # omega2 can be negative
    return results


def main():
    multilayer_path = RESULTS_DIR / "multilayer_9pathogen_results.csv"
    extended_path = RESULTS_DIR / "extended_9pathogen_results.csv"

    if multilayer_path.exists():
        df = pd.read_csv(multilayer_path)
        mcc_col = "mcc_adaptive"
    else:
        df = pd.read_csv(extended_path)
        mcc_col = "mcc"

    print(f"Total evaluations: {len(df)}")

    # Three-way ANOVA
    formula = f"{mcc_col} ~ C(score) + C(family) + C(pathogen) + C(score):C(family) + C(score):C(pathogen) + C(family):C(pathogen)"
    model = ols(formula, data=df).fit()
    aov = sm.stats.anova_lm(model, typ=2)

    ss_total = aov["sum_sq"].sum()

    # Compute omega-squared
    omega2 = omega_squared(aov, ss_total)

    print("\nThree-way ANOVA — Omega-squared (variance decomposition):")
    print(f"{'Factor':<35} {'ω²':<10} {'η²':<10} {'F':<10} {'p':<12}")
    print("-" * 77)
    for idx in aov.index:
        if idx == "Residual":
            continue
        eta2 = aov.loc[idx, "sum_sq"] / ss_total
        w2 = omega2.get(idx, 0)
        f_val = aov.loc[idx, "F"]
        p_val = aov.loc[idx, "PR(>F)"]
        print(f"{idx:<35} {w2:<10.4f} {eta2:<10.4f} {f_val:<10.2f} {p_val:<12.2e}")

    # Save
    results = []
    for idx in aov.index:
        if idx == "Residual":
            continue
        results.append({
            "factor": idx,
            "sum_sq": aov.loc[idx, "sum_sq"],
            "df": aov.loc[idx, "df"],
            "F": aov.loc[idx, "F"],
            "p": aov.loc[idx, "PR(>F)"],
            "eta_squared": aov.loc[idx, "sum_sq"] / ss_total,
            "omega_squared": omega2.get(idx, 0),
        })

    results_df = pd.DataFrame(results)
    output_path = RESULTS_DIR / "threeway_anova_omega.csv"
    results_df.to_csv(output_path, index=False)
    print(f"\nSaved to {output_path}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Run**

```bash
python scripts/run_threeway_anova.py
```

- [ ] **Step 3: Commit**

```bash
git add scripts/run_threeway_anova.py results/mutbench/threeway_anova_omega.csv
git commit -m "feat: add three-way ANOVA with omega-squared effect sizes"
```

---

### Task 12: Friedman test on top-20 methods + critical difference diagram

**Files:**
- Create: `scripts/run_friedman_top20.py`

- [ ] **Step 1: Write Friedman top-20 script with CD diagram**

```python
#!/usr/bin/env python3
"""Friedman test on top-20 methods + Nemenyi post-hoc.

Following Demsar 2006 (JMLR) guidelines for comparing classifiers across datasets.
"""

import pandas as pd
import numpy as np
from scipy.stats import friedmanchisquare, rankdata
from pathlib import Path

RESULTS_DIR = Path(__file__).parent.parent / "results" / "mutbench"


def nemenyi_cd(k, n, alpha=0.05):
    """Critical difference for Nemenyi test.

    k: number of methods
    n: number of datasets (pathogens)
    """
    # q_alpha values for Nemenyi test (two-tailed)
    # From Demsar 2006 Table 5
    q_values = {
        (5, 0.05): 2.728, (10, 0.05): 3.164, (15, 0.05): 3.397,
        (20, 0.05): 3.564, (5, 0.10): 2.459, (10, 0.10): 2.890,
        (15, 0.10): 3.124, (20, 0.10): 3.289,
    }
    # Approximate q_alpha
    q = q_values.get((k, alpha), 3.564)  # default to k=20
    cd = q * np.sqrt(k * (k + 1) / (6 * n))
    return cd


def main():
    multilayer_path = RESULTS_DIR / "multilayer_9pathogen_results.csv"
    extended_path = RESULTS_DIR / "extended_9pathogen_results.csv"

    if multilayer_path.exists():
        df = pd.read_csv(multilayer_path)
        mcc_col = "mcc_adaptive"
    else:
        df = pd.read_csv(extended_path)
        mcc_col = "mcc"

    df["combo"] = df["score"] + " + " + df["detector"]
    pathogens = sorted(df["pathogen"].unique())
    n = len(pathogens)

    # Top-20 by mean MCC
    combo_means = df.groupby("combo")[mcc_col].mean().sort_values(ascending=False)
    top20 = combo_means.head(20).index.tolist()
    k = len(top20)

    # Build rank matrix: pathogens × combos
    rank_matrix = pd.DataFrame(index=top20, columns=pathogens)
    for p in pathogens:
        p_df = df[df["pathogen"] == p]
        p_mccs = {combo: p_df[p_df["combo"] == combo][mcc_col].values[0]
                  for combo in top20 if len(p_df[p_df["combo"] == combo]) > 0}
        # Rank (1 = best)
        combos_sorted = sorted(p_mccs.keys(), key=lambda c: p_mccs[c], reverse=True)
        for rank_idx, combo in enumerate(combos_sorted):
            rank_matrix.loc[combo, p] = rank_idx + 1

    rank_matrix = rank_matrix.astype(float)
    mean_ranks = rank_matrix.mean(axis=1).sort_values()

    # Friedman test
    rank_arrays = [rank_matrix.loc[combo].values for combo in top20]
    chi2, p_value = friedmanchisquare(*rank_arrays)

    # Iman-Davenport correction
    ff = ((n - 1) * chi2) / (n * (k - 1) - chi2)
    from scipy.stats import f as f_dist
    p_iman = 1 - f_dist.cdf(ff, k - 1, (k - 1) * (n - 1))

    # Kendall's W
    W = chi2 / (n * (k - 1))

    # Critical difference
    cd = nemenyi_cd(k, n)

    print(f"Friedman test (top-{k} methods, {n} pathogens):")
    print(f"  χ² = {chi2:.2f}, p = {p_value:.2e}")
    print(f"  Iman-Davenport F = {ff:.2f}, p = {p_iman:.2e}")
    print(f"  Kendall's W = {W:.4f}")
    print(f"  Nemenyi CD (α=0.05) = {cd:.2f}")
    print(f"\nMean ranks (1=best):")
    for combo, rank in mean_ranks.items():
        print(f"  {rank:.1f}  {combo}")

    # Save
    results = {
        "n_methods": k, "n_pathogens": n,
        "chi2": chi2, "p_friedman": p_value,
        "F_iman_davenport": ff, "p_iman_davenport": p_iman,
        "kendall_W": W, "nemenyi_CD": cd,
    }

    pd.DataFrame([results]).to_csv(RESULTS_DIR / "friedman_top20.csv", index=False)
    mean_ranks.to_frame("mean_rank").to_csv(RESULTS_DIR / "friedman_top20_ranks.csv")
    print(f"\nSaved to {RESULTS_DIR / 'friedman_top20.csv'}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Run**

```bash
python scripts/run_friedman_top20.py
```

- [ ] **Step 3: Commit**

```bash
git add scripts/run_friedman_top20.py results/mutbench/friedman_top20*.csv
git commit -m "feat: add Friedman test on top-20 methods with Nemenyi CD"
```

---

## Chunk 5: Execution Order & Dependencies

### Dependency graph

```
Task 1-3 (Data download)     Task 4 (DMS download)
         \                      /
          v                    v
        Task 5 (GT redesign) + Task 6 (DMS loaders)
                    |
                    v
             Task 7 (Re-run benchmark)
              /      |       \        \
             v       v        v        v
          Task 8   Task 9   Task 10  Task 11
          (LOPO)  (Subsamp) (Boot)   (ANOVA)
                                       |
                                       v
                                    Task 12
                                   (Friedman)
```

### Parallel execution opportunities

**Wave 1 (independent):** Tasks 1, 2, 3, 4 — all data downloads, run in parallel
**Wave 2 (depends on Wave 1):** Tasks 5, 6 — GT framework, depends on DMS data existing
**Wave 3 (depends on Wave 2):** Task 7 — re-run benchmark
**Wave 4 (depends on Wave 3, all independent):** Tasks 8, 9, 10, 11 — all use benchmark results
**Wave 5 (depends on Wave 4):** Task 12 — uses same results, slightly different analysis

### Estimated runtime

| Task | Estimated time | Notes |
|------|---------------|-------|
| Tasks 1-3 | 10-30 min | NCBI download speed varies |
| Task 4 | 2-5 min | Small GitHub CSV files |
| Tasks 5-6 | Code only | No computation |
| Task 7 | 30-60 min | 3,321+ evaluations |
| Task 8 | 5-10 min | Reads existing results |
| Task 9 | 30-60 min | Repeated subsampling |
| Task 10 | 5-10 min | 10K bootstrap iterations |
| Tasks 11-12 | 2-5 min | Statistical analysis |
