import streamlit as st
import pandas as pd
import plotly.express as px

from utils import (
    clean,
    kpis,
    monthly_trend,
    top_products,
    group_analysis,
    area_analysis
)

st.set_page_config(
    page_title="Sales Intelligence Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("🏠 Sales Intelligence Dashboard")

# ==================================================
# GLOBAL FILE UPLOAD
# ==================================================

file = st.file_uploader(
    "Upload CSV / Excel",
    type=["csv", "xlsx"],
    key="global_upload"
)

if file:

    if file.name.endswith(".csv"):
        df = pd.read_csv(file)
    else:
        df = pd.read_excel(file)

    df = clean(df)

    st.session_state["df"] = df

    st.success("Data Loaded Successfully")

# ==================================================
# SESSION DATA
# ==================================================

if "df" not in st.session_state:
    st.warning("Upload data to begin analysis")
    st.stop()

df = st.session_state["df"]

st.write("Rows Loaded:", len(df))

# ==================================================
# FILTERS
# ==================================================

st.sidebar.header("Filters")

groups = st.sidebar.multiselect(
    "Group",
    sorted(df["Group"].dropna().unique()),
    default=sorted(df["Group"].dropna().unique())
)

areas = st.sidebar.multiselect(
    "Area",
    sorted(df["Area"].dropna().unique()),
    default=sorted(df["Area"].dropna().unique())
)

quarters = st.sidebar.multiselect(
    "Quarter",
    sorted(df["Quarter"].dropna().unique()),
    default=sorted(df["Quarter"].dropna().unique())
)

df = df[
    (df["Group"].isin(groups))
    & (df["Area"].isin(areas))
    & (df["Quarter"].isin(quarters))
]

# ==================================================
# KPI SECTION
# ==================================================

k = kpis(df)

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("Sales", f"{k['sales']:,.0f}")
c2.metric("Units", f"{k['units']:,.0f}")
c3.metric("Products", k["products"])
c4.metric("Areas", k["areas"])
c5.metric("Groups", k["groups"])

# ==================================================
# MONTHLY TREND
# ==================================================

st.subheader("📈 Monthly Sales Trend")

trend = monthly_trend(df)

fig = px.line(
    trend,
    x="YearMonth",
    y="Amount",
    color="Group",
    markers=True,
    color_discrete_map={
        "Blue": "#1f77b4",
        "Green": "#2ca02c"
    }
)

fig.update_layout(
    xaxis_title="Month",
    yaxis_title="Sales Amount",
    hovermode="x unified"
)

fig.update_yaxes(tickformat="~s")

st.plotly_chart(fig, use_container_width=True)

# ==================================================
# GROUP DONUT
# ==================================================

c1, c2 = st.columns(2)

with c1:

    st.subheader("Group Sales Share")

    grp = group_analysis(df)

    donut = px.pie(
        grp,
        names="Group",
        values="Amount",
        hole=.6,
        color="Group",
        color_discrete_map={
            "Blue": "#1f77b4",
            "Green": "#2ca02c"
        }
    )

    st.plotly_chart(donut, use_container_width=True)

# ==================================================
# QUARTER SALES
# ==================================================

with c2:

    st.subheader("Quarter Comparison")

    q = (
        df.groupby(["Quarter", "Group"])["Amount"]
        .sum()
        .reset_index()
    )

    qfig = px.bar(
        q,
        x="Quarter",
        y="Amount",
        color="Group",
        barmode="group",
        color_discrete_map={
            "Blue": "#1f77b4",
            "Green": "#2ca02c"
        }
    )

    qfig.update_yaxes(tickformat="~s")

    st.plotly_chart(qfig, use_container_width=True)

# ==================================================
# TOP PRODUCTS
# ==================================================

st.subheader("🏆 Top Products")

top = (
    df.groupby(["Product", "Group"])["Amount"]
    .sum()
    .reset_index()
    .sort_values("Amount", ascending=False)
    .head(15)
)

fig2 = px.bar(
    top,
    x="Amount",
    y="Product",
    color="Group",
    orientation="h",
    color_discrete_map={
        "Blue": "#1f77b4",
        "Green": "#2ca02c"
    }
)

fig2.update_xaxes(tickformat="~s")

st.plotly_chart(fig2, use_container_width=True)

# ==================================================
# TOP AREAS
# ==================================================

st.subheader("📍 Top Areas")

area = area_analysis(df).head(10)

fig3 = px.bar(
    area,
    x="Amount",
    y="Area",
    orientation="h",
    color="Amount",
    color_continuous_scale="Blues"
)

fig3.update_xaxes(tickformat="~s")

st.plotly_chart(fig3, use_container_width=True)

# ==================================================
# PRODUCT BY QUARTER
# ==================================================

st.subheader("📦 Product Performance by Quarter")

prod_q = (
    df.groupby(["Quarter", "Product"])["Amount"]
    .sum()
    .reset_index()
)

fig4 = px.bar(
    prod_q,
    x="Quarter",
    y="Amount",
    color="Product"
)

fig4.update_yaxes(tickformat="~s")

st.plotly_chart(fig4, use_container_width=True)

# ==================================================
# DATA PREVIEW
# ==================================================

with st.expander("View Raw Data"):

    st.dataframe(df, use_container_width=True)