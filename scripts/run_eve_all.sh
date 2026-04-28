#!/bin/bash
# Run EVE VAE training + evolutionary index computation for all virus proteins
# Uses GPU (RTX 4090), ~16 min per protein at 100k steps

set -e
cd /proj/paper/tools/EVE

export CUDA_VISIBLE_DEVICES=0
MSA_DIR=/proj/paper/data/eve_msa
WEIGHTS_DIR=/proj/paper/data/eve_weights
CHECKPOINT_DIR=/proj/paper/tools/EVE/results/VAE_parameters
LOG_DIR=/proj/paper/results/eve_logs
EVE_SCORES_DIR=/proj/paper/results/mutbench/eve_scores
MAPPING=$MSA_DIR/virus_mapping.csv
PARAMS=$MSA_DIR/virus_model_params.json

mkdir -p $CHECKPOINT_DIR $LOG_DIR $EVE_SCORES_DIR

# 12 proteins: index 0-11, skip index 2 (E_ZIKV)
for idx in 0 1 3 4 5 6 7 8 9 10 11; do
    PROTEIN=$(python3 -c "import pandas as pd; print(pd.read_csv('$MAPPING')['protein_name'][$idx])")
    CHECKPOINT="$CHECKPOINT_DIR/${PROTEIN}_virus_v1_final"

    echo "============================================"
    echo "[$idx] $PROTEIN"
    echo "============================================"

    # Step 1: Train VAE
    if [ -d "$CHECKPOINT" ] || [ -f "${CHECKPOINT}.pth" ] || [ -f "$CHECKPOINT" ]; then
        echo "  Checkpoint exists, skipping training"
    else
        echo "  Training VAE..."
        python3 train_VAE.py \
            --MSA_data_folder $MSA_DIR \
            --MSA_list $MAPPING \
            --protein_index $idx \
            --MSA_weights_location $WEIGHTS_DIR \
            --VAE_checkpoint_location $CHECKPOINT_DIR \
            --model_name_suffix virus_v1 \
            --model_parameters_location $PARAMS \
            --training_logs_location $LOG_DIR
        echo "  Training done"
    fi

    # Step 2: Compute evolutionary indices
    EVE_CSV="$EVE_SCORES_DIR/${PROTEIN}_20000_samples.csv"
    if [ -f "$EVE_CSV" ]; then
        echo "  Evol indices already computed"
    else
        echo "  Computing evolutionary indices..."
        python3 compute_evol_indices.py \
            --MSA_data_folder $MSA_DIR \
            --MSA_list $MAPPING \
            --protein_index $idx \
            --MSA_weights_location $WEIGHTS_DIR \
            --VAE_checkpoint_location $CHECKPOINT_DIR \
            --model_name_suffix virus_v1 \
            --model_parameters_location $PARAMS \
            --computation_mode all_singles \
            --all_singles_mutations_folder $EVE_SCORES_DIR \
            --output_evol_indices_location $EVE_SCORES_DIR \
            --num_samples_compute_evol_indices 20000 \
            --batch_size 2048
        echo "  Evol indices done"
    fi

    echo ""
done

echo "============================================"
echo "ALL EVE TRAINING COMPLETE"
echo "============================================"
