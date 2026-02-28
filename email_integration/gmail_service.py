import os
import json
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from backend.token_store import get_user, save_user
from backend.config import SCOPES

CLIENT_CONFIG = json.loads(os.getenv("GOOGLE_CLIENT_CONFIG"))

REDIRECT_URI = os.getenv("REDIRECT_URI")


def create_flow():
    return Flow.from_client_config(
        CLIENT_CONFIG,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )


def get_auth_url():
    flow = create_flow()

    auth_url, _ = flow.authorization_url(
        prompt="consent",
        access_type="offline",
        include_granted_scopes="false"
    )

    return auth_url, flow.state


def get_token(code):
    flow = create_flow()
    flow.fetch_token(code=code)

    creds = flow.credentials

    return {
        "access_token": creds.token,
        "refresh_token": creds.refresh_token,
        "token_uri": creds.token_uri,
        "client_id": creds.client_id,
        "client_secret": creds.client_secret,
        "scopes": creds.scopes,
        "email": creds.id_token["email"]
    }


def get_gmail_service_for_user(user_email):

    token = get_user(user_email)

    if not token:
        raise Exception("User not authorized")

    creds = Credentials(
        token=token["access_token"],
        refresh_token=token["refresh_token"],
        token_uri="https://oauth2.googleapis.com/token",
        client_id=token["client_id"],
        client_secret=token["client_secret"],
        scopes=token["scopes"]
    )

    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        token["access_token"] = creds.token
        save_user(user_email, token)

    return build("gmail", "v1", credentials=creds, cache_discovery=False)