"""
Tests for the TrustLens Olist data ingestion module.
"""

import pandas as pd

from src.ingestion.loader import load_dataset


def test_orders_dataset_can_be_loaded():
    """Verify that the Olist orders dataset loads correctly."""
    orders = load_dataset("orders")

    assert isinstance(orders, pd.DataFrame)
    assert not orders.empty


def test_sellers_dataset_can_be_loaded():
    """Verify that the Olist sellers dataset loads correctly."""
    sellers = load_dataset("sellers")

    assert isinstance(sellers, pd.DataFrame)
    assert not sellers.empty


def test_invalid_dataset_name():
    """Verify that an invalid dataset name raises ValueError."""
    try:
        load_dataset("invalid_dataset")
        assert False, "Expected ValueError"
    except ValueError:
        assert True