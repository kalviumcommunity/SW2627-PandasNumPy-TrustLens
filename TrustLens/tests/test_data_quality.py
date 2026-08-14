"""Tests for TrustLens data quality validation."""

import pandas as pd

from src.preprocessing.quality_checks import (
    check_dataset_not_empty,
    generate_quality_summary,
    get_duplicate_count,
    get_missing_value_report,
    validate_non_negative_columns,
    validate_order_dates,
    validate_review_scores,
)


def test_dataset_not_empty():
    df = pd.DataFrame({"id": [1, 2]})

    assert check_dataset_not_empty(df)


def test_duplicate_count():
    df = pd.DataFrame(
        {
            "id": [1, 1, 2],
        }
    )

    assert get_duplicate_count(df) == 1


def test_missing_value_report():
    df = pd.DataFrame(
        {
            "name": ["A", None],
        }
    )

    report = get_missing_value_report(df)

    assert report.loc[0, "column"] == "name"
    assert report.loc[0, "missing_count"] == 1
    assert report.loc[0, "missing_percentage"] == 50.0


def test_valid_review_scores():
    df = pd.DataFrame(
        {
            "review_score": [1, 3, 5],
        }
    )

    result = validate_review_scores(df)

    assert result["valid"]


def test_invalid_review_scores():
    df = pd.DataFrame(
        {
            "review_score": [1, 3, 6],
        }
    )

    result = validate_review_scores(df)

    assert not result["valid"]
    assert result["invalid_count"] == 1


def test_non_negative_values():
    df = pd.DataFrame(
        {
            "price": [100, 200],
        }
    )

    result = validate_non_negative_columns(
        df,
        ["price"],
    )

    assert result["price"]["valid"]


def test_invalid_negative_values():
    df = pd.DataFrame(
        {
            "price": [100, -20],
        }
    )

    result = validate_non_negative_columns(
        df,
        ["price"],
    )

    assert not result["price"]["valid"]


def test_order_date_validation():
    df = pd.DataFrame(
        {
            "order_purchase_timestamp": [
                "2018-01-01"
            ],
            "order_delivered_customer_date": [
                "2018-01-03"
            ],
        }
    )

    result = validate_order_dates(df)

    assert result["valid"]


def test_quality_summary():
    df = pd.DataFrame(
        {
            "id": [1, 2],
            "value": [10, 20],
        }
    )

    summary = generate_quality_summary(df)

    assert summary["row_count"] == 2
    assert summary["column_count"] == 2
    assert summary["duplicate_count"] == 0