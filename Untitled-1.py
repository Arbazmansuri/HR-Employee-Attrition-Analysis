
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="HR Attrition Dashboard",
    page_icon="📊",
    layout="wide"
)

st.markdown("""
<style>
    .block-container {
        padding-top: 1rem;
        padding-bottom: 0.5rem;
        padding-left: 2rem;
        padding-right: 2rem;
        max-width: 100%;
    }

    h1 {
        
h1 {
    font-size: 2rem !important;
    font-weight: 700 !important;
    line-height: 1.4 !important;
    padding-top: 0.5rem !important;
    padding-bottom: 0.5rem !important;
    margin-bottom: 0.3rem !important;
    white-space: normal !important;
    overflow: visible !important;

    }

    h2, h3 {
        font-size: 1.1rem !important;
    }

    div[data-testid="stMetric"] {
        padding: 0.4rem;
    }

    div[data-testid="stVerticalBlock"] {
        gap: 0.6rem;
    }
</style>
""", unsafe_allow_html=True)



st.title("HR Employee Attrition Dashboard")

st.caption("HR Analytics | Employee Retention & Attrition Insights")

st.divider()

st.subheader("Employee Overview")


# Load CSV file
data = pd.read_csv(
    r"C:/Users/mdjal/Downloads/Palo Alto Networks (1).csv"
)
data["AgeGroup"] = pd.cut(
    data["Age"],
    bins=[17, 25, 35, 45, 55, 65],
    labels=["18-25", "26-35", "36-45", "46-55", "56-65"]
)

# Sidebar Filters
st.sidebar.header("Dashboard Filters")

# Department Filter
departments = ["All"] + sorted(
    data["Department"].dropna().unique().tolist()
)
selected_department = st.sidebar.selectbox(
    "Select Department", departments
)

# Gender Filter
genders = ["All"] + sorted(
    data["Gender"].dropna().unique().tolist()
)
selected_gender = st.sidebar.selectbox(
    "Select Gender", genders
)

# Job Role Filter
job_roles = ["All"] + sorted(
    data["JobRole"].dropna().unique().tolist()
)
selected_job_role = st.sidebar.selectbox(
    "Select Job Role", job_roles
)

# Apply all filters
filtered_data = data.copy()

if selected_department != "All":
    filtered_data = filtered_data[
        filtered_data["Department"] == selected_department
    ]

if selected_gender != "All":
    filtered_data = filtered_data[
        filtered_data["Gender"] == selected_gender
    ]

if selected_job_role != "All":
    filtered_data = filtered_data[
        filtered_data["JobRole"] == selected_job_role
    ]



# Calculate KPIs using filtered data
total_employees = len(filtered_data)

employees_left = (
    filtered_data["Attrition"] == 1
).sum()

employees_stayed = (
    filtered_data["Attrition"] == 0
).sum()

attrition_rate = (
    employees_left / total_employees * 100
    if total_employees > 0 else 0
)

# Display KPI cards
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Employees", total_employees)
col2.metric("Employees Left", int(employees_left))
col3.metric("Employees Stayed", int(employees_stayed))
col4.metric("Attrition Rate", f"{attrition_rate:.2f}%")
st.divider()


# Dataset Preview
st.subheader("Dataset Preview")

st.dataframe(
    filtered_data,
    use_container_width=True,
    height=300
)

csv_data = filtered_data.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Filtered Dataset",
    data=csv_data,
    file_name="filtered_hr_attrition.csv",
    mime="text/csv"
)

st.success("CSV file loaded successfully!")


# Department and Overtime Analysis

col1, col2 = st.columns(2)



with col1:
    st.subheader("Department-wise Attrition Rate")

    department_attrition = (
        filtered_data.groupby("Department")["Attrition"].mean() * 100
    )

    fig, ax = plt.subplots(figsize=(5, 2.5))

    department_attrition.plot(
        kind="bar",
        ax=ax,
        width=0.5
    )

    ax.set_xlabel("Department")
    ax.set_ylabel("Attrition Rate (%)")
    ax.set_ylim(0, max(5, department_attrition.max() * 1.2))
    ax.tick_params(axis="x", rotation=0)

    for i, value in enumerate(department_attrition):
        ax.text(
            i, value + 0.5,
            f"{value:.1f}%",
            ha="center"
        )

    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)


with col2:
    st.subheader("Overtime vs Attrition Rate")

    overtime_attrition = (
        filtered_data.groupby("OverTime")["Attrition"].mean() * 100
    )

    fig, ax = plt.subplots(figsize=(5, 2.5))

    overtime_attrition.plot(
        kind="bar",
        ax=ax,
        width=0.5
    )

    ax.set_xlabel("Overtime")
    ax.set_ylabel("Attrition Rate (%)")
    ax.set_ylim(0, max(5, overtime_attrition.max() * 1.2))
    ax.tick_params(axis="x", rotation=0)

    for i, value in enumerate(overtime_attrition):
        ax.text(
            i, value + 0.5,
            f"{value:.1f}%",
            ha="center"
        )

    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

st.divider()


# Job Role and Age Group Analysis

col1, col2 = st.columns(2)



with col1:
    st.subheader("Job Role-wise Attrition Rate")

    jobrole_attrition = (
        filtered_data.groupby("JobRole")["Attrition"].mean() * 100
    ).sort_values(ascending=False)

    fig, ax = plt.subplots(figsize=(7, 3.5))

    jobrole_attrition.plot(
        kind="bar",
        ax=ax,
        width=0.6
    )

    ax.set_xlabel("Job Role")
    ax.set_ylabel("Attrition Rate (%)")
    ax.set_ylim(0, max(5, jobrole_attrition.max() * 1.2))
    ax.tick_params(axis="x", rotation=45)

    for i, value in enumerate(jobrole_attrition):
        ax.text(
            i, value + 0.5,
            f"{value:.1f}%",
            ha="center",
            fontsize=8
        )

    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)


with col2:
    st.subheader("Age Group-wise Attrition Rate")

    age_data = filtered_data.copy()

    age_data["Age Group"] = pd.cut(
        age_data["Age"],
        bins=[0, 25, 35, 45, 55, 100],
        labels=["25 and below", "26-35", "36-45", "46-55", "56+"],
        include_lowest=True
    )

    age_attrition = (
        age_data.groupby("Age Group", observed=False)["Attrition"].mean() * 100
    ).dropna()

    fig, ax = plt.subplots(figsize=(7, 3.5))

    age_attrition.plot(
        kind="bar",
        ax=ax,
        width=0.6
    )

    ax.set_xlabel("Age Group")
    ax.set_ylabel("Attrition Rate (%)")
    ax.set_ylim(0, max(5, age_attrition.max() * 1.2))
    ax.tick_params(axis="x", rotation=0)

    for i, value in enumerate(age_attrition):
        ax.text(
            i, value + 0.5,
            f"{value:.1f}%",
            ha="center",
            fontsize=9
        )

    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    st.bar_chart(age_attrition)
st.divider()


# Income and Job Satisfaction Analysis

col1, col2 = st.columns(2)

with col1:
    st.subheader("Monthly Income Group-wise Attrition Rate")

    income_data = filtered_data.copy()

    income_data["Income Group"] = pd.cut(
        income_data["MonthlyIncome"],
        bins=[0, 3000, 5000, 8000, 12000, float("inf")],
        labels=["0-3000", "3001-5000", "5001-8000",
                "8001-12000", "12000+"]
    )

    income_attrition = (
        income_data.groupby("Income Group", observed=False)["Attrition"].mean() * 100
    )

    st.bar_chart(income_attrition)

with col2:
    st.subheader("Job Satisfaction vs Attrition Rate")

    satisfaction_attrition = (
        filtered_data.groupby("JobSatisfaction")["Attrition"].mean() * 100
    )

    st.bar_chart(satisfaction_attrition)
st.divider()


# Years at Company vs Attrition
st.subheader("Years at Company vs Attrition Rate")

tenure_attrition = (
    filtered_data.groupby("YearsAtCompany")["Attrition"].mean() * 100
)

st.line_chart(tenure_attrition)
st.divider()



# Business Travel and Gender Analysis

col1, col2 = st.columns(2)

with col1:
    st.subheader("Business Travel vs Attrition Rate")

    travel_attrition = (
        filtered_data.groupby("BusinessTravel")["Attrition"].mean() * 100
    )

    st.bar_chart(travel_attrition)

with col2:
    st.subheader("Gender-wise Attrition Rate")

    gender_attrition = (
        filtered_data.groupby("Gender")["Attrition"].mean() * 100
    )

    st.bar_chart(gender_attrition)

st.divider()


# Business Insights and Recommendations
st.subheader("Business Insights & Recommendations")

st.markdown("### Key Findings")

st.write(
    f"- Employees analyzed: {len(filtered_data):,}"
)

st.write(
    f"- Employees who left: {int(employees_left):,}"
)

st.write(
    f"- Employees who stayed: {int(employees_stayed):,}"
)

st.write(
    f"- Attrition rate: {attrition_rate:.2f}%"
)

# Department with highest attrition rate
if not filtered_data.empty:
    dept_rates = (
        filtered_data.groupby("Department")["Attrition"].mean() * 100
    )

    if not dept_rates.empty:
        highest_dept = dept_rates.idxmax()
        highest_rate = dept_rates.max()

        st.write(
            f"- Highest department attrition: "
            f"{highest_dept} ({highest_rate:.2f}%)"
        )

# Overtime insight
if not filtered_data.empty:
    overtime_rates = (
        filtered_data.groupby("OverTime")["Attrition"].mean() * 100
    )

    if not overtime_rates.empty:
        highest_overtime = overtime_rates.idxmax()
        overtime_rate = overtime_rates.max()

        st.write(
            f"- Highest overtime-group attrition: "
            f"{highest_overtime} ({overtime_rate:.2f}%)"
        )

st.markdown("### Recommendations")

st.markdown("""
- Investigate departments with higher attrition rates.
- Review overtime workload and employee satisfaction.
- Examine salary and tenure patterns among employees who leave.
- Develop employee retention strategies based on verified findings.
""")

st.markdown("### Employee Retention Risk Analysis")

risk_col1, risk_col2 = st.columns(2)

with risk_col1:
    st.markdown("**Attrition by Monthly Income Group**")

    income_risk = (
        income_data.groupby(
            "Income Group", observed=True
        )["Attrition"].mean() * 100
    ).dropna()

    if not income_risk.empty:
        highest_income_group = income_risk.idxmax()
        highest_income_rate = income_risk.max()

        st.write(
            f"Highest attrition group: {highest_income_group}"
        )
        st.write(
            f"Attrition rate: {highest_income_rate:.2f}%"
        )

with risk_col2:
    st.markdown("**Attrition by Years at Company**")

    tenure_risk = (
        filtered_data.groupby("YearsAtCompany")["Attrition"].mean() * 100
    ).dropna()

    if not tenure_risk.empty:
        highest_tenure = tenure_risk.idxmax()
        highest_tenure_rate = tenure_risk.max()

        st.write(
            f"Highest attrition tenure: {highest_tenure} years"
        )
        st.write(
            f"Attrition rate: {highest_tenure_rate:.2f}%"
        )


# Data Quality Check
st.subheader("Data Quality Check")

col1, col2, col3, col4 = st.columns(4)

missing_values = int(data.isnull().sum().sum())
duplicate_rows = int(data.duplicated().sum())
total_columns = len(data.columns)

invalid_attrition = int(
    (~data["Attrition"].isin([0, 1])).sum()
)

col1.metric("Missing Values", missing_values)
col2.metric("Duplicate Rows", duplicate_rows)
col3.metric("Total Columns", total_columns)
col4.metric("Invalid Attrition Values", invalid_attrition)

# Missing values by column
st.markdown("### Missing Values by Column")

missing_by_column = data.isnull().sum()
missing_by_column = missing_by_column[missing_by_column > 0]

if missing_by_column.empty:
    st.success("No missing values found.")
else:
    missing_report = pd.DataFrame({
        "Missing Count": missing_by_column,
        "Missing Percentage": (
            missing_by_column / len(data) * 100
        ).round(2)
    })

    st.dataframe(missing_report)

# Duplicate records
st.markdown("### Duplicate Records")

if duplicate_rows == 0:
    st.success("No duplicate rows found.")
else:
    st.warning(
        f"{duplicate_rows} duplicate rows found. "
        "Review them before removing."
    )



