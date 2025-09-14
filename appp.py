

import json
import os
from datetime import datetime
import pandas as pd
import streamlit as st
from auth import register_user, login_user, reset_password
from chat import show as chat_show
from dashboard import show as dashboard_show
from history import show as history_show
from setting import show as setting_show
from home import show as home_show

SESSION_FILE = "session_state.json"




# ---------------- Save Session ----------------
def save_session():
    serializable_user_data = {}
    for user, data in st.session_state.get("user_data", {}).items():
        serializable_data = data.copy()

        # Serialize chat_history datetime
        if "chat_history" in serializable_data:
            serializable_data["chat_history"] = [
                (s, m, t.strftime("%Y-%m-%d %H:%M:%S") if isinstance(t, datetime) else t)
                for s, m, t in serializable_data["chat_history"]
            ]

        # Serialize dashboard_history datetime
        if "dashboard_history" in serializable_data:
            serializable_data["dashboard_history"] = [
                {**item, "time": item["time"].strftime("%Y-%m-%d %H:%M:%S") if isinstance(item["time"], datetime) else item["time"]}
                for item in serializable_data.get("dashboard_history", [])
            ]

        # Serialize dashboard_df
        if "dashboard_df" in serializable_data and serializable_data["dashboard_df"] is not None:
            serializable_data["dashboard_df"] = serializable_data["dashboard_df"].to_dict(orient="list")

        serializable_user_data[user] = serializable_data

    session_data = {
        "logged_in": st.session_state.get("logged_in", False),
        "username": st.session_state.get("username"),
        "current_page": st.session_state.get("current_page"),
        "user_data": serializable_user_data,
        "show_reset": st.session_state.get("show_reset", False),
        "reset_email": st.session_state.get("reset_email", "")
    }

    with open(SESSION_FILE, "w") as f:
        json.dump(session_data, f)

# ---------------- Load Session ----------------
def load_session():
    if os.path.exists(SESSION_FILE):
        try:
            with open(SESSION_FILE, "r") as f:
                data = json.load(f)
                st.session_state["logged_in"] = data.get("logged_in", False)
                st.session_state["username"] = data.get("username")
                st.session_state["current_page"] = data.get("current_page", "Dashboard")
                st.session_state["show_reset"] = data.get("show_reset", False)
                st.session_state["reset_email"] = data.get("reset_email", "")

                # Restore user_data
                user_data = data.get("user_data", {})
                restored_user_data = {}
                for user, udata in user_data.items():
                    # Restore chat_history
                    if "chat_history" in udata:
                        restored_chat = []
                        for entry in udata["chat_history"]:
                            s, m, t = entry
                            if isinstance(t, str):
                                try:
                                    t = datetime.strptime(t, "%Y-%m-%d %H:%M:%S")
                                except:
                                    t = None
                            restored_chat.append((s, m, t))
                        udata["chat_history"] = restored_chat

                    # Restore dashboard_history
                    if "dashboard_history" in udata:
                        restored_dashboard = []
                        for item in udata["dashboard_history"]:
                            new_item = item.copy()
                            if isinstance(new_item.get("time"), str):
                                try:
                                    new_item["time"] = datetime.strptime(new_item["time"], "%Y-%m-%d %H:%M:%S")
                                except:
                                    pass
                            restored_dashboard.append(new_item)
                        udata["dashboard_history"] = restored_dashboard

                    # Restore dashboard_df
                    if "dashboard_df" in udata and udata["dashboard_df"] is not None:
                        try:
                            udata["dashboard_df"] = pd.DataFrame(udata["dashboard_df"])
                        except:
                            udata["dashboard_df"] = None

                    restored_user_data[user] = udata

                st.session_state["user_data"] = restored_user_data
        except Exception:
            pass

# ---------------- Clear Session File ----------------
def clear_session_file():
    if os.path.exists(SESSION_FILE):
        try:
            os.remove(SESSION_FILE)
        except Exception:
            pass

load_session()

# ---------------- Initialize Defaults ----------------
defaults = {
    "logged_in": False,
    "username": None,
    "show_reset": False,
    "reset_email": "",
    "current_page": "Dashboard",
    "user_data": {}
}

for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val

# ---------------- Ensure user data structure ----------------
def init_user_data(username):
    if username not in st.session_state["user_data"]:
        st.session_state["user_data"][username] = {
            "chat_history": [],
            "dashboard_df": None,
            "dashboard_link": "",
            "dashboard_symbol": None,
            "dashboard_name": None,
            "dashboard_history": []
        }

# ---------------- Main Page Function ----------------
# def main_page():
#     page_options = ["Home", "Chat", "Dashboard", "History", "Settings"]
#     try:
#         index_page = page_options.index(st.session_state.current_page)
#     except ValueError:
#         index_page = 0

#     def set_page():
#         st.session_state.current_page = st.session_state.page_radio
#         save_session()

#     st.sidebar.radio(
#         "Navigation:",
#         page_options,
#         index=index_page,
#         key="page_radio",
#         on_change=set_page
#     )

#     username = st.session_state.username
#     init_user_data(username)

#     st.markdown(f"### 👋 Welcome, **{username}**")

#     page = st.session_state.current_page
#     if page == "Home":
#      home_show()
#     elif page == "Chat":
#      chat_show(st.session_state["user_data"][username])
#     elif page == "Dashboard":
#      dashboard_show(st.session_state["user_data"][username])
#     elif page == "History":
#      history_show(st.session_state["user_data"][username])
#     elif page == "Settings":
#      setting_show(st.session_state["user_data"][username])

#     if st.sidebar.button("🚪 Logout"):
#         st.session_state.logged_in = False
#         st.session_state.username = None
#         st.session_state.current_page = "login"
#         clear_session_file()
#         save_session()
#         st.session_state["refresh_page"] = st.session_state.get("refresh_page", 0) + 1
def main_page():
    page_options = ["🏠 Home", "💬 Chat", "📊 Dashboard", "📜 History", "⚙️ Settings"]
    try:
        index_page = page_options.index(st.session_state.current_page)
    except ValueError:
        index_page = 0

    def set_page():
        st.session_state.current_page = st.session_state.page_radio
        save_session()
        # Reset logout counter if page changes
        st.session_state.logout_clicks = 0

    # --- Sidebar Styling ---
    st.sidebar.markdown(
        """
        <style>
        .sidebar-title {
            font-size: 22px;
            font-weight: 600;
            color: #4B0082;
            text-align: center;
            margin-bottom: 20px;
        }
        div[data-baseweb="radio"] > div {
            display: flex;
            flex-direction: column;
        }
        div[data-baseweb="radio"] label {
            font-size: 16px !important;
            padding: 8px 12px !important;
            border-radius: 8px;
            margin: 3px 0;
            cursor: pointer;
        }
        div[data-baseweb="radio"] label:hover {
            background-color: #f0f0f5 !important;
        }
        div[data-baseweb="radio"] input:checked + div {
            background-color: #4B0082 !important;
            color: white !important;
            border-radius: 8px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Sidebar Title
    st.sidebar.markdown("<div class='sidebar-title'>📌 Navigation</div>", unsafe_allow_html=True)

    # Navigation Menu
    st.sidebar.radio(
        "",
        page_options,
        index=index_page,
        key="page_radio",
        on_change=set_page
    )

    username = st.session_state.username
    init_user_data(username)

    st.markdown(f"### 👋 Welcome, **{username}**")

    page = st.session_state.current_page
    if page == "🏠 Home":
        home_show()
    elif page == "💬 Chat":
        chat_show(st.session_state["user_data"][username])
    elif page == "📊 Dashboard":
        dashboard_show(st.session_state["user_data"][username])
    elif page == "📜 History":
        history_show(st.session_state["user_data"][username])
    elif page == "⚙️ Settings":
        setting_show(st.session_state["user_data"][username])

    st.sidebar.markdown("---")

    # --- Double click logout ---
    if "logout_clicks" not in st.session_state:
        st.session_state.logout_clicks = 0

    if st.sidebar.button("🚪 Logout", use_container_width=True):
        st.session_state.logout_clicks += 1
        if st.session_state.logout_clicks >= 2:
            st.session_state.logged_in = False
            st.session_state.username = None
            st.session_state.current_page = "login"
            clear_session_file()
            save_session()
            st.session_state.logout_clicks = 0  # reset after logout
            st.rerun()
        else:
            st.sidebar.warning("⚠️ Click again to confirm logout")



st.set_page_config(page_title="Company Dashboard", page_icon="📊", layout="wide")

if st.session_state.logged_in:
    main_page()
else:
    st.markdown(
        "<h1 style='text-align:center; color:#4B0082;'> 🚀 Company Growth Trend Prediction </h1>"
        "<h2 style='text-align:center; color:#4B0082;'>🔐 Login & Registration </h2>",
        unsafe_allow_html=True
    )

    menu = ["Login", "Register"]
    choice = st.sidebar.selectbox("Menu", menu)

    # ---------------- REGISTER ----------------
    if choice == "Register":
        st.markdown("<h3 style='color:#4B0082;'>📝 Create a New Account</h3>", unsafe_allow_html=True)

        username = st.text_input("Username", placeholder="Enter username", key="reg_username")
        email = st.text_input("Email", placeholder="Enter email", key="reg_email")
        password = st.text_input("Password", type="password", placeholder="Enter password", key="reg_password")

        if st.button("Register", use_container_width=True, key="register_btn"):
            if not username or not email or not password:
                st.warning("⚠️ Please fill all fields")
            elif "@" not in email or not email.endswith(".com"):
                st.error("❌ Please enter a valid Gmail address ending with @gmail.com")
            elif len(password) < 4:
                st.error("❌ Password must be at least 4 characters")
            else:
                success, msg = register_user(username, email, password)
                if success:
                    st.success("✅ Registration successful! You can now login.")
                    st.rerun()
                else:
                    st.error(f"❌ {msg}")

    # ---------------- LOGIN ----------------
    elif choice == "Login":
        st.markdown("<h3 style='color:#4B0082;'>🔑 Login to Your Account</h3>", unsafe_allow_html=True)

        user_input = st.text_input("Username or Email", placeholder="Enter username or email", key="login_user_input")
        password = st.text_input("Password", type="password", placeholder="Enter password", key="login_password")

        if st.button("Login", use_container_width=True, key="login_btn"):
            if not user_input or not password:
                st.warning("⚠️ Please enter both username/email and password.")
            else:
                user = login_user(user_input, password)

                # ✅ FIX: Only log in if a real user is returned
                if user and user != "not_registered":
                    st.session_state.logged_in = True
                    st.session_state.username = user[1]  # assumes 2nd column is username
                    init_user_data(user[1])
                    st.session_state.current_page = "Dashboard"
                    save_session()
                    st.success("✅ Login successful!")
                elif user == "not_registered" or user is None:
                    st.error("❌ User not found. Please register first.")
                else:
                    st.error("❌ Invalid username/email or password.")

# # ---------------- CSS ----------------
st.markdown("""
<style>
div.stButton > button {
    background-color: #f5f5f5;
    color: #333;
    border: 2px solid #ccc;
    border-radius: 6px;
    padding: 0.6em 1.2em;
    font-weight: 500;
    cursor: pointer;
    transition: background-color 0.2s ease-in-out, color 0.2s ease-in-out;
}
div.stButton > button:active {
    background-color: #FF6B6B;  
    color: white;
    border-color: #FF6B6B;
}
</style>
""", unsafe_allow_html=True)
