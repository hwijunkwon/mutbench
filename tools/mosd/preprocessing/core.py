"""Preprocessing strategies: RAW (log2), NORM (quantile + MinMax), GL (gene-level)."""
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def preprocess_raw(data: pd.DataFrame) -> pd.DataFrame:
    return np.log2(data + 1)

def quantile_normalize(df: pd.DataFrame) -> pd.DataFrame:
    rank_mean = df.stack().groupby(df.rank(method='first').stack().astype(int)).mean()
    result = df.rank(method='min').stack().astype(int).map(rank_mean).unstack()
    result.columns = df.columns
    result.index = df.index
    return result

def preprocess_norm(data: pd.DataFrame) -> pd.DataFrame:
    normed = quantile_normalize(data)
    scaler = MinMaxScaler()
    scaled = pd.DataFrame(scaler.fit_transform(normed), columns=normed.columns, index=normed.index)
    return scaled

def preprocess_gl(data: pd.DataFrame, gene_map: dict[str, str]) -> pd.DataFrame:
    mapped = data.rename(columns=gene_map)
    return mapped.T.groupby(level=0).mean().T
