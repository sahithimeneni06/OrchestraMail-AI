import os
import json
import hashlib
import base64
import secrets
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


def _generate_pkce():
    """Generate a PKCE code_verifier and code_challenge pair."""
    code_verifier = secrets.token_urlsafe(64)
    digest = hashlib.sha256(code_verifier.encode()).digest()
    code_challenge = base64.urlsafe_b64encode(digest).rstrip(b"=").decode()
    return code_verifier, code_challenge


def get_auth_url():
    """
    Returns (auth_url, state, code_verifier).
    Generates a real PKCE code_verifier so Google doesn't reject the token exchange.
    Flask stores code_verifier in session and passes it back in get_token().
    """
    try:
        flow = create_flow()
        code_verifier, code_challenge = _generate_pkce()

        auth_url, state = flow.authorization_url(
            prompt="consent",
            access_type="offline",
            include_granted_scopes="false",
            code_challenge=code_challenge,
            code_challenge_method="S256"
        )
        return auth_url, state, code_verifier
    except Exception as e:
        return str(e), None, None


def get_token(code, code_verifier=None):
    """
    Exchange auth code for tokens using PKCE code_verifier.
    Uses userinfo endpoint for email — creds.id_token is unreliable.
    """
    flow = create_flow()

    # Must pass code_verifier to satisfy Google's PKCE requirement
    flow.fetch_token(code=code, code_verifier=code_verifier)
    creds = flow.credentials

    # userinfo endpoint is reliable across all Google account types
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