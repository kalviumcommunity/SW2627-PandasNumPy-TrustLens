
"""Customer Reviews dashboard page."""

from __future__ import annotations

import sqlite3

import pandas as pd
import streamlit as st

from src.database.connection import get_connection
from src.database.risk_analytics import get_review_performance


st.title("Customer Reviews")

st.write(
    """
    Analyze customer ratings, review volume, and seller-level
    review performance.
    """
)

st.divider()


try:
    connection = get_connection()

    try:
        review_data = get_review_performance(connection)
    finally:
        connection.close()

except (sqlite3.Error, pd.errors.DatabaseError) as exc:
    st.error("Review analytics data is not available.")
    st.info(
        "Make sure the SQLite database contains seller metrics."
    )
    st.caption(f"Database error: {exc}")
    st.stop()


if review_data.empty:
    st.warning("No review analytics data is available.")
    st.stop()


# Rating filter
rating_options = ["All"]

rating_values = sorted(
    review_data["seller_average_rating"]
    .dropna()
    .round(1)
    .unique()
    .tolist()
)

selected_rating = st.selectbox(
    "Minimum Seller Rating",
    rating_options + [str(value) for value in rating_values],
)


filtered_data = review_data.copy()

if selected_rating != "All":
    minimum_rating = float(selected_rating)

    filtered_data = filtered_data[
        filtered_data["seller_average_rating"]
        >= minimum_rating
    ]


# KPI cards
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Sellers",
        f"{len(filtered_data):,}",
    )

with col2:
    st.metric(
        "Average Rating",
        f"{filtered_data['seller_average_rating'].mean():.2f}/5",
    )

with col3:
    st.metric(
        "Total Reviews",
        f"{filtered_data['seller_review_count'].sum():,}",
    )


st.divider()

st.subheader("Seller Rating Distribution")

rating_chart = (
    filtered_data[
        ["seller_id", "seller_average_rating"]
    ]
    .sort_values(
        "seller_average_rating",
        ascending=False,
    )
    .head(15)
    .set_index("seller_id")
)

st.bar_chart(
    rating_chart,
    y="seller_average_rating",
)


st.subheader("Review Performance")

st.dataframe(
    filtered_data,
    use_container_width=True,
    hide_index=True,
)

# The existing analytics layer already exposes seller review performance
# using seller_average_rating and seller_review_count.