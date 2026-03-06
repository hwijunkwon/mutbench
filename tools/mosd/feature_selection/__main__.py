"""CLI: python -m tools.mosd.feature_selection --input data.csv --labels labels.csv --method chi2 --top-pct 10"""
import argparse
import numpy as np
from tools.common.io_utils import load_csv_matrix, load_labels, save_csv_matrix
from tools.mosd.feature_selection.core import select_features_chi2, select_features_anova

def main():
    parser = argparse.ArgumentParser(description='Feature selection (Chi-square/ANOVA)')
    parser.add_argument('--input', required=True)
    parser.add_argument('--labels', required=True)
    parser.add_argument('--method', choices=['chi2', 'anova'], default='chi2')
    parser.add_argument('--top-pct', type=float, default=10.0)
    parser.add_argument('--output', required=True)
    parser.add_argument('--label-col', default='label')
    args = parser.parse_args()
    data = load_csv_matrix(args.input)
    labels = np.array(load_labels(args.labels, label_col=args.label_col))
    if args.method == 'chi2':
        selected = select_features_chi2(data, labels, args.top_pct)
    else:
        selected = select_features_anova(data, labels, args.top_pct)
    save_csv_matrix(selected, args.output)
    print(f"Selected {selected.shape[1]} features ({args.top_pct}%) -> {args.output}")

if __name__ == '__main__':
    main()
