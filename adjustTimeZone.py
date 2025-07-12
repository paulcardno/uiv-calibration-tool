from datetime import datetime, timezone, timedelta
from typing import List, Dict

# Define the New Zealand Timezone (NZT as UTC+12)
nz_timezone = timezone(timedelta(hours=12))

def to_nz_local_time(utc_dt_object: datetime) -> datetime:
    """
    Converts a UTC datetime object to New Zealand local time (UTC+12).

    Args:
        utc_dt_object (datetime): A datetime object in UTC or naive.

    Returns:
        datetime: A timezone-aware datetime object in NZ local time.
    """
    if utc_dt_object.tzinfo is None:
        utc_dt_object = utc_dt_object.replace(tzinfo=timezone.utc)
    elif utc_dt_object.tzinfo != timezone.utc:
        utc_dt_object = utc_dt_object.astimezone(timezone.utc)

    return utc_dt_object.astimezone(nz_timezone)

def apply_nz_time_conversion(
    niwa_clear_sky_hourly: List[Dict],
    niwa_cloudy_sky_hourly: List[Dict],
    uvi_5min: List[Dict]
) -> None:
    """
    Applies NZ timezone conversion to datetime entries in the UVI and NIWA datasets.

    Adds a new 'datetime_nz' field to each entry with the converted time.

    Args:
        niwa_clear_sky_hourly (List[Dict]): Clear sky forecast data.
        niwa_cloudy_sky_hourly (List[Dict]): Cloudy sky forecast data.
        uvi_5min (List[Dict]): Actual UVI 5-minute data.
    """
    for entry in niwa_clear_sky_hourly:
        if 'datetime' in entry and isinstance(entry['datetime'], datetime):
            entry['datetime_nz'] = to_nz_local_time(entry['datetime'])
            entry['datetime_nz_date'] = entry['datetime_nz'].date()  # Add date for easier filtering

    for entry in niwa_cloudy_sky_hourly:
        if 'datetime' in entry and isinstance(entry['datetime'], datetime):
            entry['datetime_nz'] = to_nz_local_time(entry['datetime'])
            entry['datetime_nz_date'] = entry['datetime_nz'].date()  # Add date for easier filtering

    for entry in uvi_5min:
        if 'datetime' in entry and isinstance(entry['datetime'], datetime):
            entry['datetime_nz'] = to_nz_local_time(entry['datetime'])
            entry['datetime_nz_date'] = entry['datetime_nz'].date()  # Add date for easier filtering
