from text_to_speech import chatgpt

with open('./prompts/custom_prompt.txt') as file:
    prompt = file.read()

response = chatgpt(prompt=prompt)
print(response)