"""Tests for TrustLens data cleaning and preprocessing."""

import pandas as pd

from src.preprocessing.cleaner import (
    clean_orders,
    clean_order_items,
    clean_reviews,
    clean_sellers,
)


def test_remove_duplicate_orders():
    df = pd.DataFrame(
        {
            "order_id": ["order_1", "order_1"],
            "order_status": ["delivered", "delivered"],
        }
    )

    cleaned = clean_orders(df)

    assert len(cleaned) == 1


def test_order_dates_are_converted():
    df = pd.DataFrame(
        {
            "order_purchase_timestamp": [
                "2018-01-01 10:00:00"
            ]
        }
    )

    cleaned = clean_orders(df)

    assert pd.api.types.is_datetime64_any_dtype(
        cleaned["order_purchase_timestamp"]
    )


def test_review_score_is_numeric():
    df = pd.DataFrame(
        {
            "review_score": ["5", "4", "3"]
        }
    )

    cleaned = clean_reviews(df)

    assert pd.api.types.is_numeric_dtype(
        cleaned["review_score"]
    )


def test_order_item_price_is_numeric():
    df = pd.DataFrame(
        {
            "price": ["100.50", "200.00"],
            "freight_value": ["10.00", "20.00"],
        }
    )

    cleaned = clean_order_items(df)

    assert pd.api.types.is_numeric_dtype(
        cleaned["price"]
    )


def test_seller_state_is_normalized():
    df = pd.DataFrame(
        {
            "seller_id": ["seller_1"],
            "seller_state": [" sp "],
        }
    )

    cleaned = clean_sellers(df)

    assert cleaned.loc[0, "seller_state"] == "SP"