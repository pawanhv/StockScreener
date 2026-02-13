import streamlit as st
import pandas as pd

hide_streamlit_style = """
<style>
header {visibility: hidden;}        /* hides top header including deploy/share button */
footer {visibility: hidden;}        /* hides footer */
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


st.set_page_config(
    page_title="Stock Screener",
    page_icon="📊",
    layout="wide"
)

# -------------------------
# MAIN PAGE NAVIGATION
# -------------------------
st.markdown("""
<style>
/* Hide Streamlit menu and footer */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- Navigation without sidebar ---
st.title("📊 Stock Screener App")
page = st.radio("Navigate to", ["Home", "Screener", "Company Profile", "Portfolio"], horizontal=True)

# --- Page Imports ---
if page == "Home":
    st.subheader("Choose a page to start")
elif page == "Screener":
    from Screener import render_screener
    render_screener()
elif page == "Company Profile":
    from CompanyProfile import render_company_profile
    render_company_profile()
elif page == "Portfolio":
    from Portfolio import render_portfolio
    render_portfolio()
