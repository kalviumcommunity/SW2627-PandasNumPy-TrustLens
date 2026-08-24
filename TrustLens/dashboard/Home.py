# """TrustLens Streamlit dashboard home page."""

# from __future__ import annotations

# import sqlite3

# import pandas as pd
# import streamlit as st

# from src.database.connection import get_connection

"""TrustLens Streamlit dashboard entry point."""

from pathlib import Path
import sys
import sqlite3
import pandas as pd
import streamlit as st

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.database.connection import get_connection


st.set_page_config(
    page_title="TrustLens",
    page_icon="📊",
    layout="wide",
)


def load_home_kpis(connection: sqlite3.Connection) -> dict[str, float | int]:
    """Load marketplace KPI values from SQLite."""

    total_orders = pd.read_sql_query(
        """
        SELECT COUNT(*) AS value
        FROM order_features
        """,
        connection,
    ).iloc[0]["value"]

    total_sellers = pd.read_sql_query(
        """
        SELECT COUNT(DISTINCT seller_id) AS value
        FROM seller_metrics
        """,
        connection,
    ).iloc[0]["value"]

    average_rating = pd.read_sql_query(
        """
        SELECT AVG(seller_average_rating) AS value
        FROM seller_metrics
        WHERE seller_average_rating > 0
        """,
        connection,
    ).iloc[0]["value"]

    average_delivery = pd.read_sql_query(
        """
        SELECT AVG(delivery_days) AS value
        FROM order_features
        WHERE delivery_days IS NOT NULL
        """,
        connection,
    ).iloc[0]["value"]

    on_time_rate = pd.read_sql_query(
        """
        SELECT AVG(on_time_delivery) * 100 AS value
        FROM order_features
        WHERE on_time_delivery IS NOT NULL
        """,
        connection,
    ).iloc[0]["value"]

    average_sti = pd.read_sql_query(
        """
        SELECT AVG(seller_trust_index) AS value
        FROM seller_metrics
        WHERE seller_trust_index IS NOT NULL
        """,
        connection,
    ).iloc[0]["value"]

    return {
        "total_orders": int(total_orders or 0),
        "total_sellers": int(total_sellers or 0),
        "average_rating": float(average_rating or 0),
        "average_delivery": float(average_delivery or 0),
        "on_time_rate": float(on_time_rate or 0),
        "average_sti": float(average_sti or 0),
    }


def main() -> None:
    """Render the TrustLens dashboard home page."""

    st.title("TrustLens")
    st.subheader("Seller Behaviour & Customer Trust Analytics")

    st.markdown(
        """
        TrustLens analyzes e-commerce seller behaviour, delivery
        performance, customer reviews, and Seller Trust Index (STI)
        metrics to identify patterns that influence customer trust.
        """
    )

    st.divider()

    try:
        connection = get_connection()

        try:
            kpis = load_home_kpis(connection)
        finally:
            connection.close()

    except (sqlite3.Error, pd.errors.DatabaseError) as exc:
        st.error("TrustLens database is not available.")
        st.info(
            "Make sure the SQLite database has been created and "
            "the feature data has been loaded."
        )
        st.caption(f"Database error: {exc}")
        return

    st.header("Marketplace Overview")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total Orders",
            f"{kpis['total_orders']:,}",
        )

    with col2:
        st.metric(
            "Total Sellers",
            f"{kpis['total_sellers']:,}",
        )

    with col3:
        st.metric(
            "Average Rating",
            f"{kpis['average_rating']:.2f}/5",
        )

    col4, col5, col6 = st.columns(3)

    with col4:
        st.metric(
            "Average Delivery Time",
            f"{kpis['average_delivery']:.2f} days",
        )

    with col5:
        st.metric(
            "On-Time Delivery Rate",
            f"{kpis['on_time_rate']:.2f}%",
        )

    with col6:
        st.metric(
            "Average Seller Trust Index",
            f"{kpis['average_sti']:.2f}",
        )

    st.divider()

    st.subheader("TrustLens Analytics")

    st.write(
        """
        Use the sidebar to explore seller performance, delivery
        behaviour, customer reviews, and trust-risk insights.
        """
    )


if __name__ == "__main__":
    main()