import os
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from dotenv import load_dotenv
from config import SCOPES

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CLIENT_SECRET_FILE = os.path.join(
    BASE_DIR, "..", "data", "client_secret_589113071583-ua6c3u59nfq3md8798jb6vo637irjp34.apps.googleusercontent.com.json"
)

REDIRECT_URI = "http://localhost:5000/oauth2callback"


def create_flow():
    return Flow.from_client_secrets_file(
        CLIENT_SECRET_FILE,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )

def get_auth_url():
    flow = create_flow()

    auth_url, state = flow.authorization_url(
        prompt="consent",
        access_type="offline",
        include_granted_scopes="false"
    )

    return auth_url, state


def get_token(code):
    flow = create_flow()
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