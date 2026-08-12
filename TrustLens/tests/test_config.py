from src.config import (
    DATABASE_PATH,
    OLIST_DATASETS,
    STI_WEIGHTS,
    TRUST_BANDS,
)


def test_olist_dataset_configuration():
    """Verify that all required Olist datasets are configured."""
    expected_datasets = {
        "orders",
        "order_items",
        "reviews",
        "sellers",
        "customers",
        "products",
    }

    assert set(OLIST_DATASETS.keys()) == expected_datasets


def test_sti_weights():
    """Verify that Seller Trust Index weights sum to 100%."""
    assert sum(STI_WEIGHTS.values()) == 1.0


def test_trust_bands():
    """Verify that all required trust bands are configured."""
    assert "High Trust" in TRUST_BANDS
    assert "Monitor" in TRUST_BANDS
    assert "High Risk" in TRUST_BANDS


def test_database_path():
    """Verify that the database path is configured."""
    assert DATABASE_PATH.name == "trustlens.db"