import pandas as pd

from src.feature_engineering.seller_analytics import (
    build_seller_analytics,
)


def test_build_seller_analytics():
    order_items = pd.DataFrame(
        {
            "order_id": ["order_1", "order_2"],
            "seller_id": ["seller_1", "seller_1"],
        }
    )

    orders = pd.DataFrame(
        {
            "order_id": ["order_1", "order_2"],
            "order_status": ["delivered", "delivered"],
            "on_time_delivery": [1, 0],
            "order_completed": [1, 1],
        }
    )

    reviews = pd.DataFrame(
        {
            "review_id": ["review_1", "review_2"],
            "order_id": ["order_1", "order_2"],
            "review_score": [5, 4],
        }
    )

    sellers = pd.DataFrame(
        {
            "seller_id": ["seller_1"],
            "seller_city": ["sao paulo"],
            "seller_state": ["SP"],
        }
    )

    result = build_seller_analytics(
        order_items=order_items,
        orders=orders,
        reviews=reviews,
        sellers=sellers,
    )

    assert not result.empty
    assert "seller_id" in result.columns
    assert "seller_average_rating" in result.columns
    assert "seller_completion_rate" in result.columns
    assert "seller_on_time_rate" in result.columns
    assert "seller_city" in result.columns
    assert "seller_state" in result.columns