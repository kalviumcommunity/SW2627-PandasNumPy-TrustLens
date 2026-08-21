"""Trust Insights dashboard page."""

import streamlit as st


st.title("Trust Insights")

st.write(
    "Identify seller trust levels and high-risk seller behaviour."
)

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.selectbox(
        "Trust Band",
        ["All", "High Trust", "Monitor", "High Risk"],
    )

with col2:
    st.selectbox(
        "Seller State",
        ["All"],
    )

st.subheader("Trust Insights")

st.info(
    "Seller Trust Index analytics and risk insights will be "
    "connected to the analytics layer in the next development stage."
)