# 🌍 World Happiness Report Dashboard

An attractive and comprehensive Streamlit dashboard analyzing World Happiness Report data from 2015-2019 with detailed visualizations and statistical insights.

## Features

### 📊 Dashboard Sections

1. **Top Countries**
   - Top 15 happiest countries
   - Bottom 15 countries
   - Detailed rankings with all factors

2. **Trends Over Time**
   - Score evolution with spline curves
   - Rank progression
   - Year-over-year changes
   - Selected country trends

3. **Factor Analysis**
   - Global factor contribution
   - Correlation analysis with happiness score
   - Scatter plots with trendlines
   - Factor comparison by year
   - Distribution analysis

4. **Regional Insights**
   - Top regions by average happiness
   - Regional statistics
   - Score distribution by region
   - Box plots showing variation

5. **Country Deep Dive**
   - Individual country analysis
   - Score and rank evolution
   - Radar chart comparing factors to global average
   - Historical factor values

6. **Statistical Analysis**
   - Score distribution histogram
   - Statistical summary (mean, median, std dev, etc.)
   - Year-over-year performance metrics
   - Growth leaders vs decliners
   - Correlation heatmap

### 🎨 Visual Features

- Interactive Plotly visualizations
- Custom color schemes (gradient-based)
- Responsive design for all screen sizes
- Real-time filtering by year and country
- Animated transitions and hover effects
- Professional styling with CSS customization

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Setup Steps

1. **Navigate to the project directory:**
   ```bash
   cd "d:\AI work\Dashboards\World Happy ratio"
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install required packages:**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Dashboard

1. **Make sure you're in the correct directory:**
   ```bash
   cd "d:\AI work\Dashboards\World Happy ratio"
   ```

2. **Run the Streamlit app:**
   ```bash
   streamlit run dashboard.py
   ```

3. **The dashboard will open in your default browser at:**
   ```
   http://localhost:8501
   ```

## Usage Guide

### Sidebar Filters
- **Select Year(s)**: Filter data by one or multiple years (2015-2019)
- **Select Country/Countries**: Choose specific countries for trend analysis
  - Default selection shows top performers: Finland, Denmark, Switzerland, Iceland, Netherlands

### Dashboard Navigation
- Use the tabs at the top to navigate between different analyses
- Hover over charts for detailed information
- Click and drag on charts to zoom, double-click to reset
- Use the download icon in chart corners to save visualizations

### Key Metrics
The main dashboard shows:
- Average Happiness Score across all selected data
- Highest and Lowest scores in the dataset
- Total countries analyzed
- Number of years covered

## Data Description

### Data Source
World Happiness Report (2015-2019)

### Key Metrics Included
- **Happiness Score**: Overall happiness ranking score
- **Rank**: Global ranking position
- **Economy (GDP per Capita)**: Economic factor contribution
- **Family**: Family support factor contribution
- **Health (Life Expectancy)**: Health and life expectancy contribution
- **Freedom**: Freedom to make life choices contribution
- **Trust (Government Corruption)**: Government trust factor
- **Generosity**: Generosity factor contribution
- **Dystopia Residual**: Unexplained portion

## Data Files
```
data/
├── 2015.csv
├── 2016.csv
├── 2017.csv
├── 2018.csv
└── 2019.csv
```

## Technical Stack

- **Framework**: Streamlit - Python web framework
- **Visualization**: Plotly - Interactive charting library
- **Data Processing**: Pandas & NumPy
- **Backend**: Python 3.8+

## Dashboard Insights

### What You Can Discover

1. **Geographic Patterns**
   - Western Europe consistently ranks highest
   - Regional happiness trends over time
   - Country-to-country variations

2. **Factor Relationships**
   - Economy has strong correlation with happiness
   - Family support is crucial
   - Freedom and trust show varied impact

3. **Temporal Trends**
   - Overall global happiness trajectory
   - Countries with improving/declining trends
   - Rank volatility over 5 years

4. **Outliers & Exceptions**
   - Countries outperforming economic indicators
   - Regions with unique happiness factors
   - Dramatic changes year-to-year

## Tips for Best Experience

1. **Start with Top Countries tab** - Get overview of happiest nations
2. **Use Trends Over Time** - Understand global happiness patterns
3. **Explore Factor Analysis** - Discover what drives happiness
4. **Deep Dive into Countries** - Analyze individual country stories
5. **Review Statistics** - Understand correlations and growth trends

## Performance Notes

- First load may take a few seconds due to data caching
- Subsequent interactions are instant due to Streamlit caching
- Charts are interactive - use zoom, pan, and hover for details

## Troubleshooting

### Issue: Port 8501 already in use
```bash
streamlit run dashboard.py --server.port 8502
```

### Issue: Missing data for some years
- This is expected - data standardization handles column variations across years
- Unknown regions are marked as "Unknown"

### Issue: Charts not displaying
- Clear browser cache
- Restart Streamlit: `Ctrl+C` then run `streamlit run dashboard.py` again

## Future Enhancements

- Add 2020-2023 data when available
- Include drill-down analysis by sub-regions
- Add predictive modeling for future trends
- Include demographic breakdowns
- Add data export functionality

## License

This dashboard uses publicly available World Happiness Report data.

## Support

For issues or suggestions, please ensure:
1. All data files are present in the `data/` directory
2. All packages in requirements.txt are installed
3. Python version is 3.8 or higher

---

**Happy Exploring! 🌍📊**
