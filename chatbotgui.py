import tkinter as tk
import openai
import os
from PIL import Image

myKey = os.environ.get("OPENAI_API_KEY")

if myKey is None:
   raise ValueError("OPENAI_API_KEY is not set in environment variables.")
else: 
   openai.api_key = myKey

history = ""
extraContext = 'context2.txt'
with open(extraContext, 'r') as file:
        context = file.read()
        context.strip()
history += f"{context}"

def conversation(prompt, history): 
   response = openai.Completion.create( 
      engine="text-davinci-003",
      prompt=prompt,
      max_tokens=1024,
      n=1,
      stop=None,
      temperature=0.4
   )
   return response.choices[0].text.strip() 

def close_window(event):
    main_window.destroy()

def drag_window(event):
    # Get the current mouse position
    x = main_window.winfo_pointerx()
    y = main_window.winfo_pointery()

    # Calculate the new window position based on the mouse movement
    new_x = x - start_x
    new_y = y - start_y
    main_window.geometry(f"+{new_x}+{new_y}")

def start_drag(event):
    # Record the starting mouse position
    global start_x, start_y
    start_x = event.x
    start_y = event.y

def stop_drag(event):
    pass

# Create the main window
main_window = tk.Tk()
main_window.title("ChatGPT")
main_window.configure(bg='#C5CDD9')
main_window.columnconfigure(2, minsize=20)
main_window.geometry("633x645")
main_window.geometry("+100+200")
main_window.bind("<ButtonPress-1>", start_drag)
main_window.bind("<ButtonRelease-1>", stop_drag)
main_window.bind("<B1-Motion>", drag_window)

# Make the window borderless
main_window.overrideredirect(True)

# Bind the Escape key to close the window
main_window.bind("<Escape>", close_window)

# Create a label with the text "ChatGPT"
label = tk.Label(main_window, text="ChatGPT", font=("Arial Rount MT Bold", 22), bg='#C5CDD9')
label.grid(row=0, column=1, padx=10, pady=10, sticky='w')

# Create the new conversation button
new_conversation_image = tk.PhotoImage(file="images/newconversation.png")
new_conversation_image = new_conversation_image.subsample(8)
new_conversation_button = tk.Label(main_window, image=new_conversation_image, bg='#C5CDD9', highlightthickness=0)
new_conversation_button.bind("<Button-1>", lambda event: new_conversation_command())
new_conversation_button.grid(row=0, column=0, columnspan=4, padx=(10,2), pady=10, sticky='e')
new_conversation_button.config(borderwidth=3, relief="flat")

# Create the history text area
history_text = tk.Text(main_window, height=27, width=65, font=("Ariel Rounded MT", 13))
history_text.grid(row=1, column=1, columnspan=2, padx=(10,2), pady=0)
history_text.config(borderwidth=3, relief="flat", state="disabled")
scrollbar = tk.Scrollbar(main_window)
scrollbar.grid(row=1, column=3, sticky='nsw')
history_text.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=history_text.yview)

# Create the user input entry box
user_input = tk.Text(main_window, width=62, height=2, font=("Ariel Rounded MT", 13))
user_input.grid(row=2, column=1, columnspan=2, padx=(10,5), pady=10, sticky='w')
user_input.config(borderwidth=3, relief="sunken")

# Create the submit button
submit_image = tk.PhotoImage(file="images/sendmessage.png")
submit_image = submit_image.subsample(22)
submit_button = tk.Label(main_window, image=submit_image, bg='#C5CDD9', highlightthickness=0)
submit_button.bind("<Button-1>", lambda event: submit_command(history, user_input.get("1.0", "end-1c")))
submit_button.grid(row=2, column=2, columnspan=4, padx=(10,2), pady=0, sticky='e')
submit_button.config(borderwidth=3, relief="flat")

# Define the submit command
def submit_command(history, userQuery):
    history_text.config(state="normal")
    history_text.insert(tk.END, f"User>> {userQuery}\n")
    prompt = f"{history}User>> {userQuery}\n"
    responseOutput = conversation(prompt, history)
    history_text.insert(tk.END, f"ChatGPT Said>> {responseOutput}\n")
    history_text.config(state="disabled")
    history += f"User Said>> {userQuery}\n {responseOutput}\n"
    user_input.delete("1.0", tk.END)

# Define the new conversation command
def new_conversation_command():
    history_text.config(state="normal")
    history_text.delete('1.0', tk.END)
    history_text.config(state="disabled")
    history = ""
    extraContext = 'context2.txt'

    with open(extraContext, 'r') as file:
        context = file.read()
        context.strip()

    history += f"{context}"

# Run the main loop
main_window.mainloop()