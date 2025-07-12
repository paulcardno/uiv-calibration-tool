from collections import defaultdict
from datetime import date
from typing import List, Dict, Tuple


def find_unique_dates(
    niwa_clear_sky_hourly: List[Dict],
    uvi_5min: List[Dict]
) -> List[date]:
   """
   Extracts unique dates from the provided Niwa clear sky hourly data and UVI 5-minute data.

   Args:
      niwa_clear_sky_hourly (list): List of dicts with 'datetime_nz' keys.
      uvi_5min (list): List of dicts with 'datetime_nz' keys.

   Returns:
      list: Sorted list of unique dates (as datetime.date objects).
   """
   # Extract unique dates from the processed data
   unique_dates = set()

   # Add dates from Niwa clear sky data
   for item in niwa_clear_sky_hourly:
      unique_dates.add(item['datetime_nz'].date())

   # Add dates from Niwa cloudy sky data (if needed, assuming same dates as clear sky)
   # for item in niwa_cloudy_sky_hourly:
   #     unique_dates.add(item['datetime'].date())

   # Add dates from UVI 5-minute data
   for item in uvi_5min:
      unique_dates.add(item['datetime_nz'].date())

   # Convert the set of unique dates to a sorted list
   sorted_unique_dates = sorted(list(unique_dates))

   print("List of unique dates:")
   for date in sorted_unique_dates:
    print(f"- {date}")

   return sorted_unique_dates



def find_date_counts(
    niwa_clear_sky_hourly: List[Dict],
    niwa_cloudy_sky_hourly: List[Dict],
    uvi_5min: List[Dict],
    sorted_unique_dates: List[date]
) -> Tuple[List[date], List[int], List[int], List[int]]:
    """
    Counts the number of UVI data points for each unique date from the given datasets.

    Args:
        niwa_clear_sky_hourly (list): List of clear sky data dicts with 'datetime_nz' keys.
        niwa_cloudy_sky_hourly (list): List of cloudy sky data dicts with 'datetime_nz' keys.
        uvi_5min (list): List of 5-minute UVI data dicts with 'datetime_nz' keys.
        sorted_unique_dates (list): List of unique datetime.date objects.

    Returns:
        tuple: (dates, niwa_clear_counts, niwa_cloudy_counts, uvi_5min_counts)
            - dates: list of datetime.date
            - niwa_clear_counts: list of int
            - niwa_cloudy_counts: list of int
            - uvi_5min_counts: list of int
    """
    date_counts = defaultdict(lambda: {'niwa_clear': 0, 'niwa_cloudy': 0, 'uvi_5min': 0})

    for date in sorted_unique_dates:
        for item in niwa_clear_sky_hourly:
            if item['datetime_nz'].date() == date:
                date_counts[date]['niwa_clear'] += 1

        for item in niwa_cloudy_sky_hourly:
            if item['datetime_nz'].date() == date:
                date_counts[date]['niwa_cloudy'] += 1

        for item in uvi_5min:
            if item['datetime_nz'].date() == date:
                date_counts[date]['uvi_5min'] += 1

    # Prepare output
    dates = sorted(date_counts.keys())
    niwa_clear_counts = [date_counts[d]['niwa_clear'] for d in dates]
    niwa_cloudy_counts = [date_counts[d]['niwa_cloudy'] for d in dates]
    uvi_5min_counts = [date_counts[d]['uvi_5min'] for d in dates]

    return dates, niwa_clear_counts, niwa_cloudy_counts, uvi_5min_counts
