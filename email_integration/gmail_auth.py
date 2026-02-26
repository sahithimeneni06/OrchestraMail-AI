from google_auth_oauthlib.flow import InstalledAppFlow
import pickle

SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]

flow = InstalledAppFlow.from_client_secrets_file(
    "data/client_secret.json",
    SCOPES
)
flow.redirect_uri = "urn:ietf:wg:oauth:2.0:oob"

auth_url, _ = flow.authorization_url(prompt="consent")
print(auth_url)

code = input("Enter the authorization code: ")
flow.fetch_token(code=code)

creds = flow.credentials

with open("data/token.pkl", "wb") as f:
    pickle.dump(creds, f)