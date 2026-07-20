import streamlit as st
import pandas as pd

# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="NAVI Fleet Operations Dashboard",
    layout="wide"
)

# =====================================
# LOGOS
# =====================================

st.image("logowhite.jpg", width=200)

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
# KPI SECTION
# =====================================

total = len(df)
active = len(df[df["Status"] == "Active"])
down = len(df[df["Status"] == "Down"])
maintenance = len(df[df["Status"] == "Maintenance"])

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

status_counts = df["Status"].value_counts()

st.bar_chart(status_counts)

st.divider()

# =====================================
# FILTER + TABLE
# =====================================

st.subheader("Fleet Status Table")

status_filter = st.selectbox(
    "Filter by Status",
    ["All", "Active", "Down", "Maintenance"]
)

if status_filter == "All":
    filtered_df = df.copy()
else:
    filtered_df = df[df["Status"] == status_filter]

display_df = filtered_df.copy()

display_df["Status"] = display_df["Status"].replace({
    "Active": "🟢 Active",
    "Down": "🔴 Down",
    "Maintenance": "🟡 Maintenance"
})

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

    filtered_active = len(
        filtered_df[
            filtered_df["Status"] == "Active"
        ]
    )

    availability = round(
        (filtered_active / len(filtered_df)) * 100,
        1
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.success(
            f"🏆 Most Utilized Vehicle: {most_used}"
        )

    with col2:
        st.info(
            f"📈 Average Monthly Mileage: {avg_miles:,.0f}"
        )

    with col3:
        st.info(
            f"✅ Fleet Availability: {availability}%"
        )
