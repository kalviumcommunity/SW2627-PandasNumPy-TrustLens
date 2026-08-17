import pandas as pd

from src.feature_engineering.order_features import create_order_features


def test_create_order_features():
    orders = pd.DataFrame(
        {
            "order_id": ["order_1"],
            "order_status": ["delivered"],
            "order_purchase_timestamp": ["2025-01-01 10:00:00"],
            "order_delivered_customer_date": ["2025-01-05 10:00:00"],
            "order_estimated_delivery_date": ["2025-01-07"],
        }
    )

    result = create_order_features(orders)

    assert "order_month" in result.columns
    assert "delivery_days" in result.columns
    assert "delivery_delay_days" in result.columns
    assert "on_time_delivery" in result.columns
    assert "order_completed" in result.columns

    assert result.loc[0, "delivery_days"] == 4
    assert result.loc[0, "delivery_delay_days"] == -2
    assert result.loc[0, "on_time_delivery"] == 1
    assert result.loc[0, "order_completed"] == 1


def test_late_delivery():
    orders = pd.DataFrame(
        {
            "order_id": ["order_2"],
            "order_status": ["delivered"],
            "order_purchase_timestamp": ["2025-01-01"],
            "order_delivered_customer_date": ["2025-01-10"],
            "order_estimated_delivery_date": ["2025-01-07"],
        }
    )

    result = create_order_features(orders)

    assert result.loc[0, "delivery_delay_days"] == 3
    assert result.loc[0, "on_time_delivery"] == 0


def test_non_delivered_order():
    orders = pd.DataFrame(
        {
            "order_id": ["order_3"],
            "order_status": ["canceled"],
            "order_purchase_timestamp": ["2025-01-01"],
            "order_delivered_customer_date": [None],
            "order_estimated_delivery_date": ["2025-01-07"],
        }
    )

    result = create_order_features(orders)

    assert result.loc[0, "order_completed"] == 0