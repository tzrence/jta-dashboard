import streamlit as st
import pandas as pd

# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="NAVI Fleet Operations Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================
# LOGOS
# =====================================

st.image("logowhite.jpg", width=200)

with st.sidebar:
    st.image("logogrey.jpg", width=180)
    st.header("Filters")

# =====================================
# HEADER
# =====================================

st.markdown("""
<div style="
background-color:#003366;
padding:15px;
border-radius:10px;
margin-bottom:20px;">

<h1 style="color:white;text-align:center;">
🚍 NAVI Fleet Operations Dashboard
</h1>

</div>
""", unsafe_allow_html=True)

st.caption("Real-Time Fleet Availability & Utilization")

# =====================================
# LOAD DATA
# =====================================

df = pd.read_excel("fleet_data.xlsx")
df.columns = df.columns.str.strip()

# =====================================
# SIDEBAR FILTER
# =====================================

status_filter = st.sidebar.selectbox(
    "Vehicle Status",
    ["All", "Active", "Down", "Maintenance"]
)

if status_filter == "All":
    filtered_df = df.copy()
else:
    filtered_df = df[df["Status"] == status_filter]

# =====================================
# KPIs
# =====================================

total = len(filtered_df)
active = len(filtered_df[filtered_df["Status"] == "Active"])
down = len(filtered_df[filtered_df["Status"] == "Down"])
maintenance = len(filtered_df[filtered_df["Status"] == "Maintenance"])

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.info(f"🚍 Total Vehicles: {total}")

with col2:
    st.success(f"🟢 Active: {active}")

with col3:
    st.error(f"🔴 Down: {down}")

with col4:
    st.warning(f"🟡 Maintenance: {maintenance}")

st.divider()

# =====================================
# CHART
# =====================================

st.subheader("Fleet Status Overview")

status_counts = filtered_df["Status"].value_counts()

st.bar_chart(status_counts)

st.divider()

# =====================================
# MAIN TABLE
# =====================================

display_df = filtered_df.copy()

display_df["Status"] = display_df["Status"].replace({
    "Active": "🟢 Active",
    "Down": "🔴 Down",
    "Maintenance": "🟡 Maintenance"
})

st.subheader("Fleet Status Table")

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True
)

st.divider()

# =====================================
# INSIGHTS
# =====================================

st.subheader("Fleet Insights")

if not filtered_df.empty:

    most_used = filtered_df.loc[
        filtered_df["Miles This Month"].idxmax(),
        "Vehicle"
    ]

    avg_miles = round(
        filtered_df["Miles This Month"].mean(),
        0
    )

    availability = round(
        (active / total) * 100,
        1
    ) if total > 0 else 0

    col1, col2, col3 = st.columns(3)

    with col1:
        st.success(f"🏆 Most Utilized Vehicle: {most_used}")

    with col2:
        st.info(f"📈 Average Monthly Mileage: {avg_miles}")

    with col3:
        st.info(f"✅ Fleet Availability: {availability}%")
