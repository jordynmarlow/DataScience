import matplotlib, folium, sys, io, requests, json
import pandas as pd
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import QWebEngineView

user_lat = 43.01272028760803
user_lon = -83.71256602748012

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
        layout = QHBoxLayout()

        distance_mi = str(round(route["legs"][0]["distance"] / 1609))
        self.distance = QLabel(distance_mi, self)
        layout.addWidget(self.distance)

        distance_lbl = QLabel('miles\naway', self)
        layout.addWidget(distance_lbl)

        duration_min = str(round(route["legs"][0]["duration"] / 60))
        self.duration = QLabel(duration_min, self)
        layout.addWidget(self.duration)

        duration_lbl = QLabel('minutes\naway', self)
        layout.addWidget(duration_lbl)

        self.distance_widget.setLayout(layout)
        self.distance_widget.resize(300, 100)
        self.distance_widget.move(5, 305)

        # -------------------------
        # init capacity widget
        # -------------------------


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