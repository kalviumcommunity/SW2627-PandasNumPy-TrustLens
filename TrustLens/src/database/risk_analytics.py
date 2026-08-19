"""Delivery, review, and seller risk analytics for TrustLens."""

from __future__ import annotations

import sqlite3

import pandas as pd


def get_delivery_performance(
    connection: sqlite3.Connection,
) -> pd.DataFrame:
    """Return delivery performance metrics."""

    query = """
        SELECT
            order_month,
            COUNT(*) AS total_orders,
            AVG(delivery_days) AS average_delivery_days,
            AVG(delivery_delay_days) AS average_delivery_delay,
            AVG(on_time_delivery) * 100 AS on_time_rate
        FROM order_features
        GROUP BY order_month
        ORDER BY order_month
    """

    return pd.read_sql_query(query, connection)


def get_review_performance(
    connection: sqlite3.Connection,
) -> pd.DataFrame:
    """Return seller review performance."""

    query = """
        SELECT
            seller_id,
            seller_average_rating,
            seller_review_count
        FROM seller_metrics
        ORDER BY seller_average_rating DESC
    """

    return pd.read_sql_query(query, connection)


def get_high_risk_sellers(
    connection: sqlite3.Connection,
) -> pd.DataFrame:
    """Return sellers with high-risk trust classification."""

    query = """
        SELECT
            seller_id,
            seller_total_orders,
            seller_average_rating,
            seller_on_time_rate,
            seller_completion_rate,
            seller_review_count,
            seller_trust_index,
            trust_band
        FROM seller_metrics
        WHERE trust_band = 'High Risk'
        ORDER BY seller_trust_index ASC
    """

    return pd.read_sql_query(query, connection)


def get_seller_risk_indicators(
    connection: sqlite3.Connection,
) -> pd.DataFrame:
    """Return seller behaviour indicators related to trust."""

    query = """
        SELECT
            seller_id,
            seller_trust_index,
            seller_average_rating,
            seller_on_time_rate,
            seller_completion_rate,
            seller_review_count,
            trust_band
        FROM seller_metrics
        ORDER BY seller_trust_index ASC
    """

    return pd.read_sql_query(query, connection)
