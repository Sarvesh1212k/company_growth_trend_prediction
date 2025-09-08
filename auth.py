import streamlit as st
import mysql.connector
import hashlib

# def get_connection():
    # return mysql.connector.connect(
    #     host="localhost",
    #     port=3306,
    #     user="root",
    #     password="root",
    #     database="user_db"
    # )
   

def get_connection():
    try:
        conn = mysql.connector.connect(
            host="sql12.freesqldatabase.com",
            user="sql12797789",
            password="cDK2JEqkn2",
            database="sql12797789",
            port=3306    # include the port!
        )
        return conn
    except Exception as e:
        print("Connection failed:", e)
        return None

# --------- CHAT HISTORY ----------
def save_chat(user_id, sender, message):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO chat_history (user_id, sender, message) VALUES (%s, %s, %s)",
                (user_id, sender, message))
    conn.commit()
    conn.close()

def load_chat(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT sender, message, timestamp FROM chat_history WHERE user_id=%s ORDER BY timestamp", (user_id,))
    rows = cur.fetchall()
    conn.close()
    return rows

def clear_chat(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM chat_history WHERE user_id=%s", (user_id,))
    conn.commit()
    conn.close()


# --------- DASHBOARD HISTORY ----------
def save_dashboard(user_id, activity):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO dashboard_history (user_id, activity) VALUES (%s, %s)", (user_id, activity))
    conn.commit()
    conn.close()

def load_dashboard(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT activity, timestamp FROM dashboard_history WHERE user_id=%s ORDER BY timestamp", (user_id,))
    rows = cur.fetchall()
    conn.close()
    return rows


# --------- USER SETTINGS ----------
def save_settings(user_id, theme):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("REPLACE INTO user_settings (user_id, theme) VALUES (%s, %s)", (user_id, theme))
    conn.commit()
    conn.close()

def load_settings(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT theme FROM user_settings WHERE user_id=%s", (user_id,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else "System Default"


def register_user(username, email, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
    if cursor.fetchone():
        st.error("❌ Email already registered.")
    else:
        hashed_pw = hashlib.sha256(password.encode()).hexdigest()
        cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                       (username, email, hashed_pw))
        conn.commit()
        st.success("✅ Registration successful! You can now login.")
    cursor.close()
    conn.close()

def login_user(user_input, password):
    conn = get_connection()
    cursor = conn.cursor()
    hashed_pw = hashlib.sha256(password.encode()).hexdigest()
    cursor.execute("SELECT * FROM users WHERE (username=%s OR email=%s) AND password=%s",
                   (user_input, user_input, hashed_pw))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    if user:
        return user
    return "not_registered"

def reset_password(email):
    if email:
        st.info(f"🔑 Reset link sent to {email} (simulation).")
