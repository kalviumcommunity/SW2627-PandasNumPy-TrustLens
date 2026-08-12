# TrustLens project configuration.
from pathlib import Path


# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent


# Data directories
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"


# Database configuration
DATABASE_DIR = PROJECT_ROOT / "database"
DATABASE_PATH = DATABASE_DIR / "trustlens.db"


# Expected Olist dataset files
OLIST_DATASETS = {
    "orders": "olist_orders_dataset.csv",
    "order_items": "olist_order_items_dataset.csv",
    "reviews": "olist_order_reviews_dataset.csv",
    "sellers": "olist_sellers_dataset.csv",
    "customers": "olist_customers_dataset.csv",
    "products": "olist_products_dataset.csv",
}


# Seller Trust Index weights
STI_WEIGHTS = {
    "rating": 0.40,
    "on_time_delivery": 0.30,
    "completion_rate": 0.20,
    "review_volume": 0.10,
}


# Seller Trust Index bands
TRUST_BANDS = {
    "High Trust": (80, 100),
    "Monitor": (60, 79),
    "High Risk": (0, 59),
}
