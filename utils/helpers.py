import re
def extract_email(raw):
    match = re.search(r"<(.+?)>", raw)
    if match:
        return match.group(1)
    return raw.strip().replace('"', '')