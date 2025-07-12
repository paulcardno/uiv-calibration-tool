import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import date
from typing import List, Dict
from IPython.display import display

def update_graph(
    selected_date: date,
    niwa_clear_sky_hourly: List[Dict],
    niwa_cloudy_sky_hourly: List[Dict],
    uvi_5min: List[Dict]
) -> None:
    """
    Filters data for the selected date and re-plots everything cleanly.

    Args:
        selected_date (date): The date to plot data for.
        niwa_clear_sky_hourly (List[Dict]): Clear sky forecast data.
        niwa_cloudy_sky_hourly (List[Dict]): Cloudy sky forecast data.
        uvi_5min (List[Dict]): Actual UVI 5-minute readings.
    """
    if selected_date is None:
        print("No data available for this date.")
        return

    # Filter data
    niwa_clear_sky_today = [
        item for item in niwa_clear_sky_hourly
        if item['datetime_nz'].date() == selected_date
    ]
    niwa_cloudy_sky_today = [
        item for item in niwa_cloudy_sky_hourly
        if item['datetime_nz'].date() == selected_date
    ]
    uvi_5min_today = [
        item for item in uvi_5min
        if item['datetime_nz'].date() == selected_date
    ]

    # Prepare data
    niwa_clear_sky_times = [item['datetime_nz'] for item in niwa_clear_sky_today]
    niwa_clear_sky_uvis = [float(item['uvi']) for item in niwa_clear_sky_today]

    niwa_cloudy_sky_times = [item['datetime_nz'] for item in niwa_cloudy_sky_today]
    niwa_cloudy_sky_uvis = [float(item['uvi']) for item in niwa_cloudy_sky_today]

    uvi_5min_times = [item['datetime_nz'] for item in uvi_5min_today]
    uvi_5min_uvis = [float(item['uvi']) for item in uvi_5min_today]

    # Re-create a new plot
    fig, ax = plt.subplots(figsize=(15, 7))
    ax.plot(niwa_clear_sky_times, niwa_clear_sky_uvis, label='Niwa Clear Sky', marker='o', linestyle='-')
    ax.plot(niwa_cloudy_sky_times, niwa_cloudy_sky_uvis, label='Niwa Cloudy Sky', marker='x', linestyle='--')
    ax.plot(uvi_5min_times, uvi_5min_uvis, label='UVI 5-minute', marker='.', linestyle='')

    ax.set_xlabel('Time (NZ Local Time)')
    ax.set_ylabel('UVI Value')
    ax.set_title(f'UVI Data for {selected_date}')
    ax.legend()
    ax.grid(True)

    ax.xaxis.set_major_locator(mdates.HourLocator(interval=1))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    plt.xticks(rotation=45)

    plt.tight_layout()
    # display(fig)
    # # plt.show()
    # plt.close(fig)  # Close the figure to free memory
    return fig
