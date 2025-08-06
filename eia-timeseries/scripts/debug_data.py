# scripts/debug_data.py
"""Debug script to inspect the merged dataset"""

import sys
from pathlib import Path
import pandas as pd

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from eia_timeseries.data_collector import EnergyWeatherCollector
from eia_timeseries.config import get_date_range

def debug_merged_data():
    """Debug the merged dataset to understand the structure"""
    print("=== Debugging Merged Dataset ===\n")
    
    try:
        # Collect data
        collector = EnergyWeatherCollector("ciso_pgae")
        start_date, end_date = get_date_range(2)  # Just 2 days to limit data
        
        print(f"Collecting data from {start_date} to {end_date}")
        eia_data, weather_data = collector.collect_data(start_date, end_date)
        
        print(f"\n--- EIA Data Info ---")
        print(f"Shape: {eia_data.shape}")
        print(f"Columns: {list(eia_data.columns)}")
        print(f"Data types:\n{eia_data.dtypes}")
        if not eia_data.empty:
            print(f"Sample data:\n{eia_data.head()}")
        
        print(f"\n--- Weather Data Info ---")
        print(f"Shape: {weather_data.shape}")
        print(f"Columns: {list(weather_data.columns)}")
        print(f"Data types:\n{weather_data.dtypes}")
        if not weather_data.empty:
            print(f"Sample data:\n{weather_data.head()}")
        
        if not eia_data.empty and not weather_data.empty:
            print(f"\n--- Merging Data ---")
            merged = collector.merge_datasets(eia_data, weather_data)
            
            print(f"Merged shape: {merged.shape}")
            print(f"Merged columns: {list(merged.columns)}")
            print(f"Merged data types:\n{merged.dtypes}")
            
            # Check for object columns that might cause issues
            object_cols = merged.select_dtypes(include=['object']).columns
            print(f"\nObject columns (potential issues): {list(object_cols)}")
            
            # Check numeric columns
            numeric_cols = merged.select_dtypes(include=['number']).columns
            print(f"Numeric columns: {list(numeric_cols)}")
            
            # Show sample of merged data
            print(f"\nSample merged data:")
            print(merged.head())
            
            # Check for null values
            print(f"\nNull values per column:")
            print(merged.isnull().sum())
            
            # Save debug data
            debug_file = "debug_merged_data.csv"
            merged.to_csv(debug_file, index=False)
            print(f"\nDebug data saved to: {debug_file}")
            
            return merged
        else:
            print("Cannot merge - one or both datasets are empty")
            return None
            
    except Exception as e:
        print(f"Error during debugging: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    debug_merged_data()