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
# RADAR CHART FUNCTIONS
# -------------------------
def plot_radar_chart(metrics_dict, company_name="Company"):
    categories = list(metrics_dict.keys())
    values = list(metrics_dict.values())
    categories += [categories[0]]  # close the loop
    values += [values[0]]

    fig = go.Figure(
        data=[
            go.Scatterpolar(
                r=values,
                theta=categories,
                fill='toself',
                name=company_name,
                line=dict(color='rgba(102, 126, 234, 0.8)', width=2)
            )
        ]
    )

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 5])
        ),
        showlegend=False,
        template="plotly_white",
        title=f"Fundamental Metrics Radar for {company_name}"
    )

    st.plotly_chart(fig, use_container_width=True)

def calculate_value_metrics(info):
    """Calculate normalized 0-5 scores for value investing axes."""
    def scale(value, min_val, max_val):
        if value is None:
            return 0
        scaled = (value - min_val) / (max_val - min_val) * 5
        return max(0, min(scaled, 5))

    pe = info.get('trailingPE') or info.get('forwardPE')
    valuation = 5 if pe is None else max(0, min(5, 50 - pe)/50*5)
    growth = scale(info.get('revenueGrowth'), 0, 0.5)
    profitability = scale(info.get('profitMargins'), 0, 0.5)
    de_ratio = info.get('debtToEquity')
    balance_sheet = scale(1 / (de_ratio + 1) if de_ratio else 0, 0, 1)
    dividends = scale(info.get('dividendYield'), 0, 0.1)
    management = scale(info.get('returnOnEquity'), 0, 0.5)

    return {
        "Valuation": valuation,
        "Growth": growth,
        "Profitability": profitability,
        "Balance Sheet": balance_sheet,
        "Dividends": dividends,
        "Management": management
    }

def plot_score_bars(scores_dict):
    fig = go.Figure()

    for score_name, score_value in scores_dict.items():

        # ---- Handle None or NaN safely ----
        if score_value is None or (isinstance(score_value, float) and math.isnan(score_value)):
            norm_value = 0
            display_value = "N/A"
        else:
            display_value = round(score_value, 2)

            # ---- Normalize depending on score type ----
            if score_name == "Beneish M-Score":
                # Typical range approx -4 to +1
                norm_value = (score_value + 4) / 5
            elif score_name == "Altman Z-Score":
                # Typical range 0–5+
                norm_value = score_value / 5
            else:  # Piotroski F-Score (0–9)
                norm_value = score_value / 9

            # Clamp between 0 and 1
            norm_value = max(0, min(norm_value, 1))

        fig.add_trace(go.Bar(
            y=[score_name],
            x=[norm_value],
            orientation='h',
            text=f"{display_value}",
            textposition='inside',
            marker=dict(
                color=norm_value,
                colorscale=[[0, 'red'], [0.5, 'yellow'], [1, 'green']]
            ),
            width=0.5,
            showlegend=False
        ))

    fig.update_layout(
        xaxis=dict(showticklabels=False, showgrid=False, range=[0, 1]),
        yaxis=dict(autorange="reversed"),
        template="plotly_white",
        height=200 + 50 * len(scores_dict)
    )

    st.plotly_chart(fig, use_container_width=True)

# -------------------------
# COMPANY PROFILE PAGE
# -------------------------
def render_company_profile():

    st.markdown('<div class="card"><div class="section-title">🔍 Company Profile</div>', unsafe_allow_html=True)
    company_input = st.text_input("Enter company symbol (e.g., MSFT, AAPL)", key="company_search")
    load_button = st.button("Load Data", key="company_button")

    if load_button and company_input:
        if(1==1):
            ticker = yf.Ticker(company_input.upper())
            info = ticker.info

            # --- Basic Info ---
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader(f"{info.get('shortName', company_input.upper())} ({company_input.upper()})")
            st.write(f"**Sector:** {info.get('sector','N/A')}")
            st.write(f"**Industry:** {info.get('industry','N/A')}")
            st.write(f"**Employees:** {info.get('fullTimeEmployees','N/A')}")
            st.write(f"**Website:** {info.get('website','N/A')}")
            st.write(f"**Description:** {info.get('longBusinessSummary','N/A')}")
            st.markdown('</div>', unsafe_allow_html=True)

            # --- Key Metrics ---
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("📊 Key Metrics")
            metrics = {
                "Market Cap": info.get('marketCap'),
                "Current Price": info.get('currentPrice'),
                "PE Ratio (TTM)": info.get('trailingPE'),
                "Forward PE": info.get('forwardPE'),
                "Dividend Yield": info.get('dividendYield'),
                "Beta": info.get('beta')
            }
            for k, v in metrics.items():
                display_value = v if v is not None else "N/A"
                if isinstance(v,float) and "Dividend" in k:
                    display_value = f"{v*100:.2f} %"
                elif isinstance(v,(int,float)) and ("Price" in k or "Cap" in k or "PE" in k or "Beta" in k):
                    display_value = f"{v:,}"
                st.write(f"**{k}:** {display_value}")
            st.markdown('</div>', unsafe_allow_html=True)

            # --- Price History + Moving Averages ---
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("📈 Price History & Moving Averages (1 Year)")
            hist = ticker.history(period="1y")
            if not hist.empty:
                hist['MA50'] = hist['Close'].rolling(50).mean()
                hist['MA200'] = hist['Close'].rolling(200).mean()

                fig = go.Figure()
                fig.add_trace(go.Scatter(x=hist.index, y=hist['Close'], mode='lines', name='Close', line=dict(color='blue')))
                fig.add_trace(go.Scatter(x=hist.index, y=hist['MA50'], mode='lines', name='MA50', line=dict(color='orange', dash='dash')))
                fig.add_trace(go.Scatter(x=hist.index, y=hist['MA200'], mode='lines', name='MA200', line=dict(color='green', dash='dash')))
                fig.update_layout(template="plotly_white", xaxis_title="Date", yaxis_title="Price")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No historical price data available.")
            st.markdown('</div>', unsafe_allow_html=True)

            # --- Volume Chart ---
            if not hist.empty:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.subheader("📊 Trading Volume (1 Year)")
                fig = go.Figure()
                fig.add_trace(go.Bar(x=hist.index, y=hist['Volume'], marker_color='purple'))
                fig.update_layout(template="plotly_white", xaxis_title="Date", yaxis_title="Volume")
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

            # --- Radar Chart ---
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("📊 Fundamental Radar")
            radar_metrics = calculate_value_metrics(info)
            plot_radar_chart(radar_metrics, company_name=info.get('shortName', company_input.upper()))
            st.markdown('</div>', unsafe_allow_html=True)

            # Scores
            piotroski = 0.8
            beneish = 0.2
            altman = 0.7

            scores = {
                "Piotroski F-Score": piotroski,
                "Beneish M-Score": beneish,
                "Altman Z-Score": altman
            }

            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("📊 Financial Health Scores")
            plot_score_bars(scores)
            st.markdown('</div>', unsafe_allow_html=True)

            peg = ticker.info.get("trailingPegRatio")
            st.write("PEG (5yr expected):", peg)

            roe = ticker.info.get("returnOnEquity")
            st.write("RoE :", round(roe*100,2))

            dte = ticker.info.get("debtToEquity")
            st.write("DtE :", round(dte,2))

            ev = ticker.info.get("enterpriseValue")
            eg = ticker.info.get("totalRevenue")
            evoeg = ev/eg
            st.write("EVOEG :", round(evoeg,2))

        else: 
            st.error(f"Error loading data: {e}")

    st.markdown('</div>', unsafe_allow_html=True)

   