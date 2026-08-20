"""Trust insights analytics for TrustLens."""

from __future__ import annotations

import pandas as pd


def rank_sellers_by_trust(
    seller_metrics: pd.DataFrame,
) -> pd.DataFrame:
    """Rank sellers from highest to lowest Seller Trust Index."""

    df = seller_metrics.copy()

    if "seller_trust_index" not in df.columns:
        raise ValueError(
            "seller_trust_index column is required"
        )

    df["trust_rank"] = (
        df["seller_trust_index"]
        .rank(method="min", ascending=False)
        .astype(int)
    )

    return df.sort_values(
        by=["seller_trust_index", "seller_id"],
        ascending=[False, True],
    ).reset_index(drop=True)


def get_trust_band_distribution(
    seller_metrics: pd.DataFrame,
) -> pd.DataFrame:
    """Return the number and percentage of sellers in each trust band."""

    if "trust_band" not in seller_metrics.columns:
        raise ValueError(
            "trust_band column is required"
        )

    distribution = (
        seller_metrics["trust_band"]
        .value_counts()
        .rename_axis("trust_band")
        .reset_index(name="seller_count")
    )

    total_sellers = len(seller_metrics)

    if total_sellers > 0:
        distribution["percentage"] = (
            distribution["seller_count"]
            / total_sellers
            * 100
        )
    else:
        distribution["percentage"] = 0.0

    return distribution


def get_high_risk_sellers(
    seller_metrics: pd.DataFrame,
) -> pd.DataFrame:
    """Return sellers classified as High Risk."""

    if "trust_band" not in seller_metrics.columns:
        raise ValueError(
            "trust_band column is required"
        )

    return (
        seller_metrics[
            seller_metrics["trust_band"].astype(str)
            == "High Risk"
        ]
        .sort_values(
            by="seller_trust_index",
            ascending=True,
        )
        .reset_index(drop=True)
    )


def get_trust_summary(
    seller_metrics: pd.DataFrame,
) -> dict[str, float | int]:
    """Return high-level Seller Trust Index summary metrics."""

    if "seller_trust_index" not in seller_metrics.columns:
        raise ValueError(
            "seller_trust_index column is required"
        )

    if seller_metrics.empty:
        return {
            "average_trust_index": 0.0,
            "minimum_trust_index": 0.0,
            "maximum_trust_index": 0.0,
            "high_risk_sellers": 0,
            "monitor_sellers": 0,
            "high_trust_sellers": 0,
        }

    trust_bands = (
        seller_metrics["trust_band"]
        .astype(str)
    )

    return {
        "average_trust_index": float(
            seller_metrics["seller_trust_index"].mean()
        ),
        "minimum_trust_index": float(
            seller_metrics["seller_trust_index"].min()
        ),
        "maximum_trust_index": float(
            seller_metrics["seller_trust_index"].max()
        ),
        "high_risk_sellers": int(
            (trust_bands == "High Risk").sum()
        ),
        "monitor_sellers": int(
            (trust_bands == "Monitor").sum()
        ),
        "high_trust_sellers": int(
            (trust_bands == "High Trust").sum()
        ),
    }


def add_risk_indicators(
    seller_metrics: pd.DataFrame,
) -> pd.DataFrame:
    """Add seller-level risk indicators for TrustLens insights."""

    df = seller_metrics.copy()

    if "seller_trust_index" not in df.columns:
        raise ValueError(
            "seller_trust_index column is required"
        )

    if "seller_on_time_rate" in df.columns:
        df["delivery_risk"] = (
            df["seller_on_time_rate"] < 80
        ).astype(int)

    if "seller_completion_rate" in df.columns:
        df["completion_risk"] = (
            df["seller_completion_rate"] < 80
        ).astype(int)

    if "seller_average_rating" in df.columns:
        df["rating_risk"] = (
            df["seller_average_rating"] < 3
        ).astype(int)

    risk_columns = [
        column
        for column in [
            "delivery_risk",
            "completion_risk",
            "rating_risk",
        ]
        if column in df.columns
    ]

    if risk_columns:
        df["risk_factor_count"] = df[risk_columns].sum(axis=1)
    else:
        df["risk_factor_count"] = 0

    return df