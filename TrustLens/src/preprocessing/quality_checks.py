"""Data quality validation utilities for TrustLens."""

from __future__ import annotations

from typing import Any

import pandas as pd


def check_dataset_not_empty(df: pd.DataFrame) -> bool:
    """Return True when the dataset contains at least one row."""
    return not df.empty


def get_missing_value_report(df: pd.DataFrame) -> pd.DataFrame:
    """Return missing-value counts and percentages by column."""
    total_rows = len(df)

    report = pd.DataFrame(
        {
            "column": df.columns,
            "missing_count": df.isna().sum().values,
        }
    )

    if total_rows > 0:
        report["missing_percentage"] = (
            report["missing_count"] / total_rows * 100
        )
    else:
        report["missing_percentage"] = 0.0

    return report


def get_duplicate_count(df: pd.DataFrame) -> int:
    """Return the number of completely duplicated rows."""
    return int(df.duplicated().sum())


def validate_review_scores(
    df: pd.DataFrame,
) -> dict[str, Any]:
    """Validate that review scores are within the 1-5 range."""
    if "review_score" not in df.columns:
        return {
            "valid": False,
            "message": "review_score column is missing",
        }

    invalid_count = int(
        (~df["review_score"].between(1, 5)).sum()
    )

    return {
        "valid": invalid_count == 0,
        "invalid_count": invalid_count,
    }


def validate_non_negative_columns(
    df: pd.DataFrame,
    columns: list[str],
) -> dict[str, Any]:
    """Validate that selected numeric columns are non-negative."""
    results = {}

    for column in columns:
        if column not in df.columns:
            results[column] = {
                "valid": False,
                "message": "column is missing",
            }
            continue

        numeric_values = pd.to_numeric(
            df[column],
            errors="coerce",
        )

        invalid_count = int(
            (numeric_values < 0).sum()
        )

        results[column] = {
            "valid": invalid_count == 0,
            "invalid_count": invalid_count,
        }

    return results


def validate_order_dates(df: pd.DataFrame) -> dict[str, Any]:
    """Check for deliveries occurring before purchases."""
    required_columns = [
        "order_purchase_timestamp",
        "order_delivered_customer_date",
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        return {
            "valid": False,
            "message": (
                f"Missing columns: {missing_columns}"
            ),
        }

    purchase_dates = pd.to_datetime(
        df["order_purchase_timestamp"],
        errors="coerce",
    )

    delivery_dates = pd.to_datetime(
        df["order_delivered_customer_date"],
        errors="coerce",
    )

    invalid_count = int(
        (delivery_dates < purchase_dates).sum()
    )

    return {
        "valid": invalid_count == 0,
        "invalid_count": invalid_count,
    }


def generate_quality_summary(
    df: pd.DataFrame,
) -> dict[str, Any]:
    """Generate a basic quality summary for a dataframe."""
    return {
        "row_count": len(df),
        "column_count": len(df.columns),
        "is_empty": df.empty,
        "duplicate_count": get_duplicate_count(df),
        "missing_values": int(df.isna().sum().sum()),
    }