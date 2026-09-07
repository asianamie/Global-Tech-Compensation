# Engineering Framework: Global Tech Compensation Analysis

## 📌 Core Engineering Problem
Corporate compensation infrastructure often suffers from fragmented data formatting and duplicate records. This analysis engineers a pipeline to standardize job classifications and compute deviations from market baselines.

## 🛠️ Data Infrastructure & Stack
*   **Engine Environment:** SQLite Engine, PostgreSQL
*   **Engineering Frameworks:** Common Table Expressions (CTEs), Partitioned Windowing Functions (`ROW_NUMBER`), Analytics Case Logic, Aggregations,Trajectory Analysis.

## 📈 Strategic Insights Discovered
1. **Classification Anomalies Detected:** Data entries contained mixed case structures and non-standard titles (e.g., `data analyst` vs `Data Analyst`). This variation skews raw metrics if not handled by explicit text manipulation tools.
2. **Compensation Imbalances:** Mid-to-Senior level engineers exhibit salary variations up to **$21,500 over average baselines**, highlighting clear opportunities to optimize regional market bands.
3. **Tiered Compensation Leaders**: Utilizing DENSE_RANK(), top-earning roles within each experience level consistently isolate specialized domain tracks (e.g., Machine Learning Infrastructure and Data Engineering) over generalist roles, establishing market ceilings for each tier.
<img width="670" height="425" alt="image" src="https://github.com/user-attachments/assets/00ba766f-4d77-4ca6-a9e2-48fe758a37e1" />

4. **Above-Market Role Benchmarking**: Cross-joining role averages against the global baseline (overall_avg) reveals which specialized titles command a premium, allowing organizations to spot high-cost functions exceeding global salary baselines.
<img width="698" height="139" alt="image" src="https://github.com/user-attachments/assets/5c94b86b-793e-489f-a1e9-69bd61759cff" />
   
5. **Tier Distribution Across Seniority**: Categorizing compensation into explicit pay bands (<$80k, $80k–$150k, >$150k) highlights the shift from mid-pay density at entry/mid levels to heavy concentration in the high-pay tier (>$150k) for senior-level roles.
<img width="657" height="255" alt="image" src="https://github.com/user-attachments/assets/503938e1-bfc0-44db-9fd7-4f26ff152c1b" />

6. **Senior Transition Value Spike**: Pivoting experience levels (MI vs. SE) shows that transitioning from Mid to Senior yields significant percentage increases (up to ~46% in key data tracks like Data Engineer and Data Scientist), quantifying the exact economic reward of senior-level progression.
<img width="556" height="192" alt="image" src="https://github.com/user-attachments/assets/da50fee9-3b8a-4784-b3e3-281081417a48" />

## 🗺️ Data Pipeline Architecture

```mermaid
graph TD
A[Raw Messy CSV Data] --> B[SQLite Staging Table]
B --> C[UPPER Text Normalization]
C --> D[Window Function Duplicate Tracking]
D --> E[Calculated Salary Variance Output]
E --> F[Tableau Executive Dashboard]
```

## 🚀 Live Interactive Application & CI/CD Deployment

This repository includes a live, interactive web application built with **Streamlit** and **Plotly** to visualize global tech compensation trends and perform salary estimations.

* **Live Demo:** [Global Tech Compensation Dashboard](https://global-tech-compensation-qcuasyhg43xcyeajq7nmr8.streamlit.app/)

### Web App Architecture & Technical Highlights

* **Automated CI/CD Pipeline:** Integrated directly with GitHub to trigger automatic redeployments to Streamlit Community Cloud upon every commit to `main`.
* **Resilient Data Ingestion:** Built an explicit data loading pipeline (`load_data()`) in `app.py` with `try-except` exception handling and `st.stop()` circuit-breaker execution guards to prevent cascading app failures.
* **Optimized In-Memory Caching:** Leveraged `@st.cache_data` decorators to eliminate redundant disk reads, drastically improving visual dashboard rendering times.
* **Interactive Data Visualization:** Utilized Plotly Express for dynamic filtering, box plot distribution analysis, and regional compensation metrics across various roles and remote setups.

---

## 🛠 Repository Structure

```text
Global-Tech-Compensation/
├── app.py                      # Main Streamlit application entry point
├── salaries.csv                # Core dataset containing compensation metrics
├── requirements.txt            # Python dependencies for cloud deployment
├── queries.sql                 # SQL scripts for backend data transformation
└── README.md                   # Project documentation
