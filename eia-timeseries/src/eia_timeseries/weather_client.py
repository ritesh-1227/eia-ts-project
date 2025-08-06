import requests
import pandas as pd
from .config import WEATHER_BASE_URL

def fetch_weather(lat, lon, variables=None, past_days=1, forecast_days=1):
    """
    Fetch weather data from Open-Meteo API
    
    Args:
        lat: Latitude
        lon: Longitude  
        variables: List of weather variables to fetch
        past_days: Number of past days to include
        forecast_days: Number of forecast days to include
    """
    # Default variables with correct Open-Meteo parameter names
    if variables is None:
        variables = [
            "temperature_2m",
            "relative_humidity_2m", 
            "wind_speed_10m",
            "shortwave_radiation"  # This is the correct parameter name for solar radiation
        ]
    
    # Validate and clean variables
    valid_variables = [
        "temperature_2m",
        "relative_humidity_2m",
        "wind_speed_10m", 
        "wind_direction_10m",
        "shortwave_radiation",
        "direct_radiation",
        "diffuse_radiation",
        "cloudcover",
        "pressure_msl",
        "surface_pressure",
        "precipitation",
        "weathercode"
    ]
    
    # Filter out invalid variables
    cleaned_variables = [var for var in variables if var in valid_variables]
    
    if not cleaned_variables:
        print(f"Warning: No valid variables found. Using defaults.")
        cleaned_variables = ["temperature_2m", "relative_humidity_2m"]
    
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": ",".join(cleaned_variables),
        "past_days": past_days,
        "forecast_days": forecast_days,
        "timezone": "auto"  # Automatically detect timezone
    }
    
    try:
        print(f"Fetching weather data for coordinates ({lat}, {lon})")
        print(f"Variables: {', '.join(cleaned_variables)}")
        
        resp = requests.get(WEATHER_BASE_URL, params=params)
        resp.raise_for_status()
        
        data = resp.json()
        
        if "error" in data and data["error"]:
            raise ValueError(f"Weather API error: {data.get('reason', 'Unknown error')}")
        
        hourly_data = data.get("hourly", {})
        if not hourly_data:
            raise ValueError("No hourly data returned from weather API")
        
        df = pd.DataFrame(hourly_data)
        
        if "time" in df.columns:
            df.rename(columns={"time": "timestamp"}, inplace=True)
            df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
        
        print(f"Successfully fetched {len(df)} weather records")
        return df
        
    except requests.exceptions.RequestException as e:
        print(f"Request error fetching weather data: {e}")
        return pd.DataFrame()
    except Exception as e:
        print(f"Error processing weather data: {e}")
        return pd.DataFrame()

# Test function to validate API parameters
def test_weather_api():
    """Test the weather API with sample coordinates"""
    # Test with San Francisco coordinates
    lat, lon = 37.7749, -122.4194
    
    print("Testing weather API...")
    df = fetch_weather(lat, lon, past_days=1, forecast_days=0)
    
    if not df.empty:
        print(f"Test successful! Retrieved {len(df)} records")
        print(f"Columns: {list(df.columns)}")
        print(f"Sample data:\n{df.head()}")
    else:
        print("Test failed - no data retrieved")
    
    return df

if __name__ == "__main__":
    test_weather_api()