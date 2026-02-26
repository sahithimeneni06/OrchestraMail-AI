from utils.prompt_loader import load_prompt
from llm.llm import call_agent2

fact_prompt = load_prompt("prompts/fact_prompt.txt")

def fact_agent(email_sub, email_body):
  user_content = f"""
    Audit the following for completeness and clarity.
    Subject : {email_sub}
    Email : {email_body}
  """
  resp = call_agent2(fact_prompt, user_content)
  return resp

def parse_fact_output(writer_res):
  score = ""
  missing_elements = []
  if "Completeness Score:" in writer_res and "Missing or Unclear Elements:" in writer_res:
    score = writer_res.split('Completeness Score:')[1].split('Missing or Unclear Elements:')[0].strip()
    missing = writer_res.split('Missing or Unclear Elements:')[1].strip()
    if missing != 'None':
      missing_elements = missing
  return {
      'completeness_score':score,
      'missing_elements':missing_elements,
      'raw_output':writer_res
  }

def fact_agent_pipeline(writer_res):
  resp = fact_agent(writer_res['subject'], writer_res['email_body'])
  structured_output = parse_fact_output(resp)
  return structured_output