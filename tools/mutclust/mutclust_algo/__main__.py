"""CLI: python -m tools.mutclust.mutclust_algo --input hscores.csv --gamma 10 --d 3 --minpts 5"""
import argparse, csv
import numpy as np
from tools.mutclust.mutclust_algo.core import mutclust

def main():
    parser = argparse.ArgumentParser(description='MutClust hotspot detection')
    parser.add_argument('--input', required=True)
    parser.add_argument('--gamma', type=int, default=10)
    parser.add_argument('--d', type=int, default=3)
    parser.add_argument('--minpts', type=int, default=5)
    parser.add_argument('--genome-size', type=int, default=29903)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    hscores = np.zeros(args.genome_size)
    with open(args.input) as f:
        reader = csv.DictReader(f)
        for row in reader:
            pos = int(row['position']) - 1
            if 0 <= pos < args.genome_size:
                hscores[pos] = float(row['hscore'])
    clusters = mutclust(hscores, gamma=args.gamma, d=args.d, minpts=args.minpts)
    with open(args.output, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['cluster_id', 'start', 'end', 'n_positions', 'mean_hscore', 'max_hscore'])
        for i, c in enumerate(clusters):
            scores = [hscores[p] for p in c.positions]
            writer.writerow([f'c{i+1}', c.start+1, c.end+1, c.size, f'{np.mean(scores):.4f}', f'{np.max(scores):.4f}'])
    print(f"MutClust: {len(clusters)} hotspots -> {args.output}")

if __name__ == '__main__':
    main()
