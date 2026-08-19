import sqlite3

import pandas as pd

from src.database.analytics import (
    get_marketplace_kpis,
    get_seller_count_by_trust_band,
    get_seller_rankings,
    get_top_sellers,
)


def create_test_database():
    connection = sqlite3.connect(":memory:")

    order_features = pd.DataFrame(
        {
            "order_id": ["o1", "o2", "o3"],
            "seller_id": ["s1", "s1", "s2"],
            "delivery_days": [3, 5, 4],
            "on_time_delivery": [1, 1, 0],
            "seller_average_rating": [4.5, 4.5, 3.5],
        }
    )

    seller_metrics = pd.DataFrame(
        {
            "seller_id": ["s1", "s2"],
            "seller_total_orders": [2, 1],
            "seller_average_rating": [4.5, 3.5],
            "seller_review_count": [2, 1],
            "seller_completion_rate": [100.0, 80.0],
            "seller_on_time_rate": [100.0, 0.0],
            "seller_trust_index": [90.0, 55.0],
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


def test_marketplace_kpis():
    connection = create_test_database()

    result = get_marketplace_kpis(connection)

    assert result["total_orders"] == 3
    assert result["total_sellers"] == 2
    assert result["average_delivery_days"] == 4.0

    connection.close()


def test_seller_rankings():
    connection = create_test_database()

    result = get_seller_rankings(connection)

    assert len(result) == 2
    assert result.iloc[0]["seller_id"] == "s1"

    connection.close()


def test_top_sellers():
    connection = create_test_database()

    result = get_top_sellers(connection, limit=1)

    assert len(result) == 1
    assert result.iloc[0]["seller_id"] == "s1"

    connection.close()


def test_trust_band_distribution():
    connection = create_test_database()

    result = get_seller_count_by_trust_band(connection)

    assert len(result) == 2
    assert "High Trust" in result["trust_band"].values
    assert "High Risk" in result["trust_band"].values

    connection.close()