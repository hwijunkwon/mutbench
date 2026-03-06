"""CLI: python -m tools.mosd.cluster_score --true labels.csv --pred pred.csv"""
import argparse, json
from tools.mosd.cluster_score.core import compute_cluster_score

def main():
    parser = argparse.ArgumentParser(description='Compute cluster-score (ARI+NMI+F-measure)/3')
    parser.add_argument('--true', required=True)
    parser.add_argument('--pred', required=True)
    parser.add_argument('--sample-col', default='sample')
    parser.add_argument('--label-col', default='label')
    parser.add_argument('--format', choices=['json', 'text'], default='text')
    args = parser.parse_args()
    result = compute_cluster_score(args.true, args.pred, args.sample_col, args.label_col)
    if args.format == 'json':
        print(json.dumps(result, indent=2))
    else:
        for k, v in result.items():
            print(f"{k}: {v:.4f}")

if __name__ == '__main__':
    main()
