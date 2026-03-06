"""CLI: python -m tools.mosd.benchmark --test sample_size --input data.csv --labels labels.csv --method CC --k 3"""
import argparse
import numpy as np
import pandas as pd
from tools.common.io_utils import load_csv_matrix, load_labels, save_csv_matrix
from tools.mosd.benchmark.core import (
    sample_size_test, feature_selection_test, preprocessing_test,
    noise_test, balance_test, subtype_combination_test, omics_combination_test,
    BenchmarkRunner,
)

TESTS = {
    'sample_size': sample_size_test,
    'feature_selection': feature_selection_test,
    'preprocessing': preprocessing_test,
    'noise': noise_test,
    'balance': balance_test,
    'subtype_combination': subtype_combination_test,
    'omics_combination': omics_combination_test,
}


def main():
    parser = argparse.ArgumentParser(description='Run MOSD benchmark tests')
    parser.add_argument('--test', choices=list(TESTS.keys()), required=True,
                        help='Which benchmark test to run')
    parser.add_argument('--inputs', nargs='+', required=True,
                        help='Input omics CSV file(s)')
    parser.add_argument('--labels', required=True,
                        help='Labels CSV file')
    parser.add_argument('--method', default='CC',
                        help='MOI method to use')
    parser.add_argument('--k', type=int, default=3,
                        help='Number of clusters')
    parser.add_argument('--repeats', type=int, default=5,
                        help='Number of repeats per condition')
    parser.add_argument('--output', required=True,
                        help='Output CSV for results')
    parser.add_argument('--label-col', default='label')
    args = parser.parse_args()

    omics = [load_csv_matrix(f) for f in args.inputs]
    data = omics[0]
    true_labels = np.array(load_labels(args.labels, label_col=args.label_col))

    test_name = args.test
    if test_name == 'sample_size':
        result = sample_size_test(data, true_labels, sizes=[20, 40, 60, 80],
                                  repeats=args.repeats, method=args.method, n_clusters=args.k)
    elif test_name == 'feature_selection':
        result = feature_selection_test(data, true_labels, repeats=args.repeats,
                                        method=args.method, n_clusters=args.k)
    elif test_name == 'preprocessing':
        result = preprocessing_test(data, true_labels, repeats=args.repeats,
                                    method=args.method, n_clusters=args.k)
    elif test_name == 'noise':
        result = noise_test(data, true_labels, repeats=args.repeats,
                            method=args.method, n_clusters=args.k)
    elif test_name == 'balance':
        result = balance_test(data, true_labels, repeats=args.repeats,
                              method=args.method, n_clusters=args.k)
    elif test_name == 'subtype_combination':
        result = subtype_combination_test(data, true_labels, repeats=args.repeats,
                                          method=args.method)
    elif test_name == 'omics_combination':
        result = omics_combination_test(omics, true_labels, repeats=args.repeats,
                                        method=args.method, n_clusters=args.k)
    else:
        raise ValueError(f"Unknown test: {test_name}")

    save_csv_matrix(result, args.output)
    print(f"Benchmark '{test_name}': {len(result)} rows -> {args.output}")
    print(result.groupby(result.columns[0])['cluster_score'].mean().to_string())


if __name__ == '__main__':
    main()
