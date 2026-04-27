import altair as alt
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import streamlit as st

# Theme Colors
COLOR_PRIMARY = "#FF4B4B" # Streamlit Red
COLOR_ALARM = "#FF0000"   # Bright Red for Alarming stats
COLOR_GOOD = "#00FF00"    # Green
COLOR_DARK_BG = "#0E1117"
COLOR_TEXT_MAIN = "#FAFAFA"

def apply_custom_style():
    """Applies custom CSS for a premium dark look."""
    st.markdown("""
        <style>
        /* General Background */
        .stApp {
            background-color: #0E1117;
            color: #FAFAFA;
        }
        
        /* Metric Cards */
        div[data-testid="stMetric"] {
            background-color: #262730;
            border: 1px solid #41444C;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 2px 2px 5px rgba(0,0,0,0.5);
            transition: transform 0.2s;
        }
        div[data-testid="stMetric"]:hover {
            transform: scale(1.02);
            border-color: #FF4B4B;
        }
        
        /* Headers */
        h1, h2, h3 {
            font-family: 'Helvetica Neue', sans-serif;
            font-weight: 600;
        }
        h1 {
            background: -webkit-linear-gradient(45deg, #FF4B4B, #FF914D);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        /* Sidebar */
        section[data-testid="stSidebar"] {
            background-color: #262730;
        }
        
        /* Tables */
        div.stDataFrame {
            border: 1px solid #41444C;
            border-radius: 5px;
        }
        
        /* Alarm Section */
        .alarm-header {
            color: #FF0000;
            font-weight: bold;
            font-size: 24px;
            margin-bottom: 10px;
            border-bottom: 2px solid #FF0000;
            padding-bottom: 5px;
        }
        </style>
    """, unsafe_allow_html=True)

def plot_global_map(df, year):
    """Plots a chloropleth map of Happiness Scores."""
    df_year = df[df['Year'] == year]
    
    fig = px.choropleth(
        df_year, 
        locations="Country", 
        locationmode='country names',
        color="Score",
        hover_name="Country",
        color_continuous_scale="Viridis", # Or split-complementary
        projection="natural earth",
        title=f"Global Happiness Scores ({year})"
    )
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=COLOR_TEXT_MAIN),
        margin={"r":0,"t":40,"l":0,"b":0},
        geo=dict(
            bgcolor='rgba(0,0,0,0)',
            showocean=True,
            oceancolor="#1E2129",
            showlakes=True,
            lakecolor="#1E2129",
            landcolor="#262730"
        )
    )
    return fig

def plot_correlation_heatmap(df, year):
    """Plots a correlation heatmap for the selected year."""
    df_year = df[df['Year'] == year]
    cols = ['Score', 'GDP', 'Social_Support', 'Health', 'Freedom', 'Corruption', 'Generosity']
    corr = df_year[cols].corr()
    
    fig = px.imshow(
        corr,
        text_auto=True,
        aspect="auto",
        color_continuous_scale="RdBu_r",
        title=f"Correlation Matrix ({year})"
    )
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=COLOR_TEXT_MAIN)
    )
    return fig

def plot_yoy_trend(df, countries):
    """Plots a trend line for selected countries over years."""
    df_filtered = df[df['Country'].isin(countries)]
    
    chart = alt.Chart(df_filtered).mark_line(point=True).encode(
        x=alt.X('Year:O', axis=alt.Axis(title='Year', labelColor=COLOR_TEXT_MAIN, titleColor=COLOR_TEXT_MAIN)),
        y=alt.Y('Score', scale=alt.Scale(domain=[2, 8]), axis=alt.Axis(title='Happiness Score', labelColor=COLOR_TEXT_MAIN, titleColor=COLOR_TEXT_MAIN)),
        color='Country',
        tooltip=['Country', 'Year', 'Score', 'GDP']
    ).properties(
        title='Happiness Trend Analysis',
        background='rgba(0,0,0,0)'
    ).configure(
        background='transparent'
    ).configure_axis(
        gridColor='#41444C',
        domainColor='#41444C'
    ).configure_view(
        strokeOpacity=0
    ).configure_legend(
        labelColor=COLOR_TEXT_MAIN,
        titleColor=COLOR_TEXT_MAIN
    ).interactive()
    
    return chart

def plot_factors_scatter(df, year):
    """3D Scatter to show relationships between key factors."""
    df_year = df[df['Year'] == year]
    
    fig = px.scatter_3d(
        df_year, 
        x='GDP', 
        y='Health', 
        z='Score',
        color='Region',
        size='Social_Support',
        hover_name='Country',
        title=f"Multidimensional Analysis ({year})",
        opacity=0.8
    )
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=COLOR_TEXT_MAIN),
        scene=dict(
            xaxis=dict(backgroundcolor="rgba(0,0,0,0)", gridcolor="#41444C", title="GDP"),
            yaxis=dict(backgroundcolor="rgba(0,0,0,0)", gridcolor="#41444C", title="Health"),
            zaxis=dict(backgroundcolor="rgba(0,0,0,0)", gridcolor="#41444C", title="Score"),
        ),
        margin={"r":0,"t":40,"l":0,"b":0}
    )
    return fig

def plot_regional_distribution(df, year):
    """Boxplot of scores by Region."""
    df_year = df[df['Year'] == year]
    
    chart = alt.Chart(df_year).mark_boxplot(extent='min-max').encode(
        x=alt.X('Region', axis=alt.Axis(title='Region', labelAngle=-45, labelColor=COLOR_TEXT_MAIN, titleColor=COLOR_TEXT_MAIN)),
        y=alt.Y('Score', scale=alt.Scale(zero=False), axis=alt.Axis(title='Happiness Score', labelColor=COLOR_TEXT_MAIN, titleColor=COLOR_TEXT_MAIN)),
        color='Region'
    ).properties(
        title=f'Regional Distribution ({year})',
        background='rgba(0,0,0,0)'
    ).configure_axis(
        gridColor='#41444C',
        domainColor='#41444C'
    ).configure_legend(
        labelColor=COLOR_TEXT_MAIN,
        titleColor=COLOR_TEXT_MAIN
    )
    return chart

def plot_sunburst(df, year):
    """Plots a Sunburst chart of Region -> Country -> Score."""
    df_year = df[df['Year'] == year]
    
    # Sunburst needs non-negative values, data is safe
    fig = px.sunburst(
        df_year,
        path=['Region', 'Country'],
        values='Score',
        color='Score',
        color_continuous_scale='RdBu',
        title=f"Happiness Hierarchy ({year})"
    )
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=COLOR_TEXT_MAIN),
        margin={"r":0,"t":40,"l":0,"b":0}
    )
    return fig

def plot_radar_chart(df, years, selected_country):
    """Plots a Radar chart comparison for a country across 6 factors vs Global Avg."""
    
    # Filter for latest year if multiple
    target_year = max(years)
    df_year = df[df['Year'] == target_year]
    
    categories = ['GDP', 'Social_Support', 'Health', 'Freedom', 'Generosity', 'Corruption']
    
    # Normalize data for radar chart (Min-Max scaling for visualization)
    normalized_df = df_year.copy()
    for col in categories:
        min_val = normalized_df[col].min()
        max_val = normalized_df[col].max()
        if max_val - min_val > 0:
            normalized_df[col] = (normalized_df[col] - min_val) / (max_val - min_val)
        else:
            normalized_df[col] = 0
            
    # Get Global Average of normalized values
    global_avg = normalized_df[categories].mean().tolist()
    
    # Get Country values
    country_data = normalized_df[normalized_df['Country'] == selected_country]
    
    if country_data.empty:
        return None
        
    country_vals = country_data[categories].iloc[0].tolist()
    
    # Close the loop
    categories = [*categories, categories[0]]
    global_avg = [*global_avg, global_avg[0]]
    country_vals = [*country_vals, country_vals[0]]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=global_avg,
        theta=categories,
        fill='toself',
        name='Global Average',
        line_color='rgba(255, 255, 255, 0.5)'
    ))
    
    fig.add_trace(go.Scatterpolar(
        r=country_vals,
        theta=categories,
        fill='toself',
        name=selected_country,
        line_color='#FF4B4B'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1],
                gridcolor='#41444C',
                showticklabels=False
            ),
            bgcolor='rgba(0,0,0,0)'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color=COLOR_TEXT_MAIN),
        showlegend=True,
        title=f"Factor Analysis: {selected_country} vs Global (Normalized)"
    )
    
    return fig
