import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="NAVI Fleet Operations Dashboard",
    layout="wide"
)

# ===== CUSTOM STYLING =====
st.markdown("""
<style>
.main {
    background-color: #f5f7fa;
}

h1 {
    color: #003366;
}

div[data-testid="metric-container"] {
    background-color: white;
    border: 2px solid #003366;
    padding: 15px;
    border-radius: 12px;
}

div[data-testid="metric-container"] label {
    color: #003366;
}
</style>
""", unsafe_allow_html=True)

# ===== TITLE =====
st.title("🚍 NAVI Fleet Operations Dashboard")
st.caption("Real-Time Fleet Availability & Utilization")

# ===== LOAD DATA =====
df = pd.read_excel("fleet_data.xlsx")
df.columns = df.columns.str.strip()

# ===== KPI CALCULATIONS =====
total = len(df)
active = len(df[df["Status"] == "Active"])
down = len(df[df["Status"] == "Down"])
maintenance = len(df[df["Status"] == "Maintenance"])

# ===== SIDEBAR =====
st.sidebar.header("Dashboard Info")
st.sidebar.write("NAVI Fleet Management")
st.sidebar.write(f"Vehicles Tracked: {total}")

# ===== KPI CARDS =====
col1, col2, col3, col4 = st.columns(4)

col1.metric("🚍 Total Vehicles", total)
col2.metric("🟢 Active", active)
col3.metric("🔴 Down", down)
col4.metric("🟡 Maintenance", maintenance)

st.divider()

# ===== STATUS CHART =====
st.subheader("Fleet Status Overview")

status_counts = df["Status"].value_counts()

