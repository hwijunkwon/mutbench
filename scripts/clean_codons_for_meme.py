#!/usr/bin/env python3
"""Clean codon alignments for HyPhy MEME: remove sequences with stop codons,
ensure length divisible by 3, mask internal stops with NNN."""
import sys
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

STOP_CODONS = {'TAA', 'TAG', 'TGA', 'taa', 'tag', 'tga'}

def clean_alignment(input_fasta, output_fasta):
    records = list(SeqIO.parse(input_fasta, 'fasta'))
    print(f"  Input: {len(records)} sequences")

    cleaned = []
    removed = 0
    for rec in records:
        seq = str(rec.seq)
        # Trim to multiple of 3
        trim_len = (len(seq) // 3) * 3
        seq = seq[:trim_len]

        # Check for stop codons
        has_internal_stop = False
        codons = [seq[i:i+3] for i in range(0, len(seq), 3)]

        # Remove terminal stop codon if present
        if codons and codons[-1].upper() in {'TAA', 'TAG', 'TGA'}:
            codons = codons[:-1]

        # Check for internal stops
        new_codons = []
        for c in codons:
            if c.upper() in {'TAA', 'TAG', 'TGA'}:
                has_internal_stop = True
                new_codons.append('NNN')  # mask with NNN
            else:
                new_codons.append(c)

        if has_internal_stop:
            removed += 1
            continue  # skip sequences with internal stop codons entirely

        new_seq = ''.join(new_codons)
        new_rec = SeqRecord(Seq(new_seq), id=rec.id, description='')
        cleaned.append(new_rec)

    # Ensure all sequences same length (pad shorter ones with gaps)
    if cleaned:
        max_len = max(len(str(r.seq)) for r in cleaned)
        # Ensure divisible by 3
        max_len = (max_len // 3) * 3
        final = []
        for r in cleaned:
            s = str(r.seq)[:max_len]
            if len(s) < max_len:
                s += '---' * ((max_len - len(s)) // 3)
            final.append(SeqRecord(Seq(s), id=r.id, description=''))
        cleaned = final

    print(f"  Removed {removed} sequences with internal stop codons")
    print(f"  Output: {len(cleaned)} sequences, {len(str(cleaned[0].seq)) if cleaned else 0} nt")

    SeqIO.write(cleaned, output_fasta, 'fasta')
    return len(cleaned)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: clean_codons_for_meme.py <input.fasta> <output.fasta>")
        sys.exit(1)
    clean_alignment(sys.argv[1], sys.argv[2])
