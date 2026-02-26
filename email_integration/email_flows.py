from .gmail_service import get_gmail_service_for_user
from .gmail_reader import get_email_data
from .gmail_sender import send_reply, send_new_email
from utils.helpers import extract_email
from chain.chain import final_pipeline


def send_new_email_flow(
    user_email,
    to_email,
    user_intent,
    sender_name,
    recipient_type=None,
    recipient_name=None,
    subject_override=None,
    send=False
):
    service = get_gmail_service_for_user(user_email)

    ai_reply = final_pipeline(
        user_intent=user_intent,
        recipient_type=recipient_type,
        sender_name=sender_name,
        recipient_name=recipient_name
    )

    subject = subject_override or ai_reply.get("final_subject")
    email_text = ai_reply.get("final_email", "No Subject")

    if send:
        send_new_email(service, to_email, subject, email_text)

    return {
        "to": to_email,
        "subject": subject,
        "email": email_text
    }


def reply_from_inbox_flow(user_email, max_results=5):

    service = get_gmail_service_for_user(user_email)

    results = service.users().messages().list(
        userId="me",
        labelIds=["INBOX"],
        maxResults=max_results
    ).execute()

    messages = results.get("messages", [])

    emails = [get_email_data(service, m["id"]) for m in messages]

    return emails


# =========================================================
# 🔍 SEARCH THREADS BY EMAIL
# =========================================================
def reply_using_email_flow(user_email, target_email, max_results=5):

    service = get_gmail_service_for_user(user_email)

    results = service.users().messages().list(
        userId="me",
        q=f"(from:{target_email} OR to:{target_email})",
        maxResults=max_results
    ).execute()

    messages = results.get("messages", [])

    return [get_email_data(service, m["id"]) for m in messages]


# =========================================================
# 🤖 GENERATE AI REPLY
# =========================================================
def generate_reply(
    selected_email,
    user_intent,
    sender_name,
    recipient_type=None,
    recipient_name=None
):

    ai_reply = final_pipeline(
        user_intent=user_intent,
        recipient_type=recipient_type,
        sender_name=sender_name,
        recipient_name=recipient_name,
        email_context=selected_email["body"]
    )

    return {
        "to": extract_email(selected_email["from"]),
        "threadId": selected_email["threadId"],
        "original_subject": selected_email["subject"],
        "subject": ai_reply.get("final_subject"),
        "email": ai_reply.get("final_email"),
    }


# =========================================================
# 📤 SEND REPLY
# =========================================================
def send_reply_flow(user_email, reply_data):

    service = get_gmail_service_for_user(user_email)

    send_reply(
        service,
        reply_data["to"],
        reply_data["original_subject"],
        reply_data["email"],
        reply_data["threadId"]
    )

    return {"status": "sent"}