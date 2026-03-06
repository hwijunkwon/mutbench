"""CLI: python -m tools.mutclust.hscore --input aligned.fasta --ref reference.fasta --output hscores.csv"""
import argparse, csv
from Bio import SeqIO
from tools.mutclust.hscore.core import compute_hscores_from_alignment

def main():
    parser = argparse.ArgumentParser(description='Compute H-scores from aligned sequences')
    parser.add_argument('--input', required=True)
    parser.add_argument('--ref', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    ref_record = next(SeqIO.parse(args.ref, 'fasta'))
    reference = str(ref_record.seq)
    alignment = [str(rec.seq) for rec in SeqIO.parse(args.input, 'fasta')]
    hscores = compute_hscores_from_alignment(alignment, reference)
    with open(args.output, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['position', 'hscore'])
        for i, h in enumerate(hscores):
            writer.writerow([i + 1, f'{h:.6f}'])
    print(f"H-scores computed for {len(hscores)} positions -> {args.output}")

if __name__ == '__main__':
    main()
