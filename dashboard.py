import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os

st.set_page_config(
    page_title="World Happiness Dashboard",
    page_icon="🌍",
    layout="wide"
)

# ---------------------------
# 🔄 LOAD DATA (SAFE)
# ---------------------------
@st.cache_data
def load_data():
    base_path = "data"
    dfs = {}

    for year in range(2015, 2020):
        filepath = os.path.join(base_path, f"{year}.csv")

        if not os.path.exists(filepath):
            st.warning(f"Missing file: {filepath}")
            continue

        try:
            df = pd.read_csv(filepath)
            df.columns = df.columns.str.strip()
            dfs[year] = df
        except Exception as e:
            st.error(f"Error loading {year}: {e}")

    if not dfs:
        st.stop()

    return dfs

# ---------------------------
# 🧠 STANDARDIZE DATA
# ---------------------------
@st.cache_data
def standardize_data(dfs):
    all_dfs = []

    for year, df in dfs.items():
        df = df.copy()
        df.columns = df.columns.str.strip()

        col_map = {}
        for col in df.columns:
            c = col.lower()

            if "country" in c:
                col_map[col] = "Country"
            elif "region" in c:
                col_map[col] = "Region"
            elif "rank" in c:
                col_map[col] = "Rank"
            elif "score" in c:
                col_map[col] = "Score"
            elif "gdp" in c or "economy" in c:
                col_map[col] = "Economy"
            elif "family" in c or "social" in c:
                col_map[col] = "Family"
            elif "health" in c:
                col_map[col] = "Health"
            elif "freedom" in c:
                col_map[col] = "Freedom"
            elif "corruption" in c or "trust" in c:
                col_map[col] = "Trust"
            elif "generosity" in c:
                col_map[col] = "Generosity"

        df = df.rename(columns=col_map)

        required = ['Country', 'Region', 'Rank', 'Score',
                    'Economy', 'Family', 'Health',
                    'Freedom', 'Trust', 'Generosity']

        for col in required:
            if col not in df.columns:
                df[col] = np.nan

        df = df[required]
        df["Year"] = year

        all_dfs.append(df)

    return pd.concat(all_dfs, ignore_index=True)

# ---------------------------
# 🚀 LOAD + CLEAN
# ---------------------------
with st.spinner("Loading data..."):
    dfs = load_data()
    df = standardize_data(dfs)

df = df.dropna(subset=["Country", "Score"])
df["Score"] = pd.to_numeric(df["Score"], errors="coerce")

# ---------------------------
# 🌙 DARK MODE TOGGLE
# ---------------------------
dark_mode = st.toggle("🌙 Dark Mode")

if dark_mode:
    st.markdown(
        "<style>body {background-color:#0e1117; color:white;}</style>",
        unsafe_allow_html=True
    )

# ---------------------------
# 🎯 FILTERS
# ---------------------------
st.sidebar.header("Filters")

years = st.sidebar.multiselect(
    "Select Year",
    sorted(df["Year"].unique()),
    default=sorted(df["Year"].unique())
)

countries = st.sidebar.multiselect(
    "Select Countries",
    sorted(df["Country"].unique())
)

search = st.sidebar.text_input("Search Country")

df_filtered = df[df["Year"].isin(years)]

if countries:
    df_filtered = df_filtered[df_filtered["Country"].isin(countries)]

if search:
    df_filtered = df_filtered[
        df_filtered["Country"].str.contains(search, case=False)
    ]

if df_filtered.empty:
    st.warning("No data found")
    st.stop()

# ---------------------------
# 📊 KPI METRICS
# ---------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("Avg Score", f"{df_filtered['Score'].mean():.2f}")
col2.metric("Max Score", f"{df_filtered['Score'].max():.2f}")
col3.metric("Countries", df_filtered["Country"].nunique())

top_country = df_filtered.groupby("Country")["Score"].mean().idxmax()
col4.metric("Top Country", top_country)

# ---------------------------
# 🌍 MAP (PRO FEATURE)
# ---------------------------
st.subheader("Global Happiness Map")

map_df = df_filtered.groupby("Country")["Score"].mean().reset_index()

fig = px.choropleth(
    map_df,
    locations="Country",
    locationmode="country names",
    color="Score",
    color_continuous_scale="Viridis"
)

st.plotly_chart(fig, use_container_width=True)

# ---------------------------
# 📈 TREND CHART
# ---------------------------
st.subheader("Trend Over Time")

trend = df_filtered.groupby(["Year", "Country"])["Score"].mean().reset_index()

fig = px.line(
    trend,
    x="Year",
    y="Score",
    color="Country",
    markers=True
)

st.plotly_chart(fig, use_container_width=True)

# ---------------------------
# 🔥 TOP 10
# ---------------------------
st.subheader("Top 10 Countries")

top10 = (
    df_filtered.groupby("Country")["Score"]
    .mean()
    .nlargest(10)
    .sort_values()
)

fig = px.bar(
    top10,
    orientation="h"
)

st.plotly_chart(fig, use_container_width=True)

# ---------------------------
# 📊 CORRELATION
# ---------------------------
st.subheader("Factor Correlation")

corr = df_filtered.select_dtypes(include=np.number).corr()

fig = px.imshow(corr, text_auto=True)
st.plotly_chart(fig, use_container_width=True)

# ---------------------------
# 📥 DOWNLOAD BUTTON
# ---------------------------
st.download_button(
    "Download Filtered Data",
    df_filtered.to_csv(index=False),
    file_name="happiness_data.csv"
)

# ---------------------------
# 📌 FOOTER
# ---------------------------
st.markdown("---")
st.caption("World Happiness Dashboard • Production Ready 🚀")
