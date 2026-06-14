import streamlit as st
import pandas as pd
from utils import clean, mom_growth

st.set_page_config(page_title="AI Executive Insights", layout="wide")

st.title("🧠 AI Executive Intelligence Engine")

# ------------------------
# LOAD DATA
# ------------------------
if "df" not in st.session_state:
    st.warning("Upload data first at Home page.")
    st.stop()

df = st.session_state["df"]


# =========================
# CORE KPIs
# =========================
total_sales = df["Amount"].sum()
total_units = df["Units"].sum()

top_product = df.groupby("Product")["Amount"].sum().idxmax()
top_area = df.groupby("Area")["Amount"].sum().idxmax()
top_group = df.groupby("Group")["Amount"].sum().idxmax()

avg_sales = df["Amount"].mean()

# =========================
# GROUP PERFORMANCE
# =========================
group_perf = df.groupby("Group")["Amount"].sum().sort_values(ascending=False)
blue_sales = group_perf.get("Blue", 0)
green_sales = group_perf.get("Green", 0)

# =========================
# MOM GROWTH ANALYSIS
# =========================
growth = mom_growth(df)
latest_growth = growth["growth%"].dropna().tail(1).values[0] if len(growth) > 1 else 0

# =========================
# LAYOUT
# =========================
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Sales", f"{total_sales:,.0f}")
col2.metric("Total Units", f"{total_units:,.0f}")
col3.metric("Top Product", top_product)
col4.metric("Top Area", top_area)

st.divider()

# =========================
# BUSINESS PERFORMANCE SNAPSHOT
# =========================
st.subheader("📊 Business Performance Snapshot")

st.write(f"""
- 🔵 Blue Group Sales: **{blue_sales:,.0f}**
- 🟢 Green Group Sales: **{green_sales:,.0f}**
- 🏆 Best Performing Group: **{top_group}**
- 📈 Average Order Value: **{avg_sales:,.2f}**
""")

# =========================
# AI INSIGHT ENGINE
# =========================
st.subheader("🧠 AI Strategic Insights")

insights = []

# SALES HEALTH
if total_sales > 0:
    if latest_growth > 10:
        insights.append("📈 Strong growth trend detected. Business is scaling positively.")
    elif latest_growth < 0:
        insights.append("⚠ Declining trend detected. Immediate corrective action required.")
    else:
        insights.append("📊 Stable performance. Opportunity for optimization exists.")

# GROUP PERFORMANCE
if blue_sales > green_sales:
    insights.append("🔵 Blue group is the dominant revenue driver.")
else:
    insights.append("🟢 Green group is outperforming Blue group.")

# PRODUCT CONCENTRATION RISK
top_product_share = df.groupby("Product")["Amount"].sum().max() / total_sales * 100
if top_product_share > 40:
    insights.append("⚠ High dependency on a single product (>40%). Risk exposure detected.")

# AREA RISK
top_area_share = df.groupby("Area")["Amount"].sum().max() / total_sales * 100
if top_area_share > 40:
    insights.append("⚠ Revenue concentration in a single area is high. Diversification needed.")

for i in insights:
    st.write("•", i)

# =========================
# STRATEGIC RECOMMENDATIONS
# =========================
st.subheader("🚀 Strategic Recommendations")

st.markdown("""
1. Expand marketing in underperforming areas  
2. Reduce dependency on top product  
3. Strengthen Green/Blue balance strategy  
4. Improve distribution efficiency in low-performing regions  
5. Focus on high-margin product mix optimization  
""")

# =========================
# EXECUTIVE SUMMARY (AUTO GENERATED)
# =========================
st.subheader("📌 Executive Summary")

st.info(f"""
Total sales are **{total_sales:,.0f}** with **{total_units:,.0f} units sold**.
The leading product is **{top_product}**, and strongest area is **{top_area}**.
Business is currently driven by **{top_group} group performance**.

Latest trend indicates **{latest_growth:.2f}% growth momentum**.
""")