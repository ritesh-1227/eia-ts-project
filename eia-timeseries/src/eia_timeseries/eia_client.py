import requests
import pandas as pd
from .config import EIA_API_KEY, EIA_BASE_URL, DEFAULT_PARENT, DEFAULT_SUBBA

def fetch_eia_region_subba(parent=DEFAULT_PARENT, subba=DEFAULT_SUBBA,
                           start_date=None, end_date=None, length=5000):
    url = f"{EIA_BASE_URL}/electricity/rto/region-sub-ba-data/data/"
    params = {
        "api_key": EIA_API_KEY,
        "frequency": "hourly",
        "data[0]": "value",
        "facets[parent][]": parent,
        "facets[subba][]": subba,
        "start": start_date,
        "end": end_date,
        "length": length,
        "offset": 0
    }
    all_rows = []
    while True:
        resp = requests.get(url, params=params)
        resp.raise_for_status()
        data = resp.json().get("response", {}).get("data", [])
        if not data:
            break
        all_rows.extend(data)
        if len(data) < length:
            break
        params["offset"] += length

    df = pd.DataFrame(all_rows)
    if not df.empty and "period" in df.columns:
        df["timestamp"] = pd.to_datetime(df["period"], utc=True)
    return df
