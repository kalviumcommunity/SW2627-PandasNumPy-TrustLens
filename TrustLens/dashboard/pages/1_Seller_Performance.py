"""Seller Performance dashboard page."""

from __future__ import annotations

import sqlite3

import pandas as pd
import streamlit as st

from src.database.connection import get_connection
from src.database.analytics import get_seller_rankings


st.title("Seller Performance")

st.write(
    """
    Analyze seller-level performance, completion rates,
    on-time delivery rates, customer ratings, and Seller Trust Index.
    """
)

st.divider()


def load_seller_data(connection: sqlite3.Connection) -> pd.DataFrame:
    """Load seller ranking data from the analytics layer."""
    return get_seller_rankings(connection)


try:
    connection = get_connection()

    try:
        seller_data = load_seller_data(connection)
    finally:
        connection.close()

except (sqlite3.Error, pd.errors.DatabaseError) as exc:
    st.error("Seller analytics data is not available.")
    st.info(
        "Make sure the SQLite database contains the seller_metrics table."
    )
    st.caption(f"Database error: {exc}")
    st.stop()


if seller_data.empty:
    st.warning("No seller analytics data is available.")
    st.stop()


# Filters
col1, col2 = st.columns(2)

with col1:
    seller_options = ["All Sellers"] + sorted(
        seller_data["seller_id"].astype(str).unique().tolist()
    )

    selected_seller = st.selectbox(
        "Seller",
        seller_options,
    )

with col2:
    trust_options = [
        "All",
        "High Trust",
        "Monitor",
        "High Risk",
    ]

    selected_trust_band = st.selectbox(
        "Trust Band",
        trust_options,
    )


filtered_data = seller_data.copy()

if selected_seller != "All Sellers":
    filtered_data = filtered_data[
        filtered_data["seller_id"].astype(str)
        == selected_seller
    ]

if selected_trust_band != "All":
    filtered_data = filtered_data[
        filtered_data["trust_band"].astype(str)
        == selected_trust_band
    ]


st.subheader("Seller Performance")

metric1, metric2, metric3, metric4 = st.columns(4)

with metric1:
    st.metric(
        "Sellers",
        f"{len(filtered_data):,}",
    )

with metric2:
    st.metric(
        "Average STI",
        f"{filtered_data['seller_trust_index'].mean():.2f}",
    )

with metric3:
    st.metric(
        "Average Rating",
        f"{filtered_data['seller_average_rating'].mean():.2f}",
    )

with metric4:
    st.metric(
        "On-Time Rate",
        f"{filtered_data['seller_on_time_rate'].mean():.2f}%",
    )


st.divider()

st.subheader("Seller Rankings")

display_columns = [
    "seller_id",
    "seller_total_orders",
    "seller_average_rating",
    "seller_review_count",
    "seller_completion_rate",
    "seller_on_time_rate",
    "seller_trust_index",
    "trust_band",
]

available_columns = [
    column
    for column in display_columns
    if column in filtered_data.columns
]

st.dataframe(
    filtered_data[available_columns],
    use_container_width=True,
    hide_index=True,
)


st.subheader("Seller Trust Index")

chart_data = (
    filtered_data[
        ["seller_id", "seller_trust_index"]
    ]
    .sort_values(
        "seller_trust_index",
        ascending=False,
    )
    .head(15)
    .set_index("seller_id")
)

st.bar_chart(
    chart_data,
    y="seller_trust_index",
)