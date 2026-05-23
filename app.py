from pathlib import Path

import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------------
st.set_page_config(
    page_title="Socialize your Knowledge",
    page_icon="👥",
    layout="wide"
)

# -------------------------------------------------------
# IMPORT DATA
# -------------------------------------------------------
df = pd.read_csv("kpis.csv")

# -------------------------------------------------------
# TITLE
# -------------------------------------------------------
st.title("Socialize your Knowledge")
st.markdown(
    "_Site that helps us analyze the performance of "
    "Socialize your Knowledge employees._"
)

# -------------------------------------------------------
# SIDEBAR: LOGO AND FILTERS
# -------------------------------------------------------
logo_path = Path("logo.jpg")

if logo_path.exists():
    st.sidebar.image(str(logo_path))

st.sidebar.markdown("## Filters")

gender = st.sidebar.multiselect(
    "Select Gender",
    options=sorted(df["gender"].dropna().unique()),
    default=sorted(df["gender"].dropna().unique())
)

performance_score = st.sidebar.multiselect(
    "Select the Performance Score",
    options=sorted(df["performance_score"].dropna().unique()),
    default=sorted(df["performance_score"].dropna().unique())
)

marital_status = st.sidebar.multiselect(
    "Select Marital Status",
    options=sorted(df["marital_status"].dropna().unique()),
    default=sorted(df["marital_status"].dropna().unique())
)

df_selection = df[
    df["gender"].isin(gender)
    & df["performance_score"].isin(performance_score)
    & df["marital_status"].isin(marital_status)
]

# -------------------------------------------------------
# VALIDATE FILTER RESULTS
# -------------------------------------------------------
if df_selection.empty:
    st.warning("There are no employees matching the selected filters.")
    st.stop()

# -------------------------------------------------------
# KPI SUMMARY
# -------------------------------------------------------
col1, col2, col3 = st.columns(3)

col1.metric("Employees", len(df_selection))
col2.metric(
    "Average Salary",
    f"${df_selection['salary'].mean():,.2f}"
)
col3.metric(
    "Average Worked Hours",
    f"{df_selection['average_work_hours'].mean():.2f}"
)

st.markdown("---")

# -------------------------------------------------------
# CHART 1: AVERAGE WORKED HOURS BY GENDER
# -------------------------------------------------------
avg_hours_gender = (
    df_selection
    .groupby("gender", as_index=False)["average_work_hours"]
    .mean()
    .sort_values(by="average_work_hours")
)

fig_hours_gender = px.bar(
    avg_hours_gender,
    x="gender",
    y="average_work_hours",
    title="Average Worked Hours by Gender",
    labels={
        "average_work_hours": "Average Worked Hours",
        "gender": "Gender"
    },
    color_discrete_sequence=["#7ECBB4"],
    template="plotly_white"
)

fig_hours_gender.update_layout(plot_bgcolor="rgba(0,0,0,0)")

st.plotly_chart(fig_hours_gender)

# -------------------------------------------------------
# CHART 2: SALARY BY AGE
# -------------------------------------------------------
fig_age = px.scatter(
    df_selection,
    x="age",
    y="salary",
    color="position",
    title="Employee Salary by Age",
    labels={
        "age": "Age",
        "salary": "Salary",
        "position": "Position"
    },
    template="plotly_white"
)

fig_age.update_layout(plot_bgcolor="rgba(0,0,0,0)")

st.plotly_chart(fig_age)

# -------------------------------------------------------
# CHART 3: PERFORMANCE SCORE DISTRIBUTION
# -------------------------------------------------------
fig_distribution_perf = px.bar(
    df_selection,
    x="name_employee",
    y="performance_score",
    title="Performance Score Distribution",
    labels={
        "name_employee": "Employee Name",
        "performance_score": "Performance Score"
    },
    color_discrete_sequence=["#7ECBB4"],
    template="plotly_white"
)

fig_distribution_perf.update_layout(plot_bgcolor="rgba(0,0,0,0)")

st.plotly_chart(fig_distribution_perf)

# -------------------------------------------------------
# CHART 4: WORKED HOURS VS PERFORMANCE SCORE
# -------------------------------------------------------
fig_perf_work = px.scatter(
    df_selection,
    x="performance_score",
    y="average_work_hours",
    size="salary",
    color="department",
    hover_name="name_employee",
    title="Worked Hours vs. Performance Score",
    labels={
        "average_work_hours": "Average Hours",
        "performance_score": "Performance Score",
        "department": "Department",
        "salary": "Salary"
    },
    template="plotly_white"
)

fig_perf_work.update_layout(plot_bgcolor="rgba(0,0,0,0)")

st.plotly_chart(fig_perf_work)

# -------------------------------------------------------
# CONCLUSION
# -------------------------------------------------------
st.markdown("## Analysis")
st.markdown(
    """
    This dashboard allows users to filter employees by gender, performance
    score and marital status in order to analyze organizational indicators.

    The charts help identify differences in average worked hours, salary
    patterns by age and position, performance score distributions, and the
    possible relation between worked hours and employee performance.
    """
)
