
from pathlib import Path


def test_dashboard_home_exists():
    """Verify that the Streamlit dashboard entry point exists."""
    dashboard_file = Path("dashboard/Home.py")

    assert dashboard_file.exists()


def test_dashboard_pages_directory_exists():
    """Verify that the dashboard pages directory exists."""
    pages_directory = Path("dashboard/pages")

    assert pages_directory.exists()
    assert pages_directory.is_dir()

