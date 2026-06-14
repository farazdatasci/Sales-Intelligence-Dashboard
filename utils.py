import pandas as pd
import re

# =========================
# MONTH PARSER (ROBUST + SAFE)
# =========================
def parse_month(value):

    if pd.isna(value):
        return pd.NaT

    value = str(value).strip()

    # Format 1: 26-Jan
    match = re.match(r"(\d{2})-([A-Za-z]{3})", value)
    if match:
        month = match.group(2)
        year = "20" + match.group(1)
        return pd.to_datetime(f"01-{month}-{year}", format="%d-%b-%Y", errors="coerce")

    # Format 2: Jan-26
    match = re.match(r"([A-Za-z]{3})-(\d{2})", value)
    if match:
        return pd.to_datetime("01-" + value, format="%d-%b-%y", errors="coerce")

    # Format 3: Excel / datetime
    return pd.to_datetime(value, errors="coerce")


# =========================
# CLEAN DATA (GLOBAL FIX)
# =========================
def clean(df):

    df = df.copy()
    df.columns = df.columns.str.strip()

    # ensure required columns exist
    required = ["Month", "Group", "Product", "Area", "Units", "Amount"]
    for col in required:
        if col not in df.columns:
            df[col] = 0

    # numeric safety
    df["Units"] = pd.to_numeric(df["Units"], errors="coerce").fillna(0)
    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce").fillna(0)

    # parse month
    df["Month"] = df["Month"].apply(parse_month)
    df = df[df["Month"].notna()].copy()

    # sort FIX (VERY IMPORTANT FOR GRAPHS)
    df = df.sort_values("Month")

    # TIME FEATURES (STANDARDIZED)
    df["Year"] = df["Month"].dt.year
    df["MonthNum"] = df["Month"].dt.month
    df["Quarter"] = "Q" + df["Month"].dt.quarter.astype(str) + "-" + df["Year"].astype(str)

    # PRIMARY SAFE X-AXIS (IMPORTANT FIX FOR YOUR ERROR)
    df["YearMonth"] = df["Month"].dt.strftime("%b-%y")
    df["MonthSort"] = df["Month"].dt.year * 100 + df["Month"].dt.month

    return df


# =========================
# KPI ENGINE
# =========================
def kpis(df):

    return {
        "sales": float(df["Amount"].sum()),
        "units": float(df["Units"].sum()),
        "products": int(df["Product"].nunique()),
        "areas": int(df["Area"].nunique()),
        "groups": int(df["Group"].nunique())
    }


# =========================
# MONTHLY TREND (FIXED FOR PLOTLY)
# =========================
def monthly_trend(df):

    trend = (
        df.groupby(["MonthSort", "YearMonth", "Group"], as_index=False)
        .agg({"Amount": "sum"})
    )

    trend = trend.sort_values("MonthSort")

    return trend


# =========================
# TOP PRODUCTS
# =========================
def top_products(df, n=10):

    return (
        df.groupby("Product", as_index=False)["Amount"]
        .sum()
        .sort_values("Amount", ascending=False)
        .head(n)
    )


# =========================
# GROUP ANALYSIS
# =========================
def group_analysis(df):

    return (
        df.groupby("Group", as_index=False)["Amount"]
        .sum()
        .sort_values("Amount", ascending=False)
    )


# =========================
# AREA ANALYSIS
# =========================
def area_analysis(df):

    return (
        df.groupby("Area", as_index=False)["Amount"]
        .sum()
        .sort_values("Amount", ascending=False)
    )


# =========================
# QUARTER ANALYSIS (POWER BI STYLE)
# =========================
def quarter_analysis(df):

    return (
        df.groupby("Quarter", as_index=False)["Amount"]
        .sum()
        .sort_values("Quarter")
    )


# =========================
# TOP PRODUCTS BY GROUP (IMPORTANT FOR YOUR DASHBOARD)
# =========================
def top_products_by_group(df):

    return (
        df.groupby(["Group", "Product"], as_index=False)["Amount"]
        .sum()
        .sort_values("Amount", ascending=False)
    )


# =========================
# MOM GROWTH
# =========================
def mom_growth(df):

    t = df.groupby("YearMonth", as_index=False)["Amount"].sum()
    t = t.sort_values("YearMonth")

    t["prev"] = t["Amount"].shift(1)
    t["growth%"] = ((t["Amount"] - t["prev"]) / t["prev"]) * 100

    return t