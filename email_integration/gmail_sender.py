import base64
import re
from email.mime.text import MIMEText


def send_new_email(service, to, subject, message_text):

    message = MIMEText(message_text)
    message["to"] = to
    message["subject"] = subject

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()

    service.users().messages().send(
        userId="me",
        body={"raw": raw}
    ).execute()

def send_reply(service, to, subject, message_text, thread_id):

    message = MIMEText(message_text)
    message["to"] = to
    message["subject"] = "Re: " + subject

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()

    service.users().messages().send(
        userId="me",
        body={"raw": raw, "threadId": thread_id}
    ).execute()