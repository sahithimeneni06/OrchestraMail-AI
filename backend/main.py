from flask import Flask, redirect, request, session, jsonify
from backend.oauth import get_auth_url, get_token
from backend.token_store import save_user, init_db
from dotenv import load_dotenv
from flask_cors import CORS
import os
from email_integration.email_flows import (
    send_new_email_flow,
    reply_from_inbox_flow,
    reply_using_email_flow,
    generate_reply,
    send_reply_flow
)
load_dotenv()

FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:8501")

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev_secret")
init_db()
app.config.update(
    SESSION_COOKIE_SAMESITE=os.getenv("SESSION_COOKIE_SAMESITE", "Lax"),
    SESSION_COOKIE_SECURE=os.getenv("SESSION_COOKIE_SECURE", "False") == "True"
)

CORS(app, supports_credentials=True, origins=[FRONTEND_URL])

@app.route("/")
def health():
    return "Backend running ✅"

def require_login():
    user = session.get("user")
    if not user:
        return None, (jsonify({"error": "Not logged in"}), 401)
    return user, None

@app.route("/login")
def login():
    auth_url, state = get_auth_url()

    if state is None:
        return auth_url   
    session["state"] = state
    session.permanent = True
    return redirect(auth_url)

@app.route("/oauth2callback")
def callback():
    try:
        code = request.args.get("code")
        state = request.args.get("state")

        if not code:
            return "❌ No authorization code received"

        if state != session.get("state"):
            return "State mismatch ❌"

        token = get_token(code)
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

@app.route("/generate-email", methods=["POST"])
def generate_email():
    user, err = require_login()
    if err:
        return err

    data = request.json

    result = send_new_email_flow(
        user_email=user,
        to=data["to"],
        user_intent=data["intent"],
        sender_name=data["sender"],
        recipient_type=data["recipient_type"],
        recipient_name=data.get("recipient_name", "")
    )

    return jsonify(result)

@app.route("/send-email", methods=["POST"])
def send_email():
    user, err = require_login()
    if err:
        return err

    data = request.json

    send_new_email_flow(
        user_email=user,
        to=data["to"],
        user_intent="",
        sender_name="",
        recipient_type="",
        recipient_name="",
        subject_override=data["subject"],
        body_override=data["body"],
        send=True
    )

    return jsonify({"status": "sent"})

@app.route("/inbox", methods=["GET"])
def inbox():
    user, err = require_login()
    if err:
        return err

    emails = reply_from_inbox_flow(user, 100)

    return jsonify(emails)

@app.route("/search", methods=["POST"])
def search_email():
    user, err = require_login()
    if err:
        return err

    data = request.json

    emails = reply_using_email_flow(
        user_email=user,
        target_email=data["email"],
        max_results=100
    )

    return jsonify(emails)

@app.route("/generate-reply", methods=["POST"])
def generate_ai_reply():
    user, err = require_login()
    if err:
        return err

    data = request.json

    result = generate_reply(
        selected_email=data["selected_email"],
        user_intent=data["intent"],
        sender_name=data["sender"],
        recipient_type=data["recipient_type"],
        recipient_name=data.get("recipient_name", "")
    )

    return jsonify(result)

@app.route("/send-reply", methods=["POST"])
def send_reply():
    user, err = require_login()
    if err:
        return err

    data = request.json

    send_reply_flow(user, data)

    return jsonify({"status": "reply sent"})



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)