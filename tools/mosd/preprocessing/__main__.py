"""CLI: python -m tools.mosd.preprocessing --input data.csv --strategy NORM --output out.csv"""
import argparse, json
from tools.common.io_utils import load_csv_matrix, save_csv_matrix
from tools.mosd.preprocessing.core import preprocess_raw, preprocess_norm, preprocess_gl

def main():
    parser = argparse.ArgumentParser(description='Multi-omics preprocessing (RAW/NORM/GL)')
    parser.add_argument('--input', required=True)
    parser.add_argument('--strategy', choices=['RAW', 'NORM', 'GL'], required=True)
    parser.add_argument('--gene-map', help='JSON file mapping probes to genes (GL only)')
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    data = load_csv_matrix(args.input)
    if args.strategy == 'RAW':
        result = preprocess_raw(data)
    elif args.strategy == 'NORM':
        result = preprocess_norm(data)
    elif args.strategy == 'GL':
        with open(args.gene_map) as f:
            gene_map = json.load(f)
        result = preprocess_gl(data, gene_map)
    save_csv_matrix(result, args.output)
    print(f"Preprocessed ({args.strategy}): {result.shape} -> {args.output}")

if __name__ == '__main__':
    main()
