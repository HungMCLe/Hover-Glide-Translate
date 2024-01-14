from PyQt5.QtWidgets import QWidget

class CustomWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.original_font_size = 12  # Example original font size
        self.initUI()
