import sqlite3
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "users.db")

def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            email TEXT PRIMARY KEY,
            token TEXT
        )
    """)

    conn.commit()
    conn.close()


init_db()


def save_user(email, token_dict):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "REPLACE INTO users (email, token) VALUES (?, ?)",
        (email, json.dumps(token_dict))
    )

    conn.commit()
    conn.close()


def get_user(email):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT token FROM users WHERE email=?", (email,))
    row = cur.fetchone()

    conn.close()

    if row:
        return json.loads(row[0])

    return None