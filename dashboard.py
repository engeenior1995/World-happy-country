import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import warnings
import os 
warnings.filterwarnings('ignore')

# Set page configuration
st.set_page_config(
    page_title="World Happiness Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with Background and Enhanced Styling
st.markdown("""
    <style>
    @import url('https://unsplash.com/photos/three-men-laughing-while-looking-in-the-laptop-inside-room-XkKCui44iM0');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    body {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .main { 
        padding: 0rem 0rem;
        background-image: linear-gradient(rgba(0,0,0,0.35), rgba(0,0,0,0.35)), 
                         url('https://images.unsplash.com/photo-1552664730-d307ca884978?w=1200&h=800&fit=crop');
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
        min-height: 100vh;
    }
    
    .metric-card {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.9), rgba(118, 75, 162, 0.9));
        padding: 25px; 
        border-radius: 15px; 
        color: white; 
        text-align: center;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        backdrop-filter: blur(10px);
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 30px rgba(102, 126, 234, 0.4);
    }
    
    .hero-section {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.5), rgba(118, 75, 162, 0.5));
        padding: 80px 40px;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 40px;
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4);
        backdrop-filter: blur(10px);
        animation: fadeInDown 0.8s ease-out;
    }
    
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .hero-headline {
        font-size: 56px;
        font-weight: 900;
        color: white;
        text-shadow: 3px 3px 6px rgba(0, 0, 0, 0.6);
        margin: 0;
        line-height: 1.3;
        letter-spacing: -1px;
    }
    
    .hero-subtitle {
        font-size: 20px;
        color: #ffeb3b;
        margin-top: 20px;
        font-weight: 700;
        font-style: italic;
        letter-spacing: 2px;
    }
    
    .hero-tagline {
        color: #f0f0f0; 
        margin-top: 20px; 
        font-size: 16px;
        letter-spacing: 0.5px;
    }
    
    .filter-section {
        background: rgba(255, 255, 255, 0.98);
        padding: 30px;
        border-radius: 15px;
        margin-bottom: 30px;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
        border: 2px solid rgba(102, 126, 234, 0.2);
    }
    
    .stats-container {
        background: rgba(255, 255, 255, 0.95);
        padding: 25px;
        border-radius: 15px;
        margin: 20px 0;
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.1);
    }
    
    h2, h3, h4 {
        color: #333;
        font-weight: 700;
    }
    
    .section-divider {
        height: 3px;
        background: linear-gradient(90deg, #667eea, #764ba2, transparent);
        margin: 30px 0;
        border-radius: 2px;
    }
    
    .info-box {
        background: linear-gradient(135deg, rgba(100, 200, 255, 0.1), rgba(150, 100, 255, 0.1));
        border-left: 4px solid #667eea;
        padding: 15px 20px;
        border-radius: 8px;
        margin: 15px 0;
    }
    
    .footer {
        text-align: center;
        color: #ccc;
        font-size: 12px;
        padding: 20px;
        border-top: 1px solid rgba(255, 255, 255, 0.2);
    }
    </style>
    """, unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    base_path = os.path.join(os.path.dirname(__file__), "data")

    data_files = {
        2015: os.path.join(base_path, "2015.csv"),
        2016: os.path.join(base_path, "2016.csv"),
        2017: os.path.join(base_path, "2017.csv"),
        2018: os.path.join(base_path, "2018.csv"),
        2019: os.path.join(base_path, "2019.csv"),
    }

    dfs = {}
    for year, filepath in data_files.items():
        df = pd.read_csv(filepath)
        dfs[year] = df

    return dfs
@st.cache_data
def standardize_data(dfs):
    # 2015
    df_2015 = dfs[2015][['Country', 'Region', 'Happiness Rank', 'Happiness Score', 
                         'Economy (GDP per Capita)', 'Family', 'Health (Life Expectancy)', 
                         'Freedom', 'Trust (Government Corruption)', 'Generosity', 'Dystopia Residual']].copy()
    df_2015.columns = ['Country', 'Region', 'Rank', 'Score', 'Economy', 'Family', 'Health', 'Freedom', 'Trust', 'Generosity', 'Dystopia']
    df_2015['Year'] = 2015
    
    # 2016
    df_2016 = dfs[2016][['Country', 'Region', 'Happiness Rank', 'Happiness Score',
                         'Economy (GDP per Capita)', 'Family', 'Health (Life Expectancy)', 
                         'Freedom', 'Trust (Government Corruption)', 'Generosity', 'Dystopia Residual']].copy()
    df_2016.columns = ['Country', 'Region', 'Rank', 'Score', 'Economy', 'Family', 'Health', 'Freedom', 'Trust', 'Generosity', 'Dystopia']
    df_2016['Year'] = 2016
    
    # 2017
    df_2017 = dfs[2017][['Country', 'Happiness.Rank', 'Happiness.Score',
                         'Economy..GDP.per.Capita.', 'Family', 'Health..Life.Expectancy.', 
                         'Freedom', 'Generosity', 'Trust..Government.Corruption.', 'Dystopia.Residual']].copy()
    df_2017.columns = ['Country', 'Rank', 'Score', 'Economy', 'Family', 'Health', 'Freedom', 'Generosity', 'Trust', 'Dystopia']
    df_2017['Region'] = 'Unknown'
    df_2017 = df_2017[['Country', 'Region', 'Rank', 'Score', 'Economy', 'Family', 'Health', 'Freedom', 'Trust', 'Generosity', 'Dystopia']]
    df_2017['Year'] = 2017
    
    # 2018
    df_2018 = dfs[2018][['Overall rank', 'Country or region', 'Score', 'GDP per capita', 'Social support',
                         'Healthy life expectancy', 'Freedom to make life choices', 'Generosity', 
                         'Perceptions of corruption']].copy()
    df_2018.columns = ['Rank', 'Country', 'Score', 'Economy', 'Family', 'Health', 'Freedom', 'Generosity', 'Trust']
    df_2018['Region'] = 'Unknown'
    df_2018['Dystopia'] = 0
    df_2018 = df_2018[['Country', 'Region', 'Rank', 'Score', 'Economy', 'Family', 'Health', 'Freedom', 'Trust', 'Generosity', 'Dystopia']]
    df_2018['Year'] = 2018
    
    # 2019
    df_2019 = dfs[2019][['Overall rank', 'Country or region', 'Score', 'GDP per capita', 'Social support',
                         'Healthy life expectancy', 'Freedom to make life choices', 'Generosity', 
                         'Perceptions of corruption']].copy()
    df_2019.columns = ['Rank', 'Country', 'Score', 'Economy', 'Family', 'Health', 'Freedom', 'Generosity', 'Trust']
    df_2019['Region'] = 'Unknown'
    df_2019['Dystopia'] = 0
    df_2019 = df_2019[['Country', 'Region', 'Rank', 'Score', 'Economy', 'Family', 'Health', 'Freedom', 'Trust', 'Generosity', 'Dystopia']]
    df_2019['Year'] = 2019
    
    combined_df = pd.concat([df_2015, df_2016, df_2017, df_2018, df_2019], ignore_index=True, sort=False)
    return combined_df

dfs = load_data()
df = standardize_data(dfs)

# Hero Section with Headline
st.markdown("""
    <div class="hero-section">
        <h1 class="hero-headline">
            🌟 Happiness begins when you believe in yourself
        </h1>
        <p class="hero-subtitle">✨ ZARQ ALI ✨</p>
        <p class="hero-tagline">
            🌍 Explore global happiness trends • Discover what makes communities thrive • 2015-2019 World Happiness Report
        </p>
    </div>
    """, unsafe_allow_html=True)

# Filter Section
st.markdown('<div class="filter-section">', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    selected_year = st.multiselect(
        "📅 Select Year(s)",
        sorted(df['Year'].unique()),
        default=[],
        help="Choose one or more years to analyze"
    )

with col2:
    selected_countries = st.multiselect(
        "🌍 Select Country/Countries",
        sorted(df['Country'].unique()),
        default=[],
        help="Choose specific countries to compare"
    )

st.markdown('</div>', unsafe_allow_html=True)

# Apply filters only if selections are made
if selected_year and selected_countries:
    df_filtered = df[(df['Year'].isin(selected_year)) & (df['Country'].isin(selected_countries))]
    show_filtered = True
elif selected_year:
    df_filtered = df[df['Year'].isin(selected_year)]
    show_filtered = True
elif selected_countries:
    df_filtered = df[df['Country'].isin(selected_countries)]
    show_filtered = True
else:
    df_filtered = df
    show_filtered = False
    st.info("👈 Select years and/or countries from the filters above to explore the data, or view all data below")

# Metrics
st.markdown("""<div class="stats-container"><h3>📊 Key Metrics Overview</h3></div>""", unsafe_allow_html=True)
col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    st.metric("🎯 Avg Score", f"{df_filtered['Score'].mean():.2f}", delta=f"±{df_filtered['Score'].std():.2f}")
with col2:
    st.metric("🏆 Highest", f"{df_filtered['Score'].max():.2f}", delta=f"of {df_filtered['Score'].min():.2f}")
with col3:
    st.metric("🌍 Countries", int(df_filtered['Country'].nunique()))
with col4:
    st.metric("📅 Years", int(df_filtered['Year'].nunique()))
with col5:
    top_country = df_filtered.groupby('Country')['Score'].mean().idxmax()
    st.metric("⭐ Top Country", top_country)
with col6:
    avg_economy = df_filtered['Economy'].mean()
    st.metric("💰 Avg Economy", f"{avg_economy:.3f}")

st.markdown("---")

# Tabs
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["🏆 Top Countries", "📈 Trends", "🔍 Factors", "🌐 Regions", "🎯 Deep Dive", "📊 Statistics", "💡 Insights"])

with tab1:
    st.subheader("Top & Bottom Performers")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 🎖️ Top 15 Countries by Happiness")
        top = df_filtered.groupby('Country')['Score'].mean().nlargest(15).reset_index()
        top.columns = ['Country', 'Score']
        top = top.sort_values('Score')
        fig = px.bar(top, x='Score', y='Country', orientation='h', color='Score', 
                     color_continuous_scale='Greens', title='Happiest Nations')
        fig.update_layout(height=450, showlegend=False, yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig, width='stretch')
    
    with col2:
        st.markdown("#### 📉 Bottom 15 Countries by Happiness")
        bottom = df_filtered.groupby('Country')['Score'].mean().nsmallest(15).reset_index()
        bottom.columns = ['Country', 'Score']
        bottom = bottom.sort_values('Score')
        fig = px.bar(bottom, x='Score', y='Country', orientation='h', color='Score', 
                     color_continuous_scale='Reds', title='Countries Needing Support')
        fig.update_layout(height=450, showlegend=False, yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig, width='stretch')

with tab2:
    st.subheader("Happiness Trends Over Time")
    
    if len(selected_countries) > 0:
        df_c = df_filtered[df_filtered['Country'].isin(selected_countries)].sort_values('Year')
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.line(df_c, x='Year', y='Score', color='Country', markers=True, 
                         line_shape='spline', title='Happiness Score Trends')
            fig.update_layout(height=380, hovermode='x unified')
            st.plotly_chart(fig, width='stretch')
        
        with col2:
            fig = px.line(df_c, x='Year', y='Rank', color='Country', markers=True, 
                         line_shape='spline', title='Rank Progress')
            fig.update_yaxes(autorange="reversed")
            fig.update_layout(height=380, hovermode='x unified')
            st.plotly_chart(fig, width='stretch')
        
        # Trend calculation
        st.markdown("#### 📊 Trend Analysis")
        for country in selected_countries:
            country_data = df_c[df_c['Country'] == country]
            if len(country_data) >= 2:
                first_score = country_data['Score'].iloc[0]
                last_score = country_data['Score'].iloc[-1]
                change = last_score - first_score
                pct_change = (change / first_score * 100) if first_score != 0 else 0
                emoji = "📈" if change > 0 else "📉"
                st.write(f"{emoji} **{country}**: {first_score:.3f} → {last_score:.3f} ({pct_change:+.1f}%)")
    else:
        st.markdown("""<div class="info-box">
        📌 Select countries to see trends over 2015-2019 period
        </div>""", unsafe_allow_html=True)

with tab3:
    st.subheader("Factor Contribution Analysis")
    factors = ['Economy', 'Family', 'Health', 'Freedom', 'Trust', 'Generosity']
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Average Factor Values")
        avg = df_filtered[factors].mean().sort_values(ascending=False)
        fig = px.bar(x=avg.values, y=avg.index, orientation='h', color=avg.values, 
                     color_continuous_scale='Viridis', title='Avg Impact by Factor')
        fig.update_layout(height=380, showlegend=False)
        st.plotly_chart(fig, width='stretch')
    
    with col2:
        st.markdown("#### Correlation with Happiness Score")
        corr = df_filtered[['Score'] + factors].corr()['Score'].drop('Score').sort_values(ascending=False)
        colors = ['#00cc96' if x > 0 else '#ef553b' for x in corr.values]
        fig = px.bar(x=corr.values, y=corr.index, orientation='h', color=corr.values, 
                     color_continuous_scale='RdBu_r', title='Factor Correlation')
        fig.update_layout(height=380, showlegend=False)
        st.plotly_chart(fig, width='stretch')
    
    # Factor breakdown
    st.markdown("#### 📈 Detailed Factor Analysis")
    col1, col2, col3 = st.columns(3)
    for i, factor in enumerate(factors):
        if i % 3 == 0:
            with col1:
                st.metric(f"{factor}", f"{df_filtered[factor].mean():.3f}", 
                         delta=f"σ={df_filtered[factor].std():.3f}")
        elif i % 3 == 1:
            with col2:
                st.metric(f"{factor}", f"{df_filtered[factor].mean():.3f}", 
                         delta=f"σ={df_filtered[factor].std():.3f}")
        else:
            with col3:
                st.metric(f"{factor}", f"{df_filtered[factor].mean():.3f}", 
                         delta=f"σ={df_filtered[factor].std():.3f}")

with tab4:
    st.subheader("Regional Analysis")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Top 10 Regions by Happiness")
        regions = df_filtered.groupby('Region')['Score'].mean().sort_values(ascending=False).head(10)
        fig = px.bar(x=regions.values, y=regions.index, orientation='h', color=regions.values, 
                     color_continuous_scale='Blues', title='Happiest Regions')
        fig.update_layout(height=380, showlegend=False)
        st.plotly_chart(fig, width='stretch')
    
    with col2:
        st.markdown("#### Regional Statistics")
        stats = df_filtered.groupby('Region')['Score'].agg(['mean', 'count', 'std']).sort_values('mean', ascending=False).head(10)
        stats.columns = ['Avg Score', 'Countries', 'Std Dev']
        st.dataframe(stats, width='stretch')
    
    # Regional distribution
    st.markdown("#### 🌍 Score Distribution by Region")
    fig = px.box(df_filtered, x='Region', y='Score', title='Happiness Distribution')
    fig.update_layout(height=380)
    st.plotly_chart(fig, width='stretch')

with tab5:
    st.subheader("Country Deep Dive Analysis")
    country = st.selectbox("Select a Country:", sorted(df_filtered['Country'].unique()))
    data = df_filtered[df_filtered['Country'] == country].sort_values('Year')
    
    if len(data) > 0:
        latest = data.iloc[-1]
        earliest = data.iloc[0]
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Current Score", f"{latest['Score']:.3f}")
        with col2:
            st.metric("Current Rank", int(latest['Rank']))
        with col3:
            st.metric("Region", latest['Region'] if latest['Region'] != 'Unknown' else 'N/A')
        with col4:
            change = ((latest['Score'] - earliest['Score']) / earliest['Score'] * 100) if earliest['Score'] != 0 else 0
            st.metric("Change %", f"{change:.1f}%", delta=f"{latest['Score']-earliest['Score']:.3f}")
        
        col1, col2 = st.columns(2)
        with col1:
            fig = px.line(data, x='Year', y='Score', markers=True, line_shape='spline', title='Score Trajectory')
            fig.update_layout(height=350)
            st.plotly_chart(fig, width='stretch')
        with col2:
            fig = px.line(data, x='Year', y='Rank', markers=True, line_shape='spline', title='Rank Evolution')
            fig.update_yaxes(autorange="reversed")
            fig.update_layout(height=350)
            st.plotly_chart(fig, width='stretch')
        
        # Factor breakdown for selected country
        st.markdown("#### 🔍 Factor Breakdown")
        factors = ['Economy', 'Family', 'Health', 'Freedom', 'Trust', 'Generosity']
        latest_factors = latest[factors]
        fig = px.bar(x=latest_factors.values, y=factors, orientation='h', 
                     color=latest_factors.values, color_continuous_scale='Plasma',
                     title=f"{country} - Factor Contributions")
        fig.update_layout(height=350, showlegend=False)
        st.plotly_chart(fig, width='stretch')

with tab6:
    st.subheader("Statistical Analysis")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Score Distribution")
        fig = px.histogram(df_filtered, x='Score', nbins=35, color_discrete_sequence=['#667eea'],
                          title='Happiness Score Distribution')
        fig.update_layout(height=380)
        st.plotly_chart(fig, width='stretch')
    
    with col2:
        st.markdown("#### Descriptive Statistics")
        stats = df_filtered['Score'].describe().round(4)
        df_stats = pd.DataFrame({'Metric': stats.index, 'Value': stats.values})
        st.dataframe(df_stats, width='stretch')
    
    st.markdown("#### Yearly Statistical Summary")
    yearly = df_filtered.groupby('Year')['Score'].agg(['mean', 'std', 'min', 'max', 'count']).round(3)
    yearly.columns = ['Mean Score', 'Std Dev', 'Minimum', 'Maximum', 'Countries']
    st.dataframe(yearly, width='stretch')
    
    st.markdown("#### Factor Correlation Matrix")
    factors = ['Score', 'Economy', 'Family', 'Health', 'Freedom', 'Trust', 'Generosity']
    corr_matrix = df_filtered[factors].corr()
    fig = px.imshow(corr_matrix, text_auto='.2f', color_continuous_scale='RdBu_r', 
                   title='Factor Correlation Matrix', zmin=-1, zmax=1)
    fig.update_layout(height=500)
    st.plotly_chart(fig, width='stretch')

with tab7:
    st.subheader("💡 Key Insights & Findings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🎯 Overall Insights")
        
        # Global average
        global_avg = df_filtered['Score'].mean()
        st.metric("Global Average Happiness", f"{global_avg:.3f}")
        
        # Top factor
        factors = ['Economy', 'Family', 'Health', 'Freedom', 'Trust', 'Generosity']
        top_factor = df_filtered[factors].mean().idxmax()
        st.write(f"**🔝 Most Impactful Factor:** {top_factor} ({df_filtered[top_factor].mean():.3f})")
        
        # Volatility
        score_std = df_filtered['Score'].std()
        st.write(f"**📊 Happiness Volatility (Std Dev):** {score_std:.3f}")
        
        # Regional spread
        regional_scores = df_filtered.groupby('Region')['Score'].mean()
        st.write(f"**🌍 Regional Range:** {regional_scores.max():.3f} - {regional_scores.min():.3f}")
    
    with col2:
        st.markdown("### 📈 Trend Insights")
        
        # Calculate global trend
        yearly_avg = df_filtered.groupby('Year')['Score'].mean()
        if len(yearly_avg) >= 2:
            trend = yearly_avg.iloc[-1] - yearly_avg.iloc[0]
            trend_emoji = "📈" if trend > 0 else "📉"
            st.write(f"{trend_emoji} **Global Trend (2015-2019):** {trend:+.3f}")
        
        # Most improved
        if len(selected_countries) > 0:
            improvements = []
            for country in selected_countries:
                country_data = df_filtered[df_filtered['Country'] == country].sort_values('Year')
                if len(country_data) >= 2:
                    change = country_data['Score'].iloc[-1] - country_data['Score'].iloc[0]
                    improvements.append((country, change))
            if improvements:
                most_improved = max(improvements, key=lambda x: x[1])
                st.write(f"**⭐ Most Improved:** {most_improved[0]} (+{most_improved[1]:.3f})")
        
        # Economic correlation
        econ_corr = df_filtered['Economy'].corr(df_filtered['Score'])
        st.write(f"**💰 Economy-Happiness Correlation:** {econ_corr:.3f}")
        
        # Family importance
        family_corr = df_filtered['Family'].corr(df_filtered['Score'])
        st.write(f"**👨‍👩‍👧 Family-Happiness Correlation:** {family_corr:.3f}")

st.markdown("""
    <div class="footer">
        <p>🌟 World Happiness Report 2015-2019 | Advanced Analytics Dashboard | Built with Streamlit + Plotly 📊</p>
        <p style="font-size: 11px; opacity: 0.8;">Data from UN Sustainable Development Solutions Network | Created by ZARQ ALI</p>
    </div>
    """, unsafe_allow_html=True)
