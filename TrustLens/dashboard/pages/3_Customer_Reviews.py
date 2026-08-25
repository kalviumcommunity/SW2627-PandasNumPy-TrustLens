
from __future__ import annotations

import sqlite3

import pandas as pd
import plotly.express as px
import streamlit as st

from src.database.connection import get_connection
from src.database.risk_analytics import (
    get_review_performance,
)


st.title("Customer Reviews")

st.write(
    """
    Analyze customer ratings, review volume, and
    seller-level review performance.
    """
)

st.divider()


# ---------------------------------------------------------
# Load review data
# ---------------------------------------------------------

try:

    connection = get_connection()

    try:
        review_data = get_review_performance(
            connection
        )
    finally:
        connection.close()

except (sqlite3.Error, pd.errors.DatabaseError) as exc:

    st.error(
        "Review analytics data is not available."
    )

    st.info(
        "Make sure the SQLite database contains "
        "seller metrics."
    )

    st.caption(f"Database error: {exc}")

    st.stop()


if review_data.empty:

    st.warning(
        "No review analytics data is available."
    )

    st.stop()


# ---------------------------------------------------------
# Rating filter
# ---------------------------------------------------------

rating_values = sorted(
    review_data[
        "seller_average_rating"
    ]
    .dropna()
    .round(1)
    .unique()
    .tolist()
)


rating_options = [
    "All"
] + [
    str(value)
    for value in rating_values
]


selected_rating = st.selectbox(
    "Minimum Seller Rating",
    rating_options,
)


filtered_data = review_data.copy()


if selected_rating != "All":

    minimum_rating = float(
        selected_rating
    )

    filtered_data = filtered_data[
        filtered_data[
            "seller_average_rating"
        ]
        >= minimum_rating
    ]


if filtered_data.empty:

    st.warning(
        "No sellers match the selected rating."
    )

    st.stop()


# ---------------------------------------------------------
# KPI cards
# ---------------------------------------------------------

total_sellers = len(
    filtered_data
)

average_rating = (
    filtered_data[
        "seller_average_rating"
    ].mean()
)

total_reviews = (
    filtered_data[
        "seller_review_count"
    ].sum()
)


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "Sellers",
        f"{total_sellers:,}",
    )


with col2:

    st.metric(
        "Average Rating",
        f"{average_rating:.2f}/5",
    )


with col3:

    st.metric(
        "Total Reviews",
        f"{total_reviews:,.0f}",
    )


st.divider()


# ---------------------------------------------------------
# Rating visualization
# ---------------------------------------------------------

st.subheader(
    "Seller Rating Distribution"
)


rating_chart = (
    filtered_data[
        [
            "seller_id",
            "seller_average_rating",
        ]
    ]
    .sort_values(
        "seller_average_rating",
        ascending=False,
    )
    .head(15)
)


fig = px.bar(
    rating_chart,
    x="seller_average_rating",
    y="seller_id",
    orientation="h",
    title="Top Sellers by Average Rating",
    labels={
        "seller_average_rating": "Average Rating",
        "seller_id": "Seller",
    },
)


fig.update_layout(
    height=500,
    yaxis=dict(
        categoryorder="total ascending"
    ),
)


st.plotly_chart(
    fig,
    use_container_width=True,
)


# ---------------------------------------------------------
# Review volume
# ---------------------------------------------------------

st.subheader(
    "Review Volume"
)


review_volume = (
    filtered_data[
        [
            "seller_id",
            "seller_review_count",
        ]
    ]
    .sort_values(
        "seller_review_count",
        ascending=False,
    )
    .head(15)
)


fig_volume = px.bar(
    review_volume,
    x="seller_id",
    y="seller_review_count",
    title="Top Sellers by Review Volume",
    labels={
        "seller_id": "Seller",
        "seller_review_count": "Review Count",
    },
)


fig_volume.update_layout(
    height=400,
)


st.plotly_chart(
    fig_volume,
    use_container_width=True,
)


# ---------------------------------------------------------
# Review table
# ---------------------------------------------------------

st.subheader(
    "Review Performance"
)


st.dataframe(
    filtered_data,
    use_container_width=True,
    hide_index=True,
)