from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt

class TranslationOverlay(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent, Qt.Popup | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)

        self.setAttribute(Qt.WA_TranslucentBackground)  # Ensure that only the QLabel is opaque
        self.setLayout(QVBoxLayout())
        
        self.label = QLabel("", self)
        self.label.setWordWrap(True)  # Enable word wrapping
        self.label.setAlignment(Qt.AlignCenter)
        self.layout().addWidget(self.label)
        self.layout().setContentsMargins(0, 0, 0, 0)
        
        self.original_font_size = 18  # Store the original font size
        self.update_stylesheet_with_font_size(self.original_font_size)
        
    def resizeEvent(self, event):
        # Calculate new font size based on the resize event (here we use a simple linear scaling)
        scale_factor = min(self.width(), self.height()) / 400.0  # Example scale factor calculation
        new_font_size = max(1, int(self.original_font_size * scale_factor))

        # Update the stylesheet with the new font size
        self.update_stylesheet_with_font_size(new_font_size)
        super().resizeEvent(event)  # Call the inherited resize event handler
        
    def update_stylesheet_with_font_size(self, font_size):
        # Update the stylesheet of the label with the new font size
        self.label.setStyleSheet(f'''
            QLabel {{
                background-color: white;
                color: black;
                padding: 10px;
                border-radius: 5px;
                font-size: {font_size}pt;  /* Adjusted dynamically */
                font-weight: bold; /* Optional: to make text bold */
            }}
        ''')

    def setText(self, text):
        self.label.setText(text)

    def mousePressEvent(self, event):
        self.close()