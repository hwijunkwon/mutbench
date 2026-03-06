"""Data I/O helpers for loading/saving matrices and labels."""
import pandas as pd


def load_csv_matrix(path: str) -> pd.DataFrame:
    """Load a CSV file as a DataFrame with first column as index."""
    return pd.read_csv(path, index_col=0)


def save_csv_matrix(df: pd.DataFrame, path: str) -> None:
    """Save a DataFrame to CSV."""
    df.to_csv(path)


def load_labels(path: str, sample_col: str = 'sample', label_col: str = 'label') -> list:
    """Load sample labels from a CSV file."""
    df = pd.read_csv(path)
    return df[label_col].tolist()
