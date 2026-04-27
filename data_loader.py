import pandas as pd
import os

def load_and_clean_data(data_dir):
    """
    Loads, cleans, and merges World Happiness Report data from 2015 to 2019.
    Backfills 'Region' for years that are missing it (2017-2019) using 2015/2016 data.
    """
    
    # Define file paths
    files = {
        2015: os.path.join(data_dir, '2015.csv'),
        2016: os.path.join(data_dir, '2016.csv'),
        2017: os.path.join(data_dir, '2017.csv'),
        2018: os.path.join(data_dir, '2018.csv'),
        2019: os.path.join(data_dir, '2019.csv')
    }

    dfs = []
    
    # Column mapping to standardize names across years
    # Target columns: Country, Region, Rank, Score, GDP, Social_Support, Health, Freedom, Corruption, Generosity, Year
    
    column_maps = {
        2015: {
            'Country': 'Country',
            'Region': 'Region',
            'Happiness Rank': 'Rank',
            'Happiness Score': 'Score',
            'Economy (GDP per Capita)': 'GDP',
            'Family': 'Social_Support',
            'Health (Life Expectancy)': 'Health',
            'Freedom': 'Freedom',
            'Trust (Government Corruption)': 'Corruption',
            'Generosity': 'Generosity'
        },
        2016: {
            'Country': 'Country',
            'Region': 'Region',
            'Happiness Rank': 'Rank',
            'Happiness Score': 'Score',
            'Economy (GDP per Capita)': 'GDP',
            'Family': 'Social_Support',
            'Health (Life Expectancy)': 'Health',
            'Freedom': 'Freedom',
            'Trust (Government Corruption)': 'Corruption',
            'Generosity': 'Generosity'
        },
        2017: {
            'Country': 'Country',
            # 'Region' missing
            'Happiness.Rank': 'Rank',
            'Happiness.Score': 'Score',
            'Economy..GDP.per.Capita.': 'GDP',
            'Family': 'Social_Support',
            'Health..Life.Expectancy.': 'Health',
            'Freedom': 'Freedom',
            'Trust..Government.Corruption.': 'Corruption',
            'Generosity': 'Generosity'
        },
        2018: {
            'Country or region': 'Country',
            # 'Region' missing in this file despite column name suggesting otherwise (it's mostly country names in 'Country or region')
            'Overall rank': 'Rank',
            'Score': 'Score',
            'GDP per capita': 'GDP',
            'Social support': 'Social_Support',
            'Healthy life expectancy': 'Health',
            'Freedom to make life choices': 'Freedom',
            'Perceptions of corruption': 'Corruption',
            'Generosity': 'Generosity'
        },
        2019: {
            'Country or region': 'Country',
            # 'Region' missing
            'Overall rank': 'Rank',
            'Score': 'Score',
            'GDP per capita': 'GDP',
            'Social support': 'Social_Support',
            'Healthy life expectancy': 'Health',
            'Freedom to make life choices': 'Freedom',
            'Perceptions of corruption': 'Corruption',
            'Generosity': 'Generosity'
        }
    }

    # First pass: Load data and apply initial renaming
    temp_dfs = {}
    for year, file_path in files.items():
        if os.path.exists(file_path):
            df = pd.read_csv(file_path)
            
            # Apply renaming
            mapping = column_maps.get(year, {})
            df = df.rename(columns=mapping)
            
            # Keep only the standardized columns we care about
            cols_to_keep = list(set(mapping.values()))
            
            # If Region is in the dataframe (2015, 2016), keep it. 
            # Note: For 2017-2019 we mapped to standardized names but Region wasn't in the source map if it didn't exist.
            # actually we only put Region in the map if it existed.
            
            # We need to ensure we select existing columns
            existing_cols = [c for c in cols_to_keep if c in df.columns]
            df = df[existing_cols].copy()
            
            df['Year'] = year
            temp_dfs[year] = df
        else:
            print(f"Warning: File for {year} not found at {file_path}")

    # Build a Country -> Region mapping from 2015 and 2016 data
    region_map = {}
    for year in [2015, 2016]:
        if year in temp_dfs:
            if 'Region' in temp_dfs[year].columns:
                for idx, row in temp_dfs[year].iterrows():
                    region_map[row['Country']] = row['Region']

    # Manual fixes for countries that might have different names or appeared later
    # This is a basic manual patch for common discrepancies
    manual_patches = {
        'Taiwan Province of China': 'Eastern Asia',
        'Hong Kong S.A.R., China': 'Eastern Asia',
        'Trinidad & Tobago': 'Latin America and Caribbean',
        'Northern Cyprus': 'Western Europe', # Often grouped with Cyprus in these datasets geographically or politically distinct
        'North Macedonia': 'Central and Eastern Europe',
        'Gambia': 'Sub-Saharan Africa',
        'Namibia': 'Sub-Saharan Africa',
        'South Sudan': 'Sub-Saharan Africa',
    }
    region_map.update(manual_patches)

    # Second pass: Apply Region mapping and concatenation
    for year, df in temp_dfs.items():
        if 'Region' not in df.columns:
            df['Region'] = df['Country'].map(region_map)
            # Fill remaining unknowns
            df['Region'] = df['Region'].fillna('Other')
        
        dfs.append(df)

    final_df = pd.concat(dfs, ignore_index=True)
    
    # Final cleanup
    # Convert numeric columns to float, handling any non-numeric strings if strictly necessary (though datasets looked clean)
    numeric_cols = ['Score', 'GDP', 'Social_Support', 'Health', 'Freedom', 'Corruption', 'Generosity']
    for col in numeric_cols:
        if col in final_df.columns:
            final_df[col] = pd.to_numeric(final_df[col], errors='coerce')
    
    # Determine the 'previous_score' for alarming calculation? 
    # That might be better done in the app or a separate analysis step, but having the dataframe ready is key.
    
    return final_df

if __name__ == "__main__":
    # Test run
    data_dir = "d:/AI work/Dashboards/World Happy ratio/data"
    df = load_and_clean_data(data_dir)
    print("Data loaded successfully.")
    print(f"Total shape: {df.shape}")
    print(f"Columns: {df.columns.tolist()}")
    print(f"Years: {df['Year'].unique()}")
    print("Missing Regions check:")
    print(df[df['Region'] == 'Other']['Country'].unique())
