from eia_timeseries.eia_client import fetch_eia_region_subba
from eia_timeseries.weather_client import fetch_weather
from eia_timeseries.config import get_date_range

if __name__ == "__main__":
    start, end = get_date_range(2)

    print("Fetching EIA data...")
    eia_df = fetch_eia_region_subba(start_date=start, end_date=end)
    print(eia_df.head())

    print("Fetching Weather data...")
    weather_df = fetch_weather(36.1156, -97.0584)
    print(weather_df.head())
