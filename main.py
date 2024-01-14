import sys
from PyQt5.QtWidgets import QApplication
from setup import vision_client, translate_client, credentials
from transparent_window import TransparentWindow

if __name__ == '__main__':
    # The QApplication needs to be created before any other PyQT classes.
    app = QApplication([])

    # Initialize and show the window
    win = TransparentWindow()

    # Run the application
    exit_code = app.exec_()
    sys.exit(exit_code)