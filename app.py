import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="NAVI Grant Management Dashboard",
    layout="wide"
)

# ===== LOGO ===== 

st.image("logowhite.jpg", width=200)

# ===== BRANDING =====

st.markdown("""
<style>
.main {
    background-color: #F4F6F8;
}

h1 {
    color: white;
}

.metric-box {
    padding: 10px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# ===== HEADER =====

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
📋 NAVI Grant Management Dashboard
</h1>

<p style="
color:white;
text-align:center;
font-size:16px;
margin-top:8px;">
Grant Tracking & AI Grant Discovery
</p>

</div>
""", unsafe_allow_html=True)

# ===== SAMPLE DATA =====

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

# ===== TABS =====

tab1, tab2 = st.tabs(
    [
        "📋 Grant Tracker",
        "🤖 AI Grant Finder"
    ]
)

# ===================================
# TAB 1
# ===================================

with tab1:

    total_grants = len(grants)

    in_progress = len(
        grants[grants["Status"] == "In Progress"]
    )

    awarded = len(
        grants[grants["Status"] == "Awarded"]
    )

    total_funding = grants["Amount"].sum()

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.info(f"📄 Total Grants\n\n{total_grants}")

    with c2:
        st.warning(f"🟡 In Progress\n\n{in_progress}")

    with c3:
        st.success(f"🟢 Awarded\n\n{awarded}")

    with c4:
        st.success(
            f"💰 Pipeline Value\n\n${total_funding:,.0f}"
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
