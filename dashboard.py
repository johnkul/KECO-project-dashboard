import streamlit as st
import pandas as pd
import plotly.express as px

# Load Data
file_path = "Kenya_Country-wise Results Report-final.xlsx"
df = pd.read_excel(file_path, sheet_name="Kenya_Country-wise Results Repo")

# Clean column names
df.columns = df.columns.str.strip().str.replace(" ", "_")

# Convert numerical columns
df["Female_Result"] = pd.to_numeric(df["Female_Result"], errors="coerce").fillna(0).astype(int)
df["Male_Result"] = pd.to_numeric(df["Male_Result"], errors="coerce").fillna(0).astype(int)
df["Total_Result"] = df["Female_Result"] + df["Male_Result"]

# Ensure Project_Number is treated as a categorical variable
df["Project_Number"] = df["Project_Number"].astype(str)

# Sidebar Filters
st.sidebar.header("Filters")
selected_indicator = st.sidebar.selectbox("Select Indicator", df["Indicator_Definition"].unique())
selected_projects = st.sidebar.multiselect("Select Projects", df["Project_Number"].unique(), default=df["Project_Number"].unique()[:5])

# Filter Data
df_filtered = df[df["Indicator_Definition"] == selected_indicator]
if selected_projects:
    df_filtered = df_filtered[df_filtered["Project_Number"].isin(selected_projects)]

# Ensure Project_Number is treated as a categorical variable
df_filtered["Project_Number"] = df_filtered["Project_Number"].astype(str)

# Title
st.title("📊 Kenya Project Results Dashboard")
st.subheader(f"Indicator: {selected_indicator}")

# Bar Chart - Total Beneficiaries per Project
fig_bar = px.bar(
    df_filtered, 
    x="Project_Number", 
    y="Total_Result", 
    color="Project_Number",
    title="Total Beneficiaries per Project",
    text_auto=True,  # Adds value labels to bars
    hover_data={"Total_Result": True, "Male_Result": True, "Female_Result": True}  # Show details on hover
)

# Update layout to treat x-axis as a categorical variable and show full numbers
fig_bar.update_layout(
    xaxis={'type': 'category'},
    yaxis={'tickformat': ','}  # Ensures full numbers without shortening to 'k'
)

st.plotly_chart(fig_bar)

# Pie Chart - Gender Distribution
gender_data = df_filtered[["Female_Result", "Male_Result"]].sum().reset_index()
gender_data.columns = ["Gender", "Count"]
fig_pie = px.pie(gender_data, names="Gender", values="Count", title="Gender Distribution")
st.plotly_chart(fig_pie)

# Table - Top Projects by Beneficiaries
st.subheader("🏆 Top Projects by Total Beneficiaries")
st.dataframe(df_filtered.sort_values(by="Total_Result", ascending=False).head(10))
