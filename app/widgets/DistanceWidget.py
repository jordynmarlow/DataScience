
from app.constants import df_ind, user_lon, user_lat
from app.data import hospitals_df

from PyQt5.QtWidgets import (
    QHBoxLayout,
    QGroupBox,
    QWidget,
    QLabel
)

from PyQt5.QtCore import Qt, QSize

import requests
import json


class DistanceWidget(QWidget):
    
    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)
        self.ui()
        # self.show()

    def sizeHint(self) -> QSize:
        return QSize(200, 50)

    def ui(self):
        # -------------------------
        # init distance widget
        # -------------------------
        lon = hospitals_df.iloc[df_ind]['lon']
        lat = hospitals_df.iloc[df_ind]['lat']
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
        self.distance_widget.resize(150, 50)
        # self.distance_widget.move(5, 305)
        self.distance_widget.setAlignment(Qt.AlignTop)
