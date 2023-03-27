import json
import openai
import os
from PIL import Image
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QComboBox, QTextEdit, QLineEdit, QPushButton, QWidget, QLabel, QFileDialog, QScrollBar)
from PyQt5.QtCore import (Qt, QSize, QPoint, QRectF)
from PyQt5.QtGui import (QColor, QPainter, QFont, QPainterPath)
import sys

class CustomButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setFixedHeight(40)
        self.setFixedWidth(100)  # Set the desired button width here

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QColor(128, 0, 128))
        painter.setPen(Qt.NoPen)

        rect = QRectF(0, 0, self.width(), self.height())
        path = QPainterPath()
        path.addRoundedRect(rect, self.height() / 2, self.height() / 2)
        painter.drawPath(path)

        painter.setPen(QColor(255, 255, 255))
        painter.setFont(QFont("Arial Rounded MT Bold", 16))
        painter.drawText(rect, Qt.AlignCenter, self.text())

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Self
        self.setWindowTitle('My AI Assistant')
        self.setFixedSize(QSize(700, 950))
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_LayoutOnEntireRect)
        
        # Grab Mouse click to drag non-maximized window to new position on screen
        self.mouse_pressed = False
        self.mouse_position = QPoint()
        
        # Set Global Font
        font = QFont('Arial Rounded MT', 13)
        QApplication.setFont(font)
        
        # Instantiate the main window layout.
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0,0,0,0)
        
        # Banner
        banner = QWidget()
        banner_label = QLabel("My AI Assistant", banner)
        banner_layout = QHBoxLayout()        

        # Purple Banner
        banner.setStyleSheet('background-color: purple; border-top-left-radius: 20px; border-top-right-radius: 20px;')
        banner.setContentsMargins(0,0,0,0)
        banner.setLayoutDirection(Qt.LeftToRight)
        banner.setFixedWidth=(self.width())
        banner.setFixedHeight(int(banner_label.height() * 2.1))
        banner.setLayout(banner_layout)

        # Application Label
        banner_label.setFont(QFont("Arial Rounded MT Bold", 28))
        banner_label.setStyleSheet("color: white")
        banner_label.setContentsMargins(10,10,20,10)
        banner_label.setFixedWidth(int(self.width()-55))
        banner_label.move(0,0)

        banner_layout.setContentsMargins(10, 0, 20, 0)
        banner_layout.addWidget(banner_label, alignment=Qt.AlignTop | Qt.AlignLeft)
        
        # Banner Yellow 'Minimize' button
        minimize_button = QPushButton("")
        minimize_button.setFixedSize(15, 15)
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
        banner_layout.addWidget(minimize_button, alignment=Qt.AlignRight)
        #minimize_button.move(635, 10)

        # Banne Green 'Maximize' button
        maximize_button = QPushButton("")
        maximize_button.setFixedSize(15, 15)
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
        banner_layout.addWidget(maximize_button, alignment=Qt.AlignRight)
        #maximize_button.move(655, 10)

        # Banner Red 'Close' button
        close_button = QPushButton("")
        close_button.setFixedSize(15, 15)
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
        #close_button.move(675, 10)
        banner_layout.addWidget(close_button, alignment=Qt.AlignRight)
        banner_layout.addStretch(1)
        
        main_layout.addWidget(banner, alignment=Qt.AlignTop)
        
        # OpenAI Model Label and Combobox
        openai_model_layout = QHBoxLayout()
        openai_model_layout.setContentsMargins(10,0,10,0)
        openai_model_label = QLabel("OpenAI Model:")
        openai_model_label.setFixedWidth(135)
        openai_model_label.setStyleSheet("padding: 10px 10px;")
        openai_model_layout.addWidget(openai_model_label, alignment=Qt.AlignLeft | Qt.AlignTop)
        
        # OpenAI Models for which the API requests have been configured in this application.
        combo_box = QComboBox()
        combo_box.addItems(['text-davinci-003'])
           # Currently, 'text-davinci-003' is the only API request in progress. STATUS: PENDING
        combo_box.setCurrentText('text-davinci-003')
        combo_box.setFixedWidth(165)
        openai_model_layout.addWidget(combo_box, alignment=Qt.AlignLeft)
        
        # Add a stretch factor to push the widgets to the left
        openai_model_layout.addStretch()
        main_layout.addLayout(openai_model_layout)
        
# Add new layouts for other api comboboxes here and pattern after the OpenAI and Stretch Factor sections    
        # Create a vertical layout for the chat history and widgets below it
        chat_layout = QVBoxLayout()
        chat_layout.setContentsMargins(0, 0, 0, 0)
        
        # Chat history
        chat_history = QTextEdit()
        chat_history.setReadOnly(True)
        chat_history.setFixedSize(self.width() - 40, 505)
        chat_history.setContentsMargins(10, 20, 20, 20)
        chat_history.setStyleSheet("""
            QTextEdit {
            background-color: #F1F3F5;
            border: 1px solid #C0C0C0;
            padding: 5px;
            }
        """)
        # Add vertical scroll bar to user_prompt
        chat_scroll_bar = QScrollBar(Qt.Vertical, self)
        chat_history.setVerticalScrollBar(chat_scroll_bar)
        chat_scroll_bar.hide()

        # Show/hide scroll bar when needed
        chat_history.textChanged.connect(lambda: chat_scroll_bar.setVisible(chat_scroll_bar.maximum() > 0))
        
        main_layout.addWidget(chat_history, alignment=Qt.AlignHCenter | Qt.AlignTop)
        main_layout.addStretch(1)
        
        # Additional Context File Selection
                
        # File Selector
        file_selector_layout = QHBoxLayout()
        file_selector_layout.setContentsMargins(20, 20, 20, 20)

        # Text box to display the selected file path
        self.file_path_box = QLineEdit()
        self.file_path_box.setReadOnly(True)
        self.file_path_box.setStyleSheet('background-color: #F3F4F6; border: none;')
        self.file_path_box.setPlaceholderText('Choose a file to add extra context...')
        self.file_path_box.setFixedHeight(40)
        self.file_path_box.setStyleSheet("""
            QLineEdit {
            background-color: #F4E0F4;
            border: 1px solid #C0C0C0;
            padding: 5px;
            }
        """)

        file_selector_layout.addWidget(self.file_path_box, stretch=2)

        # Clear button to clear the file_path_box
        clear_button = CustomButton('Clear')
        clear_button.clicked.connect(self.clear_file_path_box)
        file_selector_layout.addWidget(clear_button)

        # Browse button to open system file dialog
        browse_button = CustomButton('Browse')
        browse_button.clicked.connect(self.on_browse_button_clicked)
        file_selector_layout.addWidget(browse_button, alignment=Qt.AlignCenter)

        main_layout.addLayout(file_selector_layout)
        
        # User Prompt
        user_prompt = QTextEdit()
        user_prompt.setFixedSize(self.width() - 40, 150)
        user_prompt.setContentsMargins(0, 20, 0, 0)
        user_prompt.setStyleSheet("""
            QTextEdit {
            background-color: #F4E0F4;
            border: 1px solid #C0C0C0;
            padding: 5px;
            }
        """)
        user_prompt.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        
        # Add vertical scroll bar to user_prompt
        user_prompt_scroll_bar = QScrollBar(Qt.Vertical, self)
        user_prompt.setVerticalScrollBar(user_prompt_scroll_bar)
        user_prompt_scroll_bar.hide()

        # Show/hide scroll bar when needed
        user_prompt.textChanged.connect(lambda: user_prompt_scroll_bar.setVisible(user_prompt_scroll_bar.maximum() > 0))
        main_layout.addWidget(user_prompt, alignment=Qt.AlignHCenter)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 20, 0, 20)

        # 'New' and 'Submit' Buttons
        new_button = CustomButton('New')
        submit_button = CustomButton('Submit')

        button_layout.addWidget(new_button, alignment=Qt.AlignCenter)
        button_layout.addWidget(submit_button, alignment=Qt.AlignCenter)
        main_layout.addLayout(button_layout)
        
        # Central Widget
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        central_widget.setContentsMargins(0, 0, 0, 0)
        
        # Set focus on user_prompt on application load
        user_prompt.setFocus()
    
    def clear_file_path_box(self):
        self.file_path_box.clear()    

    def on_browse_button_clicked(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, 'Open file', '', 'All Files (*.*)')
        if file_path:
            self.file_path_box.setText(file_path)
                
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
        pass

# OpenAI API Configuration #################################################################################################################################################
myOpenAIKey = os.environ.get("OPENAI_API_KEY")
myOpenAIOrg = os.environ.get("OPENAI_API_ORG")

if myOpenAIKey is None:
   raise ValueError("OPENAI_API_KEY is not set in environment variables.")
else: 
   openai.api_key = myOpenAIKey
   openai.organization = myOpenAIOrg
# END OpenAI API Configuration #############################################################################################################################################   
   
   

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())