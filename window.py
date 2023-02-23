from time import sleep

from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QGridLayout, QHBoxLayout, QVBoxLayout, \
    QDial
from PyQt6.QtCore import QSize, QRunnable, pyqtSlot, Qt
from dualshock4 import DS4Controller

import sys


class ControllerWorker(QRunnable):
    def __init__(self):
        super(ControllerWorker, self).__init__()
        self.ds4 = DS4Controller()

    @pyqtSlot()
    def run(self):
        while True:
            sleep(1000)


class Button(QPushButton):
    def __init__(self, title):
        super().__init__(title)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")
        self.setWindowOpacity(0.6)
        self.setFixedSize(QSize(600, 300))
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)

        self.up = Button('up')
        self.down = Button('down')
        self.left = Button('left')
        self.right = Button('right')
        self.square = Button('b')
        self.triangle = Button('a')
        self.circle = Button('c')
        self.cross = Button('d')
        self.l1 = Button('L1')
        self.r1 = Button('R1')
        self.l2 = Button('L2')
        self.r2 = Button('R2')
        self.share = Button('share')
        self.options = Button('options')
        self.touchpad = Button('touchpad')
        self.left_stick = QDial()
        self.right_stick = QDial()

        self.start_stop_btn = QPushButton('Start')
        self.start_stop_btn.setCheckable(True)
        self.start_stop_btn.clicked.connect(self.start_stop)

        dpad = QGridLayout()
        dpad.addWidget(self.up, 0, 1)
        dpad.addWidget(self.left, 1, 0)
        dpad.addWidget(self.right, 1, 2)
        dpad.addWidget(self.down, 2, 1)

        buttons = QGridLayout()
        buttons.addWidget(self.triangle, 0, 1)
        buttons.addWidget(self.square, 1, 0)
        buttons.addWidget(self.circle, 1, 2)
        buttons.addWidget(self.cross, 2, 1)

        middle = QVBoxLayout()
        middle.addWidget(self.share)
        middle.addWidget(self.touchpad)
        middle.addWidget(self.options)

        hbox = QHBoxLayout()
        hbox.addWidget(self.left_stick)
        hbox.addLayout(dpad)
        hbox.addLayout(middle)
        hbox.addLayout(buttons)
        hbox.addWidget(self.right_stick)

        vbox = QVBoxLayout()

        triggers = QHBoxLayout()
        left_trigger = QVBoxLayout()
        left_trigger.addWidget(self.l2)
        left_trigger.addWidget(self.l1)
        triggers.addLayout(left_trigger)
        right_trigger = QVBoxLayout()
        right_trigger.addWidget(self.r2)
        right_trigger.addWidget(self.r1)
        triggers.addLayout(right_trigger)

        settings = QHBoxLayout()
        settings.addWidget(self.start_stop_btn)

        vbox.addLayout(settings)
        vbox.addLayout(triggers)
        vbox.addLayout(hbox)

        container = QWidget()
        container.setLayout(vbox)
        self.setCentralWidget(container)

        self.controller = DS4Controller()

    def start_stop(self):
        self.start_stop_btn.setText('Press Share to stop')
        self.controller.start()  # blocking current thread
        self.start_stop_btn.setText('Start')
        self.start_stop_btn.setChecked(False)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
