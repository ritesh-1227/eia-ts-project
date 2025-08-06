from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import Dict, Tuple

EIA_API_KEY = "BcEw4qWYMFPbqckgkzBogUcX3pEbsRihqKHrtbWy"
EIA_BASE_URL = "https://api.eia.gov/v2"
WEATHER_BASE_URL = "https://api.open-meteo.com/v1/forecast"

# Default parameters for EIA query
DEFAULT_PARENT = "CISO"  # California ISO
DEFAULT_SUBBA = "PGAE"   # Pacific Gas & Electric sub-region

@dataclass
class RegionConfig:
    """Configuration for energy regions with their geographic centers"""
    name: str
    parent: str
    subba: str
    lat: float
    lon: float
    timezone: str

# Major US electricity regions with their approximate geographic centers
REGIONS = {
    "ciso_pgae": RegionConfig(
        name="California ISO - PG&E",
        parent="CISO",
        subba="PGAE", 
        lat=37.7749,  # San Francisco area
        lon=-122.4194,
        timezone="America/Los_Angeles"
    ),
    "ercot_cps": RegionConfig(
        name="ERCOT - CPS Energy",
        parent="ERCO",
        subba="CPLE",
        lat=29.4241,  # San Antonio
        lon=-98.4936,
        timezone="America/Chicago"
    ),
    "pjm_bge": RegionConfig(
        name="PJM - Baltimore Gas & Electric",
        parent="PJM",
        subba="BGE",
        lat=39.2904,  # Baltimore
        lon=-76.6122,
        timezone="America/New_York"
    ),
    "nyiso_zona": RegionConfig(
        name="NYISO - Zone A (NYC)",
        parent="NYIS",
        subba="ZONA",
        lat=40.7128,  # NYC
        lon=-74.0060,
        timezone="America/New_York"
    )
}

def get_date_range(days_back: int = 7) -> Tuple[str, str]:
    """Get date range for data fetching"""
    end = datetime.utcnow()
    start = end - timedelta(days=days_back)
    return start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d")