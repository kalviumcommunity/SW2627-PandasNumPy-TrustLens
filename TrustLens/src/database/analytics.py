"""Core SQL analytics for TrustLens."""

from __future__ import annotations

import sqlite3

import pandas as pd


def get_marketplace_kpis(
    connection: sqlite3.Connection,
) -> dict[str, float | int]:
    """Return the main marketplace KPIs."""

    query = """
        SELECT
            COUNT(*) AS total_orders,
            COUNT(DISTINCT seller_id) AS total_sellers,
            AVG(seller_average_rating) AS average_rating,
            AVG(delivery_days) AS average_delivery_days,
            AVG(on_time_delivery) * 100 AS on_time_delivery_rate
        FROM order_features
    """

    result = pd.read_sql_query(query, connection)

    row = result.iloc[0]

    return {
        "total_orders": int(row["total_orders"]),
        "total_sellers": int(row["total_sellers"]),
        "average_rating": float(row["average_rating"] or 0),
        "average_delivery_days": float(
            row["average_delivery_days"] or 0
        ),
        "on_time_delivery_rate": float(
            row["on_time_delivery_rate"] or 0
        ),
    }


def get_seller_rankings(
    connection: sqlite3.Connection,
) -> pd.DataFrame:
    """Return sellers ranked by Seller Trust Index."""

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


def get_top_sellers(
    connection: sqlite3.Connection,
    limit: int = 10,
) -> pd.DataFrame:
    """Return the highest-ranked sellers."""

    query = """
        SELECT
            seller_id,
            seller_trust_index,
            seller_average_rating,
            seller_on_time_rate,
            seller_completion_rate,
            trust_band
        FROM seller_metrics
        ORDER BY seller_trust_index DESC
        LIMIT ?
    """

    return pd.read_sql_query(
        query,
        connection,
        params=(limit,),
    )


def get_seller_count_by_trust_band(
    connection: sqlite3.Connection,
) -> pd.DataFrame:
    """Return the number of sellers in each trust band."""

    query = """
        SELECT
            trust_band,
            COUNT(*) AS seller_count
        FROM seller_metrics
        GROUP BY trust_band
        ORDER BY seller_count DESC
    """

    return pd.read_sql_query(query, connection)