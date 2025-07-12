import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import date
from typing import List, Dict
from IPython.display import display

def update_graph(
    selected_date: date,
    niwa_clear_sky_hourly: Dict[date, List[Dict]],
    niwa_cloudy_sky_hourly: Dict[date, List[Dict]],
    uvi_5min: Dict[date, List[Dict]],
    uvi_scale: float,
    uvi_scale_upper: float
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
    # niwa_clear_sky_today = [
    #     item for item in niwa_clear_sky_hourly
    #     if item['datetime_nz'].date() == selected_date
    # ]
    # niwa_cloudy_sky_today = [
    #     item for item in niwa_cloudy_sky_hourly
    #     if item['datetime_nz'].date() == selected_date
    # ]
    # uvi_5min_today = [
    #     item for item in uvi_5min
    #     if item['datetime_nz'].date() == selected_date
    # ]

    niwa_clear_sky_today = niwa_clear_sky_hourly.get(selected_date, [])
    niwa_cloudy_sky_today = niwa_cloudy_sky_hourly.get(selected_date, [])
    uvi_5min_today = uvi_5min.get(selected_date, [])

    # Prepare data
    niwa_clear_sky_times = [item['datetime_nz'] for item in niwa_clear_sky_today]
    niwa_clear_sky_uvis = [float(item['uvi']) for item in niwa_clear_sky_today]

    niwa_cloudy_sky_times = [item['datetime_nz'] for item in niwa_cloudy_sky_today]
    niwa_cloudy_sky_uvis = [float(item['uvi']) for item in niwa_cloudy_sky_today]

    uvi_5min_times = [item['datetime_nz'] for item in uvi_5min_today]
    uvi_5min_uvis = [float(item['uvi']) for item in uvi_5min_today]

    # now scale the uvi values
    # We have two scale
    # if below 2 then scale by uvi_scale
    # if above 2 then we interpolate between uvi_scale and uvi_scale_upper based on the UVI value
    #  where 2 corresponse uvi_scale and 10 corresponds to uvi_scale_upper
    def scale_uvi(u, uvi_scale, uvi_scale_upper):
        if u < 2:
            return u * uvi_scale
        else:
            # Linear interpolation between uvi_scale and uvi_scale_upper
            # 2 -> uvi_scale, 10 -> uvi_scale_upper
            interp = uvi_scale + uvi_scale_upper * (u - 2) / (10 - 2)
            return u * interp

    uvi_5min_uvis = [scale_uvi(u, uvi_scale, uvi_scale_upper) for u in uvi_5min_uvis]

    # Re-create a new plot
    fig, ax = plt.subplots(figsize=(8, 3))
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
