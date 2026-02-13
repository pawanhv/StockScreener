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


def render_portfolio():
    st.markdown('<div class="card"><div class="section-title">💼 Portfolio</div>', unsafe_allow_html=True)
    st.info("Portfolio page under construction")
    st.markdown('</div>', unsafe_allow_html=True)