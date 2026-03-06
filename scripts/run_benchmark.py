"""Run the full MutBench benchmark with real or synthetic SARS-CoV-2 data."""
import os
import sys
import json
import numpy as np
import pandas as pd

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.mutbench.config import BenchmarkConfig
from tools.mutbench.ground_truth.dms_loader import dms_to_position_scores, get_functional_positions
from tools.mutbench.ground_truth.coord_mapper import CoordinateMapper
from tools.mutbench.ground_truth.labeler import create_ground_truth_labels, GroundTruthSource
from tools.mutbench.runner import run_benchmark
from tools.mutbench.variants.registry import get_variant
from tools.mutclust.dnds_annotation.core import annotate_clusters
from tools.mutbench.visualization.plots import (
    plot_method_comparison, plot_genome_hotspot_map,
    plot_sensitivity_heatmap, plot_dnds_enrichment,
)

RESULTS_DIR = os.path.join(os.path.dirname(__file__), '..', 'results', 'mutbench')
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'mutbench')
HSCORES_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'mutclust', 'hscores.csv')

# SARS-CoV-2 Spike gene coordinates (in genome)
SPIKE_GENE_START = 21563
SPIKE_GENE_END = 25384

# Known functional sites (AA positions in Spike)
KNOWN_FUNCTIONAL_SITES = {
    'RBD': set(range(319, 542)),
    'furin_cleavage': set(range(681, 686)),
    'fusion_peptide': set(range(816, 834)),
}


def load_hscores(path):
    """Load H-scores from CSV file."""
    if os.path.exists(path):
        df = pd.read_csv(path)
        if 'hscore' in df.columns:
            return df['hscore'].values
        return df.iloc[:, 0].values
    return None


def generate_synthetic_hscores(genome_length=29903, seed=42):
    """Generate synthetic H-scores mimicking SARS-CoV-2 patterns."""
    rng = np.random.default_rng(seed)
    hscores = rng.uniform(0, 0.02, genome_length)

    # Spike RBD region
    rbd_start = SPIKE_GENE_START + (319 - 1) * 3
    rbd_end = min(SPIKE_GENE_START + 541 * 3, genome_length)
    hscores[rbd_start:rbd_end] = rng.uniform(0.05, 0.3, rbd_end - rbd_start)

    # CCM seeds
    for aa_pos in [484, 501, 417, 452]:
        nuc_pos = SPIKE_GENE_START + (aa_pos - 1) * 3
        if nuc_pos < genome_length:
            hscores[nuc_pos] = rng.uniform(0.8, 1.2)

    # Furin cleavage site
    furin_start = SPIKE_GENE_START + (681 - 1) * 3
    furin_end = min(SPIKE_GENE_START + 685 * 3, genome_length)
    hscores[furin_start:furin_end] = rng.uniform(0.1, 0.5, furin_end - furin_start)

    # NTD region
    ntd_start = SPIKE_GENE_START + (14 - 1) * 3
    ntd_end = min(SPIKE_GENE_START + 265 * 3, genome_length)
    hscores[ntd_start:ntd_end] = rng.uniform(0.03, 0.15, ntd_end - ntd_start)

    return hscores


def build_ground_truth(genome_length):
    """Build ground truth from known functional sites."""
    mapper = CoordinateMapper(gene_start=SPIKE_GENE_START, gene_end=SPIKE_GENE_END)
    all_functional_aa = set()
    for site_name, positions in KNOWN_FUNCTIONAL_SITES.items():
        all_functional_aa.update(positions)

    functional_nuc = mapper.aa_set_to_nuc_set(all_functional_aa)
    # Filter to valid range
    functional_nuc = {p for p in functional_nuc if 0 <= p < genome_length}
    return functional_nuc


def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)
    config = BenchmarkConfig(seed=42)

    print("=" * 60)
    print("MutBench: Viral Mutation Hotspot Detection Benchmark")
    print("=" * 60)

    # Load or generate H-scores
    hscores = load_hscores(HSCORES_PATH)
    if hscores is not None:
        genome_length = len(hscores)
        print(f"Loaded real H-scores: {genome_length} positions")
    else:
        genome_length = 29903
        hscores = generate_synthetic_hscores(genome_length, seed=config.seed)
        print(f"Using synthetic H-scores: {genome_length} positions")

    # Build ground truth
    gt_positions = build_ground_truth(genome_length)
    print(f"Ground truth: {len(gt_positions)} functional nucleotide positions")

    # Run benchmark
    print("\nRunning benchmark...")
    results = run_benchmark(hscores, gt_positions, genome_length, config=config)

    method_df = results['method_results']
    sensitivity_df = results['sensitivity_results']

    # Print results table
    print("\n" + "=" * 60)
    print("Method Comparison Results")
    print("=" * 60)
    display_cols = ['method', 'precision', 'recall', 'f1', 'enrichment_ratio', 'n_detected', 'n_clusters']
    print(method_df[display_cols].to_string(index=False))

    # Save results
    method_df.to_csv(os.path.join(RESULTS_DIR, 'method_comparison.csv'), index=False)
    sensitivity_df.to_csv(os.path.join(RESULTS_DIR, 'sensitivity_results.csv'), index=False)
    print(f"\nSaved method comparison to {RESULTS_DIR}/method_comparison.csv")
    print(f"Saved sensitivity results to {RESULTS_DIR}/sensitivity_results.csv")

    # Generate figures
    print("\nGenerating figures...")
    plot_method_comparison(method_df, os.path.join(RESULTS_DIR, 'method_comparison.png'))
    print("  - method_comparison.png")

    # Genome hotspot map (using v2a-bugfix)
    v2a_clusters = get_variant('v2a-bugfix')(hscores, gamma=config.gamma, d=config.d, minpts=config.minpts)
    detected_positions = set()
    for c in v2a_clusters:
        detected_positions.update(c['positions'])
    plot_genome_hotspot_map(hscores, detected_positions, gt_positions,
                             os.path.join(RESULTS_DIR, 'genome_hotspot_map.png'))
    print("  - genome_hotspot_map.png")

    # Sensitivity heatmap
    if 'f1' in sensitivity_df.columns:
        plot_sensitivity_heatmap(sensitivity_df, metric='f1',
                                  output_path=os.path.join(RESULTS_DIR, 'sensitivity_heatmap.png'))
        print("  - sensitivity_heatmap.png")

    # dN/dS enrichment
    if v2a_clusters:
        reference_seq = 'A' * genome_length
        mutations = {c['positions'][0]: 'T' for c in v2a_clusters if c['positions']}
        annotated = annotate_clusters(v2a_clusters, reference_seq, mutations)
        plot_dnds_enrichment(annotated, os.path.join(RESULTS_DIR, 'dnds_enrichment.png'))
        print("  - dnds_enrichment.png")

    # Sanity checks
    print("\n" + "=" * 60)
    print("Sanity Checks")
    print("=" * 60)

    v1_row = method_df[method_df['method'] == 'v1-original']
    v2a_row = method_df[method_df['method'] == 'v2a-bugfix']
    if len(v1_row) > 0 and len(v2a_row) > 0:
        v1_det = v1_row['n_detected'].values[0]
        v2a_det = v2a_row['n_detected'].values[0]
        check = "PASS" if v2a_det >= v1_det else "FAIL"
        print(f"  [{check}] v2a detects >= v1 positions: {v2a_det} >= {v1_det}")

    enriched = method_df[method_df['enrichment_ratio'] >= 1.0]
    check = "PASS" if len(enriched) == len(method_df[method_df['n_detected'] > 0]) else "WARN"
    print(f"  [{check}] Methods with enrichment >= 1.0: {len(enriched)}/{len(method_df)}")

    print(f"\nBenchmark complete. Results in: {os.path.abspath(RESULTS_DIR)}")


if __name__ == '__main__':
    main()
