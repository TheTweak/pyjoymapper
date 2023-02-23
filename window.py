from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QPushButton, QGridLayout, QHBoxLayout, QVBoxLayout, \
    QDial
from PyQt6.QtCore import QSize, Qt

import sys


class Button(QPushButton):
    def __init__(self, title):
        super().__init__(title)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")
        self.setWindowOpacity(0.6)
        self.setFixedSize(QSize(600, 200))

        dpad = QGridLayout()
        dpad.addWidget(Button('up'), 0, 1)
        dpad.addWidget(Button('left'), 1, 0)
        dpad.addWidget(Button('right'), 1, 2)
        dpad.addWidget(Button('down'), 2, 1)

        buttons = QGridLayout()
        buttons.addWidget(Button('a'), 0, 1)
        buttons.addWidget(Button('b'), 1, 0)
        buttons.addWidget(Button('x'), 1, 2)
        buttons.addWidget(Button('y'), 2, 1)

        middle = QVBoxLayout()
        middle.addWidget(Button('share'))
        middle.addWidget(Button('touchpad'))
        middle.addWidget(Button('options'))

        hbox = QHBoxLayout()
        hbox.addWidget(QDial())
        hbox.addLayout(dpad)
        hbox.addLayout(middle)
        hbox.addLayout(buttons)
        hbox.addWidget(QDial())

        vbox = QVBoxLayout()

        triggers = QHBoxLayout()
        left_trigger = QVBoxLayout()
        left_trigger.addWidget(Button('L2'))
        left_trigger.addWidget(Button('L1'))
        triggers.addLayout(left_trigger)
        right_trigger = QVBoxLayout()
        right_trigger.addWidget(Button('R2'))
        right_trigger.addWidget(Button('R1'))
        triggers.addLayout(right_trigger)

        vbox.addLayout(triggers)
        vbox.addLayout(hbox)

        container = QWidget()
        container.setLayout(vbox)
        self.setCentralWidget(container)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()
