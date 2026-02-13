import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd
import math

hide_streamlit_style = """
<style>
header {visibility: hidden;}        /* hides top header including deploy/share button */
footer {visibility: hidden;}        /* hides footer */
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# -------------------------
# LOAD DATA
# -------------------------
def load_company_data():
    data = [
        ["Apple", 4, 5, 5, 4, 3, 5],
        ["Microsoft", 4, 4, 5, 5, 3, 5],
        ["Tesla", 3, 5, 2, 3, 0, 4],
        ["Coca-Cola", 3, 2, 4, 4, 5, 4],
        ["Amazon", 2, 5, 3, 3, 0, 4],
        ["Nvidia", 3, 5, 4, 4, 1, 4],
        ["JPMorgan", 4, 3, 4, 5, 4, 4],
    ]
    columns = ["Company", "Valuation", "Growth", "Profitability",
               "Balance Sheet", "Dividends", "Management"]
    return pd.DataFrame(data, columns=columns)

# -------------------------
# CSS
# -------------------------
def load_custom_css():
    st.markdown("""
    <style>
    body {font-family: 'Inter', sans-serif; background: #f5f6fa;}
    .main .block-container {padding-top:1rem; max-width:1200px;}
    .card {padding:1.5rem; border-radius:16px; box-shadow:0 4px 12px rgba(0,0,0,0.05); margin-bottom:1.5rem;}
    .section-title {font-size:1.25rem; font-weight:600; margin-bottom:1rem;}
    </style>
    """, unsafe_allow_html=True)

# -------------------------
# RENDER SCREENER
# -------------------------
def render_screener():
    load_custom_css()
    df = load_company_data()

    # Initialize session state for dropdowns
    for key in ["valuation", "growth", "profitability", "balance_sheet", "dividends", "management"]:
        if key not in st.session_state:
            st.session_state[key] = 0

    # Layout columns
    col1, col2, col3 = st.columns([1.2,1,1], gap="large")

    # LEFT COLUMN - Ratings
    with col1:
        st.markdown('<div class="card"><div class="section-title">1️⃣ Discover Companies</div>', unsafe_allow_html=True)
        for key, label in [("valuation","Valuation"),("growth","Growth"),("profitability","Profitability"),
                           ("balance_sheet","Balance Sheet"),("dividends","Dividends"),("management","Management")]:
            st.session_state[key] = st.selectbox(
                label,
                options=[0,1,2,3,4,5],
                index=st.session_state[key],
                key=f"screener_{key}"
            )
        st.markdown('</div>', unsafe_allow_html=True)

    # MIDDLE COLUMN - Filters
    with col2:
        st.markdown('<div class="card"><div class="section-title">2️⃣ Filter Companies</div>', unsafe_allow_html=True)
        country = st.selectbox("Country", ["France", "USA", "Germany", "UK"], key="screener_country")
        sector = st.selectbox("Sector", ["Tech", "Finance", "Healthcare", "Energy"], key="screener_sector")
        market_cap = st.selectbox("Market Cap", ["Small Cap", "Mid Cap", "Large Cap"], key="screener_marketcap")
        st.markdown('</div>', unsafe_allow_html=True)

    # RIGHT COLUMN - Advanced
    with col3:
        st.markdown('<div class="card"><div class="section-title">3️⃣ Advanced Filters</div>', unsafe_allow_html=True)
        if st.button("ADVANCED FILTERS", key="screener_advanced"):
            st.success("Advanced filters activated!")
        st.markdown('</div>', unsafe_allow_html=True)

    # FILTER AND DISPLAY
    st.markdown('<div class="card"><div class="section-title">📊 Matching Companies</div>', unsafe_allow_html=True)
    filters = {k: st.session_state[k] for k in ["valuation","growth","profitability","balance_sheet","dividends","management"]}
    filtered_df = df.copy()
    for col, min_rating in filters.items():
        if min_rating > 0:
            filtered_df = filtered_df[filtered_df[col] >= min_rating]
    if not filtered_df.empty:
        st.dataframe(filtered_df, use_container_width=True)
    else:
        st.warning("No companies match your criteria.")
    st.markdown('</div>', unsafe_allow_html=True)
