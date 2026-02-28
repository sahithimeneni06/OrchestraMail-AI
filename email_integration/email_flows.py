from .oauth import get_gmail_service_for_user
from .gmail_reader import get_email_data
from .gmail_sender import send_reply, send_new_email
from utils.helpers import extract_email
from chain.chain import final_pipeline


def send_new_email_flow(
    user_email,
    to_email,
    user_intent=None,
    sender_name=None,
    recipient_type=None,
    recipient_name=None,
    subject_override=None,
    body_override=None,     # FIX: added — used when sending the edited draft
    send=False
):
    """
    Two modes:
    1. Generate mode (send=False): run AI pipeline, return draft for user to review.
    2. Send mode (send=True): skip AI, use subject_override + body_override directly.
    """
    service = get_gmail_service_for_user(user_email)

    if send and subject_override and body_override:
        # User already reviewed and edited the draft — just send it
        send_new_email(service, to_email, subject_override, body_override)
        return {"status": "sent"}

    # Generate a fresh draft via AI
    ai_reply = final_pipeline(
        user_intent=user_intent,
        recipient_type=recipient_type,
        sender_name=sender_name,
        recipient_name=recipient_name or ""
    )

    subject = subject_override or ai_reply.get("final_subject", "")
    email_text = ai_reply.get("final_email", "")

    if send:
        send_new_email(service, to_email, subject, email_text)
        return {"status": "sent"}

    return {
        "to": to_email,
        "subject": subject,
        "email": email_text
    }


def reply_from_inbox_flow(user_email, max_results=100):
    """Fetch the latest N emails from the inbox."""
    service = get_gmail_service_for_user(user_email)

    results = service.users().messages().list(
        userId="me",
        labelIds=["INBOX"],
        maxResults=max_results
    ).execute()

    messages = results.get("messages", [])
    return [get_email_data(service, m["id"]) for m in messages]


def reply_using_email_flow(user_email, target_email, max_results=100):
    """Search all threads involving a specific email address."""
    service = get_gmail_service_for_user(user_email)

    results = service.users().messages().list(
        userId="me",
        q=f"(from:{target_email} OR to:{target_email})",
        maxResults=max_results
    ).execute()

    messages = results.get("messages", [])
    return [get_email_data(service, m["id"]) for m in messages]


def generate_reply(
    selected_email,
    user_intent,
    sender_name,
    recipient_type=None,
    recipient_name=None
):
    """Generate an AI reply for a selected email thread."""
    ai_reply = final_pipeline(
        user_intent=user_intent,
        recipient_type=recipient_type,
        sender_name=sender_name,
        recipient_name=recipient_name or "",
        email_context=selected_email.get("body", "")
    )

    return {
        "to": extract_email(selected_email.get("from", "")),
        "threadId": selected_email.get("threadId", ""),
        "original_subject": selected_email.get("subject", ""),
        "subject": ai_reply.get("final_subject", ""),
        "email": ai_reply.get("final_email", ""),
    }


def send_reply_flow(user_email, reply_data):
    """Send a reply to an existing thread."""
    service = get_gmail_service_for_user(user_email)

    send_reply(
        service,
        reply_data["to"],
        reply_data["original_subject"],
        reply_data["email"],
        reply_data["threadId"]
    )

    return {"status": "sent"}