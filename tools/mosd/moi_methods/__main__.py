"""CLI: python -m tools.mosd.moi_methods --method SNF --inputs ge.csv me.csv --k 3"""
import argparse
import numpy as np
import pandas as pd
from tools.common.io_utils import load_csv_matrix
from tools.mosd.moi_methods.core import METHODS

def main():
    parser = argparse.ArgumentParser(description='Run MOI clustering method')
    parser.add_argument('--method', choices=list(METHODS.keys()), required=True)
    parser.add_argument('--inputs', nargs='+', required=True)
    parser.add_argument('--k', type=int, required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    omics = [load_csv_matrix(f) for f in args.inputs]
    labels = METHODS[args.method](omics, n_clusters=args.k)
    result = pd.DataFrame({'sample': omics[0].index, 'label': labels})
    result.to_csv(args.output, index=False)
    print(f"{args.method}: {len(set(labels))} clusters, {len(labels)} samples -> {args.output}")

if __name__ == '__main__':
    main()
