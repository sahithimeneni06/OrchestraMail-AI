from utils.prompt_loader import load_prompt
from llm.llm import call_agent1

writer_prompt = load_prompt("prompts/writer_prompt.txt")

def writer_agent(user_intent, recipient_type=None, sender_name="", recipient_name=None, email_context=None):
  user_content = f"""
User Intent:
{user_intent}

Recipient Type:
{recipient_type}

Recipient Name:
{recipient_name if recipient_name else "Not provided"}

Sender Name:
{sender_name}

Original Email Context (for reply, if any):
{email_context if email_context else "None"}
"""
  resp = call_agent1(writer_prompt, user_content)
  return resp

def parse_writer_output(output):
  subject = ""
  email_body = ""
  if "Subject:" in output and "Email:" in output:
    subject = output.split('Subject:')[1].split('Email:')[0].strip()
    email_body = output.split('Email:')[1].strip()
  return {
      'subject' : subject,
      'email_body': email_body,
      'raw_output': output
  }

def writer_agent_pipeline(user_intent, recipient_type=None, sender_name="", recipient_name=None, email_context=None):
  raw_output = writer_agent(user_intent=user_intent,
        recipient_type=recipient_type,
        sender_name=sender_name,
        recipient_name=recipient_name,
        email_context=email_context
    )
  structured_output = parse_writer_output(raw_output)
  return structured_output