from utils.prompt_loader import load_prompt
from llm.llm import call_agent2

risk_prompt = load_prompt("prompts/risk_prompt.txt")

def risk_agent(email_sub, email_body):
  user_content = f"""
  Analyze professional risks and challenges in the forllowing email.
  Subject: {email_sub}
  Email: {email_body}
  """
  resp = call_agent2(risk_prompt, user_content)
  return resp

def risk_output_parser(output):
    risk_level = ""
    risk = "None"
    risks = []

    if "Risk Level:" in output and "Risks:" in output:
        risk_level = output.split("Risk Level:")[1].split("Risks:")[0].strip()
        risk = output.split("Risks:")[1].strip()

        if risk != "None":
            risks = risk

    return {
        "risk_level": risk_level,
        "risk": risk,
        "raw_output": output
    }

def risk_agent_pipeline(writer_res):
  resp = risk_agent(writer_res['subject'], writer_res['email_body'])
  structured_output = risk_output_parser(resp)
  return structured_output