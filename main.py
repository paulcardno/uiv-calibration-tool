
from matplotlib import pyplot as plt
import streamlit as st
from jsonImporting import load_uvi_and_niwa
from adjustTimeZone import apply_nz_time_conversion
from UI.plotter import update_graph
from datetime import date
from UI.ui_functions import setup_navigation
from data_functions import create_data_by_date, find_unique_dates, find_date_counts
from UI.graph_controller import make_update_graph_fn
from persist_settings import load_uvi_settings, save_uvi_settings


def main():
   uvi_path = "data/studio_results_UVI_DoctorsPt_20250711_1026.json"
   niwa_path = "data/studio_results_niwa_DoctorsPt_20250711_1034.json"
   # Load settings at startup
   load_uvi_settings()
   # Set a default value if not already set
   if "uvi_scale" not in st.session_state:
      st.session_state.uvi_scale = 1.0
   if "uvi_scale_upper" not in st.session_state:
      st.session_state.uvi_scale_upper = 0.0

   uvi_5min, niwa_clear, niwa_cloudy = load_uvi_and_niwa(uvi_path, niwa_path)

   print(f"Loaded {len(uvi_5min)} UVI entries")
   print(f"Loaded {len(niwa_clear)} NIWA clear sky entries")
   print(f"Loaded {len(niwa_cloudy)} NIWA cloudy sky entries")

   # Data is loaded so now need to apply timezone conversion
   apply_nz_time_conversion(niwa_clear, niwa_cloudy, uvi_5min)

   unique_dates = find_unique_dates(niwa_clear, uvi_5min) 

   # first speed up is to group by date
   niwa_clear_by_date, niwa_cloudy_by_date, uvi_5min_by_date = create_data_by_date(niwa_clear, niwa_cloudy, uvi_5min)

   st.set_page_config(layout="wide")

   # UI controls
   # selected_date = st.date_input("Select date", unique_dates[0], min_value=min(unique_dates), max_value=max(unique_dates))
   # # Plot
   # st.write(f"Showing data for {selected_date}")
   
   # Session state for navigation
   if "date_index" not in st.session_state:
      st.session_state.date_index = 0

   # Add a slider to let the user change uvi_scale
   st.session_state.uvi_scale = st.slider("UVI Scale - Overall", min_value=0.1, max_value=2.0, value=st.session_state.uvi_scale, step=0.05)
   st.session_state.uvi_scale_upper = st.slider("UVI Scale Upper additional factor at starts at UVI2 and goes to 10 linear between, zero at UVI2", min_value=-1.0, max_value=1.0, value=st.session_state.uvi_scale_upper, step=0.05)



   # Navigation controls
   col1, col2, col3, col4 = st.columns([1, 1, 3, 7])
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
   with col4:
      if st.button("Save UVI Settings"):
         save_uvi_settings()
         st.success("Settings saved!")

   selected_date = unique_dates[st.session_state.date_index]
   # st.write(f"Showing data for {selected_date}")


   # Plot (use Plotly for best results)
   # fig = update_graph(selected_date, niwa_clear, niwa_cloudy, uvi_5min, st.session_state.uvi_scale)
   fig = update_graph(selected_date, niwa_clear_by_date, niwa_cloudy_by_date, uvi_5min_by_date, st.session_state.uvi_scale, st.session_state.uvi_scale_upper)
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
