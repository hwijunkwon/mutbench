"""CLI: python -m tools.mutclust.hla_affinity --ref-seq ref.fasta --mut-seq mut.fasta"""
import argparse, csv
from tools.mutclust.hla_affinity.core import analyze_hla_epitopes

def main():
    parser = argparse.ArgumentParser(description='HLA-epitope affinity analysis')
    parser.add_argument('--ref-seq', required=True)
    parser.add_argument('--mut-seq', required=True)
    parser.add_argument('--min-len', type=int, default=8)
    parser.add_argument('--max-len', type=int, default=14)
    parser.add_argument('--affinity-threshold', type=float, default=500.0)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    with open(args.ref_seq) as f:
        ref = ''.join(line.strip() for line in f if not line.startswith('>'))
    with open(args.mut_seq) as f:
        mut = ''.join(line.strip() for line in f if not line.startswith('>'))
    results = analyze_hla_epitopes(ref, mut, args.min_len, args.max_len, args.affinity_threshold)
    with open(args.output, 'w', newline='') as f:
        if results:
            writer = csv.DictWriter(f, fieldnames=results[0].keys())
            writer.writeheader()
            writer.writerows(results)
    print(f"HLA affinity: {len(results)} pairs -> {args.output}")

if __name__ == '__main__':
    main()
