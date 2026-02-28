import os
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from dotenv import load_dotenv
from backend.config import SCOPES

load_dotenv()

REDIRECT_URI = os.getenv("REDIRECT_URI")
if not REDIRECT_URI:
    raise ValueError("REDIRECT_URI not set")


def create_flow():
    client_config = {
        "web": {
            "client_id": os.environ["GOOGLE_CLIENT_ID"],
            "client_secret": os.environ["GOOGLE_CLIENT_SECRET"],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
        }
    }

    return Flow.from_client_config(
        client_config,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI,
    )


def get_auth_url():
    flow = create_flow()

    auth_url, state = flow.authorization_url(
        prompt="consent",
        access_type="offline",
        include_granted_scopes="false"
    )

    return auth_url, state, flow.code_verifier

def get_token(code,code_verifier):
    flow = create_flow()
    flow.code_verifier = code_verifier
    flow.fetch_token(code=code)

    creds = flow.credentials

    oauth2 = build("oauth2", "v2", credentials=creds)
    user_info = oauth2.userinfo().get().execute()

    return {
        "access_token": creds.token,
        "refresh_token": creds.refresh_token,
        "client_id": creds.client_id,
        "client_secret": creds.client_secret,
        "scopes": creds.scopes,
        "email": user_info["email"]
    }
