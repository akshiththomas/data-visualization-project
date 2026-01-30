import os
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# ---------- DEBUG: Find CSV file ----------

def find_csv_file():
    """Find LifeExpectancyData.csv anywhere in project"""
    candidates = []
    
    # 1. Look in data folder (expected)
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(project_root, "data", "LifeExpectancyData.csv")
    candidates.append(data_path)
    
    # 2. Look in streamlit_app folder (where you put it)
    app_dir = os.path.dirname(os.path.abspath(__file__))
    candidates.append(os.path.join(app_dir, "LifeExpectancyData.csv"))
    
    # 3. Look in project root
    candidates.append(os.path.join(project_root, "LifeExpectancyData.csv"))
    
    # 4. Search current directory and subdirs
    for root, dirs, files in os.walk(project_root):
        if "LifeExpectancyData.csv" in files:
            candidates.append(os.path.join(root, "LifeExpectancyData.csv"))
    
    for path in candidates:
        if os.path.exists(path):
            st.sidebar.success(f"✅ Found CSV at: `{path}`")
            return path
    
    st.error("❌ CSV not found! Looking for: LifeExpectancyData.csv")
    st.error(f"Current app location: `{os.path.abspath(__file__)}`")
    st.error(f"Project root: `{project_root}`")
    return None

# ---------- Load data ----------

@st.cache_data
def load_data(csv_path):
    df = pd.read_csv(csv_path)
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(" ", "")
        .str.replace("-", "")
    )
    return df

# ---------- Main app ----------

st.set_page_config(page_title="Life Expectancy Explorer", layout="wide")
st.title("🔍 Life Expectancy Data Explorer")

# Find the CSV
csv_path = find_csv_file()
if csv_path is None:
    st.stop()

# Load data
df = load_data(csv_path)
st.success(f"Loaded {df.shape[0]:,} rows × {df.shape[1]} columns")

# ---------- Filters ----------

st.sidebar.header("Filters")
years = sorted(df["year"].unique())
year_selected = st.sidebar.multiselect("Year", years, default=years)
status_selected = st.sidebar.multiselect(
    "Country status",
    sorted(df["status"].unique()),
    default=list(df["status"].unique()),
)

mask = df["year"].isin(year_selected) & df["status"].isin(status_selected)
df_filtered = df[mask]

st.subheader("📊 Data Preview")
st.dataframe(df_filtered.head())

# ---------- Plots ----------

tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Life Expectancy Over Time",
    "💰 GDP vs Life Expectancy", 
    "⚠️ Adult Mortality vs Life Expectancy",
    "📏 BMI vs Life Expectancy"
])

with tab1:
    avglifeexp = df_filtered.groupby("year")["lifeexpectancy"].mean()
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(avglifeexp.index, avglifeexp.values, marker="o", linewidth=2, color="#2E86AB")
    ax.set_title("Average Life Expectancy Over Time", fontsize=16, fontweight="bold")
    ax.set_xlabel("Year")
    ax.set_ylabel("Life Expectancy (years)")
    ax.grid(True, alpha=0.3)
    st.pyplot(fig)

with tab2:
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(
        data=df_filtered,
        x="gdp", 
        y="lifeexpectancy",
        hue="status",
        palette="coolwarm",
        s=80,
        alpha=0.7,
        ax=ax,
    )
    ax.set_title("GDP vs Life Expectancy", fontsize=16, fontweight="bold")
    ax.set_xlabel("GDP per Capita")
    ax.set_ylabel("Life Expectancy (years)")
    st.pyplot(fig)

with tab3:
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(
        data=df_filtered,
        x="adultmortality",
        y="lifeexpectancy", 
        hue="status",
        palette="magma",
        s=80,
        alpha=0.7,
        ax=ax,
    )
    ax.set_title("Adult Mortality vs Life Expectancy", fontsize=16, fontweight="bold")
    ax.set_xlabel("Adult Mortality (per 1000)")
    ax.set_ylabel("Life Expectancy (years)")
    st.pyplot(fig)

with tab4:
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(
        data=df_filtered,
        x="bmi",
        y="lifeexpectancy",
        hue="status",
        palette="Set2", 
        s=80,
        alpha=0.7,
        ax=ax,
    )
    ax.set_title("BMI vs Life Expectancy", fontsize=16, fontweight="bold")
    ax.set_xlabel("Average BMI")
    ax.set_ylabel("Life Expectancy (years)")
    st.pyplot(fig)
