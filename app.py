import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import joblib
import os

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Global Tech Compensation Hub",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- CACHED DATA & MODEL LOADING ---
@st.cache_data
def load_data():
    """Load and preprocess the dataset."""
    data_path = "data/cleaned_tech_salaries.csv"  # Adjust path to match your repository
    if os.path.exists(data_path):
        df = pd.read_csv(data_path)
    else:
        # Fallback dummy data structure if file path isn't set up yet
        df = pd.DataFrame({
            'job_title': ['Data Scientist', 'Software Engineer', 'Data Engineer', 'ML Engineer'],
            'company_location': ['United States', 'Germany', 'United Kingdom', 'Canada'],
            'experience_level': ['Entry', 'Mid', 'Senior', 'Executive'],
            'salary_in_usd': [85000, 120000, 150000, 210000],
            'work_year': [2023, 2023, 2024, 2024],
            'remote_ratio': [0, 50, 100, 100],
            'company_size': ['Small', 'Medium', 'Large', 'Medium']
        })
    return df

@st.cache_resource
def load_model():
    """Load trained Machine Learning model if available."""
    model_path = "models/salary_model.pkl"  # Adjust path to match your repository
    if os.path.exists(model_path):
        return joblib.load(model_path)
    return None

df = load_data()
model = load_model()

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("📌 Navigation")
page = st.sidebar.radio(
    "Go to",
    ["Overview", "Salary Estimator", "Global Salary Analytics"]
)

st.sidebar.markdown("---")
st.sidebar.caption("Built with Streamlit • Global Tech Compensation Repo")

# --- PAGE 1: OVERVIEW ---
if page == "Overview":
    st.title("💼 Global Tech Compensation Analysis")
    st.markdown("""
    Welcome to the **Global Tech Compensation Hub**. This application explores market patterns, regional salary disparities, 
    and predicts expected compensation for technical roles across the globe.
    """)
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Records Analyzed", f"{len(df):,}")
    col2.metric("Median Global Salary", f"${df['salary_in_usd'].median():,.0f}")
    col3.metric("Unique Job Roles", f"{df['job_title'].nunique()}")
    col4.metric("Countries Represented", f"{df['company_location'].nunique()}")

    st.markdown("### Key Features")
    st.markdown("""
    - **Salary Estimator:** Interactive ML model estimating compensation based on experience, location, and role.
    - **Global Salary Analytics:** Interactive dashboard comparing total compensation across countries, remote models, and experience levels.
    """)

# --- PAGE 2: SALARY ESTIMATOR ---
elif page == "Salary Estimator":
    st.title("🎯 Salary Estimator")
    st.write("Input your profile details below to get an estimated compensation range.")

    col1, col2 = st.columns(2)

    with col1:
        job_title = st.selectbox("Job Title", sorted(df['job_title'].unique()))
        experience = st.selectbox("Experience Level", sorted(df['experience_level'].unique()))
        company_size = st.selectbox("Company Size", sorted(df['company_size'].unique()))

    with col2:
        location = st.selectbox("Company Location", sorted(df['company_location'].unique()))
        remote = st.select_slider("Remote Work Ratio (%)", options=[0, 50, 100], value=100)

    st.markdown("---")

    if st.button("Calculate Compensation Estimate", type="primary"):
        if model is not None:
            # Prepare input dataframe matching your model features
            input_data = pd.DataFrame([{
                'job_title': job_title,
                'experience_level': experience,
                'company_location': location,
                'company_size': company_size,
                'remote_ratio': remote
            }])
            
            prediction = model.predict(input_data)[0]
            st.success(f"### Estimated Base Salary: **${prediction:,.0f} USD** / year")
        else:
            # Rule-based / Median fallback estimate if no model artifact is present
            filtered_df = df[
                (df['job_title'] == job_title) & 
                (df['experience_level'] == experience)
            ]
            
            if not filtered_df.empty:
                est_salary = filtered_df['salary_in_usd'].median()
                st.success(f"### Estimated Median Salary: **${est_salary:,.0f} USD** / year")
                st.info("Note: Showing median salary from historical data for this role and experience level.")
            else:
                st.warning("Insufficient data matching this combination. Try broadening your criteria.")

# --- PAGE 3: ANALYTICS DASHBOARD ---
elif page == "Global Salary Analytics":
    st.title("📊 Global Salary Analytics")
    
    # Filter Controls
    st.sidebar.subheader("Dashboard Filters")
    selected_roles = st.sidebar.multiselect("Filter Roles", options=df['job_title'].unique(), default=df['job_title'].unique()[:3])
    
    filtered_df = df[df['job_title'].isin(selected_roles)] if selected_roles else df

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Salary Distribution by Experience Level")
        fig_box = px.box(
            filtered_df, 
            x='experience_level', 
            y='salary_in_usd', 
            color='experience_level',
            labels={'salary_in_usd': 'Salary (USD)', 'experience_level': 'Experience'},
            template="plotly_white"
        )
        st.plotly_chart(fig_box, use_container_width=True)

    with col2:
        st.subheader("Top Countries by Median Salary")
        top_countries = (
            filtered_df.groupby('company_location')['salary_in_usd']
            .median()
            .reset_index()
            .sort_values(by='salary_in_usd', ascending=False)
            .head(10)
        )
        fig_bar = px.bar(
            top_countries, 
            x='salary_in_usd', 
            y='company_location', 
            orientation='h',
            labels={'salary_in_usd': 'Median Salary (USD)', 'company_location': 'Location'},
            template="plotly_white"
        )
        fig_bar.update_layout(yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig_bar, use_container_width=True)
