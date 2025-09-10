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


# def register_user(username, email, password):
#     conn = get_connection()
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
#     if cursor.fetchone():
#         st.error("❌ Email already registered.")
#     else:
#         hashed_pw = hashlib.sha256(password.encode()).hexdigest()
#         cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
#                        (username, email, hashed_pw))
#         conn.commit()
#         st.success("✅ Registration successful! You can now login.")
#     cursor.close()
# #     conn.close()
# def register_user(username, email, password):
#     conn = get_connection()
#     cursor = conn.cursor()
#     # Check username
#     cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
#     if cursor.fetchone():
#         return False, "Username already taken."
#     # Check email
#     cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
#     if cursor.fetchone():
#         return False, "Email already registered."

#     hashed_pw = hashlib.sha256(password.encode()).hexdigest()
#     cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
#                    (username, email, hashed_pw))
#     conn.commit()
#     cursor.close()
#     conn.close()
#     return True, "Registration successful."

# def login_user(user_input, password):
#     conn = get_connection()
#     cursor = conn.cursor()
#     hashed_pw = hashlib.sha256(password.encode()).hexdigest()
#     cursor.execute("SELECT * FROM users WHERE (username=%s OR email=%s) AND password=%s",
#                    (user_input, user_input, hashed_pw))
#     user = cursor.fetchone()
#     cursor.close()
#     conn.close()
#     if user:
#         return user
#     return "not_registered"

# def reset_password(email):
#     if email:
#         st.info(f"🔑 Reset link sent to {email} (simulation).")


## I ADDED this after deploment 
def init_user_data(username):
    """
    Initialize user-specific session data when they log in.
    """
    if "user_data" not in st.session_state:
        st.session_state["user_data"] = {}
    st.session_state["user_data"]["username"] = username

def save_session():
    """
    Save the current session state.
    Currently does nothing extra since Streamlit handles session state automatically,
    but included to prevent import errors.
    """
    pass
def register_user(username, email, password):
    conn = get_connection()
    cursor = conn.cursor()
    # Check for duplicate username or email
    cursor.execute("SELECT * FROM users WHERE username=%s OR email=%s", (username, email))
    if cursor.fetchone():
        cursor.close()
        conn.close()
        return False, "Username or Email already exists."

    # Hash password
    hashed_pw = hashlib.sha256(password.encode()).hexdigest()
    cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (username, email, hashed_pw))
    conn.commit()
    cursor.close()
    conn.close()
    return True, "Registration successful!"

def login_user(username_or_email, password):
    conn = get_connection()
    cursor = conn.cursor()
    hashed_pw = hashlib.sha256(password.encode()).hexdigest()
    cursor.execute("SELECT * FROM users WHERE (username=%s OR email=%s) AND password=%s", (username_or_email, username_or_email, hashed_pw))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    if user:
        return user
    return "not_registered"

def reset_password(email, new_password=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
    user = cursor.fetchone()
    if not user:
        cursor.close()
        conn.close()
        return "not_found", "Email not registered."

    if new_password:  # Update password
        if len(new_password) < 4:
            cursor.close()
            conn.close()
            return "short_password", "Password must be at least 4 characters."
        hashed_pw = hashlib.sha256(new_password.encode()).hexdigest()
        cursor.execute("UPDATE users SET password=%s WHERE email=%s", (hashed_pw, email))
        conn.commit()
        cursor.close()
        conn.close()
        return "success", "Password updated successfully."
    
    cursor.close()
    conn.close()
    return "found", "Email verified, enter new password."