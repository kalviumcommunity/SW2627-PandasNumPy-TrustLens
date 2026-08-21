import pandas as pd

from src.analytics.category_insights import (
    calculate_category_performance,
    identify_low_performing_categories,
    rank_categories_by_delivery,
)


def sample_data():
    order_items = pd.DataFrame(
        {
            "order_id": ["o1", "o2", "o3"],
            "product_id": ["p1", "p2", "p3"],
        }
    )

    orders = pd.DataFrame(
        {
            "order_id": ["o1", "o2", "o3"],
            "order_completed": [1, 1, 0],
            "on_time_delivery": [1, 0, 0],
        }
    )

    products = pd.DataFrame(
        {
            "product_id": ["p1", "p2", "p3"],
            "product_category_name": [
                "electronics",
                "electronics",
                "furniture",
            ],
        }
    )

    return order_items, orders, products


def test_calculate_category_performance():
    items, orders, products = sample_data()

    result = calculate_category_performance(
        items,
        orders,
        products,
    )

    assert "total_orders" in result.columns
    assert "completion_rate" in result.columns
    assert "on_time_rate" in result.columns


def test_low_performing_categories():
    items, orders, products = sample_data()

    metrics = calculate_category_performance(
        items,
        orders,
        products,
    )

    result = identify_low_performing_categories(
        metrics
    )

    assert "risk_factor_count" in result.columns
    assert len(result) > 0


def test_rank_categories():
    items, orders, products = sample_data()

    metrics = calculate_category_performance(
        items,
        orders,
        products,
    )

    result = rank_categories_by_delivery(metrics)

    assert "delivery_rank" in result.columns
    assert result["delivery_rank"].min() == 1

