
from matplotlib import pyplot as plt
import streamlit as st
from jsonImporting import load_uvi_and_niwa
from adjustTimeZone import apply_nz_time_conversion
from UI.plotter import update_graph
from datetime import date
from UI.ui_functions import setup_navigation
from data_functions import find_unique_dates, find_date_counts
from UI.graph_controller import make_update_graph_fn


def main():
   uvi_path = "data/studio_results_UVI_DoctorsPt_20250711_1026.json"
   niwa_path = "data/studio_results_niwa_DoctorsPt_20250711_1034.json"

   uvi_5min, niwa_clear, niwa_cloudy = load_uvi_and_niwa(uvi_path, niwa_path)

   print(f"Loaded {len(uvi_5min)} UVI entries")
   print(f"Loaded {len(niwa_clear)} NIWA clear sky entries")
   print(f"Loaded {len(niwa_cloudy)} NIWA cloudy sky entries")

   # Data is loaded so now need to apply timezone conversion
   apply_nz_time_conversion(niwa_clear, niwa_cloudy, uvi_5min)

   unique_dates = find_unique_dates(niwa_clear, uvi_5min) 

   # UI controls
   selected_date = st.date_input("Select date", unique_dates[0], min_value=min(unique_dates), max_value=max(unique_dates))
   # Plot
   st.write(f"Showing data for {selected_date}")
   
   # Session state for navigation
   if "date_index" not in st.session_state:
      st.session_state.date_index = 0

   # Navigation controls
   col1, col2, col3 = st.columns([1, 1, 3])
   with col1:
      if st.button("Previous Day") and st.session_state.date_index > 0:
         st.session_state.date_index -= 1
   with col2:
      if st.button("Next Day") and st.session_state.date_index < len(unique_dates) - 1:
         st.session_state.date_index += 1
   with col3:
      picked_date = st.date_input(
         "Jump to Date",
         unique_dates[st.session_state.date_index],
         min_value=min(unique_dates),
         max_value=max(unique_dates)
      )
      # Update index if date picker is used
      if picked_date in unique_dates:
         st.session_state.date_index = unique_dates.index(picked_date)

   selected_date = unique_dates[st.session_state.date_index]
   st.write(f"Showing data for {selected_date}")

   # Plot (use Plotly for best results)
   fig = update_graph(selected_date, niwa_clear, niwa_cloudy, uvi_5min)
   st.pyplot(fig)
   plt.close(fig)  # This is the correct place to close the figure

   # update_graph_fn = make_update_graph_fn(niwa_clear, niwa_cloudy, uvi_5min)
   # setup_navigation(unique_dates, update_graph_fn)

   # # Now display the corrected data on the plotter
   # # selected_date = date(2025, 4, 23)  # Example date for testing
   # # update_graph(selected_date, niwa_clear, niwa_cloudy, uvi_5min)
   # input("Press Enter to exit...")
      

if __name__ == "__main__":
    main()
