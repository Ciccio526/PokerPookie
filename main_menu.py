from PySide6 import QtWidgets
from threading import Event
import sys
from PySide6.QtCore import QUrl
from PySide6.QtGui import QDesktopServices

class MainWindow(QtWidgets.QWidget):
    #sets up MainWindow 
    def __init__(self, start_event):
        super().__init__()
        self.start_event = start_event

        self.setWindowTitle("Main Menu")
        self.setGeometry(100, 100, 400, 300)

        layout = QtWidgets.QVBoxLayout()

        self.start_button = QtWidgets.QPushButton("Start Practicing", self)
        self.start_button.clicked.connect(self.start_game)
        layout.addWidget(self.start_button)

        self.website_button = QtWidgets.QPushButton("Open Help Site", self)
        self.website_button.clicked.connect(self.open_site)
        layout.addWidget(self.website_button)

        self.setLayout(layout)

    #Start game by running GUI managed by PyGame
    def start_game(self):
        self.start_event.set()
        self.close()

    def open_site(self):
        url = "http://pokerpookie.tech/"
        QDesktopServices.openUrl(QUrl(url))


def startMenu(start_event):
    appGUI = QtWidgets.QApplication(sys.argv)

    menu = MainWindow(start_event)
    menu.show()
    sys.exit(appGUI.exec())

if __name__ == "__main__":
    start_event = Event()
    startMenu(start_event)



