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

# structure in json format
from pydantic import BaseModel

class PersonalInfo(BaseModel):
    name: str
    profession: str
    experience_years: int
    email: str

schema = PersonalInfo.model_json_schema()

response_format = {
    "type": "json_object",
}
system_prompt = f"""
extraact the personal info from the ticket strictly based on the following schema: {schema}

"""
message_system = {
    "role": "system",
    "content": system_prompt
}
text = "Hello! my name is Surya and I am a software engineer. I have been working in the field of software development for over 5 years. I specialize in web development and have experience with various programming languages and frameworks. In my free time, I enjoy reading tech blogs, contributing to open-source projects, and exploring new technologies. my email is surya@example.com "

prompt = f"""
this is a customer ticket, please extract the personal info from the text and return it in a json format.The text is: {text}
"""

message = {
    "role": role,
    "content": prompt
}
messages = [message_system, message]
response = client.chat.completions.create(model=model, messages=messages,response_format=response_format)

answer=response.choices[0].message.content

import json
raw_json=answer

data_file=json.loads(raw_json)
info=PersonalInfo(**data_file)

print(info)
print(info.email)
print(info.name)