import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QComboBox, QTextEdit, QLineEdit, QPushButton, QWidget, QLabel)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QColor, QPainter, QFont, QFontMetrics, QIcon
from PyQt5.QtCore import QPoint

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Sample GUI')
        self.setFixedSize(700, 800)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.mouse_pressed = False
        self.mouse_position = QPoint()
        font = QFont('Arial Rounded MT', 13)
        QApplication.setFont(font)
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 10)
        banner = QWidget()
        banner.setStyleSheet('background-color: purple; border-top-left-radius: 20px; border-top-right-radius: 20px;')
        banner.setFixedHeight(int(50 * 1.3))
        main_layout.addWidget(banner)
        banner_label = QLabel("My AI Assistant", banner)
        banner_label.setFont(QFont("Arial Rounded MT Bold", 26))
        banner_label.setStyleSheet("color: white")
        banner_label.move(10, 10)
        openai_model_layout = QHBoxLayout()
        openai_model_label = QLabel("OpenAI Model:")
        openai_model_label.setFixedWidth(openai_model_label.fontMetrics().width(openai_model_label.text()))
        openai_model_layout.addWidget(openai_model_label, alignment=Qt.AlignLeft)
        combo_box = QComboBox()
        combo_box.addItems(['text-davinci-001', 'text-davinci-002', 'text-davinci-003'])
        combo_box.setCurrentText('text-davinci-003')
        combo_box.setFixedWidth(int(2.0 * 96))
        combo_box.move(10, 0)
        openai_model_layout.addWidget(combo_box, alignment=Qt.AlignLeft)
        main_layout.addLayout(openai_model_layout)
        chat_history = QTextEdit()
        chat_history.setReadOnly(True)
        chat_history.setFixedSize(self.width() - 20, int(self.height() * 0.6))
        chat_history.setContentsMargins(10, 0, 0, 0)
        main_layout.addWidget(chat_history, alignment=Qt.AlignHCenter)
        user_prompt = QLineEdit()
        user_prompt.setFixedHeight(int(self.height() * 0.2))
        user_prompt.setFixedSize(chat_history.width(), user_prompt.height())
        user_prompt.setContentsMargins(10, 0, 0, 0)
        main_layout.addWidget(user_prompt, alignment=Qt.AlignHCenter)
        button_layout = QHBoxLayout()
        button_width = int(1.5 * 96)
        new_button = QPushButton('New')
        new_button.setFixedWidth(button_width)
        submit_button = QPushButton('Submit')
        submit_button.setFixedWidth(button_width)
        button_layout.addWidget(new_button)
        button_layout.addWidget(submit_button)
        main_layout.addLayout(button_layout)
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        
        # Minimize button
        minimize_button = QPushButton("", banner)
        minimize_button.setFixedSize(14, 14)
        minimize_button.setStyleSheet("""
            QPushButton {
                background-color: #ffcc00;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #ffaa00;
            }
        """)
        minimize_button.clicked.connect(self.showMinimized)
        minimize_button.move(627, 10)

        # Maximize button
        maximize_button = QPushButton("", banner)
        maximize_button.setFixedSize(14, 14)
        maximize_button.setStyleSheet("""
            QPushButton {
               background-color: #4cd964;
               border-radius: 6px;
            }
            QPushButton:hover {
               background-color: #2fd14d;
            }
        """)
        maximize_button.clicked.connect(self.toggle_maximize)
        maximize_button.move(642, 10)

        # Close button
        close_button = QPushButton("", banner)
        close_button.setFixedSize(14, 14)
        close_button.setStyleSheet("""
            QPushButton {
                background-color: #ff5f57;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #ff3d3b;
            }
        """)
        close_button.clicked.connect(self.close)
        close_button.move(657, 10)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QColor(255, 255, 255))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(0, 0, self.width(), self.height(), 20, 20)
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.mouse_pressed = True
            self.mouse_position = event.globalPos() - self.pos()
            event.accept()

    def mouseMoveEvent(self, event):
        if self.mouse_pressed and event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.mouse_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.mouse_pressed = False
            event.accept()

    def toggle_maximize(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())