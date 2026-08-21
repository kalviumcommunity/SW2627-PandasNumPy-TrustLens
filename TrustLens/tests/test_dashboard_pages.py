from pathlib import Path


def test_dashboard_pages_exist():
    """Verify that all required dashboard pages exist."""

    pages = [
        "dashboard/pages/1_Seller_Performance.py",
        "dashboard/pages/2_Delivery_Performance.py",
        "dashboard/pages/3_Customer_Reviews.py",
        "dashboard/pages/4_Trust_Insights.py",
    ]

    for page in pages:
        assert Path(page).exists()