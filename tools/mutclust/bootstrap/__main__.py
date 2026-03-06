"""CLI: python -m tools.mutclust.bootstrap --hscores hscores.csv --clusters clusters.csv --n-iter 1000"""
import argparse, csv
import numpy as np
from tools.mutclust.bootstrap.core import bootstrap_all_hotspots

def main():
    parser = argparse.ArgumentParser(description='Bootstrap significance testing')
    parser.add_argument('--hscores', required=True)
    parser.add_argument('--clusters', required=True)
    parser.add_argument('--genome-size', type=int, default=29903)
    parser.add_argument('--n-iter', type=int, default=1000)
    parser.add_argument('--fdr', type=float, default=0.05)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    hscores = np.zeros(args.genome_size)
    with open(args.hscores) as f:
        for row in csv.DictReader(f):
            pos = int(row['position']) - 1
            if 0 <= pos < args.genome_size:
                hscores[pos] = float(row['hscore'])
    hotspots = []
    with open(args.clusters) as f:
        for row in csv.DictReader(f):
            hotspots.append((int(row['start'])-1, int(row['end'])-1))
    results = bootstrap_all_hotspots(hscores, hotspots, args.n_iter, args.fdr)
    with open(args.output, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['start','end','obs_count','obs_mean','obs_sum','p_value','adjusted_p','significant'])
        writer.writeheader()
        for r in results:
            r['start'] += 1; r['end'] += 1
            writer.writerow(r)
    n_sig = sum(1 for r in results if r['significant'])
    print(f"Bootstrap: {n_sig}/{len(results)} significant (FDR={args.fdr}) -> {args.output}")

if __name__ == '__main__':
    main()
