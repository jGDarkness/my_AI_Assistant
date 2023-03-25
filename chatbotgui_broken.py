### MODULE CONFIGURATION ###
###########################################################################################################################################################################

# Listed alphabetically
import json
from PIL import Image # PIL is deprecated and instead Pillow is installed, but still referenced as 'PIL'
import tkinter as tk
import openai
import os

###########################################################################################################################################################################
### END MODULE CONFIGURATION





### GLOBAL VARIABLES ###
###########################################################################################################################################################################

bgColor = '#C5CDD9'
windowDimensions = "750x800"

###########################################################################################################################################################################
### END GLOBAL VARIABLES ###





### API CONFIGURATION ###
###########################################################################################################################################################################

# API KEYS
myOpenAIKey = os.environ.get("OPENAI_API_KEY")
myOpenAIOrg = os.environ.get("OPENAI_API_ORG")

if myOpenAIKey is None:
   raise ValueError("OPENAI_API_KEY is not set in environment variables.")
else: 
   openai.api_key = myOpenAIKey
   openai.organization = myOpenAIOrg
   
# API LIST Functions
## OpenAI Models
openai_model_response = openai.Model.list()
openai_model_data = json.loads(str(openai_model_response))
openai_models = openai_model_data["data"]
openai_model_names = [model["id"] for model in openai_models] # List comprehension

###########################################################################################################################################################################
### END API CONFIGURATION ###





### OpenAI COMPLETION CONFIGURATION ###
########################################################################################################################################################################

# Provide Extra Context to the Model
extra_context_file = 'context2.txt'

# 'text-davinci-003'
class txtDavinci003:
    def __init__(self, extra_context_file):
        self.engine = "text-davinci-003"
        self.max_tokens = 1024
        self.n = 1
        self.stop = None
        self.temperature = 0.4
        
        with open(extra_context_file, 'r') as file:
            self.context = file.read().strip()
        
    def completion(self, prompt):
        prompt_with_context = f"{self.context}{prompt}"
        response = openai.Completion.create(
            engine=self.engine,
            prompt=prompt_with_context,
            max_tokens=self.max_tokens,
            n=self.n,
            stop=self.stop,
            temperature=self.temperature
        )
        return response.choices[0].text.strip()

########################################################################################################################################################################
### End OpenAI COMPLETION CONFIGURATION ###





### MAIN WINDOW CONFIGURATION ###
###########################################################################################################################################################################

# Close the application window
def close_window(event):
    main_window.destroy()

# Drag the application window
def drag_window(event):
    # Get the current mouse position
    x = main_window.winfo_pointerx()
    y = main_window.winfo_pointery()

    # Calculate the new window position based on the mouse movement
    new_x = x - start_x
    new_y = y - start_y
    main_window.geometry(f"+{new_x}+{new_y}")

# Start of Dragging
def start_drag(event):
    # Record the starting mouse position
    global start_x, start_y
    start_x = event.x
    start_y = event.y

# End of Dragging
def stop_drag(event):
    pass

# Create the application window
main_window = tk.Tk()
main_window.title("ChatGPT")
main_window.configure(bg=bgColor)
main_window.columnconfigure(2, minsize=20)
main_window.geometry(windowDimensions)
main_window.geometry("+100+200")
main_window.bind("<ButtonPress-1>", start_drag)
main_window.bind("<ButtonRelease-1>", stop_drag)
main_window.bind("<B1-Motion>", drag_window)

# Make the window borderless
main_window.overrideredirect(True)

# Bind the Escape key to close the window
main_window.bind("<Escape>", close_window)

###########################################################################################################################################################################
### END MAIN WINDOW CONFIGURATION ###





### TKINTER GRID CONFIGURATION ###
###########################################################################################################################################################################
# ROW [0]:>>        COL[0]: <EMPTY>             COL[1]: Logo Label              COL[2]: Logo Label (spanned)        COL[3]: New Button      COL[4]: New Button (spanned)
###########################################################################################################################################################################
# Set up the OpenAI model selection variable
selected_openai_model = tk.StringVar(main_window)
selected_openai_model.set(openai_model_names[18])   # Indexed [18] by default to 'text-davinci-003'
def on_select(value):
    return f"{value}"

# COL[0]: <EMPTY>

# COL[1]: Logo Label
label = tk.Label(main_window, text="ChatGPT", font=("Arial Rount MT Bold", 22), bg=bgColor)
label.grid(row=0, column=1, columnspan=2, padx=10, pady=10, sticky='w')

# COL[2]: Logo Label (spanned)

# COL[3]: New Button
new_completion_image = tk.PhotoImage(file="images/newcompletion.png")
new_completion_image = new_completion_image.subsample(8)
new_completion_button = tk.Label(main_window, image=new_completion_image, bg=bgColor, highlightthickness=0)
new_completion_button.grid(row=0, column=3, columnspan=2, padx=(10,2), pady=10, sticky='e')
new_completion_button.config(borderwidth=3, relief="flat")

if selected_openai_model.get == 'text-davinci-003':
    new_completion_button.bind("<Button-1>", lambda event: new_completion_command(txtDavinci003(extra_context_file)))

# COL[4]: New Button (spanned)

###########################################################################################################################################################################
# ROW [1]:>>         COL[0]: OpenAI Model       COL[1]: OpenAI Model (spanned)      COL[2]: <EMPTY>                    COL[3]: <EMPTY>       COL[4]: <EMPTY>
###########################################################################################################################################################################

# COL[0]: OpenAI Model
openai_menu = tk.OptionMenu(main_window, selected_openai_model, *openai_model_names, command=on_select, )
openai_menu.config(font=("Arial Rounded MT", 12), width=18, height=1, anchor='w', padx=10, bg='white')
openai_menu.grid(row=1, column=0, columnspan=2)

# COL[1]: OpenAI Model (spanned)

# COL[2]: <EMPTY>

# COL[3]: <EMPTY>

# COL[4]: <EMPTY>

###########################################################################################################################################################################
# ROW [2]:>>         COL[0]: <EMPTY>           COL[1]: Chat History                 COL[2]: Chat History (spanned)     COL[3]: Scrollbar    COL[4]: <EMPTY>
###########################################################################################################################################################################

# COL[0]: <EMPTY>

# COL[1]: Chat History
history_text = tk.Text(main_window, height=28, width=65, font=("Ariel Rounded MT", 13))
history_text.grid(row=2, column=1, columnspan=2, padx=(10,2), pady=(10,0))
history_text.config(borderwidth=3, relief="flat", state="disabled")

# COL[2]: Chat History (spanned)

# COL[3]: Scrollbar
scrollbar = tk.Scrollbar(main_window)
scrollbar.grid(row=2, column=3, sticky='nsw')
history_text.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=history_text.yview)
history_text.config(yscrollcommand=scrollbar.set)

# COL[4]: <EMPTY>

###########################################################################################################################################################################
# ROW [3]:>>         COL[0]: <EMPTY>           COL[1]: User Input                    COL[2]: User Input (spanned)     COL[3]: Submit Button COL[4]: Submit Button (spanned)
###########################################################################################################################################################################

# COL[0]: <EMPTY>

# COL[1]: User Input
user_input = tk.Text(main_window, width=62, height=2, font=("Ariel Rounded MT", 13))
user_input.grid(row=3, column=1, columnspan=2, padx=(10,5), pady=10, sticky='w')
user_input.config(borderwidth=3, relief="sunken")

# COL[2]: User Input (spanned)

# COL[3]: Submit Button
submit_image = tk.PhotoImage(file="images/sendmessage.png")
submit_image = submit_image.subsample(22)
submit_button = tk.Label(main_window, image=submit_image, bg=bgColor, highlightthickness=0)
submit_button.grid(row=3, column=3, columnspan=2, padx=(15,2), pady=0, sticky='e')
submit_button.config(borderwidth=3, relief="flat")

if selected_openai_model.get == 'text-davinci-003':
    history = txtDavinci003(extra_context_file)
    submit_button.bind("<Button-1>", lambda event: submit_command(history, user_input.get("1.0", "end-1c")))

# COL[4]: Submit Button (spanned)

########################################################################################################################################################################
### END TKINTER GRID CONFIGURATION ###





### APPLICATION CONFIGURATION ###
########################################################################################################################################################################

# Submit command to OpenAI API handler
def submit_command(history, userQuery):
    history_text.config(state="normal")
    history_text.insert(tk.END, f"User>> {userQuery}\n")
    prompt = f"User>> {userQuery}\n"
    responseOutput = txtDavinci003.completion(prompt)
    history_text.insert(tk.END, f"ChatGPT Said>> {responseOutput}\n")
    history_text.config(state="disabled")
    history += f"User Said>> {userQuery}\n {responseOutput}\n"
    user_input.delete("1.0", tk.END)

# Create a new completion
def new_completion_command(modelName):
    history_text.config(state="normal")
    history_text.delete('1.0', tk.END)
    history_text.config(state="disabled")
    history = ""
    history = modelName

# Run the main loop
main_window.mainloop()

### APPLICATION CONFIGURATION ###
########################################################################################################################################################################