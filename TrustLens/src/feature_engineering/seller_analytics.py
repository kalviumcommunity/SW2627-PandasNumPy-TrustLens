"""Build the unified seller analytics dataset for TrustLens."""

from __future__ import annotations

import pandas as pd

from src.feature_engineering.seller_features import create_seller_features
from src.feature_engineering.trust_index import calculate_seller_trust_index


def build_seller_analytics(
    order_items: pd.DataFrame,
    orders: pd.DataFrame,
    reviews: pd.DataFrame,
    sellers: pd.DataFrame,
) -> pd.DataFrame:
    """
    Build the unified seller-level analytics dataset.

    Combines:
    - seller performance metrics
    - customer review metrics
    - Seller Trust Index
    - seller location information
    """

    seller_features = create_seller_features(
        order_items=order_items,
        orders=orders,
        reviews=reviews,
    )

    trust_features = calculate_seller_trust_index(
        seller_features
    )

    seller_columns = [
        "seller_id",
        "seller_city",
        "seller_state",
    ]

    available_columns = [
        column
        for column in seller_columns
        if column in sellers.columns
    ]

    seller_info = sellers[available_columns].drop_duplicates(
        subset=["seller_id"]
    )

    analytics = trust_features.merge(
        seller_info,
        on="seller_id",
        how="left",
    )

    return analytics