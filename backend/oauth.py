import os
import json
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
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


def get_auth_url():
    """
    Returns (auth_url, state, None).
    Flask unpacks all three — None is for code_verifier (no PKCE used).
    """
    try:
        flow = create_flow()
        auth_url, state = flow.authorization_url(
            prompt="consent",
            access_type="offline",
            include_granted_scopes="false"
        )
        return auth_url, state, None
    except Exception as e:
        return str(e), None, None


def get_token(code, code_verifier=None):
    """
    Exchange auth code for tokens and return a dict.
    Uses userinfo endpoint for email — creds.id_token is unreliable.
    """
    flow = create_flow()
    flow.fetch_token(code=code)
    creds = flow.credentials

    # userinfo endpoint is reliable — id_token["email"] crashes randomly
    oauth2_service = build("oauth2", "v2", credentials=creds)
    user_info = oauth2_service.userinfo().get().execute()

    return {
        "access_token": creds.token,
        "refresh_token": creds.refresh_token,
        "token_uri": "https://oauth2.googleapis.com/token",
        "client_id": creds.client_id,
        "client_secret": creds.client_secret,
        "scopes": list(creds.scopes) if creds.scopes else [],
        "email": user_info["email"]
    }