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
    "Top performing Vehicle and other data analysis.xlsx",
    header=7
)

perf_df.columns = [
    str(col).strip()
    for col in perf_df.columns
]

# Remove Grand Total row

perf_df = perf_df[
    perf_df["Date"] != "Grand Total"
].copy()

# Convert data types

perf_df["Date"] = pd.to_datetime(
    perf_df["Date"],
    errors="coerce"
)

perf_df["Total Ridership"] = pd.to_numeric(
    perf_df["Total Ridership"],
    errors="coerce"
)

# Sort chronologically

perf_df = perf_df.sort_values(
    "Date"
)

# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.image("logogrey.jpg", width=220)

page = st.sidebar.selectbox(
    "Navigation",
    [
        "Home",
        "Ridership",
        "Performance & Insights"
    ]
)

# ==========================================
# HOME PAGE
# ==========================================

if page == "Home":

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
# ==========================================

elif page == "Ridership":

    st.image("logowhite.jpg", width=200)

    st.markdown("""
    <div style="
    background-color:#003366;
    padding:15px;
    border-radius:10px;
    margin-bottom:20px;">

    <h1 style="color:white;text-align:center;">
    👥 NAVI Ridership Dashboard
    </h1>

    </div>
    """, unsafe_allow_html=True)

    total_riders = perf_df["Total Ridership"].sum()

    avg_riders = round(
        perf_df["Total Ridership"].mean(),
        1
    )

    highest_ridership = (
        perf_df["Total Ridership"].max()
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total Riders",
            f"{int(total_riders):,}"
        )

    with col2:
        st.metric(
            "Average Daily Ridership",
            avg_riders
        )

    with col3:
        st.metric(
            "Highest Daily Ridership",
            int(highest_ridership)
        )

    st.divider()

    st.subheader("Ridership Trend")

    st.line_chart(
        perf_df.set_index("Date")
        ["Total Ridership"]
    )

    st.divider()

    st.subheader("Ridership Data")

    st.dataframe(
        perf_df[
            [
                "Date",
                "Total Ridership"
            ]
        ],
        hide_index=True,
        use_container_width=True
    )

# ==========================================
# PERFORMANCE & INSIGHTS PAGE
# ==========================================

elif page == "Performance & Insights":

    st.image("logowhite.jpg", width=200)

    st.markdown("""
    <div style="
    background-color:#003366;
    padding:15px;
    border-radius:10px;
    margin-bottom:20px;">

    <h1 style="color:white;text-align:center;">
    🏆 NAVI Performance & Insights
    </h1>

    </div>
    """, unsafe_allow_html=True)

    avg_auto = (
        perf_df["% Distance in Auto"].mean()
        * 100
    )

    avg_brake = (
        perf_df["Hard Brake %"].mean()
        * 100
    )

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Average Autonomous Distance",
            f"{avg_auto:.1f}%"
        )

    with col2:
        st.metric(
            "Average Hard Brake Rate",
            f"{avg_brake:.2f}%"
        )

    st.divider()

    st.subheader(
        "Autonomous Distance Trend"
    )

    st.line_chart(
        perf_df.set_index("Date")
        ["% Distance in Auto"]
    )

    st.divider()

    st.subheader(
        "Hard Brake Trend"
    )

    st.line_chart(
        perf_df.set_index("Date")
        ["Hard Brake %"]
    )

    st.divider()

    # ==========================================
# VEHICLE PERFORMANCE LEADERBOARD
# ==========================================

vehicle_counts = {}

for row in perf_df["Top Distance In Auto"]:

    vehicles = str(row).split("\n")

    for vehicle in vehicles:

        vehicle_name = (
            vehicle.split("–")[0]
            .strip()
        )

        if vehicle_name:

            if vehicle_name in vehicle_counts:
                vehicle_counts[vehicle_name] += 1
            else:
                vehicle_counts[vehicle_name] = 1

leaderboard = pd.DataFrame(
    vehicle_counts.items(),
    columns=[
        "Vehicle",
        "Top 3 Appearances"
    ]
)

leaderboard = leaderboard.sort_values(
    "Top 3 Appearances",
    ascending=False
)

# Champion Vehicle

best_vehicle = leaderboard.iloc[0]

st.success(
    f"""
    🥇 Fleet Champion Vehicle

    {best_vehicle['Vehicle']}

    Appeared in the Top 3
    {best_vehicle['Top 3 Appearances']} times.
    """
)

st.divider()

# Bar Chart

st.subheader(
    "📊 Top Performing Vehicles"
)

st.bar_chart(
    leaderboard
    .head(14)
    .set_index("Vehicle")
)

st.divider()

# Leaderboard Table

st.subheader(
    "🏆 Vehicle Leaderboard"
)

st.dataframe(
    leaderboard,
    use_container_width=True,
    hide_index=True
)

# ==========================================
# RIDERSHIP PAGE
