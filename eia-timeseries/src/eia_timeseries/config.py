from datetime import datetime, timedelta

EIA_API_KEY = "BcEw4qWYMFPbqckgkzBogUcX3pEbsRihqKHrtbWy"  # get one from https://www.eia.gov/opendata/register.php
EIA_BASE_URL = "https://api.eia.gov/v2"
DEFAULT_PARENT = "CISO"
DEFAULT_SUBBA = "PGAE"

WEATHER_BASE_URL = "https://api.open-meteo.com/v1/forecast"

def get_date_range(days_back=2):
    end = datetime.utcnow()
    start = end - timedelta(days=days_back)
    return start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d")
