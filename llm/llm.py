import os 
from groq import Groq
from dotenv import load_dotenv
load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def call_agent1(sys_prompt, user_content):
  return client.chat.completions.create(
      model = 'llama-3.1-8b-instant', temperature=0.3,
      messages = [
          {'role':'system', 'content': sys_prompt},
          {'role':'user', 'content': user_content},
      ]
  ).choices[0].message.content

def call_agent2(sys_prompt, user_content):
  return client.chat.completions.create(
      model = 'llama-3.3-70b-versatile', temperature=0.3,
      messages = [
          {'role':'system', 'content': sys_prompt},
          {'role':'user', 'content': user_content},
      ]
  ).choices[0].message.content