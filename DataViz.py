import matplotlib, folium, sys, io, requests, json
import pandas as pd
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import QWebEngineView

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

matplotlib.use('Qt5Agg')

user_lat = 43.01272028760803
user_lon = -83.71256602748012

df_ind = 1

class DataViz(QMainWindow):
    def __init__(self):
        super().__init__()
        self.window_width, self.window_height = 1200, 800
        self.setMinimumSize(self.window_width, self.window_height)
        self.hospitals = pd.read_excel('sample_data.xlsx').set_index('name')
    
        # -------------------------
        # init map widget
        # -------------------------
        self.map = folium.Map(location=[user_lat, user_lon], tiles='Stamen Terrain', default_zoom_start=15)
        for index, row in self.hospitals.iterrows():
            folium.Marker(location=[row['lat'], row['lon']]).add_to(self.map)

        data = io.BytesIO()
        self.map.save(data, close_file=False)

        self.map_widget = QWebEngineView(self)
        self.map_widget.resize(300, 300)
        self.map_widget.move(5, 5)
        self.map_widget.setHtml(data.getvalue().decode())

        # -------------------------
        # init distance widget
        # -------------------------
        lon = self.hospitals.loc['Hurley Medical Center']['lon']
        lat = self.hospitals.loc['Hurley Medical Center']['lat']
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
        self.distance_widget.resize(300, 100)
        self.distance_widget.move(5, 305)

        # -------------------------
        # init capacity widget
        # -------------------------

        groupbox = QGroupBox(self)
        vlayout = QVBoxLayout()

        # data
        open_beds = self.hospitals['open_beds'][df_ind]
        total_beds = self.hospitals['total_beds'][df_ind]
        val = [open_beds, total_beds - open_beds]

        # append data and assign color
        val.append(sum(val))
        colors = ['gray', 'blue', 'white']

        # plot
        fig = plt.figure(figsize=(500, 500),dpi=100)
        ax = fig.add_subplot(1,1,1)
        ax.pie(val, colors=colors)
        ax.add_artist(plt.Circle((0, 0), 0.6, color='white'))
        
        fig.subplots_adjust(0,-0.75,1,1)

        static_canvas = FigureCanvasQTAgg(fig)

        vlayout.addWidget(static_canvas)

        groupbox.setLayout(vlayout)
        groupbox.resize(500, 250)
        groupbox.move(305, 305)

        self.setLayout(vlayout)

        # -------------------------
        # init helipad widget
        # -------------------------


        # -------------------------
        # init ventilators widget
        # -------------------------


        # -------------------------
        # init tests widget
        # -------------------------


        # -------------------------
        # init insurance widget
        # -------------------------


        # -------------------------
        # init staff widget
        # -------------------------





app = QApplication(sys.argv)
#app.setStyleSheet()
window = DataViz()
window.show()
sys.exit(app.exec_())

