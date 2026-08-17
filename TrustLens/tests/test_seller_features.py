import pandas as pd

from src.feature_engineering.trust_index import calculate_seller_trust_index


def test_seller_trust_index():
    seller_metrics = pd.DataFrame(
        {
            "seller_id": ["seller_1", "seller_2"],
            "seller_average_rating": [5.0, 3.0],
            "seller_on_time_rate": [100.0, 50.0],
            "seller_completion_rate": [100.0, 80.0],
            "seller_review_count": [100, 50],
        }
    )

    result = calculate_seller_trust_index(seller_metrics)

    assert "rating_score" in result.columns
    assert "review_volume_score" in result.columns
    assert "seller_trust_index" in result.columns
    assert "trust_band" in result.columns

    assert result["seller_trust_index"].between(0, 100).all()


def test_trust_band_classification():
    seller_metrics = pd.DataFrame(
        {
            "seller_id": ["seller_1"],
            "seller_average_rating": [5.0],
            "seller_on_time_rate": [100.0],
            "seller_completion_rate": [100.0],
            "seller_review_count": [100],
        }
    )

    result = calculate_seller_trust_index(seller_metrics)

    assert result.loc[0, "trust_band"] == "High Trust"


def test_rating_normalization():
    seller_metrics = pd.DataFrame(
        {
            "seller_id": ["seller_1", "seller_2"],
            "seller_average_rating": [1.0, 5.0],
            "seller_on_time_rate": [100.0, 100.0],
            "seller_completion_rate": [100.0, 100.0],
            "seller_review_count": [10, 20],
        }
    )

    result = calculate_seller_trust_index(seller_metrics)

    assert result.loc[0, "rating_score"] == 0
    assert result.loc[1, "rating_score"] == 100