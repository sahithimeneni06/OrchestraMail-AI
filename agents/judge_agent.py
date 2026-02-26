from utils.prompt_loader import load_prompt
from llm.llm import call_agent2

debate_prompt = load_prompt("prompts/judge_prompt.txt")

def debate_agent(writer_res, tone_res, risk_res, fact_res, formatted_date):

  date_block = formatted_date if formatted_date else "No dates provided"

  user_content = f"""
ORIGINAL EMAIL:

Subject: {writer_res['subject']}

Email:
{writer_res['email_body']}

EXTRACTED DATE RANGE:
{date_block}

TONE FEEDBACK:
{tone_res['raw_output']}

RISK FEEDBACK:
{risk_res['raw_output']}

COMPLETENESS FEEDBACK:
{fact_res['raw_output']}
"""
  response = call_agent2(debate_prompt, user_content)

  return response

def parse_debate_output(debate_output):
  final_subject = ""
  final_email = ""
  summary = ""

  if "Final Subject:" in debate_output:
    final_subject = debate_output.split("Final Subject:")[1].split("Fully Improved Email:")[0].strip()

  if "Fully Improved Email:" in debate_output:
    final_email = debate_output.split("Fully Improved Email:")[1].split("Key Improvements Made:")[0].strip()

  if "Key Improvements Made:" in debate_output:
    summary = debate_output.split("Key Improvements Made:")[1].strip()

  return {
    "final_subject": final_subject,
    "final_email": final_email,
    "summary": summary,
    "raw_output": debate_output
    }

def debate_agent_pipeline(writer_res, tone_res, risk_res, fact_res, formatted_date):
  raw_output = debate_agent(writer_res, tone_res, risk_res, fact_res, formatted_date)
  structured_output = parse_debate_output(raw_output)
  return structured_output