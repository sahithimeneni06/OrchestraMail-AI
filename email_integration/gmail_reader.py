import base64

def get_header(headers, name):
    for h in headers:
        if h["name"] == name:
            return h["value"]
    return ""


def extract_body(payload):

    if "parts" in payload:
        for part in payload["parts"]:
            if part["mimeType"] == "text/plain":
                data = part["body"].get("data")
                if data:
                    return base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")

        for part in payload["parts"]:
            if part["mimeType"] == "text/html":
                data = part["body"].get("data")
                if data:
                    return base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")

    else:
        data = payload["body"].get("data")
        if data:
            return base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")

    return ""


def get_email_data(service, msg_id):

    msg = service.users().messages().get(
        userId="me",
        id=msg_id,
        format="full"
    ).execute()

    headers = msg["payload"]["headers"]

    subject = get_header(headers, "Subject")
    sender  = get_header(headers, "From")

    body = extract_body(msg["payload"])

    return {
        "id": msg["id"],
        "threadId": msg["threadId"],
        "from": sender,
        "subject": subject,
        "body": body
    }