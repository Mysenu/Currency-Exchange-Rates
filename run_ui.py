from PyQt5.QtWidgets import QApplication

from src.ui import Window

if __name__ == '__main__':
    app = QApplication([])
    window = Window()
    window.show()
    app.exec_()
