import streamlit as st
import pandas as pd

st.set_page_config(page_title="NAVI Fleet Operations Dashboard", layout="wide")

st.title("🚍 NAVI Fleet Operations Dashboard")

# Use header=1 because your headers are on the second row
df = pd.read_excel("fleet_data.xlsx", header=1)

# Clean column names
df.columns = df.columns.str.strip()

# KPIs
total = len(df)
active = len(df[df["Status"] == "Active"])
down = len(df[df["Status"] == "Down"])
maintenance = len(df[df["Status"] == "Maintenance"])

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Vehicles", total)
col2.metric("Active", active)
col3.metric("Down", down)
col4.metric("In Maintenance", maintenance)

st.divider()

# Fleet Status Table
st.subheader("Fleet Status Table")
st.dataframe(df, use_container_width=True)

# Filter
st.subheader("Filter by Status")

status_filter = st.selectbox(
    "Choose Status",
    ["All", "Active", "Down", "Maintenance"]
)

if status_filter == "All":
    filtered_df = df
else:
    filtered_df = df[df["Status"] == status_filter]

st.dataframe(filtered_df, use_container_width=True)

# Quick Insight
st.subheader("Quick Insight")

if not df.empty:
    most_used = df.loc[df["Miles This Month"].idxmax(), "Vehicle"]
    st.success(f"🚍 Most used vehicle: {most_used}")
