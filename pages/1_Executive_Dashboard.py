import streamlit as st
import pandas as pd
import plotly.express as px

from utils import clean, kpis, monthly_trend

st.set_page_config(page_title="Executive Dashboard", layout="wide")

st.title("📊 Executive Dashboard")



# ------------------------
# LOAD DATA
# ------------------------
if "df" not in st.session_state:
    st.warning("Upload data first at Home page.")
    st.stop()

df = st.session_state["df"]

# ------------------------
# KPIs
# ------------------------
kpi = kpis(df)

col1, col2, col3, col4 = st.columns(4)

col1.metric("💰 Sales", f"{kpi['sales']:,.0f}")
col2.metric("📦 Units", f"{kpi['units']:,.0f}")
col3.metric("📌 Products", kpi["products"])
col4.metric("📍 Areas", kpi["areas"])

# ------------------------
# TREND CHART
# ------------------------
trend = monthly_trend(df)

fig = px.line(
    trend,
    x="YearMonth",
    y="Amount",
    color="Group",
    markers=True,
    title="Monthly Sales Trend"
)

st.plotly_chart(fig, use_container_width=True)

# ------------------------
# RAW DATA
# ------------------------
st.subheader("Raw Data")
st.dataframe(df, use_container_width=True)