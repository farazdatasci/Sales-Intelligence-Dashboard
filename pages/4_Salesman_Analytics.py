import streamlit as st
import pandas as pd
import plotly.express as px

from utils import clean, kpis, monthly_trend, top_products

st.title("👨‍💼 Salesman Analytics")

# ------------------------
# LOAD DATA
# ------------------------
if "df" not in st.session_state:
    st.warning("Upload data first at Home page.")
    st.stop()

df = st.session_state["df"]

# ------------------------
# CHECK COLUMN EXISTENCE
# ------------------------
if "Sales_man" not in df.columns:
    st.warning("No Sales_man column in dataset")
    st.stop()

salesman = df.groupby("Sales_man", as_index=False)["Amount"].sum()

fig = px.bar(
    salesman,
    x="Sales_man",
    y="Amount",
    color="Amount",
    title="Salesman Performance"
)

st.plotly_chart(fig, use_container_width=True)