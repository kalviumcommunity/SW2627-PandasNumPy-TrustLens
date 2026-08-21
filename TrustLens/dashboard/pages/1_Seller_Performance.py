"""Seller Performance dashboard page."""

import streamlit as st


st.title("Seller Performance")

st.write(
    "Analyze seller-level performance, completion rates, "
    "on-time delivery rates, and Seller Trust Index."
)

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.selectbox(
        "Seller",
        ["All Sellers"],
    )

with col2:
    st.selectbox(
        "Trust Band",
        ["All", "High Trust", "Monitor", "High Risk"],
    )

st.subheader("Seller Performance")

st.info(
    "Seller analytics will be connected to the analytics layer "
    "in the next development stage."
)