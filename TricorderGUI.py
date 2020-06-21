from PySide2.QtWidgets import *
from PySide2.QtGui import QPixmap


class TricorderGUI:

    def __init__(self, infile, outfile, color, tleft, bright, tolerance, sensitivity):
        self.infile = infile
        self.outfile = outfile
        self.color = color
        self.tleft = tleft
        self.bright = bright
        self.tolerance = tolerance
        self.sensitivity = sensitivity

        self.app = QApplication([])
        self.root = QWidget()
        self.root.setMinimumWidth(600)
        self.root.setMinimumHeight(400)
        self.root.show()

        self.frame = QLabel('Ayyy')
        self.subs = QLabel('LMAOOO')

        self.root_layout = QHBoxLayout()
        self.root_layout.addWidget(self.frame)
        self.root_layout.addWidget(self.subs)

        self.root.setLayout(self.root_layout)
        self.root.show()


    def exec(self):
        return self.app.exec_()
