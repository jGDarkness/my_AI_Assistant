import openai
import os

myKey = os.environ.get("OPENAI_API_KEY")

if myKey is None:
   raise ValueError("OPENAI_API_KEY is not set in environment variables.")
else: 
   openai.api_key = myKey

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

print('\033[31m' + '\n' + "New Completion Established." + '\n' + '\033[0m') 

history = ""
extraContext = 'context2.txt'

with open(extraContext, 'r') as file:
   context = file.read() 
   context.strip()  
   
history += f"{context}" 

while True:  
   userQuery = input('\033[1m' + 'User>> ' + '\033[0m') 
   if userQuery.lower() in ["exit", "quit", "bye", "goodbye"]: 
      print ("Goodbye!")
      break 
   
   if userQuery.lower() in ['clear', "new session", "restart", "start over"]: 
      history = ""
      os.system("clear")
      history += f"{context}"
      
   else:  
      prompt = f"{history}User>> {userQuery}\n"
      responseOutput = conversation(prompt, history)
      print("\033[48;5;250m", end="")
      print('\n' + '\033[1;32m' + "ChatGPT Said>> " + responseOutput + '\n' + '\033[0m')
      history += f"User Said>> {userQuery}\n {responseOutput}\n" 