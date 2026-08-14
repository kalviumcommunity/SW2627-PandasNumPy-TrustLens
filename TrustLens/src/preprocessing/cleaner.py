"""Data cleaning utilities for TrustLens Olist datasets."""

from __future__ import annotations

import pandas as pd


def remove_exact_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Remove completely duplicated rows from a dataframe."""
    return df.drop_duplicates().copy()


def clean_orders(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and preprocess the Olist orders dataset."""
    cleaned = df.copy()

    timestamp_columns = [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ]

    for column in timestamp_columns:
        if column in cleaned.columns:
            cleaned[column] = pd.to_datetime(
                cleaned[column],
                errors="coerce",
            )

    cleaned = remove_exact_duplicates(cleaned)

    return cleaned


def clean_order_items(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and preprocess the Olist order items dataset."""
    cleaned = df.copy()

    numeric_columns = [
        "order_item_id",
        "price",
        "freight_value",
    ]

    for column in numeric_columns:
        if column in cleaned.columns:
            cleaned[column] = pd.to_numeric(
                cleaned[column],
                errors="coerce",
            )

    if "shipping_limit_date" in cleaned.columns:
        cleaned["shipping_limit_date"] = pd.to_datetime(
            cleaned["shipping_limit_date"],
            errors="coerce",
        )

    cleaned = remove_exact_duplicates(cleaned)

    return cleaned


def clean_reviews(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and preprocess the Olist reviews dataset."""
    cleaned = df.copy()

    if "review_score" in cleaned.columns:
        cleaned["review_score"] = pd.to_numeric(
            cleaned["review_score"],
            errors="coerce",
        )

    timestamp_columns = [
        "review_creation_date",
        "review_answer_timestamp",
    ]

    for column in timestamp_columns:
        if column in cleaned.columns:
            cleaned[column] = pd.to_datetime(
                cleaned[column],
                errors="coerce",
            )

    cleaned = remove_exact_duplicates(cleaned)

    return cleaned


def clean_sellers(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and preprocess the Olist sellers dataset."""
    cleaned = df.copy()

    if "seller_id" in cleaned.columns:
        cleaned["seller_id"] = cleaned["seller_id"].astype("string").str.strip()

    if "seller_city" in cleaned.columns:
        cleaned["seller_city"] = (
            cleaned["seller_city"].astype("string").str.strip()
        )

    if "seller_state" in cleaned.columns:
        cleaned["seller_state"] = (
            cleaned["seller_state"].astype("string").str.strip().str.upper()
        )

    cleaned = remove_exact_duplicates(cleaned)

    return cleaned


def clean_customers(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and preprocess the Olist customers dataset."""
    cleaned = df.copy()

    string_columns = [
        "customer_id",
        "customer_unique_id",
        "customer_city",
        "customer_state",
    ]

    for column in string_columns:
        if column in cleaned.columns:
            cleaned[column] = (
                cleaned[column].astype("string").str.strip()
            )

    if "customer_state" in cleaned.columns:
        cleaned["customer_state"] = (
            cleaned["customer_state"].str.upper()
        )

    cleaned = remove_exact_duplicates(cleaned)

    return cleaned


def clean_products(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and preprocess the Olist products dataset."""
    cleaned = df.copy()

    numeric_columns = [
        "product_name_lenght",
        "product_description_lenght",
        "product_photos_qty",
        "product_weight_g",
        "product_length_cm",
        "product_height_cm",
        "product_width_cm",
    ]

    for column in numeric_columns:
        if column in cleaned.columns:
            cleaned[column] = pd.to_numeric(
                cleaned[column],
                errors="coerce",
            )

    if "product_category_name" in cleaned.columns:
        cleaned["product_category_name"] = (
            cleaned["product_category_name"]
            .astype("string")
            .str.strip()
        )

    cleaned = remove_exact_duplicates(cleaned)

    return cleaned