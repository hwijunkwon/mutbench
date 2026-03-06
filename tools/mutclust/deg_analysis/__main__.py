"""CLI: python -m tools.mutclust.deg_analysis --counts counts.csv --groups groups.csv --fdr 0.05"""
import argparse
import pandas as pd
from tools.common.io_utils import load_csv_matrix
from tools.mutclust.deg_analysis.core import find_degs, filter_low_expression

def main():
    parser = argparse.ArgumentParser(description='DEG analysis')
    parser.add_argument('--counts', required=True)
    parser.add_argument('--groups', required=True)
    parser.add_argument('--fdr', type=float, default=0.05)
    parser.add_argument('--test', choices=['mannwhitney', 'ttest'], default='mannwhitney')
    parser.add_argument('--filter-zeros', type=float, default=0.8)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    counts = load_csv_matrix(args.counts)
    groups_df = pd.read_csv(args.groups)
    groups = groups_df['group'].tolist()
    counts = filter_low_expression(counts, args.filter_zeros)
    result = find_degs(counts, groups, fdr=args.fdr, test=args.test)
    result.to_csv(args.output, index=False)
    n_sig = result['significant'].sum()
    print(f"DEG: {n_sig}/{len(result)} significant (FDR={args.fdr}) -> {args.output}")

if __name__ == '__main__':
    main()
