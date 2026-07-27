import streamlit as st
import pandas as pd

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="NAVI Fleet Operations Dashboard",
    layout="wide"
)

# ==========================================
# LOAD FLEET DATA
# ==========================================

fleet_df = pd.read_excel("fleet_data.xlsx")
fleet_df.columns = fleet_df.columns.str.strip()

# ==========================================
# LOAD RIDERSHIP / PERFORMANCE DATA
# ==========================================

perf_df = pd.read_excel(
    "Top performing Vehicle and other data analysis.xlsx"
)

perf_df.columns = [
    str(col).strip()
    for col in perf_df.columns
]

st.write("Performance File Columns:")
st.write(perf_df.columns.tolist())

# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.image("logogrey.jpg", width=220)

page = st.sidebar.selectbox(
    "Navigation",
    [
        "🏠 Home",
        "👥 Ridership",
        "🏆 Performance & Insights"
    ]
)

# ==========================================
# HOME PAGE
# ==========================================

if page == "🏠 Home":

    st.image("logowhite.jpg", width=200)

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

    total = len(fleet_df)
    active = len(fleet_df[fleet_df["Status"] == "Active"])
    down = len(fleet_df[fleet_df["Status"] == "Down"])
    maintenance = len(
        fleet_df[fleet_df["Status"] == "Maintenance"]
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Vehicles", total)

    with col2:
        st.metric("Active Vehicles", active)

    with col3:
        st.metric("Down Vehicles", down)

    with col4:
        st.metric("Maintenance", maintenance)

    st.divider()

    st.subheader("Fleet Status Overview")

    status_counts = fleet_df["Status"].value_counts()

    st.bar_chart(status_counts)

    st.divider()

    st.subheader("Fleet Status Table")

    status_filter = st.selectbox(
        "Filter by Status",
        ["All", "Active", "Down", "Maintenance"]
    )

    if status_filter == "All":
        filtered_df = fleet_df.copy()
    else:
        filtered_df = fleet_df[
            fleet_df["Status"] == status_filter
        ]

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
            (
                len(
                    filtered_df[
                        filtered_df["Status"] == "Active"
                    ]
                )
                / len(filtered_df)
            ) * 100,
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

# ==========================================
# RIDERSHIP PAGE
