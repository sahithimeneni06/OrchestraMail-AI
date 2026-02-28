import os
import json
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from backend.token_store import get_user, save_user
from backend.config import SCOPES

config_str = os.getenv("GOOGLE_CLIENT_CONFIG")
if not config_str:
    raise ValueError("GOOGLE_CLIENT_CONFIG not set")

CLIENT_CONFIG = json.loads(config_str)

REDIRECT_URI = os.getenv("REDIRECT_URI")
if not REDIRECT_URI:
    raise ValueError("REDIRECT_URI not set")


def create_flow():
    return Flow.from_client_config(
        CLIENT_CONFIG,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )


def get_gmail_service_for_user(user_email):
    """
    Build an authenticated Gmail API service for the given user.
    Loads token from DB and refreshes if expired.
    """
    token = get_user(user_email)

    if not token:
        raise Exception(f"User {user_email} not found. Please log in again.")

    creds = Credentials(
        token=token["access_token"],
        refresh_token=token["refresh_token"],
        token_uri=token.get("token_uri", "https://oauth2.googleapis.com/token"),
        client_id=token["client_id"],
        client_secret=token["client_secret"],
        scopes=token.get("scopes", [])
    )

    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        token["access_token"] = creds.token
        save_user(user_email, token)

    return build("gmail", "v1", credentials=creds, cache_discovery=False)