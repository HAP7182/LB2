from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtCore import pyqtSignal

# Переопределение методов класса QlineEdit для реализции нажатия по полю ввода
class Overridden(QLineEdit):
    clicked = pyqtSignal()
    pressed = pyqtSignal()
    data = ""

    def mouseReleaseEvent(self, ev):
        super().mouseReleaseEvent(ev)
        self.clicked.emit()

    def keyReleaseEvent(self, ev):
        super().keyReleaseEvent(ev)
        self.pressed.emit()

        self.data = f'{ev.text()!r}'