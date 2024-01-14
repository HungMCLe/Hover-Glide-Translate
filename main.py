import sys
from PyQt5.QtWidgets import QApplication
from setup import vision_client, translate_client, credentials
from classes.transparent_window import TransparentWindow

if __name__ == '__main__':
    app = QApplication([])
    win = TransparentWindow()
    win.show()
    exit_code = app.exec_()
    sys.exit(exit_code)