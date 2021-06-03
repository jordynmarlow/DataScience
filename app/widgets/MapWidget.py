
from app.constants import user_lon, user_lat
from app.data import hospitals_df

import PyQt5.QtCore as QtCore
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import (
    QWidget
)

import typing
import folium
import io


class MapWidget(QWidget):

    def __init__(self, parent: typing.Optional['QWidget']) -> None:
        super().__init__(parent=parent)
        self.ui()

    def ui(self):

        self.left=50*2
        self.top=50*2
        self.width=640
        self.height=480

        # self.setGeometry(self.left,self.top,self.width,self.height)

        # -------------------------
        # init map widget
        # -------------------------
        fMap = folium.Map(location=[user_lat, user_lon], tiles='Stamen Terrain', default_zoom_start=15)
        for _, row in hospitals_df.iterrows():
            folium.Marker(location=[row['lat'], row['lon']]).add_to(fMap)

        data = io.BytesIO()
        fMap.save(data, close_file=False)

        self.map_widget = QWebEngineView(self)
        self.map_widget.resize(410, 460)
        # self.map_widget.move(5, 5)
        self.map_widget.setHtml(data.getvalue().decode())

        self.show()