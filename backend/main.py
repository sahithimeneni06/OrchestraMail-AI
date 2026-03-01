from flask import Flask, redirect, request, session, jsonify
from backend.token_store import save_user, init_db
from dotenv import load_dotenv
from flask_cors import CORS
import os
import traceback

load_dotenv()

FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:8501").rstrip("/")

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
if not app.secret_key:
    raise RuntimeError("SECRET_KEY environment variable is not set.")

app.config.update(
    SESSION_COOKIE_SAMESITE="None",
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    PERMANENT_SESSION_LIFETIME=86400 * 7
)

CORS(app,
     supports_credentials=True,
     origins=[FRONTEND_URL],
     allow_headers=["Content-Type", "Authorization", "X-User-Email"],
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
    return "OrchestraMail backend running"


@app.route("/debug")
def debug():
    from backend.token_store import get_user
    email = request.headers.get("X-User-Email")
    has_token = bool(get_user(email)) if email else False
    return jsonify({
        "x_user_email": email,
        "has_token_in_db": has_token,
    })


def require_login():
    user = request.headers.get("X-User-Email")
    if not user:
        # No header at all → not logged in
        return None, (jsonify({"error": "Not logged in — X-User-Email header missing"}), 401)
    from backend.token_store import get_user
    if not get_user(user):
        # Header present but no Gmail token in DB → need to grant OAuth
        return None, (jsonify({"error": "oauth_not_granted", "detail": f"No Gmail token for {user}"}), 403)
    return user, None


# ── AUTH ──────────────────────────────────────────────────

@app.route("/login")
def login():
    from backend.oauth import get_auth_url
    auth_url, state, code_verifier = get_auth_url()
    if state is None:
        return f"OAuth configuration error: {auth_url}", 500
    session["state"] = state
    session["code_verifier"] = code_verifier
    session.permanent = True
    return redirect(auth_url)


@app.route("/oauth2callback")
def callback():
    try:
        code = request.args.get("code")
        state = request.args.get("state")
        if not code:
            return "No authorization code received", 400
        stored_state = session.get("state")
        if stored_state and state != stored_state:
            return "State mismatch", 400
        from backend.oauth import get_token
        token = get_token(code, session.get("code_verifier"))
        user_email = token["email"]
        save_user(user_email, token)
        return redirect(f"{FRONTEND_URL}/?login=success&user={user_email}")
    except Exception as e:
        traceback.print_exc()
        return f"OAuth Error: {str(e)}", 500


@app.route("/me")
def get_current_user():
    user = request.headers.get("X-User-Email")
    if user:
        from backend.token_store import get_user
        if get_user(user):
            return jsonify({"email": user})
    return jsonify({"email": None}), 401


@app.route("/logout")
def logout():
    session.clear()
    return jsonify({"status": "logged out"})


@app.route("/request-access", methods=["POST"])
def request_access():
    """Store access requests from users who don't have Gmail OAuth yet."""
    email = request.json.get("email", "").strip()
    if not email:
        return jsonify({"error": "Email required"}), 400
    # Visible in Render logs dashboard
    print(f"[ACCESS REQUEST] {email}", flush=True)
    try:
        from datetime import datetime
        with open("/tmp/access_requests.txt", "a") as f:
            f.write(f"{datetime.utcnow().isoformat()} {email}\n")
    except Exception:
        pass
    return jsonify({"msg": "Request received."})


@app.route("/access-requests")
def list_access_requests():
    """Admin view — visit in browser to see who requested access."""
    try:
        with open("/tmp/access_requests.txt") as f:
            return f.read(), 200, {"Content-Type": "text/plain"}
    except FileNotFoundError:
        return "No requests yet.", 200


# ── EMAIL ROUTES ──────────────────────────────────────────

@app.route("/generate-email", methods=["POST"])
def generate_email():
    from email_integration.email_flows import send_new_email_flow
    user, err = require_login()
    if err: return err
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


@app.route("/send-email", methods=["POST"])
def send_email():
    from email_integration.email_flows import send_new_email_flow
    user, err = require_login()
    if err: return err
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


@app.route("/inbox")
def inbox():
    from email_integration.email_flows import reply_from_inbox_flow
    user, err = require_login()
    if err: return err
    try:
        emails = reply_from_inbox_flow(user, 100)
        return jsonify(emails)
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e), "trace": traceback.format_exc()}), 500


@app.route("/search", methods=["POST"])
def search_email():
    from email_integration.email_flows import reply_using_email_flow
    user, err = require_login()
    if err: return err
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


@app.route("/generate-reply", methods=["POST"])
def generate_ai_reply():
    from email_integration.email_flows import generate_reply
    user, err = require_login()
    if err: return err
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


@app.route("/send-reply", methods=["POST"])
def send_reply():
    from email_integration.email_flows import send_reply_flow
    user, err = require_login()
    if err: return err
    data = request.json
    try:
        send_reply_flow(user, data)
        return jsonify({"status": "reply sent"})
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e), "trace": traceback.format_exc()}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)