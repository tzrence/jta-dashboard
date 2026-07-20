import streamlit as st 

import pandas as pd 

  

st.set_page_config( 

    page_title="NAVI Fleet Operations Dashboard", 

    layout="wide" 

) 

  

# ===== LOGO ===== 

st.image("logowhite.jpg", width=200) 

st.sidebar.image("logogrey.jpg", width=180) 

  

# ===== NAVI HEADER ===== 

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

  

# ===== LOAD DATA ===== 

df = pd.read_excel("fleet_data.xlsx") 

  

# Clean column names 

df.columns = df.columns.str.strip() 

  

# ===== KPIs ===== 

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

  

# ===== CHART ===== 

st.subheader("Fleet Status Overview") 

  

status_counts = df["Status"].value_counts() 

  

st.bar_chart(status_counts) 

  

st.divider() 

  

# ===== TABLE ===== 

display_df = df.copy() 

  

display_df["Status"] = display_df["Status"].replace({ 

    "Active": "🟢 Active", 

    "Down": "🔴 Down", 

    "Maintenance": "🟡 Maintenance" 

}) 

  

st.subheader("Fleet Status Table") 

  

st.dataframe( 

    display_df, 

    use_container_width=True 

) 

  

# ===== FILTER ===== 

st.subheader("Filter by Status") 

  

status_filter = st.selectbox( 

    "Choose Status", 

    ["All", "Active", "Down", "Maintenance"] 

) 

  

if status_filter == "All": 

    filtered_df = df 

else: 

    filtered_df = df[df["Status"] == status_filter] 

  

st.dataframe( 

    filtered_df, 

    use_container_width=True 

) 

  

st.divider() 

  

# ===== INSIGHTS ===== 

st.subheader("Fleet Insights") 

  

if not df.empty: 

  

    most_used = df.loc[ 

        df["Miles This Month"].idxmax(), 

        "Vehicle" 

    ] 

  

    avg_miles = round( 

        df["Miles This Month"].mean(), 

        0 

    ) 

  

    availability = round( 

        (active / total) * 100, 

        1 

    ) 

  

    st.success(f"🏆 Most Utilized Vehicle: {most_used}") 

    st.info(f"📈 Average Monthly Mileage: {avg_miles}") 

    st.info(f"✅ Fleet Availability: {availability}%") 
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="NAVI Grant Management Dashboard",
    layout="wide"
)

# =========================
# LOGO
# =========================

st.image("logowhite.jpg", width=200)

# =========================
# HEADER
# =========================

st.markdown("""
<div style="
background-color:#003366;
padding:20px;
border-radius:10px;
margin-bottom:20px;">

<h1 style="
color:white;
text-align:center;
font-weight:bold;
margin:0;">
NAVI Grant Management Dashboard
</h1>

<p style="
color:white;
text-align:center;
font-size:16px;
margin-top:8px;">
Grant Management & AI Grant Discovery
</p>

</div>
""", unsafe_allow_html=True)

# =========================
# SAMPLE DATA
# =========================

grants = pd.DataFrame({
    "Grant Name": [
        "FTA Low-No Program",
        "RAISE Grant",
        "State Mobility Grant",
        "Workforce Development Grant"
    ],
    "Status": [
        "In Progress",
        "Submitted",
        "Awarded",
        "Not Started"
    ],
    "Deadline": [
        "2026-08-15",
        "2026-09-01",
        "2026-07-30",
        "2026-10-12"
    ],
    "Amount": [
        2000000,
        1500000,
        500000,
        250000
    ]
})

# =========================
# TABS
# =========================

tab1, tab2 = st.tabs(
    ["📋 Grant Tracker", "🤖 AI Grant Finder"]
)

# =========================
# TAB 1
# =========================

with tab1:

    total_grants = len(grants)

    in_progress = len(
        grants[grants["Status"] == "In Progress"]
    )

    awarded = len(
        grants[grants["Status"] == "Awarded"]
    )

    potential_funding = grants["Amount"].sum()

    awarded_funding = grants[
        grants["Status"] == "Awarded"
    ]["Amount"].sum()

    c1, c2, c3, c4, c5 = st.columns(5)

    with c1:
        st.info(f"📄 Total Grants\n\n{total_grants}")

    with c2:
        st.warning(f"🟡 In Progress\n\n{in_progress}")

    with c3:
        st.success(f"🏆 Awarded\n\n{awarded}")

    with c4:
        st.info(
            f"💰 Potential Funding\n\n${potential_funding:,.0f}"
        )

    with c5:
        st.success(
            f"💵 Awarded Funding\n\n${awarded_funding:,.0f}"
        )

    st.divider()

    display_df = grants.copy()

    display_df["Status"] = display_df["Status"].replace({
        "Awarded": "🟢 Awarded",
        "Submitted": "✅ Submitted",
        "In Progress": "🟡 In Progress",
        "Not Started": "🔴 Not Started"
    })


    st.subheader("Grant Portfolio")


    st.dataframe(
        display_df,
        use_container_width=True
    )


    st.subheader("Grant Status Overview")


    st.bar_chart(
        grants["Status"].value_counts()
    )

# ===================================
# TAB 2
# ===================================


with tab2:


    st.subheader("AI Grant Discovery")


    organization_type = st.selectbox(
        "Organization Type",
        [
            "Public Transit",
            "Nonprofit",
            "Local Government",
            "Education"
        ]
    )


    keywords = st.text_input(
        "Keywords",
        placeholder="Electric buses, mobility, transportation"
    )


    if st.button("Find Opportunities"):


        st.success("Recommended Grants")


        st.markdown("""
### 🚍 FTA Low-No Emissions Program


**Match Score:** 95%


Supports fleet modernization,
electric buses, and sustainable transit.


**Potential Funding:** $2M+
        """)


        st.markdown("""
### 🏗️ RAISE Program


**Match Score:** 89%


Supports transportation infrastructure
and mobility projects.


**Potential Funding:** $1M+
        """)


        st.markdown("""
### 🌱 Clean Transportation Grant


**Match Score:** 83%


Supports emissions reduction projects
and environmental initiatives.
        """)
