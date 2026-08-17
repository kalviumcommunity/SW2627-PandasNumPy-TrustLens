import pandas as pd


def create_order_features(orders: pd.DataFrame) -> pd.DataFrame:
    """
    Create TrustLens order and delivery features.

    Expected input columns:
    - order_id
    - order_status
    - order_purchase_timestamp
    - order_delivered_customer_date
    - order_estimated_delivery_date
    """

    df = orders.copy()

    # Convert timestamp columns to datetime
    date_columns = [
        "order_purchase_timestamp",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ]

    for column in date_columns:
        if column in df.columns:
            df[column] = pd.to_datetime(df[column], errors="coerce")

    # Month of order purchase
    df["order_month"] = df["order_purchase_timestamp"].dt.to_period("M").astype(str)

    # Delivery duration in days
    df["delivery_days"] = (
        df["order_delivered_customer_date"]
        - df["order_purchase_timestamp"]
    ).dt.total_seconds() / (24 * 60 * 60)

    # Delivery delay compared with estimated delivery date
    df["delivery_delay_days"] = (
        df["order_delivered_customer_date"].dt.normalize()
        - df["order_estimated_delivery_date"].dt.normalize()
        ).dt.days

    # On-time delivery indicator
    df["on_time_delivery"] = (
        df["order_delivered_customer_date"].notna()
        & df["order_estimated_delivery_date"].notna()
        & (
            df["order_delivered_customer_date"]
            <= df["order_estimated_delivery_date"]
        )
    ).astype(int)

    # Completed order indicator
    df["order_completed"] = (
        df["order_status"].eq("delivered")
    ).astype(int)

    return df