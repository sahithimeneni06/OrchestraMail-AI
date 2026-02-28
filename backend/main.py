from flask import Flask, redirect, request, session, jsonify
from backend.token_store import save_user, init_db
from dotenv import load_dotenv
from flask_cors import CORS
import os
import traceback

load_dotenv()

FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:8501").rstrip("/")  # FIX 4: strip trailing slash

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")  # FIX 3: no insecure default — will raise if missing
if not app.secret_key:
    raise RuntimeError("SECRET_KEY environment variable is not set. Set it to a long random string.")

# FIX 1 + 2: Cross-origin Streamlit → Flask requires SameSite=None + Secure=True.
# These MUST be set as env vars on Render. Default "Lax" blocks the cookie entirely
# when frontend and backend are on different domains.
app.config.update(
    SESSION_COOKIE_SAMESITE="None",      # FIX 1: hardcode None for cross-origin
    SESSION_COOKIE_SECURE=True,          # FIX 2: hardcode True (Render is always HTTPS)
    SESSION_COOKIE_HTTPONLY=True,        # FIX 5 (new): prevent JS access to cookie
    PERMANENT_SESSION_LIFETIME=86400 * 7 # FIX 6 (new): 7 days, not browser-session only
)

# FIX 4b: allow_headers needed so JSON POSTs from requests.Session work cross-origin
CORS(app,
     supports_credentials=True,
     origins=[FRONTEND_URL],
     allow_headers=["Content-Type", "Authorization"],
     methods=["GET", "POST", "OPTIONS"]
)

db_initialized = False

@app.before_request
def ensure_db():
    global db_initialized
    if not db_initialized:
        init_db()
        db_initialized = True

@app.errorhandler(Exception)
def handle_exception(e):
    """Catch ALL unhandled exceptions and return JSON with full traceback.
    This replaces Flask's default HTML 500 page so Streamlit can show
    the real error message."""
    traceback.print_exc()
    return jsonify({
        "error": str(e),
        "type": type(e).__name__,
        "trace": traceback.format_exc()
    }), 500

@app.errorhandler(500)
def handle_500(e):
    traceback.print_exc()
    return jsonify({
        "error": str(e),
        "type": "InternalServerError",
        "trace": traceback.format_exc()
    }), 500


@app.route("/")
def health():
    return "Backend running"

@app.route("/debug")
def debug():
    """Call this from Streamlit to verify the X-User-Email header is arriving."""
    from backend.token_store import get_user
    email = request.headers.get("X-User-Email")
    has_token = bool(get_user(email)) if email else False
    return jsonify({
        "x_user_email": email,
        "has_token_in_db": has_token,
        "session_user": session.get("user"),
    })

def require_login():
    """
    Identify the caller from the X-User-Email header sent by Streamlit.
    """
    user = request.headers.get("X-User-Email")
    if not user:
        return None, (jsonify({"error": "Not logged in — X-User-Email header missing"}), 401)
    # Verify this email actually has a token in our DB (prevents spoofing)
    from backend.token_store import get_user
    if not get_user(user):
        return None, (jsonify({"error": f"No token found for {user}. Please log in again."}), 401)
    return user, None


# LOGIN
@app.route("/login")
def login():
    from backend.oauth import get_auth_url
    auth_url, state, code_verifier = get_auth_url()

    if state is None:
        # auth_url contains the error message in this case
        return f"OAuth configuration error: {auth_url}", 500

    session["state"] = state
    session["code_verifier"] = code_verifier  # None for non-PKCE flow, kept for compat
    session.permanent = True

    return redirect(auth_url)


# CALLBACK
@app.route("/oauth2callback")
def callback():
    try:
        code = request.args.get("code")
        state = request.args.get("state")

        if not code:
            return "No authorization code received", 400

        # Only check state if we stored one (non-PKCE flow always stores state)
        stored_state = session.get("state")
        if stored_state and state != stored_state:
            return "State mismatch — possible CSRF attack", 400

        from backend.oauth import get_token
        # code_verifier is None for non-PKCE; get_token accepts it gracefully
        token = get_token(code, session.get("code_verifier"))
        user_email = token["email"]

        save_user(user_email, token)
        return redirect(f"{FRONTEND_URL}/?login=success&user={user_email}")

    except Exception as e:
        import traceback
        traceback.print_exc()
        return f"OAuth Error: {str(e)}", 500


@app.route("/me")
def get_current_user():
    # /me is called by Streamlit right after the OAuth redirect to confirm
    # the email is valid and registered in our DB
    user = request.headers.get("X-User-Email")
    if user:
        from backend.token_store import get_user
        if get_user(user):
            return jsonify({"email": user})
    return jsonify({"email": None}), 401


@app.route("/logout")
def logout():
    session.clear()
    # Called by Python (requests.Session), not the browser — return JSON not redirect
    return jsonify({"status": "logged out"})


# GENERATE EMAIL
@app.route("/generate-email", methods=["POST"])
def generate_email():
    from email_integration.email_flows import send_new_email_flow

    user, err = require_login()
    if err:
        return err

    data = request.json

    try:
        result = send_new_email_flow(
            user_email=user,
            to_email=data["to"],
            user_intent=data["intent"],
            sender_name=data["sender"],
            recipient_type=data["recipient_type"],
            recipient_name=data.get("recipient_name", "")
        )
        return jsonify(result)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e), "trace": traceback.format_exc()}), 500


# SEND EMAIL
@app.route("/send-email", methods=["POST"])
def send_email():
    from email_integration.email_flows import send_new_email_flow

    user, err = require_login()
    if err:
        return err

    data = request.json

    try:
        send_new_email_flow(
            user_email=user,
            to_email=data["to"],
            subject_override=data["subject"],
            body_override=data["body"],
            send=True
        )
        return jsonify({"status": "sent"})
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e), "trace": traceback.format_exc()}), 500


# INBOX
@app.route("/inbox")
def inbox():
    from email_integration.email_flows import reply_from_inbox_flow

    user, err = require_login()
    if err:
        return err

    try:
        emails = reply_from_inbox_flow(user, 100)
        return jsonify(emails)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e), "trace": traceback.format_exc()}), 500


# SEARCH
@app.route("/search", methods=["POST"])
def search_email():
    from email_integration.email_flows import reply_using_email_flow

    user, err = require_login()
    if err:
        return err

    data = request.json

    try:
        emails = reply_using_email_flow(
            user_email=user,
            target_email=data["email"],
            max_results=100
        )
        return jsonify(emails)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e), "trace": traceback.format_exc()}), 500


# GENERATE REPLY
@app.route("/generate-reply", methods=["POST"])
def generate_ai_reply():
    from email_integration.email_flows import generate_reply

    user, err = require_login()
    if err:
        return err

    data = request.json

    try:
        result = generate_reply(
            selected_email=data["selected_email"],
            user_intent=data["intent"],
            sender_name=data["sender"],
            recipient_type=data["recipient_type"],
            recipient_name=data.get("recipient_name", "")
        )
        return jsonify(result)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e), "trace": traceback.format_exc()}), 500


# SEND REPLY
@app.route("/send-reply", methods=["POST"])
def send_reply():
    from email_integration.email_flows import send_reply_flow

    user, err = require_login()
    if err:
        return err

    data = request.json

    try:
        send_reply_flow(user, data)
        return jsonify({"status": "reply sent"})
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e), "trace": traceback.format_exc()}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)  