
"""Category-level trust analytics for TrustLens."""

from __future__ import annotations

import pandas as pd


def calculate_category_performance(
    order_items: pd.DataFrame,
    orders: pd.DataFrame,
    products: pd.DataFrame,
) -> pd.DataFrame:
    """
    Calculate category-level delivery and completion performance.
    """

    items = order_items.copy()
    order_data = orders.copy()
    product_data = products.copy()

    required_order_columns = [
        "order_id",
        "order_completed",
        "on_time_delivery",
    ]

    available_order_columns = [
        column
        for column in required_order_columns
        if column in order_data.columns
    ]

    order_data = order_data[available_order_columns]

    merged = items.merge(
        order_data,
        on="order_id",
        how="left",
    )

    merged = merged.merge(
        product_data[
            [
                "product_id",
                "product_category_name",
            ]
        ],
        on="product_id",
        how="left",
    )

    merged["product_category_name"] = (
        merged["product_category_name"]
        .fillna("Unknown")
    )

    category_metrics = (
        merged.groupby("product_category_name")
        .agg(
            total_orders=("order_id", "nunique"),
            completed_orders=("order_completed", "sum"),
            on_time_orders=("on_time_delivery", "sum"),
        )
        .reset_index()
    )

    category_metrics["completion_rate"] = (
        category_metrics["completed_orders"]
        / category_metrics["total_orders"]
        * 100
    )

    category_metrics["on_time_rate"] = (
        category_metrics["on_time_orders"]
        / category_metrics["total_orders"]
        * 100
    )

    return category_metrics


def identify_low_performing_categories(
    category_metrics: pd.DataFrame,
    on_time_threshold: float = 80.0,
    completion_threshold: float = 80.0,
) -> pd.DataFrame:
    """Identify categories with weaker delivery or completion performance."""

    df = category_metrics.copy()

    df["delivery_risk"] = (
        df["on_time_rate"] < on_time_threshold
    ).astype(int)

    df["completion_risk"] = (
        df["completion_rate"] < completion_threshold
    ).astype(int)

    df["risk_factor_count"] = (
        df["delivery_risk"]
        + df["completion_risk"]
    )

    return df[
        df["risk_factor_count"] > 0
    ].sort_values(
        by="risk_factor_count",
        ascending=False,
    ).reset_index(drop=True)


def rank_categories_by_delivery(
    category_metrics: pd.DataFrame,
) -> pd.DataFrame:
    """Rank product categories by on-time delivery performance."""

    df = category_metrics.copy()

    df["delivery_rank"] = (
        df["on_time_rate"]
        .rank(method="min", ascending=False)
        .astype(int)
    )

    return df.sort_values(
        by="on_time_rate",
        ascending=False,
    ).reset_index(drop=True)

