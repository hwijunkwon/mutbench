#!/bin/bash
# Run MEME for all 11 pathogens (excluding Zika which is already done)
set -e

cd /proj/paper

OUTDIR="results/mutbench/feature_analysis"
CLEANDIR="data/meme_clean"
mkdir -p "$OUTDIR" "$CLEANDIR"

# Define pathogens: name, alignment, tree
declare -A PATHOGENS
PATHOGENS["EV-A71"]="data/enterovirus/eva71_vp1_nt_cds_aligned.fasta"
PATHOGENS["Rabies"]="data/rabies/rabies_g_nt_cds_aligned.fasta"
PATHOGENS["RSV"]="data/rsv/rsv_f_nt_cds_aligned.fasta"
PATHOGENS["H3N2"]="data/influenza/h3n2_ha_nt_cds_aligned.fasta"
PATHOGENS["Influenza_B"]="data/influenza/influenza_b_ha_nt_cds_aligned.fasta"
PATHOGENS["Norovirus"]="data/norovirus/norovirus_vp1_nt_cds_aligned.fasta"
PATHOGENS["SARS-CoV-2"]="data/ncbi_temporal/sars2_spike_nt_cds_aligned.fasta"
PATHOGENS["Dengue"]="data/dengue/dengue_e_nt_cds_aligned.fasta"
PATHOGENS["HIV-1"]="data/hiv/hiv1_gp120_nt_cds_aligned.fasta"
PATHOGENS["MERS"]="data/mers/mers_spike_nt_cds_aligned.fasta"
PATHOGENS["HCV"]="data/hcv/hcv_e2_nt_cds_aligned.fasta"

# Order (smallest first)
ORDER=("EV-A71" "Influenza_B" "H3N2" "RSV" "Rabies" "MERS" "Norovirus" "SARS-CoV-2" "Dengue" "HCV" "HIV-1")

for NAME in "${ORDER[@]}"; do
    ALN="${PATHOGENS[$NAME]}"
    CSV="$OUTDIR/${NAME}_meme.csv"

    # Skip if already done
    if [ -f "$CSV" ]; then
        echo "=== $NAME: already done, skipping ==="
        continue
    fi

    echo ""
    echo "============================================"
    echo "=== Processing: $NAME ==="
    echo "============================================"

    # Step 1: Clean alignment
    CLEAN_ALN="$CLEANDIR/${NAME}_clean.fasta"
    echo "  Cleaning alignment..."
    python3 scripts/clean_codons_for_meme.py "$ALN" "$CLEAN_ALN"

    # Step 2: Build tree from clean alignment
    TREE="$CLEANDIR/${NAME}_clean.nwk"
    echo "  Building tree..."
    fasttree -nt -gtr "$CLEAN_ALN" > "$TREE" 2>/dev/null

    # Step 3: Run MEME
    JSON="$OUTDIR/${NAME}_meme.json"
    echo "  Running MEME..."
    if timeout 3600 hyphy meme --alignment "$CLEAN_ALN" --tree "$TREE" --output "$JSON" 2>&1 | tail -5; then
        echo "  MEME completed successfully"
    else
        echo "  WARNING: MEME failed or timed out for $NAME"
        continue
    fi

    # Step 4: Parse JSON to CSV
    echo "  Parsing results..."
    python3 scripts/parse_meme_json.py "$JSON" "$CSV"
    echo "=== $NAME: DONE ==="
done

echo ""
echo "============================================"
echo "=== ALL DONE ==="
echo "============================================"
echo ""
echo "Results:"
for NAME in "${ORDER[@]}"; do
    CSV="$OUTDIR/${NAME}_meme.csv"
    if [ -f "$CSV" ]; then
        NSIG=$(tail -n +2 "$CSV" | awk -F',' '$3==1' | wc -l)
        NTOT=$(tail -n +2 "$CSV" | wc -l)
        echo "  $NAME: $NSIG/$NTOT significant sites"
    else
        echo "  $NAME: FAILED"
    fi
done
