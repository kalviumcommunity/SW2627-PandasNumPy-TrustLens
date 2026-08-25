from __future__ import annotations

import sqlite3

import pandas as pd
import plotly.express as px
import streamlit as st

from src.database.connection import get_connection
from src.database.risk_analytics import (
    get_delivery_performance,
)


st.title("Delivery Performance")

st.write(
    """
    Analyze delivery duration, delivery delays, and
    on-time delivery performance over time.
    """
)

st.divider()


# ---------------------------------------------------------
# Load delivery data
# ---------------------------------------------------------

try:

    connection = get_connection()

    try:
        delivery_data = get_delivery_performance(
            connection
        )
    finally:
        connection.close()

except (sqlite3.Error, pd.errors.DatabaseError) as exc:

    st.error(
        "Delivery analytics data is not available."
    )

    st.info(
        "Make sure the SQLite database contains "
        "order feature data."
    )

    st.caption(f"Database error: {exc}")

    st.stop()


if delivery_data.empty:

    st.warning(
        "No delivery analytics data is available."
    )

    st.stop()


# ---------------------------------------------------------
# Time-period filter
# ---------------------------------------------------------

available_periods = (
    delivery_data["order_month"]
    .dropna()
    .astype(str)
    .sort_values()
    .unique()
    .tolist()
)


period_options = [
    "All Time"
] + available_periods


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


# ---------------------------------------------------------
# KPI cards
# ---------------------------------------------------------

total_orders = (
    filtered_data["total_orders"].sum()
)

average_delivery = (
    filtered_data["average_delivery_days"].mean()
)

average_delay = (
    filtered_data["average_delivery_delay"].mean()
)

on_time_rate = (
    filtered_data["on_time_rate"].mean()
)


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Orders",
        f"{total_orders:,.0f}",
    )


with col2:

    st.metric(
        "Average Delivery",
        f"{average_delivery:.2f} days",
    )


with col3:

    st.metric(
        "Average Delay",
        f"{average_delay:.2f} days",
    )


with col4:

    st.metric(
        "On-Time Rate",
        f"{on_time_rate:.2f}%",
    )


st.divider()


# ---------------------------------------------------------
# Delivery trend
# ---------------------------------------------------------

st.subheader(
    "Delivery Performance Trend"
)


trend_data = filtered_data[
    [
        "order_month",
        "average_delivery_days",
        "average_delivery_delay",
    ]
].copy()


fig = px.line(
    trend_data,
    x="order_month",
    y=[
        "average_delivery_days",
        "average_delivery_delay",
    ],
    markers=True,
    title="Delivery Time and Delay Trend",
    labels={
        "order_month": "Month",
        "value": "Days",
        "variable": "Metric",
    },
)


fig.update_layout(
    height=450,
)


st.plotly_chart(
    fig,
    use_container_width=True,
)


# ---------------------------------------------------------
# On-time delivery trend
# ---------------------------------------------------------

st.subheader(
    "On-Time Delivery Rate"
)


on_time_data = filtered_data[
    [
        "order_month",
        "on_time_rate",
    ]
].copy()


fig_on_time = px.bar(
    on_time_data,
    x="order_month",
    y="on_time_rate",
    title="Monthly On-Time Delivery Rate",
    labels={
        "order_month": "Month",
        "on_time_rate": "On-Time Delivery (%)",
    },
)


fig_on_time.update_layout(
    height=400,
)


st.plotly_chart(
    fig_on_time,
    use_container_width=True,
)


# ---------------------------------------------------------
# Delivery data table
# ---------------------------------------------------------

st.subheader(
    "Monthly Delivery Metrics"
)


st.dataframe(
    filtered_data,
    use_container_width=True,
    hide_index=True,
)
