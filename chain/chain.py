from agents.tone_agent import tone_agent_pipeline
from agents.fact_agent import fact_agent_pipeline
from agents.judge_agent import debate_agent_pipeline
from agents.writer_agent import writer_agent_pipeline
from agents.risk_agent import risk_agent_pipeline
from utils.extract_date import extract_dates, format_date_range

def final_pipeline(user_intent, recipient_type=None, sender_name=None, recipient_name=None, email_context=None):

  date_info = extract_dates(user_intent)

  formatted_date = None
  if date_info:
    formatted_date = format_date_range(date_info)

  writer_res = writer_agent_pipeline(
        user_intent=user_intent,
        recipient_type=recipient_type,
        sender_name=sender_name,
        recipient_name=recipient_name,
        email_context = email_context
    )

  tone_res = tone_agent_pipeline(writer_res)
  risk_res = risk_agent_pipeline(writer_res)
  fact_res = fact_agent_pipeline(writer_res)

  debate_res = debate_agent_pipeline(
        writer_res, tone_res, risk_res, fact_res, formatted_date
    )

  return debate_res