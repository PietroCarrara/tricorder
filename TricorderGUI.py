from PySide2.QtWidgets import *
from PySide2.QtGui import QPixmap
from PySide2.QtCore import Qt, Slot, Signal, QObject
from multiprocessing import Process
from TricorderNotifier import GUINotifier
from tricorder import scan
from PIL.Image import Image
from PIL.ImageQt import ImageQt
import PySide2.QtCore as QtCore
import srt


class TricorderGUI(QObject):

    notify_frame = Signal(Image, float)
    notify_subtitles = Signal(list)

    def __init__(self, infile, outfile, color, tleft, bright, tolerance, sensitivity):
        super().__init__()

        self.notify_frame.connect(self.update_frame)
        self.notify_subtitles.connect(self.update_subtitles)

        self.app = QApplication([])
        self.root = QWidget()
        self.root.setMinimumWidth(600)
        self.root.setMinimumHeight(400)
        self.root.show()

        self.threadpool = QtCore.QThreadPool(self.app)

        self.frame = QLabel()
        self.frame.setAlignment(Qt.AlignCenter)
        sz = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sz.setVerticalStretch(2)
        self.frame.setSizePolicy(sz)

        self.subs = QTextEdit()
        self.subs.setEnabled(False)
        sz = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sz.setVerticalStretch(8)
        self.subs.setSizePolicy(sz)

        self.scan = ScanRunnable(
            infile, outfile, color, tleft, bright, tolerance, sensitivity, self)

        self.root_layout = QVBoxLayout()
        self.root_layout.addWidget(self.frame)
        self.root_layout.addWidget(self.subs)

        self.root.setLayout(self.root_layout)
        self.root.show()

    def exec(self):
        self.threadpool.start(self.scan)
        return self.app.exec_()

    @Slot(Image, float)
    def update_frame(self, frame, completion):
        frame = ImageQt(frame)
        self.frame.setPixmap(QPixmap.fromImage(frame).scaled(
            self.frame.width(), self.frame.height(), Qt.KeepAspectRatio))

    @Slot(list)
    def update_subtitles(self, subs):
        self.subs.setText(srt.compose(subs))
        self.subs.verticalScrollBar().setValue(self.subs.verticalScrollBar().maximum())


class ScanRunnable(QtCore.QRunnable):
    def __init__(self, infile, outfile, color, tleft, bright, tolerance, sensitivity, app):
        self.infile = infile
        self.outfile = outfile
        self.color = color
        self.tleft = tleft
        self.bright = bright
        self.tolerance = tolerance
        self.sensitivity = sensitivity
        self.app = app

        super(ScanRunnable, self).__init__()

    @QtCore.Slot()
    def run(self):
        scan(self.infile, self.outfile, self.color, self.tleft,
             self.bright, self.tolerance, self.sensitivity, GUINotifier(self.app))
