import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("GROQ_API_KEY environment variable is not set.")

client = Groq(api_key=my_api_key)

model="openai/gpt-oss-20b"

role = "user"

prompt = "Who is VIRAT KOHLI? how he works in detailed? what is his role in cricket? what is his contribution to cricket?"

message = {
    "role": role,
    "content": prompt
}
messages = [message]
# response1 = client.chat.completions.create(model=model, messages=messages)

# print(response1.choices[0].message.content)

#streamming response

stream_response = client.chat.completions.create(model=model, messages=messages,stream=True)

for chunk in stream_response:
    content=chunk.choices[0].delta.content
    if content:
        print(content,end="",flush=True)


