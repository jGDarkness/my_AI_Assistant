import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QComboBox, QTextEdit, QLineEdit, QPushButton, QWidget, QLabel)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QColor, QPainter, QFont, QFontMetrics, QIcon

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Sample GUI')
        self.setFixedSize(700, 800)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        font = QFont('Arial Rounded MT', 13)
        QApplication.setFont(font)
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 10, 0, 10)
        banner = QWidget()
        banner.setStyleSheet('background-color: purple; border-top-left-radius: 20px; border-top-right-radius: 20px;')
        banner.setFixedHeight(int(50 * 1.3))
        main_layout.addWidget(banner)
        close_button = QPushButton("X")
        close_button.clicked.connect(self.close)
        close_button.setParent(banner)
        close_button.move(660, 10)
        combo_box = QComboBox()
        combo_box.addItems(['text-davinci-001', 'text-davinci-002', 'text-davinci-003'])
        combo_box.setCurrentText('text-davinci-003')
        combo_box.setFixedWidth(int(1/5 * 96))
        combo_box.setContentsMargins(10, 0, 0, 0)
        main_layout.addWidget(combo_box, alignment=Qt.AlignLeft)
        chat_history = QTextEdit()
        chat_history.setReadOnly(True)
        chat_history.setContentsMargins(10, 0, 0, 0)
        main_layout.addWidget(chat_history)
        user_prompt = QLineEdit()
        user_prompt.setFixedHeight(user_prompt.height() * 3)
        user_prompt.setContentsMargins(10, 0, 0, 0)
        main_layout.addWidget(user_prompt)
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

    def paintEvent(self, event):
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