
from app.data import hospitals_df
from app.constants import DARK_BLUE, df_ind

from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg


class StaffWidget():

    def __init__(self) -> None:
        self.ui()

    def ui(self):

        # -------------------------
        # init staff widget
        # -------------------------
        labels = 12 * [''] # use this to store time
        staff = 12 * [0]
        staff[-1] = hospitals_df.iloc[df_ind]['staff']
        fig = plt.figure(figsize=(1, 5), dpi=100)
        ax = fig.add_subplot(1, 1, 1)
        ax.plot(labels, staff, color=DARK_BLUE)

        ax.set_ylabel('Time')
        ax.set_title('Available Staff')

        self.widget = FigureCanvasQTAgg(fig)
