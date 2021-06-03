
from app.constants import df_ind, LIGHT_GRAY, DARK_BLUE
from app.data import hospitals_df

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import matplotlib.pyplot as plt

# --------------------------------------------------------------------------
# Canvas' are weird in Qt; that's why this class does not extend QWidget, 
# rather it sets the widget instance varible to the canvas.
# --------------------------------------------------------------------------

class BedCapacityWidget():

    def __init__(self) -> None:
        self.ui()

    def ui(self):
        # -------------------------
        # init capacity widget
        # -------------------------

        # data
        open_beds = hospitals_df.iloc[df_ind]['open_beds']
        total_beds = hospitals_df.iloc[df_ind]['total_beds']
        val = [open_beds, total_beds - open_beds]

        # append data and assign color
        val.append(sum(val))
        colors = [LIGHT_GRAY, DARK_BLUE, 'white']

        # plot
        fig = plt.figure(figsize=(4, 5), dpi=100)
        ax = fig.add_subplot(1, 1, 1)
        ax.pie(val, colors=colors)
        ax.add_artist(plt.Circle((0, 0), 0.6, color='white'))
        
        fig.subplots_adjust(0, -0.75, 1, 1)

        static_canvas = FigureCanvasQTAgg(fig)

        self.widget = static_canvas
