"""Utilities for loading TrustLens data into SQLite."""

from __future__ import annotations

import pandas as pd

from src.database.connection import get_connection


def load_dataframe(
    df: pd.DataFrame,
    table_name: str,
    if_exists: str = "replace",
) -> None:
    """Load a Pandas DataFrame into a SQLite table."""

    if df.empty:
        raise ValueError(
            f"Cannot load empty dataframe into table '{table_name}'."
        )

    with get_connection() as connection:
        df.to_sql(
            table_name,
            connection,
            if_exists=if_exists,
            index=False,
        )


def load_feature_data(
    orders: pd.DataFrame,
    seller_metrics: pd.DataFrame,
) -> None:
    """Load TrustLens feature-engineered datasets into SQLite."""

    load_dataframe(
        orders,
        table_name="order_features",
    )

    load_dataframe(
        seller_metrics,
        table_name="seller_metrics",
    )