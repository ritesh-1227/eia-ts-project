import requests
import pandas as pd
from .config import WEATHER_BASE_URL

def fetch_weather(lat, lon, variables=["temperature_2m", "relative_humidity_2m"],
                  past_days=1, forecast_days=1):
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": ",".join(variables),
        "past_days": past_days,
        "forecast_days": forecast_days
    }
    resp = requests.get(WEATHER_BASE_URL, params=params)
    resp.raise_for_status()
    data = resp.json().get("hourly", {})
    df = pd.DataFrame(data)
    if "time" in df.columns:
        df.rename(columns={"time": "timestamp"}, inplace=True)
        df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True)
    return df
