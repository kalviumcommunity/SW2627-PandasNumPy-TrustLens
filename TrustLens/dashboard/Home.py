"""TrustLens Streamlit dashboard home page."""

from __future__ import annotations

from pathlib import Path
import sys
import sqlite3

import pandas as pd
import plotly.express as px
import streamlit as st


# ---------------------------------------------------------
# Project path configuration
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from src.database.connection import get_connection


# ---------------------------------------------------------
# Page configuration
# ---------------------------------------------------------

st.set_page_config(
    page_title="TrustLens",
    page_icon="📊",
    layout="wide",
)


# ---------------------------------------------------------
# Database helpers
# ---------------------------------------------------------

def load_home_kpis(
    connection: sqlite3.Connection,
) -> tuple[dict[str, float | int], pd.DataFrame]:
    """Load homepage KPI values and trust-band distribution."""

    # Marketplace KPIs that come from order-level data
    kpi_query = """
        SELECT
            COUNT(*) AS total_orders,
            AVG(delivery_days) AS average_delivery,
            AVG(on_time_delivery) * 100 AS on_time_rate
        FROM order_features
    """

    # Seller-level KPIs that come from seller metrics
    seller_query = """
        SELECT
            COUNT(*) AS total_sellers,
            AVG(seller_average_rating) AS average_rating,
            AVG(seller_trust_index) AS average_sti
        FROM seller_metrics
        WHERE seller_average_rating > 0
    """

    # Trust-band distribution
    trust_query = """
        SELECT
            trust_band,
            COUNT(*) AS seller_count
        FROM seller_metrics
        GROUP BY trust_band
        ORDER BY seller_count DESC
    """

    kpi_result = pd.read_sql_query(
        kpi_query,
        connection,
    )

    seller_result = pd.read_sql_query(
        seller_query,
        connection,
    )

    trust_data = pd.read_sql_query(
        trust_query,
        connection,
    )

    kpi_row = kpi_result.iloc[0]
    seller_row = seller_result.iloc[0]

    kpis = {
        "total_orders": int(
            kpi_row["total_orders"] or 0
        ),
        "total_sellers": int(
            seller_row["total_sellers"] or 0
        ),
        "average_rating": float(
            seller_row["average_rating"] or 0
        ),
        "average_delivery": float(
            kpi_row["average_delivery"] or 0
        ),
        "on_time_rate": float(
            kpi_row["on_time_rate"] or 0
        ),
        "average_sti": float(
            seller_row["average_sti"] or 0
        ),
    }

    return kpis, trust_data


# ---------------------------------------------------------
# Header
# ---------------------------------------------------------

st.title("TrustLens")

st.subheader(
    "Seller Behaviour & Customer Trust Analytics"
)

st.markdown(
    """
    TrustLens analyzes e-commerce seller behaviour,
    delivery performance, customer reviews, and Seller
    Trust Index (STI) metrics to identify patterns that
    influence customer trust.
    """
)

st.divider()


# ---------------------------------------------------------
# Load data
# ---------------------------------------------------------

try:
    connection = get_connection()

    try:
        kpis, trust_data = load_home_kpis(connection)
    finally:
        connection.close()

except (sqlite3.Error, pd.errors.DatabaseError) as exc:

    st.error("TrustLens database is not available.")

    st.info(
        "Make sure the SQLite database has been created "
        "and the feature data has been loaded."
    )

    st.caption(f"Database error: {exc}")

    st.stop()


# ---------------------------------------------------------
# Marketplace KPIs
# ---------------------------------------------------------

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


# ---------------------------------------------------------
# Trust overview
# ---------------------------------------------------------

st.header("Trust Overview")

if not trust_data.empty:

    chart = px.bar(
        trust_data,
        x="trust_band",
        y="seller_count",
        title="Seller Trust Band Distribution",
        labels={
            "trust_band": "Trust Band",
            "seller_count": "Number of Sellers",
        },
    )

    chart.update_layout(
        height=400,
        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20,
        ),
    )

    st.plotly_chart(
        chart,
        use_container_width=True,
    )

else:

    st.info(
        "No seller trust-band data is available."
    )


# ---------------------------------------------------------
# Dashboard navigation information
# ---------------------------------------------------------

st.divider()

st.header("Explore TrustLens")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.info(
        "**Seller Performance**\n\n"
        "Compare seller performance and STI."
    )

with col2:
    st.info(
        "**Delivery Performance**\n\n"
        "Analyze delivery duration and delays."
    )

with col3:
    st.info(
        "**Customer Reviews**\n\n"
        "Explore customer ratings and review metrics."
    )

with col4:
    st.info(
        "**Trust Insights**\n\n"
        "Identify high-risk seller behaviour."
    )