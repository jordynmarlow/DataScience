import matplotlib, folium, sys, io, requests, json, operator, time
import pandas as pd
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import QWebEngineView

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

matplotlib.use('Qt5Agg')

# -------------------------
# constants
# -------------------------
PURPLE = '#9868d4'
DARK_BLUE = '#68a0e3'
LIGHT_BLUE = '#88d5eb'
GREEN = '#66d195'
LIGHT_GRAY = '#e0e0e0'

user_lat = 43.01272028760803
user_lon = -83.71256602748012

df_ind = 1

class DataViz(QMainWindow):
    def __init__(self):
        super().__init__()
        self.window_width, self.window_height = 1200, 800
        self.setMinimumSize(self.window_width, self.window_height)
        self.showMaximized()
        self.window_width, self.window_height = self.width(), self.height()
        self.hospitals = pd.read_excel('sample_data.xlsx')

        # --------------------------------------------------
        # main horizontal layout w/three columns
        # --------------------------------------------------
        self.hbox_main = QGroupBox(self)
        hlayout_main = QHBoxLayout()

        # --------------------------------------------------
        # left col w/map and distance widgets
        # --------------------------------------------------
        self.vbox_left = QGroupBox(self)
        vlayout_left = QVBoxLayout()
        self.vbox_left.setLayout(vlayout_left)
        # self.vbox_left.resize(self.window_width/3, self.window_height)
        #self.vbox_left.move(0, 0)
        
        # add column to main horizontal layout
        hlayout_main.addWidget(self.vbox_left)

        # --------------------------------------------------
        # center col w/staff, vents, and test widgets
        # --------------------------------------------------
        self.vbox_center = QGroupBox(self)
        vlayout_center = QVBoxLayout()
        self.vbox_center.setLayout(vlayout_center)
        # self.vbox_center.resize(self.window_width/3, self.window_height)
        #self.vbox_center.move(300, 0)
        
        # add column to main horizontal layout
        hlayout_main.addWidget(self.vbox_center)

        # --------------------------------------------------
        # right col w/capacity, insurance, helipad widgets
        # --------------------------------------------------
        self.vbox_right = QGroupBox(self)
        vlayout_right = QVBoxLayout()
        self.vbox_right.setLayout(vlayout_right)
        # self.vbox_right.resize(self.window_width/3, self.window_height)
        #self.vbox_right.move(800, 0)
        
        # add column to main horizontal layout
        hlayout_main.addWidget(self.vbox_right)


        self.hbox_main.setLayout(hlayout_main)
        self.setCentralWidget(self.hbox_main)


        # -------------------------
        # init map widget
        # -------------------------
        self.map = folium.Map(location=[user_lat, user_lon], tiles='Stamen Terrain', default_zoom_start=15)
        for index, row in self.hospitals.iterrows():
            folium.Marker(location=[row['lat'], row['lon']]).add_to(self.map)

        data = io.BytesIO()
        self.map.save(data, close_file=False)

        self.map_widget = QWebEngineView(self)
        self.map_widget.resize(10, 10)
        self.map_widget.move(5, 5)
        self.map_widget.setHtml(data.getvalue().decode())

        vlayout_left.addWidget(self.map_widget)


        # -------------------------
        # init distance widget
        # -------------------------
        lon = self.hospitals.iloc[df_ind]['lon']
        lat = self.hospitals.iloc[df_ind]['lat']
        r = requests.get(f"http://router.project-osrm.org/route/v1/driving/{user_lon},{user_lat};{lon},{lat}?overview=false""")
        route = json.loads(r.content).get("routes")[0]


        self.distance_widget = QGroupBox(self)
        hlayout = QHBoxLayout()

        distance_mi = str(round(route["legs"][0]["distance"] / 1609))
        self.distance = QLabel(distance_mi, self)
        hlayout.addWidget(self.distance)

        distance_lbl = QLabel('miles\naway', self)
        hlayout.addWidget(distance_lbl)

        duration_min = str(round(route["legs"][0]["duration"] / 60))
        self.duration = QLabel(duration_min, self)
        hlayout.addWidget(self.duration)

        duration_lbl = QLabel('minutes\naway', self)
        hlayout.addWidget(duration_lbl)

        self.distance_widget.setLayout(hlayout)
        self.distance_widget.resize(10, 10)
        self.distance_widget.move(5, 305)

        vlayout_left.addWidget(self.distance_widget)


        # -------------------------
        # init capacity widget
        # -------------------------

        # data
        open_beds = self.hospitals.iloc[df_ind]['open_beds']
        total_beds = self.hospitals.iloc[df_ind]['total_beds']
        val = [open_beds, total_beds - open_beds]

        # append data and assign color
        val.append(sum(val))
        colors = [LIGHT_GRAY, DARK_BLUE, 'white']

        # plot
        fig = plt.figure(figsize=(10, 10), dpi=100)
        ax = fig.add_subplot(1, 1, 1)
        ax.pie(val, colors=colors)
        ax.add_artist(plt.Circle((0, 0), 0.6, color='white'))
        
        fig.subplots_adjust(0, -0.75, 1, 1)

        static_canvas = FigureCanvasQTAgg(fig)

        vlayout_right.addWidget(static_canvas)


        # -------------------------
        # init helipad widget
        # -------------------------
        self.helipad_widget = QGroupBox(self)
        hlayout_helipad = QHBoxLayout()

        helipad_count = self.hospitals.iloc[df_ind]['helipads']
        self.helipads = QLabel(str(helipad_count), self)
        hlayout_helipad.addWidget(self.helipads)

        lbl = 'helipad' if helipad_count == 1 else 'helipads'
        helipad_lbl = QLabel(lbl, self)
        hlayout_helipad.addWidget(helipad_lbl)

        self.helipad_widget.setLayout(hlayout_helipad)
        self.helipad_widget.resize(10, 10)
        self.helipad_widget.move(5, 305)

        vlayout_left.addWidget(self.helipad_widget)


        # -------------------------
        # init staff widget
        # -------------------------
        labels = 12 * [''] # use this to store time
        staff = 12 * [0]
        staff[-1] = self.hospitals.iloc[df_ind]['staff']
        fig = plt.figure(figsize=(20, 10), dpi=100)
        ax = fig.add_subplot(1, 1, 1)
        ax.plot(labels, staff, color=DARK_BLUE)

        ax.set_ylabel('Time')
        ax.set_title('Available Staff')

        vlayout_center.addWidget(FigureCanvasQTAgg(fig))


        # --------------------------------------------------
        # bottom horizontal layout w/ vents, tests widgets
        # --------------------------------------------------
        self.hbox_bottom = QGroupBox(self)
        hlayout_bottom = QHBoxLayout()
        self.hbox_bottom.setLayout(hlayout_bottom)
        self.hbox_bottom.resize(300, self.window_height / 2)
        #self.hbox_bottom.move(5, self.window_height / 2)
        
        # add column to main horizontal layout
        vlayout_center.addWidget(self.hbox_bottom)


        # -------------------------
        # init ventilators widget
        # -------------------------
        labels = self.hospitals['name'].tolist()
        open_vents = self.hospitals['open_vents'].tolist()
        total_vents = self.hospitals['total_vents'].tolist()
        used_vents = [i - j for i, j in zip(total_vents, open_vents)]
        width = 0.5

        fig = plt.figure(figsize=(10, 10), dpi=100)
        ax = fig.add_subplot(1, 1, 1)
        ax.bar(labels, open_vents, width, label='Open Ventilators', color=DARK_BLUE)
        ax.bar(labels, used_vents, width, label='Occupied Ventilators', color=LIGHT_GRAY, bottom=open_vents)

        ax.set_ylabel('Number of Ventilators')
        ax.set_title('Ventilators')

        ax.legend()

        hlayout_bottom.addWidget(FigureCanvasQTAgg(fig))


        # -------------------------
        # init tests widget
        # -------------------------
        labels = self.hospitals['name'].tolist()
        rapid_tests = self.hospitals['rapid_covid_tests'].tolist()
        lab_tests = self.hospitals['lab_covid_tests'].tolist()
        width = 0.5

        fig = plt.figure(figsize=(10, 10), dpi=100)
        ax = fig.add_subplot(1, 1, 1)
        ax.barh(labels, rapid_tests, width, label='Rapid COVID-19 Test Kits', color=LIGHT_BLUE)
        ax.barh(labels, lab_tests, width, label='Lab COVID-19 Test Kits', color=DARK_BLUE)

        ax.set_xlabel('Number of COVID-19 Tests')
        ax.set_title('COVID-19 Tests')

        ax.legend()

        hlayout_bottom.addWidget(FigureCanvasQTAgg(fig))


        # -------------------------
        # init insurance widget
        # -------------------------
        self.insurance_widget = QListWidget(self)
        insurances = self.hospitals.iloc[df_ind]['insurance'].split(',')
        for name in insurances:
            self.insurance_widget.addItem(QListWidgetItem(name))
        scroll_bar = QScrollBar(self)
        #scroll_bar.setStyleSheet()
        self.insurance_widget.setVerticalScrollBar(scroll_bar)

        vlayout_right.addWidget(self.insurance_widget)

        

app = QApplication(sys.argv)
#app.setStyleSheet()
window = DataViz()
window.show()
sys.exit(app.exec_())

