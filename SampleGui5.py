import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QComboBox, QTextEdit, QLineEdit, QPushButton, QWidget, QLabel)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QColor, QPainter, QFont, QFontMetrics, QIcon

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('My AI Assistant v0.1 beta')
        self.setFixedSize(700, 800)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        font = QFont('Arial Rounded MT', 13)
        QApplication.setFont(font)
        main_layout = QVBoxLayout()

        banner = QWidget()
        banner.setStyleSheet('background-color: purple; border-top-left-radius: 20px; border-top-right-radius: 20px;')
        banner.setMaximumHeight(int(50 * 2.5))
        banner.setLayoutDirection(Qt.LeftToRight)
        banner_label = QLabel("My AI Assistant", banner)
        banner_label.setFont(QFont("Arial Rounded MT Bold", 24))
        banner_label.setStyleSheet("color: white")
        banner_label.move(10, 10)
        banner.setFixedHeight(int(50 * 2.5))
        banner.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(banner)
                
        # OpenAI Model label
        openai_model_layout = QHBoxLayout()
        openai_model_label = QLabel("OpenAI Model:", banner)
        openai_model_label.setFont(QFont("Arial Rounded MT Bold", 13))
        openai_model_label.adjustSize()
        openai_model_layout.addWidget(openai_model_label, alignment=Qt.AlignLeft)

        
        combo_box = QComboBox()
        combo_box.addItems(['text-davinci-001', 'text-davinci-002', 'text-davinci-003'])
        combo_box.setCurrentText('text-davinci-003')
        combo_box.setFixedWidth(int(2.0 * 96))
        openai_model_layout.addWidget(combo_box, alignment=Qt.AlignLeft)
        
        main_layout.addLayout(openai_model_layout)
        
        
        # Create chat history
        self.chat_history = QTextEdit(self)
        self.chat_history.setReadOnly(True)
        self.chat_history.setFixedWidth(self.width() - 20)  # Adjusted width
        self.chat_history.setFixedHeight(int(self.height() * 0.6))  # Adjusted height
        self.chat_history.move(10, banner.height() + 10)
        self.chat_history.setStyleSheet("""
            font: 13px "Arial Rounded MT Bold";
            border-radius: 10px;
            border: 2px solid gray;
            padding: 10px;
            margin: 0px;
        """)        

        openai_model_label.move(self.chat_history.x() + 10, 0)  # Adjusted position        
        
        main_layout.addWidget(self.chat_history, alignment=Qt.AlignHCenter)
        
        user_prompt = QLineEdit(self)
        user_prompt.setFixedHeight(int(self.height() * 0.15))
        user_prompt.setFixedWidth(self.width() - 20)
        user_prompt.move(10, self.chat_history.y() + self.chat_history.height() + 30)
        user_prompt.setStyleSheet("""
           font: 13px "Arial Rounded MT Bold";
           border-radius: 10px;
           border: 2px solid gray;
           padding: 10px;
           margin: 0px;
        """)
        
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
        
        main_layout.setContentsMargins(0, 0, 0, 0)
        central_widget.setContentsMargins(0, 0, 0, 0)

        
        # Minimize button
        minimize_button = QPushButton("", banner)
        minimize_button.setFixedSize(16, 16)
        minimize_button.setStyleSheet("""
           QPushButton {
              background-color: #ffcc00;
              border-radius: 8px;
           }
           QPushButton:hover {
              background-color: #ffaa00;
           }
        """)
        minimize_button.clicked.connect(self.showMinimized)
        minimize_button.move(625, 10)  # Adjusted position

        # Maximize button
        maximize_button = QPushButton("", banner)
        maximize_button.setFixedSize(16, 16)
        maximize_button.setStyleSheet("""
           QPushButton {
              background-color: #4cd964;
              border-radius: 8px;
           }
           QPushButton:hover {
              background-color: #2fd14d;
           }
        """)
        maximize_button.clicked.connect(self.toggle_maximize)
        maximize_button.move(646, 10)  # Adjusted position based on new button size

        # Close button
        close_button = QPushButton("", banner)
        close_button.setFixedSize(16, 16)
        close_button.setStyleSheet("""
           QPushButton {
              background-color: #ff5f57;
              border-radius: 8px;
           }
           QPushButton:hover {
              background-color: #ff3d3b;
           }
        """)
        close_button.clicked.connect(self.close)
        close_button.move(667, 10)  # Adjusted position based on new button size
        
    def toggle_maximize(self):
        if self.isMaximized():
           self.showNormal()
        else:
           self.showMaximized()

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
