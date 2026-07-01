import streamlit as st
import pandas as pd

st.set_page_config(page_title="Fleet Dashboard", layout="wide")

st.title("NAVI Fleet Performance Dashboard")

data = {
    "Vehicle": ["Bus 1501", "Bus 1502", "Bus 1503", "Bus 1504", "Bus 1505"],
    "Status": ["Active", "Active", "Maintenance", "Down", "Active"],
    "Miles This Month": [3200, 2800, 0, 0, 4100],
    "Days Used": [25, 22, 0, 0, 28]
}

df = pd.DataFrame(data)

# --- KPIs ---
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

# --- Table ---
st.subheader("Fleet Status Table")
st.dataframe(df, use_container_width=True)

# --- Filters ---
st.subheader("Filter by Status")
status_filter = st.selectbox("Choose status", ["All", "Active", "Down", "Maintenance"])

if status_filter != "All":
    filtered_df = df[df["Status"] == status_filter]
else:
    filtered_df = df

st.dataframe(filtered_df, use_container_width=True)

# --- Simple Insights ---
st.subheader("Quick Insight")

most_used = df.loc[df["Miles This Month"].idxmax(), "Vehicle"]
st.write(f"🚍 Most used vehicle this month: **{most_used}**")
