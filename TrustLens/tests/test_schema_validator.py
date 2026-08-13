"""
Tests for TrustLens dataset schema validation.
"""

import pandas as pd

from src.ingestion.schema_validator import validate_schema


def test_orders_schema_is_valid():
    """Verify that the required Orders columns are detected."""
    dataframe = pd.DataFrame(
        columns=[
            "order_id",
            "customer_id",
            "order_status",
            "order_purchase_timestamp",
            "order_approved_at",
            "order_delivered_carrier_date",
            "order_delivered_customer_date",
            "order_estimated_delivery_date",
        ]
    )

    valid, missing = validate_schema(dataframe, "orders")

    assert valid is True
    assert missing == []


def test_missing_column_is_detected():
    """Verify that missing required columns are detected."""
    dataframe = pd.DataFrame(
        columns=[
            "order_id",
            "customer_id",
        ]
    )

    valid, missing = validate_schema(dataframe, "orders")

    assert valid is False
    assert "order_status" in missing


def test_unknown_dataset_is_rejected():
    """Verify that an unknown dataset raises ValueError."""
    dataframe = pd.DataFrame()

    try:
        validate_schema(dataframe, "unknown")
        assert False, "Expected ValueError"
    except ValueError:
        assert True
