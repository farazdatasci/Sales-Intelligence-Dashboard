import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression

st.set_page_config(page_title="Forecasting", layout="wide")

st.title("🔮 Sales Forecasting Engine")

# ------------------------
# LOAD DATA (SESSION ONLY)
# ------------------------
if "df" not in st.session_state:
    st.warning("Please upload data from Home page first.")
    st.stop()

df = st.session_state["df"]

# ------------------------
# PREP DATA (IMPORTANT FIX)
# ------------------------
df["Month"] = pd.to_datetime(df["Month"], errors="coerce")
df = df.dropna(subset=["Month"])

monthly = df.groupby("Month", as_index=False)["Amount"].sum()
monthly = monthly.sort_values("Month")

# Create proper time index
monthly["t"] = np.arange(len(monthly))

if len(monthly) < 3:
    st.error(
        "At least 3 months of sales history are required for forecasting."
    )
    st.stop()

# ------------------------
# MODEL TRAINING
# ------------------------
model = LinearRegression()
model.fit(monthly[["t"]], monthly["Amount"])

# ------------------------
#  Next 3 months
# ------------------------

future_dates = pd.date_range(
    start=monthly["Month"].max(),
    periods=4,
    freq="MS"
)[1:]

future_t = np.arange(
    len(monthly),
    len(monthly) + 3
).reshape(-1, 1)

future_pred = model.predict(future_t)

forecast_df = pd.DataFrame({
    "Month": future_dates,
    "Forecast": np.maximum(future_pred, 0)
})

forecast_df["MonthLabel"] = forecast_df["Month"].dt.strftime("%b-%y")

# ------------------------
# VISUALIZATION (PRO STYLE)
# ------------------------
fig = go.Figure()

# Actual line
fig.add_trace(go.Scatter(
    x=monthly["Month"],
    y=monthly["Amount"],
    mode="lines+markers",
    name="Actual Sales",
    line=dict(color="blue", width=3)
))

# Forecast line
fig.add_trace(go.Scatter(
    x=forecast_df["Month"],
    y=forecast_df["Forecast"],
    mode="lines+markers",
    name="Forecast Sales",
    line=dict(color="orange", dash="dash", width=3)
))

fig.update_layout(
    title="Sales Trend & Forecast (Next 3 Months)",
    xaxis_title="Month",
    yaxis_title="Sales Amount",
    hovermode="x unified"
)

st.plotly_chart(fig, use_container_width=True)

# ------------------------
# BUSINESS EXPLANATION (VERY IMPORTANT)
# ------------------------
st.subheader("📊 Forecast Interpretation")

avg_growth = (monthly["Amount"].iloc[-1] - monthly["Amount"].iloc[0]) / len(monthly)

st.info(f"""
This model uses historical monthly sales trends to predict future performance.

📌 Key Insights:
- Trend direction is based on past sales movement
- Forecast assumes same growth pattern continues
- Average monthly movement: {avg_growth:,.0f}

⚠ Note:
This is a linear forecast (basic model). For enterprise accuracy, use ARIMA or Prophet model.
""")

# ------------------------
# FORECAST TABLE
# ------------------------
st.subheader("📅 Forecast Table")
st.dataframe(forecast_df)
