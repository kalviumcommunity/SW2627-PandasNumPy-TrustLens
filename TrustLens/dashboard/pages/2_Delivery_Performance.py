"""Delivery Performance dashboard page."""

from __future__ import annotations

import sqlite3

import pandas as pd
import streamlit as st

from src.database.connection import get_connection
from src.database.risk_analytics import get_delivery_performance


st.title("Delivery Performance")

st.write(
    """
    Analyze delivery duration, delivery delays, and on-time
    delivery performance over time.
    """
)

st.divider()


try:
    connection = get_connection()

    try:
        delivery_data = get_delivery_performance(connection)
    finally:
        connection.close()

except (sqlite3.Error, pd.errors.DatabaseError) as exc:
    st.error("Delivery analytics data is not available.")
    st.info(
        "Make sure the SQLite database contains order feature data."
    )
    st.caption(f"Database error: {exc}")
    st.stop()


if delivery_data.empty:
    st.warning("No delivery analytics data is available.")
    st.stop()


# Time-period filter
available_periods = (
    delivery_data["order_month"]
    .dropna()
    .astype(str)
    .sort_values()
    .unique()
    .tolist()
)

period_options = ["All Time"] + available_periods

selected_period = st.selectbox(
    "Time Period",
    period_options,
)

filtered_data = delivery_data.copy()

if selected_period != "All Time":
    filtered_data = filtered_data[
        filtered_data["order_month"].astype(str)
        == selected_period
    ]


# KPI cards
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Orders",
        f"{filtered_data['total_orders'].sum():,}",
    )

with col2:
    st.metric(
        "Average Delivery Time",
        f"{filtered_data['average_delivery_days'].mean():.2f} days",
    )

with col3:
    st.metric(
        "On-Time Delivery Rate",
        f"{filtered_data['on_time_rate'].mean():.2f}%",
    )


st.divider()

st.subheader("Delivery Trends")

chart_data = filtered_data[
    [
        "order_month",
        "average_delivery_days",
        "average_delivery_delay",
    ]
].copy()

chart_data = chart_data.set_index("order_month")

st.line_chart(
    chart_data,
    y=[
        "average_delivery_days",
        "average_delivery_delay",
    ],
)


st.subheader("Monthly Delivery Metrics")

st.dataframe(
    filtered_data,
    use_container_width=True,
    hide_index=True,
)