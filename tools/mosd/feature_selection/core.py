"""Feature selection: Chi-square (GE/MI/ME) and ANOVA (CNV)."""
import numpy as np
import pandas as pd
from sklearn.feature_selection import chi2, f_classif

def select_features_chi2(data: pd.DataFrame, labels: np.ndarray, top_pct: float = 10.0) -> pd.DataFrame:
    k = max(1, int(len(data.columns) * top_pct / 100))
    scores, _ = chi2(data.values, labels)
    top_idx = np.argsort(scores)[-k:]
    return data.iloc[:, sorted(top_idx)]

def select_features_anova(data: pd.DataFrame, labels: np.ndarray, top_pct: float = 10.0) -> pd.DataFrame:
    k = max(1, int(len(data.columns) * top_pct / 100))
    scores, _ = f_classif(data.values, labels)
    top_idx = np.argsort(scores)[-k:]
    return data.iloc[:, sorted(top_idx)]
