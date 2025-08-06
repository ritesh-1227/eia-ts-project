"""Script for quick regional analysis"""
from eia_timeseries import EnergyWeatherCollector, EnergyWeatherAnalyzer, get_date_range, REGIONS

def analyze_region(region_key: str, days: int = 7):
    """Analyze a specific region"""
    if region_key not in REGIONS:
        print(f"Available regions: {list(REGIONS.keys())}")
        return
    
    start_date, end_date = get_date_range(days)
    
    collector = EnergyWeatherCollector(region_key)
    eia_data, weather_data = collector.collect_data(start_date, end_date)
    
    print(f"EIA data shape: {eia_data.shape}")
    print(f"Weather data shape: {weather_data.shape}")
    
    if not eia_data.empty and not weather_data.empty:
        merged = collector.merge_datasets(eia_data, weather_data)
        analyzer = EnergyWeatherAnalyzer(merged)
        print(analyzer.generate_report())
    else:
        print("No data available for analysis")

if __name__ == "__main__":
    # Example usage
    analyze_region("ciso_pgae", 3)  # California