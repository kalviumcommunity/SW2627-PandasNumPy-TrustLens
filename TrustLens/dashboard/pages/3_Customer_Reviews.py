"""Customer Reviews dashboard page."""

import streamlit as st


st.title("Customer Reviews")

st.write(
    "Analyze customer ratings, review volume, and review trends."
)

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.selectbox(
        "Rating",
        ["All", "1", "2", "3", "4", "5"],
    )

with col2:
    st.selectbox(
        "Review Period",
        ["All Time"],
    )

st.subheader("Review Analytics")

st.info(
    "Customer review analytics will be connected to the "
    "analytics layer in the next development stage."
)