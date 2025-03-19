import streamlit as st
import pandas as pd
import plotly.express as px

# --- STREAMLIT PAGE CONFIG ---
st.set_page_config(page_title="Kenya Project Dashboard", layout="wide")

# --- TITLE ---
st.markdown("<h1 style='text-align: center;'>Finn Church Aid (FCA) Kenya Projects Dashboard</h1>", unsafe_allow_html=True)
st.markdown("### FCA KECO CPAR 2024 AGGREGATED DATA")

# --- LOAD DATA ---
file_path = "Kenya_Country-wise Results Report-final.xlsx"
df = pd.read_excel(file_path, sheet_name="Kenya_Country-wise Results Repo")

# Clean column names
df.columns = df.columns.str.strip().str.replace(" ", "_")

# Convert numerical columns
df["Female_Result"] = pd.to_numeric(df["Female_Result"], errors="coerce").fillna(0).astype(int)
df["Male_Result"] = pd.to_numeric(df["Male_Result"], errors="coerce").fillna(0).astype(int)
df["Total_Result"] = df["Female_Result"] + df["Male_Result"]

# Ensure categorical columns
df["Project_Number"] = df["Project_Number"].astype(str)
df["Project_thematic_Area"] = df["Project_thematic_Area"].astype(str)
df["Indicator_Definition"] = df["Indicator_Definition"].astype(str)

# --- PROJECT DESCRIPTION SECTION ---
project_descriptions = {
    "13229": "Business from Waste for Women in Kenya (Nairobi & Mombasa) – phase II",
    "12274": "Creative Industries program Kenya",
    "12254": "Promoting Peace through livelihood opportunities for rural communities in Kenya",
    "13247": "WICE",
    "13331": "Youth Employment and TVET in Kenya (TAMK)",
    "12253": "Development and Inclusive peace for all in Kenya (DIPAK)",
    "13216": "Provision of equitable access to safe & secure, inclusive, quality learning- ECW",
    "13323": "ECHO-HIP - Promoting access to quality inclusive education in protective learning",
    "13363": "PROSPECTS 2.0 - Enhanced environment for socioeconomic inclusion of Refugees",
    "13326": "Flooding Emergency Response for El Nino affected Communities in Marsabit and Samburu",
    "13364": "Emergency Response and Peacebuilding Program for Kalobeyei Refugee Settlement",
    "13270": "Dummy project for Kalobeyei settlement 2023 Annual Reporting (which included projects such as 13241, 13288, 13194, 13195, 13271)",
    "13248": "Resilience Programme to improve access to safe and adequate water"
}

# --- SIDEBAR FILTERS ---
st.sidebar.header("🎛 **Filters**")

# Thematic Area Filter
selected_thematic_area = st.sidebar.selectbox("🌍 **Select Thematic Area**", df["Project_thematic_Area"].unique())

# Filter indicators based on selected thematic area
indicator_options = df[df["Project_thematic_Area"] == selected_thematic_area]["Indicator_Definition"].unique()
selected_indicator = st.sidebar.selectbox("📊 **Select Indicator**", indicator_options)

# Get valid project options based on selected thematic area and indicator
project_options = df[(df["Project_thematic_Area"] == selected_thematic_area) & (df["Indicator_Definition"] == selected_indicator)]["Project_Number"].unique()

# Ensure default values exist in the options
default_projects = [p for p in df["Project_Number"].unique()[:5] if p in project_options]

# Project Selection
selected_projects = st.sidebar.multiselect("🏢 **Select Projects**", project_options, default=default_projects)

# --- DATA FILTERING ---
df_filtered = df[(df["Project_thematic_Area"] == selected_thematic_area) & (df["Indicator_Definition"] == selected_indicator)]
if selected_projects:
    df_filtered = df_filtered[df_filtered["Project_Number"].isin(selected_projects)]

# --- AGGREGATE DATA PER PROJECT ---
df_grouped = df_filtered.groupby("Project_Number", as_index=False).agg({
    "Total_Result": "sum",
    "Male_Result": "sum",
    "Female_Result": "sum"
})

# --- DISPLAY PROJECT DESCRIPTIONS ---
st.markdown("### 📌 Project Descriptions")
for project in selected_projects:
    if project in project_descriptions:
        st.markdown(f"**{project}** - {project_descriptions[project]}")

# --- CHARTS AND DASHBOARD CONTENT ---
st.markdown(f'### 📊 Indicator Data for {selected_thematic_area} - {selected_indicator}')
if df_filtered.empty:
    st.warning("⚠️ No data available for the selected filters.")
else:
    # --- BAR CHART - Total Beneficiaries per Project ---
    fig_bar = px.bar(
        df_grouped, 
        x="Project_Number", 
        y="Total_Result", 
        title="📈 Total Beneficiaries per Project",
        text_auto=True,
        hover_data={"Total_Result": True, "Female_Result": True, "Male_Result": True},  # Show all values on hover
        color="Project_Number",  # Different colors for each project
        color_discrete_sequence=px.colors.qualitative.Set2
    )

    fig_bar.update_layout(
        xaxis={'type': 'category'},
        yaxis={'tickformat': ','},
        plot_bgcolor="#121212",
        paper_bgcolor="#121212",
        font=dict(color="white"),
        title_font=dict(size=18, color="white"),
    )

    st.plotly_chart(fig_bar, use_container_width=True)

    # --- PIE CHART - Gender Distribution ---
    total_male = df_grouped["Male_Result"].sum()
    total_female = df_grouped["Female_Result"].sum()

    gender_data = pd.DataFrame({
        "Gender": ["Female", "Male"],
        "Count": [total_female, total_male]
    })

    fig_pie = px.pie(
        gender_data, 
        names="Gender", 
        values="Count", 
        title="👩🏾‍🤝‍👨🏾 Gender Distribution",
        color_discrete_sequence=["#FF69B4", "#3498DB"],
    )

    fig_pie.update_layout(
        plot_bgcolor="#121212",
        paper_bgcolor="#121212",
        font=dict(color="white"),
        title_font=dict(size=18, color="white"),
    )

    st.plotly_chart(fig_pie, use_container_width=True)

    # --- SUMMARY METRICS ---
    st.markdown("### 📌 Summary")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Beneficiaries", f"{df_grouped['Total_Result'].sum():,}")
    col2.metric("Male Beneficiaries", f"{total_male:,}")
    col3.metric("Female Beneficiaries", f"{total_female:,}")

    # --- TABLE - Top Projects ---
    st.markdown("### 🏆 Top Projects by Total Beneficiaries")
    st.dataframe(df_filtered.sort_values(by="Total_Result", ascending=False).head(10), height=300, width=800)

st.markdown("---")

# --- FOOTER ---
st.markdown("""
    <div style="text-align:center; font-size:14px; color:#DDDDDD;">
        🚀 Developed by <b>JOHN KUL</b> | FINN CHURCH AID (FCA) KECO CPAR 2024 AGGREGATED DATA | <i>Last Updated: 2025</i>
    </div>
""", unsafe_allow_html=True)
