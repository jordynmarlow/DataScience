import matplotlib, folium, sys, io
import pandas as pd
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import QWebEngineView

user_lat = 43.01272028760803
user_lon = -83.71256602748012

hospitals = pd.read_excel('sample_data.xlsx').set_index('name')


class DataViz(QApplication):
    def __init__(self):
        super().__init__()
        self.window_width, self.window_height = 1600, 1200
        self.setMinimumSize(self.window_width, self.window_height)

        layout = QVBoxLayout()
        self.setLayout(layout)

        map = folium.Map(location=[user_lat, user_lon], tiles='Stamen Terrain', default_zoom_start=15)
        for index, row in hospitals.iterrows():
            folium.Marker(location=[row['lat'], row['lon']]).add_to(map)

        data = io.BytesIO()
        map.save(data, close_file=False)

        webView = QWebEngineView()
        webView.setHtml(data.getvalue().decode())
        layout.addWidget(webView)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    #app.setStyleSheet('')
    
    data_viz = DataViz()
    data_viz.show()

    sys.exit(app.exec_())