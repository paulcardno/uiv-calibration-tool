import json
from datetime import datetime, timezone
from typing import List, Dict, Optional, Tuple

def load_uvi_and_niwa(
    uvi_file_path: str,
    niwa_file_path: str
) -> Tuple[List[Dict], List[Dict], List[Dict]]:
    """
    Loads and processes UVI and NIWA forecast data from given JSON files.

    Args:
        uvi_file_path (str): Path to the UVI JSON data file.
        niwa_file_path (str): Path to the NIWA JSON forecast file.

    Returns:
        tuple: (uvi_5min, niwa_clear_sky_hourly, niwa_cloudy_sky_hourly)
            - uvi_5min: List of 5-minute UVI data dicts
            - niwa_clear_sky_hourly: List of hourly clear sky forecast dicts
            - niwa_cloudy_sky_hourly: List of hourly cloudy sky forecast dicts
    """

    def parse_datetime_z(dt_str: str) -> Optional[datetime]:
        try:
            return datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
        except ValueError:
            return None

    # Load UVI data
    try:
        with open(uvi_file_path, 'r') as f:
            data1_UVI = json.load(f)
    except Exception as e:
        print(f"Failed to load UVI file: {e}")
        return [], [], []

    try:
        with open(niwa_file_path, 'r') as f:
            data2_Niwa = json.load(f)
    except Exception as e:
        print(f"Failed to load NIWA file: {e}")
        return [], [], []

    # Process NIWA data
    niwa_clear_sky_hourly = []
    niwa_cloudy_sky_hourly = []

    for i, current_day_data in enumerate(data2_Niwa):
        current_day_updated_at = current_day_data.get('UpdatedAt')
        cutoff_time = None

        if i + 1 < len(data2_Niwa):
            next_day_data = data2_Niwa[i+1]
            try:
                forecast_data = json.loads(next_day_data.get('ForecastData', '{}'))
            except json.JSONDecodeError:
                forecast_data = {}

            for product in forecast_data.get("products", []):
                if product.get("name") == "clear_sky_uv_index" and product.get("values"):
                    first_next = product["values"][0]
                    if "time" in first_next:
                        cutoff_time = parse_datetime_z(first_next["time"])

        try:
            current_forecast_data = json.loads(current_day_data.get("ForecastData", '{}'))
        except json.JSONDecodeError:
            current_forecast_data = {}

        for product in current_forecast_data.get("products", []):
            name = product.get("name")
            for entry in product.get("values", []):
                dt = parse_datetime_z(entry.get("time", ""))
                if not dt or (cutoff_time and dt >= cutoff_time):
                    continue
                if name == "clear_sky_uv_index":
                    niwa_clear_sky_hourly.append({'datetime': dt, 'uvi': entry['value'], 'updatedAt': current_day_updated_at})
                elif name == "cloudy_sky_uv_index":
                    niwa_cloudy_sky_hourly.append({'datetime': dt, 'uvi': entry['value'], 'updatedAt': current_day_updated_at})

    # Process UVI data
    uvi_5min = []
    for item in data1_UVI:
        ts = item.get("Timestamp")
        val = item.get("Value")
        if not ts or val is None:
            continue
        if '.' in ts:
            ts = ts.split('.')[0]
        if ts.count(':') > 1:
            ts = ':'.join(ts.split(':')[:2])
        try:
            dt = datetime.strptime(ts, '%Y-%m-%d %H:%M').replace(tzinfo=timezone.utc)
            uvi_5min.append({'datetime': dt, 'uvi': val})
        except ValueError:
            print(f"Could not parse datetime from UVI data: {ts}")

    return uvi_5min, niwa_clear_sky_hourly, niwa_cloudy_sky_hourly
