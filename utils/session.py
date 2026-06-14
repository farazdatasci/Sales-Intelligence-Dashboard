import streamlit as st
import pandas as pd
import plotly.express as px

from utils import clean, kpis, monthly_trend, top_products

# -------------------------
# STORE DATA (GLOBAL)
# -------------------------
def set_data(df):
    st.session_state["df"] = df


# -------------------------
# GET DATA (GLOBAL SAFE ACCESS)
# -------------------------
def get_data():
    if "df" not in st.session_state:
        return None
    return st.session_state["df"]


# -------------------------
# CHECK DATA
# -------------------------
def has_data():
    return "df" in st.session_state