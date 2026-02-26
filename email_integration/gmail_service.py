import os
from google_auth_oauthlib.flow import Flow
from dotenv import load_dotenv
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from backend.token_store import get_user 
from google.auth.transport.requests import Request
from backend.token_store import save_user
from backend.config import SCOPES

load_dotenv()

CLIENT_SECRET_FILE = "data/client_secret_589113071583-ua6c3u59nfq3md8798jb6vo637irjp34.apps.googleusercontent.com.json"


REDIRECT_URI = "http://localhost:5000/oauth2callback"


def get_auth_url():
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRET_FILE,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )

    auth_url, _ = flow.authorization_url(
        prompt="consent",
access_type="offline",
include_granted_scopes="false"
    )

    return auth_url


def get_token(code):

    flow = Flow.from_client_secrets_file(
        CLIENT_SECRET_FILE,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )

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
        raise Exception("User not authorized. Please login again.")

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