
from app.data import hospitals_df
from app.constants import DARK_BLUE, LIGHT_GRAY

from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg


class VentilatorsWidget():

    def __init__(self) -> None:
        self.ui()

    def ui(self):

        # -------------------------
        # init ventilators widget
        # -------------------------
        labels = hospitals_df['name'].tolist()
        open_vents = hospitals_df['open_vents'].tolist()
        total_vents = hospitals_df['total_vents'].tolist()
        used_vents = [i - j for i, j in zip(total_vents, open_vents)]
        width = 0.5

        fig = plt.figure(figsize=(5, 5), dpi=100)
        ax = fig.add_subplot(1, 1, 1)
        ax.bar(labels, open_vents, width, label='Open Ventilators', color=DARK_BLUE)
        ax.bar(labels, used_vents, width, label='Occupied Ventilators', color=LIGHT_GRAY, bottom=open_vents)

        ax.set_ylabel('Number of Ventilators')
        ax.set_title('Ventilators')

        ax.legend()

        self.widget = FigureCanvasQTAgg(fig)