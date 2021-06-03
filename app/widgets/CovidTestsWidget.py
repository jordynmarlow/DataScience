
from app.data import hospitals_df
from app.constants import DARK_BLUE, LIGHT_BLUE

from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg


class CovidTestsWidget():

    def __init__(self) -> None:
        self.ui()

    def ui(self):

        # -------------------------
        # init tests widget
        # -------------------------
        labels = hospitals_df['name'].tolist()
        rapid_tests = hospitals_df['rapid_covid_tests'].tolist()
        lab_tests = hospitals_df['lab_covid_tests'].tolist()
        width = 0.5

        fig = plt.figure(figsize=(3, 5), dpi=100)
        ax = fig.add_subplot(1, 1, 1)
        ax.bar(labels, rapid_tests, width, label='Rapid COVID-19 Test Kits', color=LIGHT_BLUE)
        ax.bar(labels, lab_tests, width, label='Lab COVID-19 Test Kits', color=DARK_BLUE)

        ax.set_ylabel('Number of COVID-19 Tests')
        ax.set_title('COVID-19 Tests')

        ax.legend()

        self.widget = FigureCanvasQTAgg(fig)