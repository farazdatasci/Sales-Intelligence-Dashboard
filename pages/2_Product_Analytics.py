import streamlit as st
import pandas as pd
import plotly.express as px

from utils import top_products

st.title("📦 Product Analytics")

# ------------------------
# LOAD DATA
# ------------------------
if "df" not in st.session_state:
    st.warning("Upload data first at Home page.")
    st.stop()

df = st.session_state["df"]

# ------------------------
# FILTER GROUP
# ------------------------
groups = st.multiselect("Select Group", df["Group"].unique(), df["Group"].unique())
df = df[df["Group"].isin(groups)]

# ------------------------
# TOP PRODUCTS
# ------------------------
top = top_products(df, 10)

fig = px.bar(
    top,
    x="Amount",
    y="Product",
    orientation="h",
    color="Amount",
    title="Top Products"
)

st.plotly_chart(fig, use_container_width=True)

# ------------------------
# PRODUCT TABLE
# ------------------------
st.dataframe(top)