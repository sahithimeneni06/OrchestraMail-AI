from flask import Flask, redirect, request, session, jsonify
from backend.oauth import get_auth_url, get_token
from backend.token_store import save_user, init_db
from dotenv import load_dotenv
from flask_cors import CORS
import os
from token_store import init_db

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev_secret")

app.config.update(
    SESSION_COOKIE_SAMESITE=os.getenv("SESSION_COOKIE_SAMESITE", "Lax"),
    SESSION_COOKIE_SECURE=os.getenv("SESSION_COOKIE_SECURE", "False") == "True"
)

CORS(
    app,
    supports_credentials=True,
    origins=[os.getenv("FRONTEND_URL", "http://localhost:8501")]
)
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:8501")


# 🔐 LOGIN
@app.route("/login")
def login():
    auth_url, state = get_auth_url()

    session.permanent = True
    session["state"] = state

    return redirect(auth_url)

# 🔁 GOOGLE CALLBACK
@app.route("/oauth2callback")
def callback():
    try:
        code = request.args.get("code")

        if not code:
            return "❌ No authorization code received"
        state = request.args.get("state")

        if state != session.get("state"):
            return "State mismatch ❌"
        token = get_token(code)

        if not isinstance(token, dict):
            return f"OAuth Error: {token}"

        user_email = token["email"]

        save_user(user_email, token)
        session["user"] = user_email
        
        return redirect(f"{FRONTEND_URL}/?login=success&user={user_email}")

    except Exception as e:
        return f"❌ OAuth Error: {str(e)}"


# 👤 CURRENT USER
@app.route("/me")
def get_current_user():
    user = session.get("user")

    if user:
        return jsonify({"email": user})

    return jsonify({"email": None}), 401


@app.route("/logout")
def logout():
    session.clear()
    return redirect(FRONTEND_URL)


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))