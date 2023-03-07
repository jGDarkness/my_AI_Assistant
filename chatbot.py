import openai

openai.api_key = "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"

def conversation(prompt, history):
   response = openai.Completion.create(
      engine="text-davinci-003",
      prompt=prompt,
      max_tokens=1024,
      n=1,
      stop=None,
      temperature=0.7
   )
   return response.choices[0].text.strip()

print('\033[31m' + '\n' + "New Conversation Established." + '\n' + '\033[0m')
history = ""
while True:
   userQuery = input('\033[1m' + 'You said> ' + '\033[0m')
   if userQuery.lower() in ["exit", "Exit", "quit", "Quit", "bye", "Bye", "goodby", "Goodbye"]:
      print ("Goodbye!")
      break
   else:
      prompt = f"{history}You said: {userQuery}\n"
      responseOutput = conversation(prompt, history)
      print('\n' + '\033[1;32m' + 'ChatGPT said> ' + responseOutput + '\n' + '\033[0m')
      history += f"You said> {userQuery}\n {responseOutput}\n"