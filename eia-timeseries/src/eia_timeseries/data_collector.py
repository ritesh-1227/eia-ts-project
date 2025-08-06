import pandas as pd
from typing import Optional, Tuple
from .eia_client import fetch_eia_region_subba
from .weather_client import fetch_weather
from .config import REGIONS, RegionConfig

class EnergyWeatherCollector:
    """Collects and correlates energy and weather data for specific regions"""
    
    def __init__(self, region_key: str):
        if region_key not in REGIONS:
            raise ValueError(f"Region '{region_key}' not found. Available: {list(REGIONS.keys())}")
        
        self.region = REGIONS[region_key]
        self.region_key = region_key
    
    def collect_data(self, start_date: str, end_date: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Collect both EIA and weather data for the region"""
        print(f"Collecting data for {self.region.name}...")
        
        # Fetch EIA data
        print("Fetching EIA energy data...")
        eia_data = fetch_eia_region_subba(
            parent=self.region.parent,
            subba=self.region.subba,
            start_date=start_date,
            end_date=end_date
        )
        
        # Fetch weather data for the same geographic area
        print("Fetching weather data...")
        weather_data = fetch_weather(
            lat=self.region.lat,
            lon=self.region.lon,
            variables=["temperature_2m", "relative_humidity_2m", "wind_speed_10m", "shortwave_radiation"],
            past_days=7,  # Get more historical data
            forecast_days=0  # No forecast needed for analysis
        )
        
        return eia_data, weather_data
    
    def merge_datasets(self, eia_data: pd.DataFrame, weather_data: pd.DataFrame) -> pd.DataFrame:
        """Merge energy and weather data on timestamp"""
        if eia_data.empty or weather_data.empty:
            raise ValueError("Cannot merge empty datasets")
        
        # Ensure both have timestamp columns
        if 'timestamp' not in eia_data.columns or 'timestamp' not in weather_data.columns:
            raise ValueError("Both datasets must have 'timestamp' column")
        
        # Merge on timestamp (inner join to get overlapping time periods)
        merged = pd.merge(
            eia_data, 
            weather_data, 
            on='timestamp', 
            how='inner',
            suffixes=('_energy', '_weather')
        )
        
        # Add region information
        merged['region'] = self.region.name
        merged['region_key'] = self.region_key
        
        return merged
