import ipywidgets as widgets
from IPython.display import display, clear_output
from datetime import date

# These will need to be set externally
sorted_unique_dates = []
currentlySelectedDate = None
previous_button = widgets.Button(description="Previous Day")
next_button = widgets.Button(description="Next Day")
date_picker = widgets.DatePicker(description='Jump to Date:', disabled=False)


def setup_navigation(unique_dates: list, update_graph_fn):
    global sorted_unique_dates, currentlySelectedDate
    sorted_unique_dates = unique_dates

    if sorted_unique_dates:
        currentlySelectedDate = sorted_unique_dates[1] if len(sorted_unique_dates) > 1 else sorted_unique_dates[0]
        print(f"Currently selected date: {currentlySelectedDate}")
    else:
        currentlySelectedDate = None
        print("No unique dates found in the data.")
        return

    def update_ui(date):
        clear_output(wait=True)
        navigation_box = widgets.VBox([previous_button, next_button, date_picker])
        display(navigation_box)
        update_graph_fn(date)

    def on_previous_button_clicked(b):
        current_index = sorted_unique_dates.index(currentlySelectedDate)
        if current_index > 0:
            currentlySelectedDate = sorted_unique_dates[current_index - 1]
            update_ui(currentlySelectedDate)
            previous_button.disabled = (currentlySelectedDate == sorted_unique_dates[0])
            next_button.disabled = False

    def on_next_button_clicked(b):
        current_index = sorted_unique_dates.index(currentlySelectedDate)
        if current_index < len(sorted_unique_dates) - 1:
            currentlySelectedDate = sorted_unique_dates[current_index + 1]
            update_ui(currentlySelectedDate)
            next_button.disabled = (currentlySelectedDate == sorted_unique_dates[-1])
            previous_button.disabled = False

    def on_date_selected(change):
        if change['new'] in sorted_unique_dates:
            currentlySelectedDate = change['new']
            update_ui(currentlySelectedDate)
            previous_button.disabled = (currentlySelectedDate == sorted_unique_dates[0])
            next_button.disabled = (currentlySelectedDate == sorted_unique_dates[-1])
        else:
            print(f"No data available for {change['new']}")

    previous_button.on_click(on_previous_button_clicked)
    next_button.on_click(on_next_button_clicked)
    date_picker.observe(on_date_selected, names='value')

    previous_button.disabled = (currentlySelectedDate == sorted_unique_dates[0])
    next_button.disabled = (currentlySelectedDate == sorted_unique_dates[-1])

    # Initial display
    # navigation_box = widgets.VBox([previous_button, next_button, date_picker])
    # display(navigation_box)
    # update_graph_fn(currentlySelectedDate)

    update_ui(currentlySelectedDate)
