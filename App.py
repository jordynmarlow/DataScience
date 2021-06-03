
from app.widgets.InsuranceWidget import InsuranceWidget
from app.widgets.CovidTestsWidget import CovidTestsWidget
from app.widgets.VentilatorsWidget import VentilatorsWidget
from app.widgets.StaffWidget import StaffWidget
from app.widgets.BedCapacityWidget import BedCapacityWidget
from app.widgets.DistanceWidget import DistanceWidget
from app.widgets.HelipadWidget import HelipadWidget
from app.widgets.MapWidget import MapWidget

from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QHBoxLayout,
    QVBoxLayout,
    QGroupBox
)

from PyQt5.QtCore import Qt

import sys


class TestApp2(QMainWindow):

    def __init__(self) -> None:
        super().__init__()

        self.initUI()

    def initUI(self):
        self.window_width, self.window_height = 1200, 800
        self.setMinimumSize(self.window_width, self.window_height)
        self.setWindowTitle('Test')
        self.showMaximized()
        self.window_width, self.window_height = self.width(), self.height()

        self._createHorizontalLayout()

        self.show()

    def _createLeftWidget(self):
        self.leftWidget = QGroupBox(self)

        left_layout = QVBoxLayout()
        map_widget = MapWidget(parent=self)
        left_layout.addWidget(map_widget)
        
        self.innerTextsWidget = QGroupBox(self)
        inner_layout = QVBoxLayout()
        inner_layout.addWidget(DistanceWidget(parent=self))
        inner_layout.addWidget(HelipadWidget(parent=self))
        inner_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.innerTextsWidget.setLayout(inner_layout)

        left_layout.addWidget(self.innerTextsWidget)

        self.leftWidget.setLayout(left_layout)

    def _createMiddleWidget(self):
        self.middleWidget = QGroupBox(self)
        middle_layout = QVBoxLayout()

        middle_layout.addWidget(StaffWidget().widget)
        middle_layout.addWidget(CovidTestsWidget().widget)
        middle_layout.addWidget(VentilatorsWidget().widget)

        self.middleWidget.setLayout(middle_layout)

    def _createRightWidget(self):
        self.rightWidget = QGroupBox(self)

        right_layout = QVBoxLayout()
        right_layout.addWidget(BedCapacityWidget().widget, 60)

        self.innerInsuranceWrapperWidget = QGroupBox(self)
        inner_layout = QVBoxLayout()
        inner_layout.addWidget(InsuranceWidget(parent=self), 40)
        inner_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.innerInsuranceWrapperWidget.setLayout(inner_layout)

        right_layout.addWidget(self.innerInsuranceWrapperWidget)

        self.rightWidget.setLayout(right_layout)

    def _createHorizontalLayout(self):
        self.horizontalGroupBox = QGroupBox("H Group Box", self)

        layout = QHBoxLayout()

        self._createLeftWidget()
        self._createMiddleWidget()
        self._createRightWidget()
        
        layout.addWidget(self.leftWidget, 23)
        layout.addWidget(self.middleWidget, 54)
        layout.addWidget(self.rightWidget, 23)

        self.horizontalGroupBox.setLayout(layout)

        self.setCentralWidget(self.horizontalGroupBox)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    _ = TestApp2()
    sys.exit(app.exec_())