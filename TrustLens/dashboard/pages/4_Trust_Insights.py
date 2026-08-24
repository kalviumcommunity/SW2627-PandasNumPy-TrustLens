
"""Trust Insights dashboard page."""

from __future__ import annotations

import sqlite3

import pandas as pd
import streamlit as st

from src.database.connection import get_connection
from src.database.queries import get_seller_metrics
from src.analytics.trust_insights import (
    add_risk_indicators,
    get_high_risk_sellers,
    get_trust_band_distribution,
    get_trust_summary,
)


st.title("Trust Insights")

st.write(
    """
    Identify seller trust levels and behavioural risk factors
    that may reduce customer trust.
    """
)

st.divider()


try:
    connection = get_connection()

    try:
        seller_data = get_seller_metrics(connection)
    finally:
        connection.close()

except (sqlite3.Error, pd.errors.DatabaseError) as exc:
    st.error("Trust analytics data is not available.")
    st.info(
        "Make sure the SQLite database contains seller metrics."
    )
    st.caption(f"Database error: {exc}")
    st.stop()


if seller_data.empty:
    st.warning("No seller trust data is available.")
    st.stop()


seller_data = add_risk_indicators(seller_data)


# Filters
col1, col2 = st.columns(2)

with col1:
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

with col2:
    st.write("")

    state_message = st.caption(
        "Seller state filtering will be connected when "
        "seller geography is included in the analytics table."
    )


filtered_data = seller_data.copy()

if selected_trust_band != "All":
    filtered_data = filtered_data[
        filtered_data["trust_band"].astype(str)
        == selected_trust_band
    ]


# Summary metrics
summary = get_trust_summary(filtered_data)


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Average STI",
        f"{summary['average_trust_index']:.2f}",
    )

with col2:
    st.metric(
        "High Trust Sellers",
        f"{summary['high_trust_sellers']:,}",
    )

with col3:
    st.metric(
        "Monitor Sellers",
        f"{summary['monitor_sellers']:,}",
    )

with col4:
    st.metric(
        "High Risk Sellers",
        f"{summary['high_risk_sellers']:,}",
    )


st.divider()

# Trust band distribution
st.subheader("Trust Band Distribution")

distribution = get_trust_band_distribution(
    filtered_data
)

distribution_chart = distribution.set_index(
    "trust_band"
)

st.bar_chart(
    distribution_chart,
    y="seller_count",
)


# Risk indicators
st.subheader("Seller Risk Indicators")

risk_columns = [
    "seller_id",
    "seller_trust_index",
    "seller_average_rating",
    "seller_on_time_rate",
    "seller_completion_rate",
    "seller_review_count",
    "delivery_risk",
    "completion_risk",
    "rating_risk",
    "risk_factor_count",
    "trust_band",
]

available_risk_columns = [
    column
    for column in risk_columns
    if column in filtered_data.columns
]

risk_data = (
    filtered_data[available_risk_columns]
    .sort_values(
        "seller_trust_index",
        ascending=True,
    )
)

st.dataframe(
    risk_data,
    use_container_width=True,
    hide_index=True,
)


st.subheader("High-Risk Sellers")

high_risk = get_high_risk_sellers(
    filtered_data
)

if high_risk.empty:
    st.success("No high-risk sellers found.")
else:
    st.dataframe(
        high_risk,
        use_container_width=True,
        hide_index=True,
    )
# The existing Trust Insights layer already supports:
# ...
# ...