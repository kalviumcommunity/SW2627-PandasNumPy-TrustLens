"""Core SQL analytics for TrustLens."""

from __future__ import annotations

import sqlite3

import pandas as pd


def get_marketplace_kpis(
    connection: sqlite3.Connection,
) -> dict[str, float | int]:
    """Return the main marketplace KPIs."""

    order_query = """
        SELECT
            COUNT(*) AS total_orders,
            AVG(delivery_days) AS average_delivery_days,
            AVG(on_time_delivery) * 100 AS on_time_delivery_rate
        FROM order_features
    """

    seller_query = """
        SELECT
            COUNT(DISTINCT seller_id) AS total_sellers,
            AVG(seller_average_rating) AS average_rating,
            AVG(seller_trust_index) AS average_seller_trust_index
        FROM seller_metrics
    """

    order_result = pd.read_sql_query(
        order_query,
        connection,
    )

    seller_result = pd.read_sql_query(
        seller_query,
        connection,
    )

    order_row = order_result.iloc[0]
    seller_row = seller_result.iloc[0]

    return {
        "total_orders": int(order_row["total_orders"] or 0),
        "total_sellers": int(seller_row["total_sellers"] or 0),
        "average_rating": float(
            seller_row["average_rating"] or 0
        ),
        "average_delivery_days": float(
            order_row["average_delivery_days"] or 0
        ),
        "on_time_delivery_rate": float(
            order_row["on_time_delivery_rate"] or 0
        ),
        "average_seller_trust_index": float(
            seller_row["average_seller_trust_index"] or 0
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

    return pd.read_sql_query(
        query,
        connection,
    )


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

    return pd.read_sql_query(
        query,
        connection,
    )


def get_delivery_trends(
    connection: sqlite3.Connection,
) -> pd.DataFrame:
    """Return monthly delivery performance metrics."""

    query = """
        SELECT
            order_month,
            COUNT(*) AS total_orders,
            AVG(delivery_days) AS average_delivery_days,
            AVG(delivery_delay_days) AS average_delivery_delay,
            AVG(on_time_delivery) * 100 AS on_time_delivery_rate
        FROM order_features
        GROUP BY order_month
        ORDER BY order_month
    """

    return pd.read_sql_query(
        query,
        connection,
    )


def get_high_risk_sellers(
    connection: sqlite3.Connection,
) -> pd.DataFrame:
    """Return sellers classified as High Risk."""

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
        WHERE trust_band = 'High Risk'
        ORDER BY seller_trust_index ASC
    """

    return pd.read_sql_query(
        query,
        connection,
    )


def get_trust_distribution(
    connection: sqlite3.Connection,
) -> pd.DataFrame:
    """Return Seller Trust Index distribution by trust band."""

    query = """
        SELECT
            trust_band,
            COUNT(*) AS seller_count,
            AVG(seller_trust_index) AS average_trust_index
        FROM seller_metrics
        GROUP BY trust_band
        ORDER BY
            CASE trust_band
                WHEN 'High Risk' THEN 1
                WHEN 'Monitor' THEN 2
                WHEN 'High Trust' THEN 3
                ELSE 4
            END
    """

    return pd.read_sql_query(
        query,
        connection,
    )