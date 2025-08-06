# scripts/test_apis.py
"""Test script to verify both EIA and weather APIs are working"""

import sys
from pathlib import Path

# Add src to path so we can import our modules
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from eia_timeseries.eia_client import fetch_eia_region_subba
from eia_timeseries.weather_client import fetch_weather, test_weather_api
from eia_timeseries.config import get_date_range, REGIONS

def test_eia_api():
    """Test EIA API"""
    print("=== Testing EIA API ===")
    start_date, end_date = get_date_range(2)  # Last 2 days
    
    try:
        # Test with California region
        region = REGIONS["ciso_pgae"]
        df = fetch_eia_region_subba(
            parent=region.parent,
            subba=region.subba,
            start_date=start_date,
            end_date=end_date,
            length=100  # Limit records for testing
        )
        
        if not df.empty:
            print(f"✅ EIA API test successful! Retrieved {len(df)} records")
            print(f"Columns: {list(df.columns)}")
            print(f"Date range: {df['timestamp'].min()} to {df['timestamp'].max()}")
            return True
        else:
            print("❌ EIA API test failed - no data retrieved")
            return False
            
    except Exception as e:
        print(f"❌ EIA API test failed with error: {e}")
        return False

def test_weather_api_simple():
    """Test weather API with simple parameters"""
    print("\n=== Testing Weather API ===")
    
    try:
        # Test with San Francisco coordinates (California region)
        region = REGIONS["ciso_pgae"]
        df = fetch_weather(
            lat=region.lat,
            lon=region.lon,
            variables=["temperature_2m", "relative_humidity_2m"],  # Simple variables
            past_days=1,
            forecast_days=0
        )
        
        if not df.empty:
            print(f"✅ Weather API test successful! Retrieved {len(df)} records")
            print(f"Columns: {list(df.columns)}")
            return True
        else:
            print("❌ Weather API test failed - no data retrieved")
            return False
            
    except Exception as e:
        print(f"❌ Weather API test failed with error: {e}")
        return False

def test_full_integration():
    """Test the full integration"""
    print("\n=== Testing Full Integration ===")
    
    try:
        from eia_timeseries.data_collector import EnergyWeatherCollector
        
        collector = EnergyWeatherCollector("ciso_pgae")
        start_date, end_date = get_date_range(1)  # Just 1 day for testing
        
        eia_data, weather_data = collector.collect_data(start_date, end_date)
        
        if not eia_data.empty and not weather_data.empty:
            merged = collector.merge_datasets(eia_data, weather_data)
            print(f"✅ Integration test successful!")
            print(f"EIA records: {len(eia_data)}")
            print(f"Weather records: {len(weather_data)}")
            print(f"Merged records: {len(merged)}")
            return True
        else:
            print("❌ Integration test failed - missing data")
            print(f"EIA data empty: {eia_data.empty}")
            print(f"Weather data empty: {weather_data.empty}")
            return False
            
    except Exception as e:
        print(f"❌ Integration test failed with error: {e}")
        return False

if __name__ == "__main__":
    print("Running API tests...\n")
    
    eia_ok = test_eia_api()
    weather_ok = test_weather_api_simple()
    
    if eia_ok and weather_ok:
        integration_ok = test_full_integration()
        if integration_ok:
            print("\n🎉 All tests passed! Your setup is working correctly.")
        else:
            print("\n⚠️  APIs work individually but integration failed.")
    else:
        print("\n❌ Some API tests failed. Check your configuration.")
        if not eia_ok:
            print("   - EIA API issue (check API key)")
        if not weather_ok:
            print("   - Weather API issue (check internet connection)")