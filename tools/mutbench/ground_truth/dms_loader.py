"""Load and process Deep Mutational Scanning (DMS) datasets."""
import pandas as pd
import numpy as np


def load_dms_fitness(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


def dms_to_position_scores(df: pd.DataFrame, gene: str) -> dict[int, float]:
    gene_df = df[df['gene'] == gene]
    scores = gene_df.groupby('aa_site')['fitness'].apply(
        lambda x: np.mean(np.abs(x))
    ).to_dict()
    return scores


def get_functional_positions(scores: dict[int, float],
                              threshold_percentile: float = 80) -> set[int]:
    values = np.array(list(scores.values()))
    threshold = np.percentile(values, threshold_percentile)
    return {pos for pos, val in scores.items() if val >= threshold}
