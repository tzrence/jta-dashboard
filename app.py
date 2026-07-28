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

    # ==========================================
    # RIDERSHIP CALCULATIONS
    # ==========================================

    total_riders = int(
        perf_df["Total Ridership"].sum()
    )

    avg_riders = round(
        perf_df["Total Ridership"].mean(),
        1
    )

    highest_ridership = int(
        perf_df["Total Ridership"].max()
    )

    lowest_ridership = int(
        perf_df["Total Ridership"].min()
    )

    # Monthly Ridership

    monthly_ridership = (
        perf_df.groupby(
            perf_df["Date"].dt.to_period("M")
        )["Total Ridership"]
        .sum()
    )

    best_month = monthly_ridership.idxmax()
    best_month_total = int(
        monthly_ridership.max()
    )

    # Growth Rate

    if len(monthly_ridership) >= 2:

        growth_rate = (
            (
                monthly_ridership.iloc[-1]
                -
                monthly_ridership.iloc[-2]
            )
            /
            monthly_ridership.iloc[-2]
        ) * 100

    else:

        growth_rate = 0

    # Best Week

    weekly_ridership = (
        perf_df.set_index("Date")
        .resample("W")
        ["Total Ridership"]
        .sum()
    )
    
    best_week_date = weekly_ridership.idxmax()
    
    best_week_total = int(
        weekly_ridership.max()
    )

week_start = (
    best_week_date -
    pd.Timedelta(days=6)
)


    # Days Above 100

    days_above_100 = len(
        perf_df[
            perf_df["Total Ridership"] > 100
        ]
    )

    # Best Day Of Week

    weekday_avg = (
        perf_df.groupby(
            perf_df["Date"]
            .dt.day_name()
        )["Total Ridership"]
        .mean()
    )

    best_weekday = (
        weekday_avg.idxmax()
    )

    best_weekday_avg = round(
        weekday_avg.max(),
        1
    )

    # ==========================================
    # RIDERSHIP HEALTH SCORE
    # ==========================================

    score = 0

    score += min(avg_riders, 100) * 0.4

    score += min(days_above_100, 25)

    score += max(
        min(growth_rate, 25),
        0
    )

    score += 10 if avg_riders > 75 else 0

    score = round(
        min(score, 100),
        0
    )

    if score >= 90:
        score_status = "Excellent"

    elif score >= 80:
        score_status = "Strong"

    elif score >= 70:
        score_status = "Moderate"

    else:
        score_status = "Needs Attention"

    # ==========================================
    # KPI ROW
    # ==========================================

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Riders",
            f"{total_riders:,}"
        )

    with col2:
        st.metric(
            "Average Daily Ridership",
            avg_riders
        )

    with col3:
        st.metric(
            "Highest Daily Ridership",
            highest_ridership
        )

    with col4:
        st.metric(
            "Ridership Health Score",
            f"{score}/100"
        )

    st.info(
        f"""
        Ridership Health Score Status: **{score_status}**

        *Ridership Health Score is determined by average daily ridership,
        month-over-month ridership growth, the number of 100+ rider days,
        and overall ridership performance trends.
        """
    )

    st.divider()

    # ==========================================
    # ADDITIONAL INSIGHTS
    # ==========================================

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Growth Rate",
            f"{growth_rate:.1f}%"
        )
        st.caption(
    "Compared to the previous operating month"
)

    with col2:
        st.metric(
            "100+ Rider Days",
            days_above_100
        )

    with col3:
        st.metric(
            "Best Weekday",
            best_weekday
        )

    with col4:
        st.metric(
            "Lowest Daily Ridership",
            lowest_ridership
        )

    st.divider()

    # ==========================================
    # CHART
    # ==========================================

    st.subheader("Ridership Trend")

    st.line_chart(
        perf_df.set_index("Date")
        ["Total Ridership"]
    )

    st.divider()

    # ==========================================
    # BEST MONTH / WEEK
    # ==========================================

    col1, col2 = st.columns(2)

    with col1:

        st.success(
            f"""
            🏆 Best Ridership Month

            {best_month}

            Total Riders:
            {best_month_total:,}
            """
        )

    with col2:

        st.success(
            f"""
            📅 Best Ridership Week

            Total Riders:
            {best_week_total:,}
            """
        )

    st.divider()

    # ==========================================
    # DATA TABLE
    # ==========================================

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

    st.divider()

    # ==========================================
    # EXECUTIVE SUMMARY
    # ==========================================

    st.subheader("📝 Executive Summary")

    st.success(
        f"""
        • Total riders served: {total_riders:,}

        • Average daily ridership: {avg_riders}

        • Ridership growth rate: {growth_rate:.1f}%

        • Best ridership month:
        {best_month} ({best_month_total:,} riders)

        • {days_above_100} operating days
        exceeded 100 riders.

        • Highest average ridership occurs
        on {best_weekday}s
        ({best_weekday_avg} riders).
        """
    )

    # ==========================================
    # AREAS FOR IMPROVEMENT
    # ==========================================

    st.subheader("🎯 Areas for Improvement")

    improvements = []

    if growth_rate < 0:
        improvements.append(
            f"Ridership declined {abs(growth_rate):.1f}% from the previous month."
        )

    if avg_riders < 75:
        improvements.append(
            "Average daily ridership remains below the 75-rider target."
        )

    if days_above_100 < 20:
        improvements.append(
            "Increase the number of operating days exceeding 100 riders."
        )

    if not improvements:
        improvements.append(
            "No major ridership concerns identified."
        )

    for item in improvements:
        st.warning(item)

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

    # ==========================================
    # PERFORMANCE GRADE
    # ==========================================

    if avg_auto >= 90:
        grade = "A"

    elif avg_auto >= 80:
        grade = "B"

    elif avg_auto >= 70:
        grade = "C"

    else:
        grade = "D"

    # ==========================================
    # LONGEST 90%+ STREAK
    # ==========================================

    perf_df["Above90"] = (
        perf_df["% Distance in Auto"] >= 0.90
    )

    longest_streak = 0
    current_streak = 0

    for value in perf_df["Above90"]:

        if value:
            current_streak += 1
            longest_streak = max(
                longest_streak,
                current_streak
            )
        else:
            current_streak = 0

    # ==========================================
    # KPI ROW
    # ==========================================

    col1, col2, col3, col4 = st.columns(4)

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

    with col3:
        st.metric(
            "Performance Grade",
            grade
        )

    with col4:
        st.metric(
            "Longest 90%+ Streak",
            f"{longest_streak} Days"
        )

    st.divider()

    # ==========================================
    # TRENDS
    # ==========================================

    st.subheader(
        "Autonomous Distance Trend"
    )

    st.line_chart(
        perf_df.set_index("Date")
        ["% Distance in Auto"]
    )

    st.divider()

    # ==========================================
    # VEHICLE LEADERBOARD
    # ==========================================

    vehicle_counts = {}

    for row in perf_df[
        "Top Distance In Auto"
    ]:

        vehicles = str(row).split("\n")

        for vehicle in vehicles:

            vehicle_name = (
                vehicle.split("–")[0]
                .strip()
            )

            if vehicle_name:

                if vehicle_name in vehicle_counts:
                    vehicle_counts[
                        vehicle_name
                    ] += 1
                else:
                    vehicle_counts[
                        vehicle_name
                    ] = 1

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

    best_vehicle = leaderboard.iloc[0]

    st.success(
        f"""
        🥇 Most Consistent Autonomous Vehicle

        {best_vehicle['Vehicle']}

        Ranked among NAVI's Top 3
        daily-performing autonomous
        vehicles on
        {best_vehicle['Top 3 Appearances']}
        operating days.
        """
    )

    st.divider()

    st.subheader(
        "📊 Top Performing Vehicles"
    )

    st.bar_chart(
        leaderboard
        .head(14)
        .set_index("Vehicle")
    )

    st.divider()

    st.subheader(
        "🏆 Vehicle Leaderboard"
    )

    st.dataframe(
        leaderboard.rename(
            columns={
                "Top 3 Appearances":
                "Days Ranked Among Top Performers"
            }
        ),
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # ==========================================
    # MONTHLY PERFORMANCE
    # ==========================================

    monthly_auto = (
        perf_df.groupby(
            perf_df["Date"]
            .dt.strftime("%B %Y")
        )["% Distance in Auto"]
        .mean()
        .mul(100)
    )

    best_months = (
        monthly_auto
        .sort_values(
            ascending=False
        )
        .head(5)
    )

    worst_months = (
        monthly_auto
        .sort_values(
            ascending=True
        )
        .head(5)
    )

    st.subheader(
        "📅 Monthly Performance"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.subheader(
            "🏆 Best Months"
        )

        st.dataframe(
            best_months
            .round(2)
            .reset_index()
            .rename(
                columns={
                    "Date":"Month",
                    "% Distance in Auto":
                    "Average Auto %"
                }
            ),
            hide_index=True,
            use_container_width=True
        )

    with col2:

        st.subheader(
            "⚠️ Lowest Months"
        )

        st.dataframe(
            worst_months
            .round(2)
            .reset_index()
            .rename(
                columns={
                    "Date":"Month",
                    "% Distance in Auto":
                    "Average Auto %"
                }
            ),
            hide_index=True,
            use_container_width=True
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
    # SAFETY LEADERBOARD
    # ==========================================

    vehicle_safety = {}

    for _, row in perf_df.iterrows():

        vehicles = str(
            row["Top Distance In Auto"]
        ).split("\n")

        for vehicle in vehicles:

            vehicle_name = (
                vehicle.split("–")[0]
                .strip()
            )

            if vehicle_name:

                if vehicle_name not in vehicle_safety:

                    vehicle_safety[
                        vehicle_name
                    ] = []

                if pd.notna(
                    row["Hard Brake %"]
                ):

                    vehicle_safety[
                        vehicle_name
                    ].append(
                        row["Hard Brake %"]
                    )

    safety_results = []

    for vehicle, brakes in (
        vehicle_safety.items()
    ):

        if len(brakes) == 0:
            continue

        average_brake = (
            sum(brakes)
            / len(brakes)
        ) * 100

        safety_results.append(
            [
                vehicle,
                round(
                    average_brake,
                    2
                )
            ]
        )

    safety_results = pd.DataFrame(
        safety_results,
        columns=[
            "Vehicle",
            "Average Hard Brake %"
        ]
    )

    safety_results = (
        safety_results
        .sort_values(
            "Average Hard Brake %",
            ascending=True
        )
    )

    safest_vehicle = (
        safety_results.iloc[0]
    )

    st.subheader(
        "🛡️ Safest Vehicles"
    )

    st.success(
        f"""
        🥇 Safest Vehicle

        {safest_vehicle['Vehicle']}

        Average Hard Brake Rate:
        {safest_vehicle['Average Hard Brake %']}%
        """
    )

    st.dataframe(
        safety_results.head(14),
        hide_index=True,
        use_container_width=True
    )
