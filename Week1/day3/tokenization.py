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


prompt1="hi!"
prompt2="explain garud puran in simple and easy way !"
prompt3="write a general view on islamic radiacalization in 1000 words!"

prompts=[prompt1,prompt2,prompt3]
for prompt in prompts:
    message = {
        "role": role,
        "content": prompt
    }

    messages = [ message]
    response = client.chat.completions.create(model=model, messages=messages,max_tokens=100)

    # print(response.choices[0].message.content)
    usage = response.usage
    print(f"Prompt: {prompt} --> prompt tokens used: {usage.prompt_tokens}--> completion tokens used: {usage.completion_tokens},--> total tokens used: {usage.total_tokens} ****finish Reason : {response.choices[0].finish_reason}****")

# prompt = "who is Virat kohli?"

# message = {
#     "role": role,
#     "content": prompt
# }

# messages = [ message]
# response = client.chat.completions.create(model=model, messages=messages,temperature=1)

# print(response.choices[0].message.content)