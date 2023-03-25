import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QComboBox,
                             QTextEdit, QLineEdit, QPushButton, QWidget)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QColor, QPainter, QFont, QFontMetrics

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up window properties
        self.setWindowTitle('Sample GUI')
        self.setFixedSize(700, 800)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Set the font
        font = QFont('Arial Rounded MT', 13)
        QApplication.setFont(font)

        # Create the main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 10, 0, 10)

        # Create a purple banner row
        banner = QWidget()
        banner.setStyleSheet('background-color: purple;')
        banner.setFixedHeight(int(50 * 1.3))
        main_layout.addWidget(banner)

        # Create a drop-down text box
        combo_box = QComboBox()
        combo_box.addItems(['text-davinci-001', 'text-davinci-002', 'text-davinci-003'])
        combo_box.setCurrentText('text-davinci-003')
        main_layout.addWidget(combo_box)

        # Create a chat history display area
        chat_history = QTextEdit()
        chat_history.setReadOnly(True)
        main_layout.addWidget(chat_history)

        # Create a user prompt text entry box with triple the height
        user_prompt = QLineEdit()
        user_prompt.setFixedHeight(user_prompt.height() * 3)
        main_layout.addWidget(user_prompt)

        # Create "New" and "Submit" buttons with the specified width
        button_layout = QHBoxLayout()
        button_width = int(1.5 * 96)  # Convert inches to pixels (1.5 inches * 96 DPI)
        new_button = QPushButton('New')
        new_button.setFixedWidth(button_width)
        submit_button = QPushButton('Submit')
        submit_button.setFixedWidth(button_width)
        button_layout.addWidget(new_button)
        button_layout.addWidget(submit_button)
        main_layout.addLayout(button_layout)

        # Set up the central widget and layout
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def paintEvent(self, event):
         # Create rounded corners
         painter = QPainter(self)
         painter.setRenderHint(QPainter.Antialiasing)
         painter.setBrush(QColor(255, 255, 255))
         painter.setPen(Qt.NoPen)
         painter.drawRoundedRect(0, 0, self.width(), self.height(), 20, 20)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
