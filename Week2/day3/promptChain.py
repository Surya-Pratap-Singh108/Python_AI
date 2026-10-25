import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
import time

load_dotenv()
my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("GROQ_API_KEY environment variable is not set.")

client = Groq(api_key=my_api_key)

model="openai/gpt-oss-20b"

JD="""
We are hiring a Backend Python Developer.

Requirements:
- Strong Python
- FastAPI or Django
- PostgreSQL
- Docker
- AWS
- REST APIs
- 2+ years of experience
"""
RESUME="""
Name: Rahul Sharma

Experience:
3 years as a Software Developer.

Skills:
Python, FastAPI, MySQL, Docker,
REST APIs, Git

Projects:
Built a food delivery backend using
FastAPI and MySQL.

Deployed applications using Docker.
"""

def ask_llm(system_prompt, user_prompt):
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    response = client.chat.completions.create(model=model, messages=messages)
    return response.choices[0].message.content  

def resume_extract():
    print ("step 1")
    system_prompt = """You are a helpful assistant that extracts relevant information from resumes." \
    Output Format:
    Skills should be separated by commas. Just return comma separated skills do not return any other filler information
    """
    user_prompt = f"Extract the relevant skills and experience from the following resume:\n{RESUME}"
    return ask_llm(system_prompt, user_prompt)

def JD_extract():
    print ("step 2")
    system_prompt = """You are a helpful assistant that extracts relevant information from job descriptions." \
    Output Format:
    Skills should be separated by commas. Just return comma separated skills do not return any other filler information
    """
    user_prompt = f"Extract the relevant skills and experience from the following job description:\n{JD}"
    return ask_llm(system_prompt, user_prompt)

def match_skills(candidate, JD):
    print ("step 3")
    system_prompt = """You are a helpful assistant that matches skills from candidate and job descriptions." nad produce a final score out of 100 also producta short verdice  \

    whether the candidate is suitable for the job or not based on the matching skills.
    output Format:
    Score: <score out of 100>
    Verdict: <suitable or not suitable in short>
    
    """
    user_prompt = f"Compare and match the skills from the following candidate and job description:\nCandidate Skills: {candidate}\nJob Description Skills: {JD}"
    return ask_llm(system_prompt, user_prompt)

candidate_skills = resume_extract()
print("Candidate Skills:", candidate_skills)
print("-------------------")
time.sleep(2)  # Adding a delay to avoid hitting rate limits
job_skills = JD_extract()
print("Job Description Skills:", job_skills)
print("-------------------")


time.sleep(2)  # Adding a delay to avoid hitting rate limits
final_result = match_skills(candidate_skills, job_skills)
time.sleep(2)  # Adding a delay to avoid hitting rate limits
print("Final Result:", final_result)
print("-------------------")
