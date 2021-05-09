import matplotlib, folium, sys, io
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

        self.map_view = QWebEngineView(self)
        self.map_view.resize(300, 300)
        self.map_view.setHtml(data.getvalue().decode())

        # -------------------------
        # init distance widget
        # -------------------------


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