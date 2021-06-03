
from app.constants import df_ind
from app.data import hospitals_df

from PyQt5.QtWidgets import (
    QHBoxLayout,
    QGroupBox,
    QWidget,
    QLabel
)

from PyQt5.QtCore import Qt, QSize

class HelipadWidget(QWidget):

    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)
        self.ui()

    def sizeHint(self) -> QSize:
        return QSize(200, 50)

    def ui(self):

        # -------------------------
        # init helipad widget
        # -------------------------
        self.helipad_widget = QGroupBox(self)
        hlayout_helipad = QHBoxLayout()

        helipad_count = hospitals_df.iloc[df_ind]['helipads']
        self.helipads = QLabel(str(helipad_count), self)
        hlayout_helipad.addWidget(self.helipads)

        lbl = 'helipad' if helipad_count == 1 else 'helipads'
        helipad_lbl = QLabel(lbl, self)
        hlayout_helipad.addWidget(helipad_lbl)

        self.helipad_widget.setLayout(hlayout_helipad)
        self.helipad_widget.resize(100, 35)
        self.helipad_widget.setAlignment(Qt.AlignTop)
        # self.helipad_widget.move(5, 305)

        # self.show()
