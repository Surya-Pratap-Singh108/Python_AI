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

prompt = "suggest a name for my new food company."

message_system = {
    "role": "system",
    "content": "You are my brand manager. suggestme a single name for my new food company. name should be in one word"
}

message = {
    "role": role,
    "content": prompt
}

messages = [message_system, message]
response = client.chat.completions.create(model=model, messages=messages,temperature=1)

print(response.choices[0].message.content)