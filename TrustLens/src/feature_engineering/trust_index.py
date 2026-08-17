import pandas as pd


def calculate_seller_trust_index(
    seller_metrics: pd.DataFrame,
) -> pd.DataFrame:
    """
    Calculate the TrustLens Seller Trust Index (STI).

    Components:
    - Rating Score: 40%
    - On-Time Delivery Rate: 30%
    - Completion Rate: 20%
    - Review Volume Score: 10%
    """

    df = seller_metrics.copy()

    # Normalize average rating from 1-5 to 0-100
    df["rating_score"] = (
        (df["seller_average_rating"] - 1) / 4 * 100
    ).clip(lower=0, upper=100)

    # Normalize review volume using min-max normalization
    min_reviews = df["seller_review_count"].min()
    max_reviews = df["seller_review_count"].max()

    if max_reviews == min_reviews:
        df["review_volume_score"] = 100.0
    else:
        df["review_volume_score"] = (
            (df["seller_review_count"] - min_reviews)
            / (max_reviews - min_reviews)
            * 100
        )

    # Calculate Seller Trust Index
    df["seller_trust_index"] = (
        (df["rating_score"] * 0.40)
        + (df["seller_on_time_rate"] * 0.30)
        + (df["seller_completion_rate"] * 0.20)
        + (df["review_volume_score"] * 0.10)
    ).clip(lower=0, upper=100)

    # Trust band classification
    df["trust_band"] = pd.cut(
        df["seller_trust_index"],
        bins=[-1, 59, 79, 100],
        labels=[
            "High Risk",
            "Monitor",
            "High Trust",
        ],
    )

    return df