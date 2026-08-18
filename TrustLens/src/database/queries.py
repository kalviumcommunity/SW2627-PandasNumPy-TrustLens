"""SQL query utilities for TrustLens."""

from __future__ import annotations

import sqlite3

import pandas as pd


def get_seller_metrics(
    connection: sqlite3.Connection,
) -> pd.DataFrame:
    """Return seller-level TrustLens metrics."""

    query = """
        SELECT
            seller_id,
            seller_total_orders,
            seller_average_rating,
            seller_review_count,
            seller_completion_rate,
            seller_on_time_rate,
            seller_trust_index,
            trust_band
        FROM seller_metrics
        ORDER BY seller_trust_index DESC
    """

    return pd.read_sql_query(query, connection)


def get_high_risk_sellers(
    connection: sqlite3.Connection,
) -> pd.DataFrame:
    """Return sellers classified as high risk."""

    query = """
        SELECT *
        FROM seller_metrics
        WHERE trust_band = 'High Risk'
        ORDER BY seller_trust_index ASC
    """

    return pd.read_sql_query(query, connection)
