"""Delivery Performance dashboard page."""

import streamlit as st


st.title("Delivery Performance")

st.write(
    "Analyze delivery duration, delays, and on-time delivery "
    "performance."
)

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.selectbox(
        "Delivery Status",
        ["All", "On Time", "Delayed"],
    )

with col2:
    st.selectbox(
        "Time Period",
        ["All Time"],
    )

st.subheader("Delivery Analytics")

st.info(
    "Delivery analytics will be connected to the analytics "
    "layer in the next development stage."
)