import pandas as pd


def create_seller_features(
    order_items: pd.DataFrame,
    orders: pd.DataFrame,
    reviews: pd.DataFrame,
) -> pd.DataFrame:
    """
    Create seller-level TrustLens metrics.

    Combines order items, order-level delivery features,
    and review information to produce seller-level metrics.
    """

    # Work on copies
    items = order_items.copy()
    order_data = orders.copy()
    review_data = reviews.copy()

    # Keep only required order-level features
    order_columns = [
        "order_id",
        "order_status",
        "on_time_delivery",
    ]

    order_data = order_data[
        [column for column in order_columns if column in order_data.columns]
    ]

    # Join order information to seller/order-item data
    seller_orders = items.merge(
        order_data,
        on="order_id",
        how="left",
    )

    # Seller-level order metrics
    seller_metrics = (
        seller_orders.groupby("seller_id")
        .agg(
            seller_total_orders=("order_id", "nunique"),
            seller_completed_orders=("order_completed", "sum"),
            seller_on_time_orders=("on_time_delivery", "sum"),
        )
        .reset_index()
    )

    # Completion rate
    seller_metrics["seller_completion_rate"] = (
        seller_metrics["seller_completed_orders"]
        / seller_metrics["seller_total_orders"]
        * 100
    )

    # On-time delivery rate
    seller_metrics["seller_on_time_rate"] = (
        seller_metrics["seller_on_time_orders"]
        / seller_metrics["seller_total_orders"]
        * 100
    )

    # Join seller information to reviews through order_id
    review_orders = items[
        ["order_id", "seller_id"]
    ].drop_duplicates()

    seller_reviews = review_data.merge(
        review_orders,
        on="order_id",
        how="inner",
    )

    review_metrics = (
        seller_reviews.groupby("seller_id")
        .agg(
            seller_average_rating=("review_score", "mean"),
            seller_review_count=("review_id", "nunique"),
        )
        .reset_index()
    )

    # Combine seller metrics
    seller_metrics = seller_metrics.merge(
        review_metrics,
        on="seller_id",
        how="left",
    )

    seller_metrics["seller_average_rating"] = (
        seller_metrics["seller_average_rating"].fillna(0)
    )

    seller_metrics["seller_review_count"] = (
        seller_metrics["seller_review_count"].fillna(0)
    )

    return seller_metrics