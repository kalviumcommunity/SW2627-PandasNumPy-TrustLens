import pandas as pd

from src.analytics.trust_insights import (
    add_risk_indicators,
    get_high_risk_sellers,
    get_trust_band_distribution,
    get_trust_summary,
    rank_sellers_by_trust,
)


def sample_sellers():
    return pd.DataFrame(
        {
            "seller_id": [
                "seller_1",
                "seller_2",
                "seller_3",
            ],
            "seller_trust_index": [
                90.0,
                70.0,
                45.0,
            ],
            "trust_band": [
                "High Trust",
                "Monitor",
                "High Risk",
            ],
            "seller_on_time_rate": [
                95.0,
                75.0,
                60.0,
            ],
            "seller_completion_rate": [
                98.0,
                85.0,
                70.0,
            ],
            "seller_average_rating": [
                4.8,
                3.8,
                2.5,
            ],
        }
    )


def test_rank_sellers_by_trust():
    result = rank_sellers_by_trust(sample_sellers())

    assert result.iloc[0]["seller_id"] == "seller_1"
    assert result.iloc[0]["trust_rank"] == 1


def test_trust_band_distribution():
    result = get_trust_band_distribution(sample_sellers())

    assert result["seller_count"].sum() == 3
    assert set(result["trust_band"]) == {
        "High Trust",
        "Monitor",
        "High Risk",
    }


def test_high_risk_sellers():
    result = get_high_risk_sellers(sample_sellers())

    assert len(result) == 1
    assert result.iloc[0]["seller_id"] == "seller_3"


def test_trust_summary():
    result = get_trust_summary(sample_sellers())

    assert result["high_risk_sellers"] == 1
    assert result["monitor_sellers"] == 1
    assert result["high_trust_sellers"] == 1
    assert result["average_trust_index"] == 68.33333333333333


def test_risk_indicators():
    result = add_risk_indicators(sample_sellers())

    assert "delivery_risk" in result.columns
    assert "completion_risk" in result.columns
    assert "rating_risk" in result.columns
    assert "risk_factor_count" in result.columns

    seller_3 = result[
        result["seller_id"] == "seller_3"
    ].iloc[0]

    assert seller_3["risk_factor_count"] == 3