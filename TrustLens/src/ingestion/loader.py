"""
Utilities for loading TrustLens Olist datasets.

This module provides a centralized CSV loading mechanism for
the datasets used by the TrustLens analytics pipeline.
"""

from pathlib import Path

import pandas as pd

from src.config import OLIST_DATASETS, RAW_DATA_DIR


def load_dataset(dataset_name: str) -> pd.DataFrame:
    """
    Load a single Olist dataset from the raw data directory.

    Parameters
    ----------
    dataset_name : str
        Dataset key defined in OLIST_DATASETS.

    Returns
    -------
    pd.DataFrame
        Loaded dataset.

    Raises
    ------
    ValueError
        If the dataset name is not configured.
    FileNotFoundError
        If the expected CSV file does not exist.
    """
    if dataset_name not in OLIST_DATASETS:
        raise ValueError(
            f"Unknown dataset: {dataset_name}. "
            f"Available datasets: {list(OLIST_DATASETS.keys())}"
        )

    file_name = OLIST_DATASETS[dataset_name]
    file_path = RAW_DATA_DIR / file_name

    if not file_path.exists():
        raise FileNotFoundError(
            f"Dataset file not found: {file_path}"
        )

    return pd.read_csv(file_path)


def load_all_datasets() -> dict[str, pd.DataFrame]:
    """
    Load all configured Olist datasets.

    Returns
    -------
    dict[str, pd.DataFrame]
        Dictionary containing each dataset as a DataFrame.
    """
    datasets = {}

    for dataset_name in OLIST_DATASETS:
        datasets[dataset_name] = load_dataset(dataset_name)

    return datasets