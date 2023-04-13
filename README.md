# OpenAI Chatbot
 A Python-based implementation of a chatbot based on OpenAI's ChatCompletion models.

## Python Bindings
   - datetime
   - openai
   - os
   - pygments
   - PyQt5
   - re
   - sys
   - transformers

## App UI Structure

   - PyQt5 GUI Objects, Widgets, and Classes, or Custom-coded Class Objects
      - QApplication
         - 'central_widget' QWidget()
            - 'main_layout' QVBoxLayout()
               - 'banner' QWidget()
                  - 'banner_layout' QHBoxLayout()
                     - 'banner_label' QLabel()
                     - 'minimize_button' class create_button()
                     - 'maximize_button' class create_button()
                     - 'close_button' class create_button()
               - 'openai_model_layout' QHBoxLayout()
                  - 'combo_box' QComboBox()
               - 'chat_history_container' QWidget()
                  - 'chat_history_layout' QVBoxLayout()
                     - 'chat_scroll_bar' QScrollBar()
                     - 'chat_token_count_layout QHBoxLayout()
                        - chat_token_count_label class create_label()
               - 'file_selector_layout' QHBoxLayout()
                  - 'file_path_box' QLineEdit()
                  - 'clear_button' Class CustomButton()
                  - 'browse_button' Class CustomButton()
               - 'user_prompt_container' QWidget()
                  - 'user_prompt' QVBoxLayout()
                     - 'user_prompt' QTextEdit()
                     - 'user_prompt_scroll_bar' QScrollBar()
                     - 'user_prompt_token_count_label class create_label()
               - 'button_layout' QHBoxLayout()
                  - 'new_button' Class CustomButton()
                  - 'submit_button' Class CustomButton()

## App Code Structure

   - OpenAI API Configuration
   
   - class CustomButton(QPushButton) - serves as a button style template, that can be used over and over when buttons are needed in the app.
      - def __init__(self, text, parent=None) - initializes the instance and sets the height and width of the buttons
      - def paintEvent(self, event) - sets the button color, font attributes, and alignment, and draws the button.
   
   - class MouseHandler - handles specific mouse events for UI manipulation
      - def __init__(self) - initializes the instance
      - def handle_mouse_press(self, event) - handles left mouse button press
      - def handle_mouse_move(self, event, target_widget) - handles moving the app's position
      - def handle_mouse_release(self,event) - handles left mouse button release