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

    notify_frame = Signal(Image)
    notify_completion = Signal(float)
    notify_subtitles = Signal(list)
    notify_display = Signal(str)

    def __init__(self, infile, outfile, color, tleft, bright, tolerance, sensitivity, frameskip):
        super().__init__()

        self.notify_frame.connect(self.update_frame)
        self.notify_completion.connect(self.update_completion)
        self.notify_subtitles.connect(self.update_subtitles)
        self.notify_display.connect(self.update_display)

        self.app = QApplication([])
        self.root = QWidget()
        self.root.setMinimumWidth(600)
        self.root.setMinimumHeight(400)

        self.threadpool = QtCore.QThreadPool(self.app)

        self.frame = QLabel()
        self.frame.setAlignment(Qt.AlignCenter)
        sz = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sz.setVerticalStretch(2)
        self.frame.setSizePolicy(sz)

        hcontainer = QWidget()
        sz = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sz.setVerticalStretch(8)
        hcontainer.setSizePolicy(sz)

        hlayout = QHBoxLayout()
        hcontainer.setLayout(hlayout)

        self.subs = QPlainTextEdit()
        self.subs.setReadOnly(True)
        sz = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sz.setHorizontalStretch(5)
        self.subs.setSizePolicy(sz)

        infobox = QWidget()
        sz = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sz.setHorizontalStretch(5)
        infobox.setSizePolicy(sz)

        infolayout = QVBoxLayout()
        infobox.setLayout(infolayout)

        self.display = QLabel('')
        self.display.setAlignment(Qt.AlignCenter)

        self.progress = QProgressBar()
        self.progress.setRange(0, 100)

        self.scan = ScanRunnable(
            infile, outfile, color, tleft, bright, tolerance, sensitivity, frameskip, self)

        infolayout.addWidget(self.display)
        infolayout.addWidget(self.progress)

        hlayout.addWidget(self.subs)
        hlayout.addWidget(infobox)

        root_layout = QVBoxLayout()
        root_layout.addWidget(self.frame)
        root_layout.addWidget(hcontainer)

        self.root.setLayout(root_layout)
        self.root.show()

    def exec(self):
        self.threadpool.start(self.scan)
        return self.app.exec_()

    @Slot(Image)
    def update_frame(self, frame):
        frame = ImageQt(frame)
        self.frame.setPixmap(QPixmap.fromImage(frame).scaled(
            self.frame.width(), self.frame.height(), Qt.KeepAspectRatio))

    @Slot(float)
    def update_completion(self, completion):
        self.progress.setValue(int(completion*100))

    @Slot(list)
    def update_subtitles(self, subs):
        self.subs.appendPlainText(subs.to_srt())

    @Slot(str)
    def update_display(self, contents):
        self.display.setText(contents)


class ScanRunnable(QtCore.QRunnable):
    def __init__(self, infile, outfile, color, tleft, bright, tolerance, sensitivity, frameskip, app):
        self.infile = infile
        self.outfile = outfile
        self.color = color
        self.tleft = tleft
        self.bright = bright
        self.tolerance = tolerance
        self.sensitivity = sensitivity
        self.frameskip = frameskip
        self.app = app

        super(ScanRunnable, self).__init__()

    @QtCore.Slot()
    def run(self):
        scan(self.infile, self.outfile, self.color, self.tleft,
             self.bright, self.tolerance, self.sensitivity, self.frameskip, GUINotifier(self.app))
