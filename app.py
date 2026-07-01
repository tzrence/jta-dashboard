import streamlit as st
import pandas as pd

st.set_page_config(page_title="NAVI Fleet Operations Dashboard", layout="wide")

st.title("🚍 NAVI Fleet Operations Dashboard")

# Load Excel file
df = pd.read_excel("fleet_data.xlsx")

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

if status_filter != "All":
    filtered_df = df[df["Status"] == status_filter]
else:
    filtered_df = df

st.dataframe(filtered_df, use_container_width=True)

# Quick Insight
st.subheader("Quick Insight")

if not df.empty:
    most_used = df.loc[df["Miles This Month"].idxmax(), "Vehicle"]
    st.write(f"🚍 Most used vehicle this month: **{most_used}**")
else:
    st.write("No data available.")
