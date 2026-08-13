"""
Schema definitions and validation utilities for TrustLens Olist datasets.
"""

import pandas as pd


EXPECTED_COLUMNS = {
    "orders": [
        "order_id",
        "customer_id",
        "order_status",
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ],
    "order_items": [
        "order_id",
        "order_item_id",
        "product_id",
        "seller_id",
        "shipping_limit_date",
        "price",
        "freight_value",
    ],
    "reviews": [
        "review_id",
        "order_id",
        "review_score",
        "review_comment_title",
        "review_comment_message",
        "review_creation_date",
        "review_answer_timestamp",
    ],
    "sellers": [
        "seller_id",
        "seller_zip_code_prefix",
        "seller_city",
        "seller_state",
    ],
    "customers": [
        "customer_id",
        "customer_unique_id",
        "customer_zip_code_prefix",
        "customer_city",
        "customer_state",
    ],
    "products": [
        "product_id",
        "product_category_name",
        "product_name_lenght",
        "product_description_lenght",
        "product_photos_qty",
        "product_weight_g",
        "product_length_cm",
        "product_height_cm",
        "product_width_cm",
    ],
}


def validate_schema(
    dataframe: pd.DataFrame,
    dataset_name: str,
) -> tuple[bool, list[str]]:
    """
    Validate whether a dataset contains the required columns.

    Parameters
    ----------
    dataframe : pd.DataFrame
        Dataset to validate.

    dataset_name : str
        Dataset name defined in EXPECTED_COLUMNS.

    Returns
    -------
    tuple[bool, list[str]]
        Validation result and list of missing columns.
    """
    if dataset_name not in EXPECTED_COLUMNS:
        raise ValueError(
            f"Unknown dataset: {dataset_name}"
        )

    expected = set(EXPECTED_COLUMNS[dataset_name])
    actual = set(dataframe.columns)

    missing_columns = sorted(expected - actual)

    return len(missing_columns) == 0, missing_columns

