from datetime import datetime
import openai
import os
from pygments import highlight
from pygments.lexers import guess_lexer, TextLexer
from pygments.formatters import HtmlFormatter
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QComboBox, QTextEdit, QLineEdit, QPushButton, QWidget, QLabel, QFileDialog, 
                             QScrollBar, QDialog)
from PyQt5.QtCore import (Qt, QSize, QPoint, QRectF, QThread, pyqtSignal)
from PyQt5.QtGui import (QColor, QPainter, QFont, QPainterPath)
import re
import sys
from transformers import GPT2Tokenizer



# OpenAI API Configuration
myOpenAIKey = os.environ.get("OPENAI_API_KEY") 
myOpenAIOrg = os.environ.get("OPENAI_API_ORG")

if myOpenAIKey is None:
   raise ValueError("OPENAI_API_KEY is not set in environment variables.")
else: 
   openai.api_key = myOpenAIKey
   openai.organization = myOpenAIOrg



# Class 'CustomButton' creates a custom button style that can be used throughout the application.
class CustomButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setFixedHeight(40)  # Set the desired button height
        self.setFixedWidth(100)  # Set the desired button width

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
            
        # Seth the RGB Value for Purple used throughout this app.
        painter.setBrush(QColor(128, 0, 128))   # HEX: #800080
        painter.setPen(Qt.NoPen)

        rect = QRectF(0, 0, self.width(), self.height())
        path = QPainterPath()
        
        path.addRoundedRect(rect, self.height() / 2, self.height() / 2)
        
        painter.drawPath(path)
        painter.setPen(QColor(255, 255, 255))   # set the font color to white HED: #ffffff
        painter.setFont(QFont("Arial Rounded MT Bold", 16)) # set the font and size
        painter.drawText(rect, Qt.AlignCenter, self.text())


# Class "MouseHandler" handles mouse events.
class MouseHandler:
    def __init__(self):
        self.mouse_pressed = False
        self.mouse_position = QPoint()

    def handle_mouse_press(self, event):
        if event.button() == Qt.LeftButton:
            self.mouse_pressed = True
            self.mouse_position = event.globalPos() - event.widget().pos()
            event.accept()

    def handle_mouse_move(self, event, target_widget):
        if self.mouse_pressed and event.buttons() == Qt.LeftButton:
            target_widget.move(event.globalPos() - self.mouse_position)
            event.accept()

    def handle_mouse_release(self, event):
        if event.button() == Qt.LeftButton:
            self.mouse_pressed = False
            event.accept()



# Class 'MainWindow' creates the main window of the application and houses the layouts and widgets.
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle('My AI Assistant')
        self.setFixedSize(QSize(800, 1150))
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_LayoutOnEntireRect)
        
        # Setup the tokenizer for counting tokens in chat_history and user_prompt.
        self.tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
        
        # Get's the mouse position when the user clicks to drag the app around the screen.
        self.mouse_pressed = False
        self.mouse_position = QPoint() 
        
        # Set Global Font.
        font = QFont('Arial Rounded MT', 13)
        QApplication.setFont(font)
        
        # Instantiate the main window layout.
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0,0,0,0)
        
        # Banner Widget.
        banner = QWidget()
        
        # Banner Layout.
        banner_label = QLabel("My AI Assistant", banner)
        banner_layout = QHBoxLayout()        

        # Purple Banner.
        banner.setStyleSheet('background-color: purple; border-top-left-radius: 20px; border-top-right-radius: 20px;')
        banner.setContentsMargins(0,0,0,0)
        banner.setLayoutDirection(Qt.LeftToRight)
        banner.setFixedWidth=(self.width())
        banner.setFixedHeight(int(banner_label.height() * 2.1))
        banner.setLayout(banner_layout)

        # Application Label.
        banner_label.setFont(QFont("Arial Rounded MT Bold", 28))
        banner_label.setStyleSheet("color: white")
        banner_label.setContentsMargins(10,10,20,10)
        banner_label.setFixedWidth(int(self.width()-55))
        banner_label.move(0,0)

        banner_layout.setContentsMargins(10, 0, 20, 0)
        banner_layout.addWidget(banner_label, alignment=Qt.AlignTop | Qt.AlignLeft)
        
        minimize_button = self.create_button('#ffcc00', '#ffaa00', self.showMinimized) # RGB: 255, 204, 0 (Yellow)
        maximize_button = self.create_button('#4cd964', '#2fd14d', self.toggle_maximize) # RGB: 76, 217, 99 (Green)
        close_button = self.create_button('#ff5f57', '#ff3d3b', self.close) # RGB: 255, 95, 87 (Red)
        banner_layout.addWidget(minimize_button, alignment=Qt.AlignRight)
        banner_layout.addWidget(maximize_button, alignment=Qt.AlignRight)
        banner_layout.addWidget(close_button, alignment=Qt.AlignRight)       
        
        banner_layout.addStretch(1)
        
        main_layout.addWidget(banner, alignment=Qt.AlignTop)
        
        # OpenAI model label and Combobox.
        openai_model_layout = QHBoxLayout()
        openai_model_layout.setContentsMargins(10,0,10,0)
        openai_model_label = QLabel("OpenAI Model:")
        openai_model_label.setFixedWidth(135)
        openai_model_label.setStyleSheet("padding: 10px 10px;")
        openai_model_layout.addWidget(openai_model_label, alignment=Qt.AlignLeft | Qt.AlignTop)
        
        # OpenAI Models for which the API requests have been configured in this application.
        self.combo_box = QComboBox()
        self.combo_box.addItems(['gpt-3.5-turbo'])
        self.combo_box.addItems(['gpt-4'])  
        self.combo_box.setCurrentText('gpt-4')
        self.combo_box.setFixedWidth(165)
        
        openai_model_layout.addWidget(self.combo_box, alignment=Qt.AlignLeft)
        openai_model_layout.addStretch()
        
        main_layout.addLayout(openai_model_layout)
        
        ##### PLACEHOLDER: Add new layouts for other api comboboxes here.    

        # Create a vertical layout for the chat history and widgets below it.
        self.chat_layout = QVBoxLayout()
        self.chat_layout.setContentsMargins(0, 0, 0, 0)
        
        # Chat History Layout.
        chat_history_layout = QVBoxLayout()
        
        # Chat history.
        self.chat_history = QTextEdit()
        self.chat_history.setReadOnly(True)
        self.chat_history.setFixedSize(self.width() - 40, 585)
        self.chat_history.setContentsMargins(10, 20, 20, 20)
        self.set_widget_style(self.chat_history)
        
        # Add vertical scroll bar to user_prompt.
        chat_scroll_bar = QScrollBar(Qt.Vertical, self)
        self.chat_history.setVerticalScrollBar(chat_scroll_bar)
        chat_scroll_bar.hide()

        # Show/hide scroll bar when needed.
        self.chat_history.textChanged.connect(lambda: chat_scroll_bar.setVisible(chat_scroll_bar.maximum() > 0))
        chat_history_layout.addWidget(self.chat_history)

        # Chat Token Counter.
        # Add a label to display token count in chat history.
        self.chat_token_count_label = self.create_label("", 10, "grey")
        self.chat_history.textChanged.connect(self.update_chat_token_count)

        # Create QHBoxLayout to hold the chat_token_count_label and align it to the right.
        chat_token_count_layout = QHBoxLayout()
        
        # Stretch to push label to the right.
        chat_token_count_layout.addStretch(1)  
        chat_token_count_layout.addWidget(self.chat_token_count_label, alignment=Qt.AlignRight)

        chat_history_layout.addLayout(chat_token_count_layout)

        chat_history_container = QWidget()
        chat_history_container.setLayout(chat_history_layout)

        main_layout.addWidget(chat_history_container, alignment=Qt.AlignHCenter | Qt.AlignTop)
        main_layout.addStretch(1)

        # File Selector.
        file_selector_layout = QHBoxLayout()
        file_selector_layout.setContentsMargins(20, 20, 20, 20)

        # Text box to display the selected file path.
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

        # Clear button to clear the file_path_box.
        clear_button = CustomButton('Clear')
        clear_button.clicked.connect(self.clear_file_path_box)
        file_selector_layout.addWidget(clear_button)

        # Browse button to open system file dialog.
        browse_button = CustomButton('Browse')
        browse_button.clicked.connect(self.on_browse_button_clicked)
        file_selector_layout.addWidget(browse_button, alignment=Qt.AlignCenter)
        main_layout.addLayout(file_selector_layout)
        
        # Add User Prompt Layout.
        user_prompt_layout = QVBoxLayout()
        
        # User Prompt.
        self.user_prompt = QTextEdit()
        self.user_prompt.setFixedSize(self.width() - 40, 200)
        self.user_prompt.setContentsMargins(0, 20, 0, 0)
        self.set_widget_style(self.user_prompt)
        self.user_prompt.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        user_prompt_scroll_bar = QScrollBar(Qt.Vertical, self)
        self.user_prompt.setVerticalScrollBar(user_prompt_scroll_bar)
        user_prompt_scroll_bar.hide()
        self.user_prompt.textChanged.connect(lambda: user_prompt_scroll_bar.setVisible(user_prompt_scroll_bar.maximum() > 0))
        user_prompt_layout.addWidget(self.user_prompt, alignment=Qt.AlignHCenter)

        # Add a label to display token count in user prompt.
        self.user_prompt_token_count_label = self.create_label("", 10, "grey")
        user_prompt_layout.addWidget(self.user_prompt_token_count_label, alignment=Qt.AlignRight)
        user_prompt_layout.setAlignment(self.user_prompt_token_count_label, Qt.AlignRight)
        self.user_prompt.textChanged.connect(self.update_user_prompt_token_count)
        
        user_prompt_container = QWidget()
        user_prompt_container.setLayout(user_prompt_layout)
        
        main_layout.addWidget(user_prompt_container, alignment=Qt.AlignHCenter)
        main_layout.addStretch(1)

        # Buttons.
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 20, 0, 20)
    
        # 'New' and 'Submit' Buttons.
        new_button = CustomButton('New')
        new_button.clicked.connect(lambda: self.on_new_button_clicked())
        
        submit_button = CustomButton('Submit')
        
        # Connect the submit_prompt method.
        submit_button.clicked.connect(self.submit_prompt)  
        
        button_layout.addWidget(new_button, alignment=Qt.AlignCenter)
        button_layout.addWidget(submit_button, alignment=Qt.AlignCenter)
        
        main_layout.addLayout(button_layout)
        
        # Central Widget.
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        central_widget.setContentsMargins(0, 0, 0, 0)
        
        # Set focus on user_prompt on application load.
        self.user_prompt.setFocus()
    
    def create_label(self, text, font_size, color):
        label = QLabel(text)
        label.setStyleSheet(f"color: {color}; font-size: {font_size}px;")
        return label
    
    def get_token_count(self, text):
        return len(self.tokenizer.encode(text))
    
    def create_button(self, color, hover_color, clicked_event=None):
        button = QPushButton("")
        button.setFixedSize(15, 15)
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                border-radius: 6px;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
            }}
        """)
        if clicked_event:
            button.clicked.connect(clicked_event)
        return button

    def on_new_button_clicked(self):
        # Create a confirmation dialog.
        confirm_dialog = QDialog(self)
        confirm_dialog.setWindowTitle("Start New Conversation")
        confirm_dialog.setFixedSize(400, 150)

        # Create a layout for the dialog.
        dialog_layout = QVBoxLayout()

        # Create a label for the confirmation message.
        confirm_label = QLabel("Are you sure you want to start a \nnew conversation? You will lose all \ncontext of the current conversation.")
        confirm_label.setAlignment(Qt.AlignCenter)
        dialog_layout.addWidget(confirm_label)
        
        # Create a layout for the buttons.
        button_layout = QHBoxLayout()

        # Create the 'Yes' button and handle its click event.
        yes_button = CustomButton('Yes')
        yes_button.clicked.connect(lambda: self.start_new_conversation(confirm_dialog))
        button_layout.addWidget(yes_button, alignment=Qt.AlignCenter)

        # Create the 'No' button and handle its click event.
        no_button = CustomButton('No')
        no_button.clicked.connect(confirm_dialog.close)
        button_layout.addWidget(no_button, alignment=Qt.AlignCenter)

        # Add the button layout to the dialog layout.
        dialog_layout.addLayout(button_layout)

        # Set the dialog layout.
        confirm_dialog.setLayout(dialog_layout)

        # Show the dialog.
        confirm_dialog.exec_()
    
    def set_widget_style(self, widget): # BG Color RGB: 244, 224, 244 (Light Purple); Border Color RGB: 192, 192, 192 (Light Gray)
        widget.setStyleSheet("""
            QTextEdit {
            background-color: #E8E8E8;
            border: 1px solid #000000;
            padding: 5px;
            }
        """)
        
    def get_timestamp(self):
        # Get the current date/time.
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return timestamp
    
    def start_new_conversation(self, dialog):
        # Clear the contents of chat_history and user_prompt.
        self.chat_history.clear()
        self.user_prompt.clear()

        # Reset the message history (if needed, depends on how you manage message history).
        self.messages = []

        # Inform the user only once per session if not already informed.
        if hasattr(self, "truncation_warning_given"):
            del self.truncation_warning_given

        # Close the confirmation dialog.
        dialog.close() 
    
    def format_code_snippets(self, response):
        # Define a regular expression pattern to match code snippets.
        code_pattern = re.compile(r'```(.*?)```', re.DOTALL)
        
        # Define a function to format and highlight code snippets.
        def replacer(match):
            code = match.group(1).strip()
            
            try:
                lexer = guess_lexer(code)
            except:
                lexer = TextLexer()
            formatter = HtmlFormatter()
            highlighted_code = highlight(code, lexer, formatter)
            return highlighted_code
        
        # Use the replacer function to replace code snippets with formatted ones.
        formatted_response = code_pattern.sub(replacer, response)
        return formatted_response
    
    def submit_prompt(self):        
        # Check the value of self.combo_box and call the matching function.
        selected_model = self.combo_box.currentText()
        self.submit_to_model(selected_model)
    
    def submit_to_model(self, model_name):        
        # Get the conversation history and user's prompt.
        conversation_history = self.chat_history.toPlainText()
        user_prompt = self.user_prompt.toPlainText()
        
        # Create a list to store messages.
        messages = []
       
        try:
            contextFile = self.file_path_box.text()
            with open(contextFile, 'r') as f:
                context = f.read().splitlines()
                context = [line.strip() for line in context]
                context = str(context)
            messages.append({"role": "user", "content": context})
            self.file_path_box.clear()
        except:
            pass
      
        # Split the conversation history into lines and create messages.
        for line in conversation_history.split('\n'):
            if line.startswith('User: '):
                messages.append({"role": "user", "content": line[6:]})
            elif line.startswith('Assistant: '):
                messages.append({"role": "assistant", "content": line[12:]})

        # Append user's prompt to the messages.
        messages.append({"role": "user", "content": user_prompt})
         
        # Token count check.
        token_count = sum(self.get_token_count(msg["content"]) for msg in messages)

        # Ensure the total token count doesn't exceed 1024 tokens.
        if token_count > 4000:
            # Truncate messages to fit within the 4096-token limit.
            while token_count > 4000 and len(messages) > 1:
                token_count -= self.get_token_count(messages.pop(0)["content"])
            # Inform the user only once per session if not already informed
            if not hasattr(self, "truncation_warning_given"):
                self.chat_history.append("If you are using gpt-3.5-turbo, your message history will now begin to truncate the oldes messages. gpt-4 is rougly half way there.<br><br>")
                self.truncation_warning_given = True
        
        # Check if user's individual prompt exceeds 1024 tokens.
        if self.get_token_count(user_prompt) > 1300:
            self.chat_history.append("Your individual prompt exceeds an estimated 1,024 tokens. Please enter a shorter prompt. Your message history is maintained to the token limit.<br>     {timestamp_style}[{timestamp}]<br>")
            return
        
        try:
            timestamp = self.get_timestamp()
            self.append_to_chat_history("User", user_prompt)
            
            # Call OpenAI API to get model response.
            response = openai.ChatCompletion.create(
                model=model_name,  
                messages=messages,  
                max_tokens=1024
            )
            
            # Append the model's response to the chat history.
            assistant_response = response["choices"][0]["message"]["content"]
            
            # Check the assistant's response for code snippets, and format accordingly.
            formatted_response = self.format_code_snippets(assistant_response)
            self.append_to_chat_history("Assistant", None, formatted_response)

            self.user_prompt.clear()
            
        except openai.error.OpenAIError as e:
            # Display the error message in the chat_history.
            self.append_to_chat_history("Error", str(e))

    def append_to_chat_history(self, role, content, formatted_response=None):
        # Style the timestamp to reduce size and not be so obtrusive in the conversation.
        timestamp_style = """
            <span style="
                font-size: 8pt;     /* Bring Font Size Down */
                color: #808080;     /* Light grey color */
            ">
        """
        
        user_style = """
            <span style="
                font-size: 10pt;     /* Bring Font Size Down */
                font-weight: bold;
                color: #800080;     /* Light grey color */
            ">
        """
        
        assistant_style = """
            <span style="
                font-size: 10pt;     /* Bring Font Size Down */
                font-weight: bold;
                color: black;        /* black color */
            ">
        """
        
        text_style = """
            <span style="
                font-size: 11pt;     /* Bring Font Size Down */
                font-weight: normal;
                color: black;        /* black color */
            ">
        """
        
        role_style = {'User': user_style, 'Assistant': assistant_style}[role]
        timestamp = self.get_timestamp()
        if formatted_response:
            self.chat_history.append(f"{role_style}{role}: </span>{text_style}{formatted_response}</span><br>     {timestamp_style}[{timestamp}]<br>")
        else:
            self.chat_history.append(f"{role_style}{role}: </span>{text_style}{content}</span><br>     {timestamp_style}[{timestamp}]<br>")
 
    def update_chat_token_count(self):
        text = self.chat_history.toPlainText()
        token_count = self.get_token_count(text)
        self.chat_token_count_label.setText(f"Tokens: {token_count}")

    def update_user_prompt_token_count(self):
        text = self.user_prompt.toPlainText()
        token_count = self.get_token_count(text)
        self.user_prompt_token_count_label.setText(f"Tokens: {token_count}")
        
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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())