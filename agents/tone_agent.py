from utils.prompt_loader import load_prompt
from llm.llm import call_agent1

tone_prompt = load_prompt("prompts/tone_prompt.txt")


def tone_agent(sub_email, body_email):
  user_content = f"""
  Analyze the tone of the following email.
  subject : {sub_email}
  Email :
  {body_email}
  """
  resp = call_agent1(tone_prompt, user_content)
  return resp

def parse_tone_output(output):
  tone = ""
  issues = []
  if 'Tone:' in output and 'Issues:' in output:
    tone = output.split('Tone:')[1].split('Issues:')[0].strip()
    issue = output.split('Issues:')[1].strip()
    if issue!="None":
      issues = issue
  return {
      "tone": tone,
      "issues": issues,
      "raw_output":output
  }

def tone_agent_pipeline(writer_res):
  resp = tone_agent(writer_res['subject'], writer_res['email_body'])
  structured_output = parse_tone_output(resp)
  return structured_output