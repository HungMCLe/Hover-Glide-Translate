from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt5.QtCore import Qt, QPoint, QRect, QByteArray, QBuffer, QIODevice
from PyQt5.QtGui import QGuiApplication, QPixmap, QFont
from setup import vision_client, translate_client, credentials
from translation_overlay import TranslationOverlay
from google.cloud import vision

class TransparentWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.oldPos = None
        self.resizing = False
        self.resizeDirection = None

    def initUI(self):
        self.setWindowOpacity(0.5)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setStyleSheet("background-color: lightblue;")

        main_layout = QVBoxLayout()
        side_layout = QHBoxLayout()
        side_layout.addStretch(1)
        btn = QPushButton("Translate", self)
        btn.clicked.connect(self.on_translate)
        side_layout.addWidget(btn)

        main_layout.addStretch(1)
        main_layout.addLayout(side_layout)
        self.setLayout(main_layout)

        self.setGeometry(300, 300, 300, 200)
        self.show()

        self.setMouseTracking(True)

    def on_translate(self):
        # 1. Capture the screen
        screenshot = self.capture_screen()

        # 2. Extract text from the captured image
        extracted_text = self.extract_text_from_image(screenshot)

        # Optional: Remove the word "Translate" from the extracted text
        extracted_text = extracted_text.replace("Translate", "")

        # 3. Translate the text
        translated_text = self.translate_text(extracted_text)

        # 4. Display the translation using the overlay
        if not hasattr(self, 'overlay'):
            self.overlay = TranslationOverlay(self)
            self.overlay.setFixedSize(self.size())  # Make overlay the same size as the main window
        self.overlay.setText(translated_text)
        self.overlay.move(self.pos())
        self.overlay.show()

    def capture_screen(self):
        screen = QGuiApplication.primaryScreen()
        screenshot = screen.grabWindow(0, self.x(), self.y(), self.width(), self.height())
        return screenshot

    def extract_text_from_image(self, pixmap: QPixmap):
        byte_array = QByteArray()
        buffer = QBuffer(byte_array)
        buffer.open(QIODevice.WriteOnly)
        pixmap.save(buffer, "PNG")
        image_bytes = byte_array.data()

        image = vision.Image(content=image_bytes)
        response = vision_client.text_detection(image=image)
        texts = response.text_annotations

        if texts:
            text = texts[0].description
        else:
            text = ''

        if response.error.message:
            raise Exception(f'{response.error.message}')

        return text

    def translate_text(self, text, target_language="en"):
        if text:
            result = translate_client.translate(text, target_language=target_language)
            return result['translatedText']
        else:
            return ''

    def show_translation(self, translated_text):
        msg_box = QMessageBox(self)
        msg_box.setText(translated_text)
        msg_box.exec_()


    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()
        self.checkResizeCorners(event.pos())

    def checkResizeCorners(self, pos):
        if QRect(self.width() - 10, self.height() - 10, 10, 10).contains(pos):
            self.resizing = True
            self.resizeDirection = "SE"
        elif QRect(0, self.height() - 10, 10, 10).contains(pos):
            self.resizing = True
            self.resizeDirection = "SW"
        elif QRect(self.width() - 10, 0, 10, 10).contains(pos):
            self.resizing = True
            self.resizeDirection = "NE"
        elif QRect(0, 0, 10, 10).contains(pos):
            self.resizing = True
            self.resizeDirection = "NW"
        else:
            self.resizing = False

    def mouseMoveEvent(self, event):
        # Check the cursor position and set the cursor type
        if (QRect(self.width() - 10, self.height() - 10, 10, 10).contains(event.pos())):
            self.setCursor(Qt.SizeFDiagCursor)
        elif (QRect(0, self.height() - 10, 10, 10).contains(event.pos())):
            self.setCursor(Qt.SizeBDiagCursor)
        elif (QRect(self.width() - 10, 0, 10, 10).contains(event.pos())):
            self.setCursor(Qt.SizeBDiagCursor)
        elif (QRect(0, 0, 10, 10).contains(event.pos())):
            self.setCursor(Qt.SizeFDiagCursor)
        else:
            self.setCursor(Qt.ArrowCursor)

        # Existing move and resize logic
        if not self.oldPos:
            return

        if self.resizing:
            delta = event.globalPos() - self.oldPos
            self.oldPos = event.globalPos()

            if self.resizeDirection == "SE":
                self.resize(self.width() + delta.x(), self.height() + delta.y())
            elif self.resizeDirection == "SW":
                self.resize(self.width() - delta.x(), self.height() + delta.y())
                self.move(self.x() + delta.x(), self.y())
            elif self.resizeDirection == "NE":
                self.resize(self.width() + delta.x(), self.height() - delta.y())
                self.move(self.x(), self.y() + delta.y())
            elif self.resizeDirection == "NW":
                self.resize(self.width() - delta.x(), self.height() - delta.y())
                self.move(self.x() + delta.x(), self.y() + delta.y())
        else:
            delta = event.globalPos() - self.oldPos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPos()

    def mouseReleaseEvent(self, event):
        self.resizing = False
        self.resizeDirection = None
        self.oldPos = None
        self.setCursor(Qt.ArrowCursor)