import sqlite3

import pandas as pd

from src.database.risk_analytics import (
    get_delivery_performance,
    get_high_risk_sellers,
    get_review_performance,
    get_seller_risk_indicators,
)


def create_test_database():
    connection = sqlite3.connect(":memory:")

    order_features = pd.DataFrame(
        {
            "order_id": ["o1", "o2", "o3"],
            "seller_id": ["s1", "s1", "s2"],
            "order_month": [
                "2025-01",
                "2025-01",
                "2025-02",
            ],
            "delivery_days": [3, 5, 7],
            "delivery_delay_days": [-2, 1, 2],
            "on_time_delivery": [1, 1, 0],
        }
    )

    seller_metrics = pd.DataFrame(
        {
            "seller_id": ["s1", "s2"],
            "seller_total_orders": [2, 1],
            "seller_average_rating": [4.5, 2.5],
            "seller_on_time_rate": [100.0, 0.0],
            "seller_completion_rate": [100.0, 50.0],
            "seller_review_count": [2, 1],
            "seller_trust_index": [90.0, 40.0],
            "trust_band": ["High Trust", "High Risk"],
        }
    )

    order_features.to_sql(
        "order_features",
        connection,
        index=False,
    )

    seller_metrics.to_sql(
        "seller_metrics",
        connection,
        index=False,
    )

    return connection


def test_delivery_performance():
    connection = create_test_database()

    result = get_delivery_performance(connection)

    assert len(result) == 2
    assert "average_delivery_days" in result.columns
    assert "on_time_rate" in result.columns

    connection.close()


def test_review_performance():
    connection = create_test_database()

    result = get_review_performance(connection)

    assert len(result) == 2
    assert "seller_average_rating" in result.columns

    connection.close()


def test_high_risk_sellers():
    connection = create_test_database()

    result = get_high_risk_sellers(connection)

    assert len(result) == 1
    assert result.iloc[0]["seller_id"] == "s2"
    assert result.iloc[0]["trust_band"] == "High Risk"

    connection.close()


def test_seller_risk_indicators():
    connection = create_test_database()

    result = get_seller_risk_indicators(connection)

    assert len(result) == 2
    assert result.iloc[0]["seller_id"] == "s2"

    connection.close()

