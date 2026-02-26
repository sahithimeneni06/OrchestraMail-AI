from flask import Flask, redirect, request, session, jsonify
from oauth import get_auth_url, get_token
from token_store import save_user
from dotenv import load_dotenv
from flask_cors import CORS
import os
from token_store import init_db

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev_secret")

app.config.update(
    SESSION_COOKIE_SAMESITE="None",
    SESSION_COOKIE_SECURE=True
)

CORS(
    app,
    supports_credentials=True,
    origins=[
        "https://orchestramail-ai-1.onrender.com"
    ]
)
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

        return redirect(f"https://orchestramail-ai-1.onrender.com/?login=success&user={user_email}")

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
    return redirect("https://orchestramail-ai-1.onrender.com")


if __name__ == "__main__":
    init_db()
    app.run(port=5000, debug=False)