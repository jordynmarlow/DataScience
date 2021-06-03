
from app.constants import df_ind
from app.data import hospitals_df

from PyQt5.QtWidgets import (
    QWidget,
    QListWidget,
    QListWidgetItem,
    QScrollBar
)

from PyQt5.QtCore import QSize

class InsuranceWidget(QWidget):

    def __init__(self, parent) -> None:
        super().__init__(parent=parent)
        self.ui()

    def sizeHint(self) -> QSize:
        return QSize(1000, 200)

    def ui(self):

        # -------------------------
        # init insurance widget
        # -------------------------
        self.insurance_widget = QListWidget(self)
        insurances = hospitals_df.iloc[df_ind]['insurance'].split(',')
        for name in insurances:
            self.insurance_widget.addItem(QListWidgetItem(name))
        scroll_bar = QScrollBar(self)
        #scroll_bar.setStyleSheet()
        self.insurance_widget.setVerticalScrollBar(scroll_bar)
        self.insurance_widget.resize(390, 200)
