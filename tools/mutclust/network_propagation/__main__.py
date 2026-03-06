"""CLI: python -m tools.mutclust.network_propagation --seeds seeds.txt --network ppi.tsv"""
import argparse, csv
import networkx as nx
from tools.mutclust.network_propagation.core import propagate, get_top_genes

def main():
    parser = argparse.ArgumentParser(description='Network propagation on PPI')
    parser.add_argument('--seeds', required=True)
    parser.add_argument('--network', required=True)
    parser.add_argument('--alpha', type=float, default=0.01)
    parser.add_argument('--top-n', type=int, default=100)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    with open(args.seeds) as f:
        seeds = {line.strip() for line in f if line.strip()}
    G = nx.read_edgelist(args.network, delimiter='\t')
    scores = propagate(G, seeds, alpha=args.alpha)
    top = get_top_genes(scores, n=args.top_n, exclude=seeds)
    with open(args.output, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['gene', 'score'])
        for gene, score in top:
            writer.writerow([gene, f'{score:.6f}'])
    print(f"Network propagation: top {len(top)} genes -> {args.output}")

if __name__ == '__main__':
    main()
