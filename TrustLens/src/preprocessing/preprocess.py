"""Preprocessing pipeline for TrustLens Olist datasets."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.preprocessing.cleaner import (
    clean_customers,
    clean_order_items,
    clean_orders,
    clean_products,
    clean_reviews,
    clean_sellers,
)


DATASETS = {
    "orders": "olist_orders_dataset.csv",
    "order_items": "olist_order_items_dataset.csv",
    "reviews": "olist_order_reviews_dataset.csv",
    "sellers": "olist_sellers_dataset.csv",
    "customers": "olist_customers_dataset.csv",
    "products": "olist_products_dataset.csv",
}


CLEANERS = {
    "orders": clean_orders,
    "order_items": clean_order_items,
    "reviews": clean_reviews,
    "sellers": clean_sellers,
    "customers": clean_customers,
    "products": clean_products,
}


def preprocess_dataset(
    dataset_name: str,
    raw_dir: Path,
    processed_dir: Path,
) -> pd.DataFrame:
    """Load, clean, and save one Olist dataset."""
    if dataset_name not in DATASETS:
        raise ValueError(f"Unknown dataset: {dataset_name}")

    raw_path = raw_dir / DATASETS[dataset_name]

    if not raw_path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {raw_path}"
        )

    df = pd.read_csv(raw_path)

    cleaner = CLEANERS[dataset_name]
    cleaned_df = cleaner(df)

    processed_dir.mkdir(parents=True, exist_ok=True)

    output_path = processed_dir / DATASETS[dataset_name]
    cleaned_df.to_csv(output_path, index=False)

    return cleaned_df


def preprocess_all(
    raw_dir: Path,
    processed_dir: Path,
) -> dict[str, pd.DataFrame]:
    """Preprocess all configured Olist datasets."""
    processed_data = {}

    for dataset_name in DATASETS:
        processed_data[dataset_name] = preprocess_dataset(
            dataset_name=dataset_name,
            raw_dir=raw_dir,
            processed_dir=processed_dir,
        )

    return processed_data


if __name__ == "__main__":
    project_root = Path(__file__).resolve().parents[2]

    raw_directory = project_root / "data" / "raw"
    processed_directory = project_root / "data" / "processed"

    preprocess_all(
        raw_dir=raw_directory,
        processed_dir=processed_directory,
    )

    print("TrustLens preprocessing completed successfully.")