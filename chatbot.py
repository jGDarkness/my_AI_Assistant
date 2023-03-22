import openai # Import 'openai' module
import os # Import 'os' module

myKey = os.environ.get("OPENAI_API_KEY") # Get API token from environment variables.

if myKey is None: # Test for a properly set environment variable with API token.
   raise ValueError("OPENAI_API_KEY is not set in environment variables.") # Notify the user if their API 
      # token is not set.
else: 
   openai.api_key = myKey # Load the API token into the python module properties.

def conversation(prompt, history): # Define the function "conversation" with a prompt, and previous history.
   response = openai.Completion.create( # Create a new completion with these model parameters.
      engine="text-davinci-003",
      prompt=prompt,
      max_tokens=4096,
      n=1,
      stop=None,
      temperature=0.4
   )
   return response.choices[0].text.strip() # Strip the responses of empty or whitespace characters.

#\033 - This is an ASCII escape sequence which is widely used to format terminal output.

print('\033[31m' + '\n' + "New Completion Established." + '\n' + '\033[0m') # Display a message that the 
   # completion has been established.

history = "" # Establish an empty completion history.

extraContext = 'context2.txt'  # This text file is used to set any large context you want to insert before a 
   # new completion begins.

with open(extraContext, 'r') as file: # Open the extra context file
   context = file.read() # Read the extra context file
   context.strip()  # Strips the file of empty or whitespace characters.
   
history += f"{context}" # Add the additional context to the completion history.

while True:  # Runs the script until terminated.
   userQuery = input('\033[1m' + 'User>> ' + '\033[0m') # Format the user's terminal input.

   if userQuery.lower() in ["exit", "quit", "bye", "goodbye"]: # Test inputs for completion ending commands.
      print ("Goodbye!") # Tells the user "Goodbye!"
      break # Breaks the terminal session.
   
   if userQuery.lower() in ['clear', "new session", "restart", "start over"]: # Test input for reset 
         #completion commands.
      history = "" # Reset completion history.
      os.system("clear") # Clear the terminal for a fresh completion.
      history += f"{context}" # Add the additional context to the completion history.         
      
   else:  
      prompt = f"{history}User>> {userQuery}\n" # Send the completion history + new prompt to the model.
      responseOutput = conversation(prompt, history) # Collect the response.
      print("\033[48;5;250m", end="") # Format the chatbot's terminal output.
      print('\n' + '\033[1;32m' + "ChatGPT Said>> " + responseOutput + '\n' + '\033[0m') # Format the model's 
         # response.
      history += f"User Said>> {userQuery}\n {responseOutput}\n" # append the new prompt to the completion 
         #history.