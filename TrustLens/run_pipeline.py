"""TrustLens end-to-end data pipeline."""

from pathlib import Path

from src.preprocessing.preprocess import preprocess_all
from src.feature_engineering.order_features import create_order_features
from src.feature_engineering.seller_features import create_seller_features
from src.feature_engineering.trust_index import calculate_seller_trust_index
from src.database.loader import load_feature_data
from src.database.connection import get_database_path
from src.database.validation import get_table_names, get_row_count


def main() -> None:
    """Run the TrustLens data pipeline."""

    project_root = Path(__file__).resolve().parent

    raw_dir = project_root / "data" / "raw"
    processed_dir = project_root / "data" / "processed"

    print("Starting TrustLens pipeline...")

    # ---------------------------------------------------------
    # 1. Preprocess raw Olist datasets
    # ---------------------------------------------------------
    print("\n[1/4] Cleaning and preprocessing datasets...")

    processed_data = preprocess_all(
        raw_dir=raw_dir,
        processed_dir=processed_dir,
    )

    print("Preprocessing completed.")

    # ---------------------------------------------------------
    # 2. Create order-level features
    # ---------------------------------------------------------
    print("\n[2/4] Creating order features...")

    orders = processed_data["orders"]

    order_features = create_order_features(orders)

    print(
        f"Created order features for "
        f"{len(order_features):,} records."
    )

    # ---------------------------------------------------------
    # 3. Create seller-level features and Seller Trust Index
    # ---------------------------------------------------------
    print("\n[3/4] Creating seller features and Seller Trust Index...")

    seller_metrics = create_seller_features(
        order_items=processed_data["order_items"],
        orders=order_features,
        reviews=processed_data["reviews"],
    )

    seller_metrics = calculate_seller_trust_index(
        seller_metrics
    )

    print(
        f"Created seller metrics for "
        f"{len(seller_metrics):,} sellers."
    )

    # ---------------------------------------------------------
    # 4. Load feature data into SQLite
    # ---------------------------------------------------------
    print("\n[4/4] Loading feature data into SQLite...")

    load_feature_data(
        orders=order_features,
        seller_metrics=seller_metrics,
    )

    database_path = get_database_path()

    print(f"\nDatabase created/updated at:")
    print(database_path)

    # ---------------------------------------------------------
    # Validate database tables
    # ---------------------------------------------------------
    from src.database.connection import get_connection

    with get_connection() as connection:
        tables = get_table_names(connection)

        print("\nDatabase tables:")
        for table in tables:
            print(f" - {table}")

        for table in ["order_features", "seller_metrics"]:
            if table in tables:
                count = get_row_count(connection, table)
                print(f"{table}: {count:,} rows")

    print("\nTrustLens pipeline completed successfully.")


if __name__ == "__main__":
    main()