import streamlit as st
import pandas as pd
import plotly.express as px

from utils import clean, kpis, monthly_trend, top_products

st.title("📍 Area Analytics")

# ------------------------
# LOAD DATA
# ------------------------
if "df" not in st.session_state:
    st.warning("Upload data first at Home page.")
    st.stop()

df = st.session_state["df"]

# ------------------------
# AREA WISE SALES
# ------------------------
area = df.groupby("Area", as_index=False)["Amount"].sum()

fig = px.pie(
    area,
    names="Area",
    values="Amount",
    title="Area Wise Sales Distribution"
)

st.plotly_chart(fig, use_container_width=True)

# ------------------------
# BAR VIEW
# ------------------------
fig2 = px.bar(area, x="Area", y="Amount", color="Amount")
st.plotly_chart(fig2, use_container_width=True)