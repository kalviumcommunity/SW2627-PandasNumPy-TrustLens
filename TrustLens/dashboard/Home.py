
"""TrustLens Streamlit dashboard entry point."""

import streamlit as st


st.set_page_config(
    page_title="TrustLens",
    page_icon="📊",
    layout="wide",
)


def main() -> None:
    """Render the TrustLens dashboard home page."""

    st.title("TrustLens")
    st.subheader("Seller Behaviour & Customer Trust Analytics")

    st.markdown(
        """
        TrustLens is a Business Intelligence dashboard that analyzes
        e-commerce seller behaviour, delivery performance, customer
        reviews, and Seller Trust Index (STI).
        """
    )

    st.divider()

    st.header("Marketplace Overview")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Orders", "—")

    with col2:
        st.metric("Total Sellers", "—")

    with col3:
        st.metric("Average Rating", "—")

    col4, col5, col6 = st.columns(3)

    with col4:
        st.metric("Average Delivery Time", "—")

    with col5:
        st.metric("On-Time Delivery Rate", "—")

    with col6:
        st.metric("Average Seller Trust Index", "—")

    st.info(
        "Analytics data will be connected to these KPIs "
        "through the TrustLens analytics layer."
    )


if __name__ == "__main__":
    main()
