

from UI.plotter import update_graph

def make_update_graph_fn(niwa_clear, niwa_cloudy, uvi_5min):
    def updateGraphForDate(selected_date):
        update_graph(selected_date, niwa_clear, niwa_cloudy, uvi_5min)
    return updateGraphForDate