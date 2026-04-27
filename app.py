import streamlit as st
import pandas as pd
import utils
from data_loader import load_and_clean_data
import auth
import os

# Page config
st.set_page_config(
    page_title="World Happiness Analytics",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="collapsed" 
)

# Load Data
@st.cache_data
def get_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, 'data')
    return load_and_clean_data(data_dir)

def login_page():
    utils.apply_custom_style()
    
    # Background
    st.markdown(
        """
        <style>
        .stApp {
            background-image: url("assets/login_bg.png"); 
            background-size: cover;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        st.title("🔒 Secure Access")
        st.markdown("### World Happiness Analytics Dashboard")
        
        tab_login, tab_register = st.tabs(["Login", "Register"])
        
        with tab_login:
            username = st.text_input("Username", key="login_user")
            password = st.text_input("Password", type="password", key="login_pass")
            
            if st.button("Login", type="primary"):
                if auth.login_user(username, password):
                    st.session_state['authenticated'] = True
                    st.session_state['username'] = username
                    st.rerun()
                else:
                    st.error("Invalid username or password")
                    
        with tab_register:
            new_user = st.text_input("New Username", key="reg_user")
            new_pass = st.text_input("New Password", type="password", key="reg_pass")
            
            if st.button("Create Account"):
                success, msg = auth.register_user(new_user, new_pass)
                if success:
                    st.success(msg)
                else:
                    st.error(msg)
                    
def dashboard_page():
    utils.apply_custom_style()
    df = get_data()
    
    # Banner
    st.image("assets/banner_happiness.png", use_column_width=True)
    
    # Sidebar
    st.sidebar.title(f"👤 Welcome, {st.session_state.get('username', 'Guest')}")
    if st.sidebar.button("Logout"):
        st.session_state['authenticated'] = False
        st.rerun()
        
    st.sidebar.markdown("---")
    st.sidebar.title("🌍 Controls")
    
    # Year Selection
    years = sorted(df['Year'].unique())
    selected_year = st.sidebar.selectbox("Select Year", years, index=len(years)-1)
    
    # Region Filter
    all_regions = sorted(df['Region'].unique().tolist())
    selected_regions = st.sidebar.multiselect("Filter by Region", all_regions, default=all_regions)
    
    # Country Filter
    filtered_df = df[df['Region'].isin(selected_regions)]
    current_year_df = filtered_df[filtered_df['Year'] == selected_year]
    
    st.title(f"World Happiness Report {selected_year}")
    
    # Top KPI Row
    col1, col2, col3, col4 = st.columns(4)
    avg_score = current_year_df['Score'].mean()
    top_country = current_year_df.loc[current_year_df['Score'].idxmax()]['Country'] if not current_year_df.empty else "N/A"
    top_score = current_year_df['Score'].max() if not current_year_df.empty else 0
    lowest_country = current_year_df.loc[current_year_df['Score'].idxmin()]['Country'] if not current_year_df.empty else "N/A"
    
    with col1: st.metric("Global Average Score", f"{avg_score:.2f}")
    with col2: st.metric("Happiest Nation", top_country, f"{top_score:.2f}")
    with col3: st.metric("Least Happy", lowest_country, delta_color="inverse")
    with col4: st.metric("Countries Analyzed", len(current_year_df))

    # Tab Structure
    tab_overview, tab_deep_dive, tab_trends, tab_profile = st.tabs([
        "🌐 Global Overview", "🔍 Deep Analysis", "📉 Trends", "📍 Country Profile"
    ])
    
    with tab_overview:
        col_map, col_sun = st.columns([2, 1])
        with col_map:
            st.subheader("Interactive Global Map")
            st.plotly_chart(utils.plot_global_map(current_year_df, selected_year), width='stretch')
        with col_sun:
            st.subheader("Regional Hierarchy")
            st.plotly_chart(utils.plot_sunburst(current_year_df, selected_year), width='stretch')
            
        # Alarm Section (Keep it, user liked it)
        st.markdown("---")
        st.markdown('<p class="alarm-header">🚨 Critical Insights</p>', unsafe_allow_html=True)
        
        if selected_year > 2015:
            prev_year = selected_year - 1
            prev_df = df[df['Year'] == prev_year][['Country', 'Score']].rename(columns={'Score': 'Score_Prev'})
            merged_scores = pd.merge(current_year_df[['Country', 'Score', 'Corruption']], prev_df, on='Country', how='inner')
            merged_scores['Change'] = merged_scores['Score'] - merged_scores['Score_Prev']
            
            drops = merged_scores.sort_values('Change').head(5)
            
            col_a1, col_a2 = st.columns(2)
            with col_a1:
                st.markdown(f"**Biggest Drops ({prev_year}-{selected_year})**")
                st.dataframe(
                    drops[['Country', 'Score', 'Change']].style.format({"Score": "{:.2f}", "Change": "{:.2f}"})
                    .background_gradient(cmap='Reds_r', subset=['Change']), width='stretch'
                )
            with col_a2:
                st.markdown("**High Corruption / Low Trust**")
                lowest_trust = current_year_df.sort_values('Corruption').head(5)
                st.dataframe(
                     lowest_trust[['Country', 'Corruption', 'Score']].style.format({"Corruption": "{:.3f}", "Score": "{:.3f}"}),
                     width='stretch'
                )

    with tab_deep_dive:
        c1, c2 = st.columns(2)
        with c1:
            st.plotly_chart(utils.plot_factors_scatter(current_year_df, selected_year), width='stretch')
        with c2:
            st.altair_chart(utils.plot_regional_distribution(current_year_df, selected_year), width='stretch')

    with tab_trends:
        all_countries_list = sorted(df['Country'].unique().tolist())
        target_countries = st.multiselect("Compare Countries Trend", all_countries_list, default=all_countries_list[:5])
        if target_countries:
            st.altair_chart(utils.plot_yoy_trend(df, target_countries), width='stretch')

    with tab_profile:
        profile_country = st.selectbox("Select Country for Profile", all_countries_list)
        
        col_prof1, col_prof2 = st.columns([1, 2])
        
        with col_prof1:
            st.markdown(f"### {profile_country}")
            # Stats for this country
            c_data = current_year_df[current_year_df['Country'] == profile_country]
            if not c_data.empty:
                score = c_data.iloc[0]['Score']
                rank = c_data.iloc[0]['Rank']
                st.metric("Score", f"{score:.3f}")
                st.metric("Global Rank", f"#{rank}")
        
        with col_prof2:
            radar_chart = utils.plot_radar_chart(df, years, profile_country)
            if radar_chart:
                st.plotly_chart(radar_chart, width='stretch')
            else:
                st.info("Insufficient data for radar chart.")

def main():
    if auth.check_auth():
        dashboard_page()
    else:
        login_page()

if __name__ == "__main__":
    main()
