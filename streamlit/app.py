import os
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# ---------------- Page config ----------------
st.set_page_config(
    page_title="Life Expectancy Dashboard",
    layout="wide"
)

st.title("🌍 Life Expectancy Data Visualization Dashboard")

# ---------------- File path ----------------
DATA_PATH = os.path.join("data", "LifeExpectancyData.csv")

# ---------------- File existence check (IMPORTANT) ----------------
if not os.path.exists(DATA_PATH):
    st.error("❌ Dataset not found at: data/LifeExpectancyData.csv")
    st.info("👉 Please ensure the file exists and is committed to the repository.")
    st.stop()

# ---------------- Load data (CACHE ONLY PURE FUNCTION) ----------------
@st.cache_data
def load_data(path):
    return pd.read_csv(path)

df = load_data(DATA_PATH)

# ---------------- Clean column names ----------------
df.columns = (
    df.columns.str.strip()
    .str.lower()
    .str.replace(" ", "_")
    .str.replace("-", "_")
)

st.success(f"✅ Dataset loaded: {df.shape[0]} rows × {df.shape[1]} columns")

# ---------------- Sidebar filters ----------------
st.sidebar.header("🔎 Filters")

years = sorted(df["year"].dropna().unique())
statuses = sorted(df["status"].dropna().unique())

selected_years = st.sidebar.multiselect(
    "Select Years",
    years,
    default=years[-10:] if len(years) >= 10 else years
)

selected_status = st.sidebar.multiselect(
    "Country Status",
    statuses,
    default=statuses
)

df_filtered = df[
    df["year"].isin(selected_years) &
    df["status"].isin(selected_status)
]

if df_filtered.empty:
    st.warning("⚠️ No data available for the selected filters.")
    st.stop()

# ---------------- Tabs ----------------
tabs = st.tabs([
    "📈 Avg Life Expectancy Over Time",
    "🏆 Top 10 Countries",
    "💰 GDP vs Life Expectancy",
    "⚠️ Adult Mortality vs Life Expectancy",
    "📏 BMI vs Life Expectancy",
    "📊 Life Expectancy Distribution",
    "📦 Life Expectancy by Status",
    "🎓 Schooling vs Life Expectancy",
    "👶 Infant Deaths vs Life Expectancy",
    "🔗 Correlation Heatmap"
])

# 1️⃣ Average Life Expectancy Over Time
with tabs[0]:
    avg_life = df_filtered.groupby("year")["life_expectancy"].mean()
    fig, ax = plt.subplots()
    ax.plot(avg_life.index, avg_life.values, marker="o")
    ax.set_title("Average Life Expectancy Over Time")
    ax.set_xlabel("Year")
    ax.set_ylabel("Life Expectancy")
    st.pyplot(fig)

# 2️⃣ Top 10 Countries
with tabs[1]:
    latest_year = df_filtered["year"].max()
    top10 = (
        df_filtered[df_filtered["year"] == latest_year]
        .nlargest(10, "life_expectancy")
    )
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(
        data=top10,
        x="life_expectancy",
        y="country",
        ax=ax
    )
    ax.set_title(f"Top 10 Countries by Life Expectancy ({latest_year})")
    st.pyplot(fig)

# 3️⃣ GDP vs Life Expectancy
with tabs[2]:
    fig, ax = plt.subplots()
    sns.scatterplot(
        data=df_filtered,
        x="gdp",
        y="life_expectancy",
        hue="status",
        ax=ax
    )
    ax.set_title("GDP vs Life Expectancy")
    st.pyplot(fig)

# 4️⃣ Adult Mortality vs Life Expectancy
with tabs[3]:
    fig, ax = plt.subplots()
    sns.scatterplot(
        data=df_filtered,
        x="adult_mortality",
        y="life_expectancy",
        hue="status",
        ax=ax
    )
    ax.set_title("Adult Mortality vs Life Expectancy")
    st.pyplot(fig)

# 5️⃣ BMI vs Life Expectancy
with tabs[4]:
    fig, ax = plt.subplots()
    sns.scatterplot(
        data=df_filtered,
        x="bmi",
        y="life_expectancy",
        hue="status",
        ax=ax
    )
    ax.set_title("BMI vs Life Expectancy")
    st.pyplot(fig)

# 6️⃣ Distribution
with tabs[5]:
    fig, ax = plt.subplots()
    sns.histplot(
        df_filtered["life_expectancy"],
        bins=30,
        kde=True,
        ax=ax
    )
    ax.set_title("Distribution of Life Expectancy")
    st.pyplot(fig)

# 7️⃣ Boxplot by Status
with tabs[6]:
    fig, ax = plt.subplots()
    sns.boxplot(
        data=df_filtered,
        x="status",
        y="life_expectancy",
        ax=ax
    )
    ax.set_title("Life Expectancy by Country Status")
    st.pyplot(fig)

# 8️⃣ Schooling vs Life Expectancy
with tabs[7]:
    fig, ax = plt.subplots()
    sns.scatterplot(
        data=df_filtered,
        x="schooling",
        y="life_expectancy",
        hue="status",
        ax=ax
    )
    ax.set_title("Schooling vs Life Expectancy")
    st.pyplot(fig)

# 9️⃣ Infant Deaths vs Life Expectancy
with tabs[8]:
    fig, ax = plt.subplots()
    sns.scatterplot(
        data=df_filtered,
        x="infant_deaths",
        y="life_expectancy",
        hue="status",
        ax=ax
    )
    ax.set_title("Infant Deaths vs Life Expectancy")
    st.pyplot(fig)

# 🔟 Correlation Heatmap
with tabs[9]:
    numeric_df = df_filtered.select_dtypes(include="number")
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(
        numeric_df.corr(),
        cmap="coolwarm",
        linewidths=0.5,
        ax=ax
    )
    ax.set_title("Correlation Heatmap")
    st.pyplot(fig)
