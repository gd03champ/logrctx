import ollama

def chat(messages, stream=False, model='phi3'):
    response =  ollama.chat(model=model, messages=messages, stream=stream)
    if stream:
        for chunk in response:
            print(chunk['message']['content'], end='', flush=True)
    return response


messages = []

while True:

  query = {
      "role": "user", 
      "content": input("\nQuery: ")
      }
  
  if query["content"] == "exit":
      break
  
  messages.append(query)

  chat(messages=messages, stream=False, model='phi3')