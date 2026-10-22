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

def llm_ans(prompt):
    message={
        "role": "user",
        "content": prompt
    }
    messages=[message]
    response = client.chat.completions.create(model=model, messages=messages)
    return response.choices[0].message.content

bad_Prompt="""
this is a user complain:
My Laptop is not working.
classify this
"""
good_Prompt="""
#ROLE: You are a support assistant at a mobile/laptop company
#TASK: Classify the user's complaint in a category.
#CONSTRAINTS: Use only the following categories: "billing", "technical issue", "return".
#OUTPUT FORMAT: Return only the category name given in constraints in lowercase, without any additional text or explanation.
#ONE SHOT EXAMPLE:if user want a refund then the category is "return".
#FALLBACK: If the complaint does not fit any of the categories, return "Not related".
this is a user complain:
My Gf is sad.
"""

# print(llm_ans(bad_Prompt)) 
print("--------------------------------------------------")
print(llm_ans(good_Prompt)) 