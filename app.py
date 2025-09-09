


# import json
# import os
# from datetime import datetime
# import pandas as pd
# import streamlit as st
# from auth import register_user, login_user, reset_password
# from chat import show as chat_show
# from dashboard import show as dashboard_show
# from history import show as history_show

# from setting import show as setting_show

#   # keep your original setting page name
# SESSION_FILE = "session_state.json"

# # ---------------- Session Save/Load ----------------
# def save_session():
#     session_data = {
#         "logged_in": st.session_state.get("logged_in", False),
#         "username": st.session_state.get("username"),
#         "current_page": st.session_state.get("current_page"),
#         "chat_history": [
#             (s, m, t.strftime("%Y-%m-%d %H:%M:%S")) for (s, m, t) in st.session_state.get("chat_history", [])
#         ] if st.session_state.get("chat_history") else None,
#         "dashboard_link": st.session_state.get("dashboard_link"),
#         "dashboard_df": st.session_state.get("dashboard_df").to_dict(orient="list") if st.session_state.get("dashboard_df") is not None else None,
#         "dashboard_symbol": st.session_state.get("dashboard_symbol"),
#         "dashboard_name": st.session_state.get("dashboard_name"),
#         "dashboard_history": st.session_state.get("dashboard_history"),
#         "show_reset": st.session_state.get("show_reset", False),
#         "reset_email": st.session_state.get("reset_email", "")
#     }
#     with open(SESSION_FILE, "w") as f:
#         json.dump(session_data, f)

# def load_session():
#     if os.path.exists(SESSION_FILE):
#         try:
#             with open(SESSION_FILE, "r") as f:
#                 data = json.load(f)
#                 for key in ["logged_in", "username", "current_page", "dashboard_link", "dashboard_symbol", "dashboard_name", "dashboard_history", "show_reset", "reset_email"]:
#                     if key in data:
#                         st.session_state[key] = data[key]
#                 if data.get("chat_history"):
#                     restored = []
#                     for s, m, tstr in data["chat_history"]:
#                         try:
#                             t = datetime.strptime(tstr, "%Y-%m-%d %H:%M:%S")
#                         except Exception:
#                             t = datetime.now()
#                         restored.append((s, m, t))
#                     st.session_state["chat_history"] = restored
#                 else:
#                     if "chat_history" not in st.session_state:
#                         st.session_state["chat_history"] = []
#                 if data.get("dashboard_df") is not None:
#                     try:
#                         st.session_state["dashboard_df"] = pd.DataFrame(data["dashboard_df"])
#                     except Exception:
#                         st.session_state["dashboard_df"] = None
#                 else:
#                     if "dashboard_df" not in st.session_state:
#                         st.session_state["dashboard_df"] = None
#         except Exception:
#             pass

# def clear_session_file():
#     if os.path.exists(SESSION_FILE):
#         try:
#             os.remove(SESSION_FILE)
#         except Exception:
#             pass

# load_session()

# # ---------------- Main Page Function ----------------
# def main_page():
#     if "current_page" not in st.session_state:
#         st.session_state.current_page = "Dashboard"

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

#     page = st.session_state.current_page
#     st.markdown(f"### 👋 Welcome, **{st.session_state.username}**")

#     # ---------------- Display Pages ----------------
#     if page == "Home":
#         st.markdown("🏠 Home Page")
#         st.write("Your dashboard home page")
#     elif page == "Chat":
#         chat_show()
#     elif page == "Dashboard":
#         dashboard_show()
#     elif page == "History":
#        history_show()

#     elif page == "Settings":
#         setting_show()

#     # ---------------- Logout ----------------
#     if st.sidebar.button("🚪 Logout"):
#         st.session_state.logged_in = False
#         st.session_state.username = None
#         st.session_state.current_page = "login"
#         st.session_state.messages = []
#         st.session_state.dashboard_history = []
#         clear_session_file()
#         save_session()
#         st.rerun()

# # ---------------- App Configuration ----------------
# st.set_page_config(page_title="Company Dashboard", page_icon="📊", layout="wide")
# st.markdown("<h1 style='text-align:center; color:#4B0082;'>🔐 Login & Registration System</h1>", unsafe_allow_html=True)

# # ---------------- Initialize Session Defaults ----------------
# defaults = {
#     "logged_in": False,
#     "username": None,
#     "show_reset": False,
#     "reset_email": "",
#     "messages": [],
#     "dashboard_history": [],
#     "chat_history": [],
#     "dashboard_df": None,
#     "dashboard_link": "",
#     "dashboard_link_temp": "",
#     "dashboard_symbol": None,
#     "dashboard_name": None,
#     "current_page": "Dashboard"
# }

# for key, val in defaults.items():
#     if key not in st.session_state:
#         st.session_state[key] = val
# if "dashboard_link_temp" not in st.session_state:
#     st.session_state.dashboard_link_temp = st.session_state.dashboard_link

# # ---------------- Show Pages ----------------
# if st.session_state.logged_in:
#     main_page()
# else:
#     menu = ["Login", "Register"]
#     choice = st.sidebar.selectbox("Menu", menu)

#     if choice == "Register":
#         st.markdown("<h3 style='color:#4B0082;'>📝 Create a New Account</h3>", unsafe_allow_html=True)
#         username = st.text_input("Username", placeholder="Enter username")
#         email = st.text_input("Email", placeholder="Enter email")
#         password = st.text_input("Password", type="password", placeholder="Enter password")
#         if st.button("Register", use_container_width=True):
#             if username and email and password:
#                 register_user(username, email, password)
#             else:
#                 st.warning("⚠️ Please fill all fields")

#     elif choice == "Login":
#         st.markdown("<h3 style='color:#4B0082;'>🔑 Login to Your Account</h3>", unsafe_allow_html=True)
#         if not st.session_state.show_reset:
#             user_input = st.text_input("Username or Email", placeholder="Enter username or email")
#             password = st.text_input("Password", type="password", placeholder="Enter password")
#             if st.button("Login", use_container_width=True):
#                 user = login_user(user_input, password)
#                 if user and user != "not_registered":
#                     st.session_state.logged_in = True
#                     st.session_state.username = user[1]
#                     st.session_state.current_page = "Dashboard"
#                     save_session()
#                     st.success("✅ Login successful!")
#                     st.rerun()
#                 elif user == "not_registered":
#                     st.error("❌ User not found. Please register first.")
#                 else:
#                     st.error("❌ Invalid username/email or password.")

#             st.markdown("---")
#             if st.button("Forgot Password?", use_container_width=True):
#                 st.session_state.show_reset = True
#                 save_session()
#                 st.rerun()
#         else:
#             st.markdown("<h3 style='color:#4B0082;'>🔑 Reset Password</h3>", unsafe_allow_html=True)
#             if not st.session_state.reset_email:
#                 st.session_state.reset_email = st.text_input("Enter your registered email", key="email_for_reset")
#             reset_password(st.session_state.reset_email)
#             if st.button("Back to Login", use_container_width=True):
#                 st.session_state.show_reset = False
#                 save_session()
#                 st.rerun()

# import json
# import os
# from datetime import datetime
# import pandas as pd
# import streamlit as st
# from auth import register_user, login_user, reset_password
# from chat import show as chat_show
# from dashboard import show as dashboard_show
# from history import show as history_show
# from setting import show as setting_show  # keep your original setting page name

# SESSION_FILE = "session_state.json"

# # ---------------- Session Save/Load ----------------
# def save_session():
#     session_data = {
#         "logged_in": st.session_state.get("logged_in", False),
#         "username": st.session_state.get("username"),
#         "current_page": st.session_state.get("current_page"),
#         "chat_history": [
#             (s, m, t.strftime("%Y-%m-%d %H:%M:%S")) for (s, m, t) in st.session_state.get("chat_history", [])
#             if len((s,m,t))==3
#         ] if st.session_state.get("chat_history") else [],
#         "dashboard_link": st.session_state.get("dashboard_link"),
#         "dashboard_df": st.session_state.get("dashboard_df").to_dict(orient="list") if st.session_state.get("dashboard_df") is not None else None,
#         "dashboard_symbol": st.session_state.get("dashboard_symbol"),
#         "dashboard_name": st.session_state.get("dashboard_name"),
#         "dashboard_history": st.session_state.get("dashboard_history"),
#         "show_reset": st.session_state.get("show_reset", False),
#         "reset_email": st.session_state.get("reset_email", "")
#     }
#     with open(SESSION_FILE, "w") as f:
#         json.dump(session_data, f)

# def load_session():
#     if os.path.exists(SESSION_FILE):
#         try:
#             with open(SESSION_FILE, "r") as f:
#                 data = json.load(f)
#                 for key in ["logged_in", "username", "current_page", "dashboard_link", "dashboard_symbol", "dashboard_name", "dashboard_history", "show_reset", "reset_email"]:
#                     if key in data:
#                         st.session_state[key] = data[key]
#                 # Chat history restore
#                 if data.get("chat_history"):
#                     restored = []
#                     for entry in data["chat_history"]:
#                         try:
#                             if len(entry) == 3:
#                                 s, m, tstr = entry
#                                 t = datetime.strptime(tstr, "%Y-%m-%d %H:%M:%S")
#                                 restored.append((s, m, t))
#                             else:
#                                 restored.append(tuple(entry))
#                         except Exception:
#                             restored.append(tuple(entry))
#                     st.session_state["chat_history"] = restored
#                 else:
#                     st.session_state["chat_history"] = []
#                 # Dashboard df restore
#                 if data.get("dashboard_df") is not None:
#                     try:
#                         st.session_state["dashboard_df"] = pd.DataFrame(data["dashboard_df"])
#                     except Exception:
#                         st.session_state["dashboard_df"] = None
#                 else:
#                     st.session_state["dashboard_df"] = None
#         except Exception:
#             pass

# def clear_session_file():
#     if os.path.exists(SESSION_FILE):
#         try:
#             os.remove(SESSION_FILE)
#         except Exception:
#             pass

# load_session()

# # ---------------- Main Page Function ----------------
# def main_page():
#     if "current_page" not in st.session_state:
#         st.session_state.current_page = "Dashboard"

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

#     page = st.session_state.current_page
#     st.markdown(f"### 👋 Welcome, **{st.session_state.username}**")

#     # ---------------- Display Pages ----------------
#     if page == "Home":
#         st.markdown("🏠 Home Page")
#         st.write("Your dashboard home page")
#     elif page == "Chat":
#         chat_show()
#     elif page == "Dashboard":
#         dashboard_show()
#     elif page == "History":
#         history_show()
#     elif page == "Settings":
#         setting_show()

#     # ---------------- Logout ----------------
#     if st.sidebar.button("🚪 Logout"):
#         st.session_state.logged_in = False
#         st.session_state.username = None
#         st.session_state.current_page = "login"
#         st.session_state.messages = []
#         st.session_state.dashboard_history = []
#         clear_session_file()
#         save_session()
#         st.rerun()  # original rerun kept

# # ---------------- App Configuration ----------------
# st.set_page_config(page_title="Company Dashboard", page_icon="📊", layout="wide")
# st.markdown("<h1 style='text-align:center; color:#4B0082;'>🔐 Login & Registration System</h1>", unsafe_allow_html=True)

# # ---------------- Initialize Session Defaults ----------------
# defaults = {
#     "logged_in": False,
#     "username": None,
#     "show_reset": False,
#     "reset_email": "",
#     "messages": [],
#     "dashboard_history": [],
#     "chat_history": [],
#     "dashboard_df": None,
#     "dashboard_link": "",
#     "dashboard_link_temp": "",
#     "dashboard_symbol": None,
#     "dashboard_name": None,
#     "current_page": "Dashboard"
# }

# for key, val in defaults.items():
#     if key not in st.session_state:
#         st.session_state[key] = val

# # ---------------- Show Pages ----------------
# if st.session_state.logged_in:
#     main_page()
# else:
#     menu = ["Login", "Register"]
#     choice = st.sidebar.selectbox("Menu", menu)

#     if choice == "Register":
#         st.markdown("<h3 style='color:#4B0082;'>📝 Create a New Account</h3>", unsafe_allow_html=True)
#         username = st.text_input("Username", placeholder="Enter username")
#         email = st.text_input("Email", placeholder="Enter email")
#         password = st.text_input("Password", type="password", placeholder="Enter password")
#         if st.button("Register", use_container_width=True):
#             if username and email and password:
#                 register_user(username, email, password)
#             else:
#                 st.warning("⚠️ Please fill all fields")

#     elif choice == "Login":
#         st.markdown("<h3 style='color:#4B0082;'>🔑 Login to Your Account</h3>", unsafe_allow_html=True)
#         if not st.session_state.show_reset:
#             user_input = st.text_input("Username or Email", placeholder="Enter username or email")
#             password = st.text_input("Password", type="password", placeholder="Enter password")
#             if st.button("Login", use_container_width=True):
#                 user = login_user(user_input, password)
#                 if user and user != "not_registered":
#                     st.session_state.logged_in = True
#                     st.session_state.username = user[1]
#                     st.session_state.current_page = "Dashboard"
#                     save_session()
#                     st.success("✅ Login successful!")
#                     st.rerun()
#                 elif user == "not_registered":
#                     st.error("❌ User not found. Please register first.")
#                 else:
#                     st.error("❌ Invalid username/email or password.")

#             st.markdown("---")
#             if st.button("Forgot Password?", use_container_width=True):
#                 st.session_state.show_reset = True
#                 save_session()
#                 st.rerun()
#         else:
#             st.markdown("<h3 style='color:#4B0082;'>🔑 Reset Password</h3>", unsafe_allow_html=True)
#             if not st.session_state.reset_email:
#                 st.session_state.reset_email = st.text_input("Enter your registered email", key="email_for_reset")
#             reset_password(st.session_state.reset_email)
#             if st.button("Back to Login", use_container_width=True):
#                 st.session_state.show_reset = False
#                 save_session()
#                 st.rerun()

# import json
# import os
# from datetime import datetime
# import pandas as pd
# import streamlit as st
# from auth import register_user, login_user, reset_password
# from chat import show as chat_show
# from dashboard import show as dashboard_show
# from history import show as history_show
# from setting import show as setting_show  # keep your original setting page name

# SESSION_FILE = "session_state.json"

# # ---------------- Session Save/Load ----------------
# def save_session():
#     session_data = {
#         "logged_in": st.session_state.get("logged_in", False),
#         "username": st.session_state.get("username"),
#         "current_page": st.session_state.get("current_page"),
#         "chat_history": [
#             (s, m, t.strftime("%Y-%m-%d %H:%M:%S")) for (s, m, t) in st.session_state.get("chat_history", [])
#             if len((s, m, t)) == 3
#         ] if st.session_state.get("chat_history") else [],
#         "dashboard_link": st.session_state.get("dashboard_link"),
#         "dashboard_df": st.session_state.get("dashboard_df").to_dict(orient="list") if st.session_state.get("dashboard_df") is not None else None,
#         "dashboard_symbol": st.session_state.get("dashboard_symbol"),
#         "dashboard_name": st.session_state.get("dashboard_name"),
#         "dashboard_history": st.session_state.get("dashboard_history"),
#         "show_reset": st.session_state.get("show_reset", False),
#         "reset_email": st.session_state.get("reset_email", "")
#     }
#     with open(SESSION_FILE, "w") as f:
#         json.dump(session_data, f)

# def load_session():
#     if os.path.exists(SESSION_FILE):
#         try:
#             with open(SESSION_FILE, "r") as f:
#                 data = json.load(f)
#                 for key in ["logged_in", "username", "current_page", "dashboard_link", "dashboard_symbol", "dashboard_name", "dashboard_history", "show_reset", "reset_email"]:
#                     if key in data:
#                         st.session_state[key] = data[key]
#                 # Chat history restore
#                 if data.get("chat_history"):
#                     restored = []
#                     for entry in data["chat_history"]:
#                         try:
#                             if len(entry) == 3:
#                                 s, m, tstr = entry
#                                 t = datetime.strptime(tstr, "%Y-%m-%d %H:%M:%S")
#                                 restored.append((s, m, t))
#                             else:
#                                 restored.append(tuple(entry))
#                         except Exception:
#                             restored.append(tuple(entry))
#                     st.session_state["chat_history"] = restored
#                 else:
#                     st.session_state["chat_history"] = []
#                 # Dashboard df restore
#                 if data.get("dashboard_df") is not None:
#                     try:
#                         st.session_state["dashboard_df"] = pd.DataFrame(data["dashboard_df"])
#                     except Exception:
#                         st.session_state["dashboard_df"] = None
#                 else:
#                     st.session_state["dashboard_df"] = None
#         except Exception:
#             pass

# def clear_session_file():
#     if os.path.exists(SESSION_FILE):
#         try:
#             os.remove(SESSION_FILE)
#         except Exception:
#             pass

# load_session()

# # ---------------- Main Page Function ----------------
# def main_page():
#     if "current_page" not in st.session_state:
#         st.session_state.current_page = "Dashboard"

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

#     page = st.session_state.current_page
#     st.markdown(f"### 👋 Welcome, **{st.session_state.username}**")

#     # ---------------- Display Pages ----------------
#     if page == "Home":
#         st.markdown("🏠 Home Page")
#         st.write("Your dashboard home page")
#     elif page == "Chat":
#         chat_show()
#     elif page == "Dashboard":
#         dashboard_show()
#     elif page == "History":
#         history_show()
#     elif page == "Settings":
#         setting_show()

#     # ---------------- Logout ----------------
#     if st.sidebar.button("🚪 Logout"):
#         st.session_state.logged_in = False
#         st.session_state.username = None
#         st.session_state.current_page = "login"
#         st.session_state.messages = []
#         st.session_state.dashboard_history = []
#         clear_session_file()
#         save_session()
#         st.rerun()  # original rerun kept

# # ---------------- App Configuration ----------------
# st.set_page_config(page_title="Company Dashboard", page_icon="📊", layout="wide")

# # ---------------- Initialize Session Defaults ----------------
# defaults = {
#     "logged_in": False,
#     "username": None,
#     "show_reset": False,
#     "reset_email": "",
#     "messages": [],
#     "dashboard_history": [],
#     "chat_history": [],
#     "dashboard_df": None,
#     "dashboard_link": "",
#     "dashboard_link_temp": "",
#     "dashboard_symbol": None,
#     "dashboard_name": None,
#     "current_page": "Dashboard"
# }

# for key, val in defaults.items():
#     if key not in st.session_state:
#         st.session_state[key] = val

# # ---------------- Show Pages ----------------
# if st.session_state.logged_in:
#     # After login, header is removed
#     main_page()
# else:
#     # Only show login/registration header here
#     st.markdown("<h1 style='text-align:center; color:#4B0082;'>🔐 Login & Registration System</h1>", unsafe_allow_html=True)

#     menu = ["Login", "Register"]
#     choice = st.sidebar.selectbox("Menu", menu)

#     if choice == "Register":
#         st.markdown("<h3 style='color:#4B0082;'>📝 Create a New Account</h3>", unsafe_allow_html=True)
#         username = st.text_input("Username", placeholder="Enter username")
#         email = st.text_input("Email", placeholder="Enter email")
#         password = st.text_input("Password", type="password", placeholder="Enter password")
#         if st.button("Register", use_container_width=True):
#             if username and email and password:
#                 register_user(username, email, password)
#             else:
#                 st.warning("⚠️ Please fill all fields")

#     elif choice == "Login":
#         st.markdown("<h3 style='color:#4B0082;'>🔑 Login to Your Account</h3>", unsafe_allow_html=True)
#         if not st.session_state.show_reset:
#             user_input = st.text_input("Username or Email", placeholder="Enter username or email")
#             password = st.text_input("Password", type="password", placeholder="Enter password")
#             if st.button("Login", use_container_width=True):
#                 user = login_user(user_input, password)
#                 if user and user != "not_registered":
#                     st.session_state.logged_in = True
#                     st.session_state.username = user[1]
#                     st.session_state.current_page = "Dashboard"
#                     save_session()
#                     st.success("✅ Login successful!")
#                     st.rerun()
#                 elif user == "not_registered":
#                     st.error("❌ User not found. Please register first.")
#                 else:
#                     st.error("❌ Invalid username/email or password.")

#             st.markdown("---")
#             if st.button("Forgot Password?", use_container_width=True):
#                 st.session_state.show_reset = True
#                 save_session()
#                 st.rerun()
#         else:
#             st.markdown("<h3 style='color:#4B0082;'>🔑 Reset Password</h3>", unsafe_allow_html=True)
#             if not st.session_state.reset_email:
#                 st.session_state.reset_email = st.text_input("Enter your registered email", key="email_for_reset")
#             reset_password(st.session_state.reset_email)
#             if st.button("Back to Login", use_container_width=True):
#                 st.session_state.show_reset = False
#                 save_session()
#                 st.rerun()

# import json
# import os
# from datetime import datetime
# import pandas as pd
# import streamlit as st
# from auth import register_user, login_user, reset_password
# from chat import show as chat_show
# from dashboard import show as dashboard_show
# from history import show as history_show
# from setting import show as setting_show  # keep your original setting page name

# SESSION_FILE = "session_state.json"

# # ---------------- Session Save/Load ----------------
# def save_session():
#     session_data = {
#         "logged_in": st.session_state.get("logged_in", False),
#         "username": st.session_state.get("username"),
#         "current_page": st.session_state.get("current_page"),
#         "user_data": st.session_state.get("user_data", {}),
#         "show_reset": st.session_state.get("show_reset", False),
#         "reset_email": st.session_state.get("reset_email", "")
#     }
#     with open(SESSION_FILE, "w") as f:
#         json.dump(session_data, f)

# def load_session():
#     if os.path.exists(SESSION_FILE):
#         try:
#             with open(SESSION_FILE, "r") as f:
#                 data = json.load(f)
#                 st.session_state["logged_in"] = data.get("logged_in", False)
#                 st.session_state["username"] = data.get("username")
#                 st.session_state["current_page"] = data.get("current_page", "Dashboard")
#                 st.session_state["user_data"] = data.get("user_data", {})
#                 st.session_state["show_reset"] = data.get("show_reset", False)
#                 st.session_state["reset_email"] = data.get("reset_email", "")
#         except Exception:
#             pass

# def clear_session_file():
#     if os.path.exists(SESSION_FILE):
#         try:
#             os.remove(SESSION_FILE)
#         except Exception:
#             pass

# load_session()

# # ---------------- Initialize Session Defaults ----------------
# defaults = {
#     "logged_in": False,
#     "username": None,
#     "show_reset": False,
#     "reset_email": "",
#     "current_page": "Dashboard",
#     "user_data": {}  # per-user data
# }

# for key, val in defaults.items():
#     if key not in st.session_state:
#         st.session_state[key] = val

# # ---------------- Ensure user data structure ----------------
# def init_user_data(username):
#     if username not in st.session_state["user_data"]:
#         st.session_state["user_data"][username] = {
#             "chat_history": [],
#             "dashboard_df": None,
#             "dashboard_link": "",
#             "dashboard_symbol": None,
#             "dashboard_name": None,
#             "dashboard_history": []
#         }

# # ---------------- Main Page Function ----------------
# def main_page():
#     if "current_page" not in st.session_state:
#         st.session_state.current_page = "Dashboard"

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
#     init_user_data(username)  # ensure user has data

#     st.markdown(f"### 👋 Welcome, **{username}**")

#     # ---------------- Display Pages ----------------
#     page = st.session_state.current_page
#     if page == "Home":
#         st.markdown("🏠 Home Page")
#         st.write("Your dashboard home page")
#     elif page == "Chat":
#         chat_show(st.session_state["user_data"][username])
#     elif page == "Dashboard":
#         dashboard_show(st.session_state["user_data"][username])
#     elif page == "History":
#         history_show(st.session_state["user_data"][username])
#     elif page == "Settings":
#         setting_show(st.session_state["user_data"][username])

#     # ---------------- Logout ----------------
#     if st.sidebar.button("🚪 Logout"):
#         st.session_state.logged_in = False
#         st.session_state.username = None
#         st.session_state.current_page = "login"
#         clear_session_file()
#         save_session()
#         st.rerun()

# # ---------------- App Configuration ----------------
# st.set_page_config(page_title="Company Dashboard", page_icon="📊", layout="wide")

# # ---------------- Show Pages ----------------
# if st.session_state.logged_in:
#     main_page()
# else:
#     # Only show login/registration header here
#     st.markdown("<h1 style='text-align:center; color:#4B0082;'>🔐 Login & Registration System</h1>", unsafe_allow_html=True)

#     menu = ["Login", "Register"]
#     choice = st.sidebar.selectbox("Menu", menu)

#     if choice == "Register":
#         st.markdown("<h3 style='color:#4B0082;'>📝 Create a New Account</h3>", unsafe_allow_html=True)
#         username = st.text_input("Username", placeholder="Enter username")
#         email = st.text_input("Email", placeholder="Enter email")
#         password = st.text_input("Password", type="password", placeholder="Enter password")
#         if st.button("Register", use_container_width=True):
#             if username and email and password:
#                 register_user(username, email, password)
#             else:
#                 st.warning("⚠️ Please fill all fields")

#     elif choice == "Login":
#         st.markdown("<h3 style='color:#4B0082;'>🔑 Login to Your Account</h3>", unsafe_allow_html=True)
#         if not st.session_state.show_reset:
#             user_input = st.text_input("Username or Email", placeholder="Enter username or email")
#             password = st.text_input("Password", type="password", placeholder="Enter password")
#             if st.button("Login", use_container_width=True):
#                 user = login_user(user_input, password)
#                 if user and user != "not_registered":
#                     st.session_state.logged_in = True
#                     st.session_state.username = user[1]
#                     init_user_data(user[1])
#                     st.session_state.current_page = "Dashboard"
#                     save_session()
#                     st.success("✅ Login successful!")
#                     st.rerun()
#                 elif user == "not_registered":
#                     st.error("❌ User not found. Please register first.")
#                 else:
#                     st.error("❌ Invalid username/email or password.")

#             st.markdown("---")
#             if st.button("Forgot Password?", use_container_width=True):
#                 st.session_state.show_reset = True
#                 save_session()
#                 st.rerun()
#         else:
#             st.markdown("<h3 style='color:#4B0082;'>🔑 Reset Password</h3>", unsafe_allow_html=True)
#             if not st.session_state.reset_email:
#                 st.session_state.reset_email = st.text_input("Enter your registered email", key="email_for_reset")
#             reset_password(st.session_state.reset_email)
#             if st.button("Back to Login", use_container_width=True):
#                 st.session_state.show_reset = False
#                 save_session()
#                 st.rerun()

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
def main_page():
    page_options = ["Home", "Chat", "Dashboard", "History", "Settings"]
    try:
        index_page = page_options.index(st.session_state.current_page)
    except ValueError:
        index_page = 0

    def set_page():
        st.session_state.current_page = st.session_state.page_radio
        save_session()

    st.sidebar.radio(
        "Navigation:",
        page_options,
        index=index_page,
        key="page_radio",
        on_change=set_page
    )

    username = st.session_state.username
    init_user_data(username)

    st.markdown(f"### 👋 Welcome, **{username}**")

    page = st.session_state.current_page
    if page == "Home":
     home_show()
    elif page == "Chat":
     chat_show(st.session_state["user_data"][username])
    elif page == "Dashboard":
     dashboard_show(st.session_state["user_data"][username])
    elif page == "History":
     history_show(st.session_state["user_data"][username])
    elif page == "Settings":
     setting_show(st.session_state["user_data"][username])

    if st.sidebar.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.session_state.current_page = "login"
        clear_session_file()
        save_session()
        st.session_state["refresh_page"] = st.session_state.get("refresh_page", 0) + 1

# ---------------- App Configuration ----------------
st.set_page_config(page_title="Company Dashboard", page_icon="📊", layout="wide")

# ---------------- Show Pages ----------------
# if st.session_state.logged_in:
#     main_page()
# else:
#     st.markdown("<h1 style='text-align:center; color:#4B0082;'>🔐 Login & Registration System</h1>", unsafe_allow_html=True)

#     menu = ["Login", "Register"]
#     choice = st.sidebar.selectbox("Menu", menu)
# # ---------------- REGISTER ----------------
# if choice == "Register":
#     st.markdown("<h3 style='color:#4B0082;'>📝 Create a New Account</h3>", unsafe_allow_html=True)

#     # Input fields
#     username = st.text_input("Username", placeholder="Enter username", key="reg_username")
#     email = st.text_input("Email", placeholder="Enter email", key="reg_email")
#     password = st.text_input("Password", type="password", placeholder="Enter password", key="reg_password")

#     # Register button
#     if st.button("Register", use_container_width=True, key="register_btn"):
#         if not username or not email or not password:
#             st.warning("⚠️ Please fill all fields")
#         elif "@" not in email or not email.endswith(".com"):
#             st.error("❌ Please enter a valid Gmail address ending with @gmail.com")
#         elif len(password) < 4:
#             st.error("❌ Password must be at least 4 characters")
#         else:
#             # Call auth.py to handle database registration
#             success, msg = register_user(username, email, password)
#             if success:
#                 st.success("✅ Registration successful! You can now login.")
#                 # Clear inputs without touching st.session_state of widgets
#                 st.experimental_rerun()  # This is safe here just to clear inputs after success
#             else:
#                 st.error(f"❌ {msg}")
# # ---------------- LOGIN ----------------
#     elif choice == "Login":
#         st.markdown("<h3 style='color:#4B0082;'>🔑 Login to Your Account</h3>", unsafe_allow_html=True)
#         if not st.session_state.show_reset:
#             user_input = st.text_input("Username or Email", placeholder="Enter username or email")
#             password = st.text_input("Password", type="password", placeholder="Enter password")
#             if st.button("Login", use_container_width=True):
#                 user = login_user(user_input, password)
#                 if user and user != "not_registered":
#                     st.session_state.logged_in = True
#                     st.session_state.username = user[1]
#                     init_user_data(user[1])
#                     st.session_state.current_page = "Dashboard"
#                     save_session()
#                     st.success("✅ Login successful!")
#                     st.session_state["refresh_page"] = st.session_state.get("refresh_page", 0) + 1
#                 elif user == "not_registered":
#                     st.error("❌ User not found. Please register first.")
#                 else:
#                     st.error("❌ Invalid username/email or password.")

#             st.markdown("---")
#             if st.button("Forgot Password?", use_container_width=True):
#                 st.session_state.show_reset = True
#                 save_session()
#                 st.session_state["refresh_page"] = st.session_state.get("refresh_page", 0) + 1
#         else:
#             st.markdown("<h3 style='color:#4B0082;'>🔑 Reset Password</h3>", unsafe_allow_html=True)
#             if not st.session_state.reset_email:
#                 st.session_state.reset_email = st.text_input("Enter your registered email", key="email_for_reset")
#             reset_password(st.session_state.reset_email)
#             if st.button("Back to Login", use_container_width=True):
#                 st.session_state.show_reset = False
#                 save_session()
#                 st.session_state["refresh_page"] = st.session_state.get("refresh_page", 0) + 1
# # ---------------- CSS ----------------
# st.markdown("""
# <style>
# div.stButton > button {
#     background-color: #f5f5f5;
#     color: #333;
#     border: 2px solid #ccc;
#     border-radius: 6px;
#     padding: 0.6em 1.2em;
#     font-weight: 500;
#     cursor: pointer;
#     transition: background-color 0.2s ease-in-out, color 0.2s ease-in-out;
# }
# div.stButton > button:active {
#     background-color: #FF6B6B;  
#     color: white;
#     border-color: #FF6B6B;
# }
# </style>
# """, unsafe_allow_html=True)



# import streamlit as st
# from auth import register_user, login_user, reset_password, init_user_data, save_session

# # ---------------- CSS ----------------
# st.markdown("""
# <style>
# div.stButton > button {
#     background-color: #f5f5f5;
#     color: #333;
#     border: 2px solid #ccc;
#     border-radius: 6px;
#     padding: 0.6em 1.2em;
#     font-weight: 500;
#     cursor: pointer;
#     transition: background-color 0.2s ease-in-out, color 0.2s ease-in-out;
# }
# div.stButton > button:active {
#     background-color: #FF6B6B;  
#     color: white;
#     border-color: #FF6B6B;
# }
# </style>
# """, unsafe_allow_html=True)

# # ---------------- MAIN PAGE ----------------
# if st.session_state.get("logged_in", False):
#     st.markdown(f"### Welcome, {st.session_state.username}!")
#     # call your main dashboard function here
# else:
#     st.markdown("<h1 style='text-align:center; color:#4B0082;'>🔐 Login & Registration System</h1>", unsafe_allow_html=True)

#     menu = ["Login", "Register"]
#     choice = st.sidebar.selectbox("Menu", menu)

#     # ---------------- REGISTER ----------------
#     if choice == "Register":
#         st.markdown("<h3 style='color:#4B0082;'>📝 Create a New Account</h3>", unsafe_allow_html=True)
#         username = st.text_input("Username", placeholder="Enter username")
#         email = st.text_input("Email", placeholder="Enter email")
#         password = st.text_input("Password", type="password", placeholder="Enter password")

#         if st.button("Register", use_container_width=True):
#             if not username or not email or not password:
#                 st.warning("⚠️ Please fill all fields")
#             elif "@" not in email or not email.endswith(".com"):
#                 st.error("❌ Please enter a valid Gmail address ending with @gmail.com")
#             elif len(password) < 4:
#                 st.error("❌ Password must be at least 4 characters")
#             else:
#                 success, msg = register_user(username, email, password)
#                 if success:
#                     st.success("✅ Registration successful! You can now login.")
#                 else:
#                     st.error(f"❌ {msg}")

#     # ---------------- LOGIN ----------------
#     elif choice == "Login":
#         st.markdown("<h3 style='color:#4B0082;'>🔑 Login to Your Account</h3>", unsafe_allow_html=True)

#         if "show_reset" not in st.session_state:
#             st.session_state.show_reset = False

#         # ---------------- NORMAL LOGIN ----------------
#         if not st.session_state.show_reset:
#             user_input = st.text_input("Username or Email", placeholder="Enter username or email", key="login_user_input")
#             password = st.text_input("Password", type="password", placeholder="Enter password", key="login_password")

#             if st.button("Login", use_container_width=True, key="login_btn"):
#                 user = login_user(user_input, password)
#                 if user and user != "not_registered":
#                     st.session_state.logged_in = True
#                     st.session_state.username = user[1]
#                     init_user_data(user[1])
#                     st.session_state.current_page = "Dashboard"
#                     save_session()
#                     st.success("✅ Login successful!")
#                 elif user == "not_registered":
#                     st.error("❌ User not found. Please register first.")
#                 else:
#                     st.error("❌ Invalid username/email or password.")

#             st.markdown("---")
#             if st.button("Forgot Password?", use_container_width=True, key="forgot_btn"):
#                 st.session_state.show_reset = True

#         # ---------------- FORGOT PASSWORD ----------------
#         else:  # Forgot Password
#             st.markdown("<h3 style='color:#4B0082;'>🔑 Reset Password</h3>", unsafe_allow_html=True)

#             if "reset_step" not in st.session_state:
#                 st.session_state.reset_step = 1  # 1 = email, 2 = new password

#             # Step 1: Enter email
#             if st.session_state.reset_step == 1:
#                 email = st.text_input("Enter your registered email", key="reset_email_input")
#                 if st.button("Verify Email", use_container_width=True):
#                     result = reset_password(email)
#                     if result == "not_found":
#                         st.error("❌ Email not found. Please enter your registered email.")
#                     else:
#                         st.session_state.reset_email = email
#                         st.session_state.reset_step = 2

#             # Step 2: Enter new password
#             elif st.session_state.reset_step == 2:
#                 new_password = st.text_input("Enter new password", type="password", key="new_pass_input")
#                 if st.button("Reset Password", use_container_width=True):
#                     result = reset_password(st.session_state.reset_email, new_password)
#                     if result == "short_password":
#                         st.warning("⚠️ Password must be at least 4 characters.")
#                     elif result == "success":
#                         st.success("✅ Password successfully updated! You can now login.")
#                         st.session_state.reset_step = 1
#                         st.session_state.reset_email = ""

#             # Back to Login
#             if st.button("Back to Login", use_container_width=True):
#                 st.session_state.show_reset = False
#                 st.session_state.reset_step = 1
#                 st.session_state.reset_email = ""

if st.session_state.logged_in:
    main_page()
else:
    st.markdown("<h1 style='text-align:center; color:#4B0082;'>🔐 Login & Registration System</h1>", unsafe_allow_html=True)

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
                    st.experimental_rerun()
                else:
                    st.error(f"❌ {msg}")

    # ---------------- LOGIN ----------------
    elif choice == "Login":
        st.markdown("<h3 style='color:#4B0082;'>🔑 Login to Your Account</h3>", unsafe_allow_html=True)

        if not st.session_state.show_reset:
            user_input = st.text_input("Username or Email", placeholder="Enter username or email", key="login_user_input")
            password = st.text_input("Password", type="password", placeholder="Enter password", key="login_password")

            if st.button("Login", use_container_width=True, key="login_btn"):
                user = login_user(user_input, password)
                if user and user != "not_registered":
                    st.session_state.logged_in = True
                    st.session_state.username = user[1]
                    init_user_data(user[1])
                    st.session_state.current_page = "Dashboard"
                    save_session()
                    st.success("✅ Login successful!")
                elif user == "not_registered":
                    st.error("❌ User not found. Please register first.")
                else:
                    st.error("❌ Invalid username/email or password.")

        #     st.markdown("---")
        #     if st.button("Forgot Password?", use_container_width=True, key="forgot_btn"):
        #         st.session_state.show_reset = True

        # else:
        #     st.markdown("<h3 style='color:#4B0082;'>🔑 Reset Password</h3>", unsafe_allow_html=True)
        #     if not st.session_state.reset_email:
        #         st.session_state.reset_email = st.text_input("Enter your registered email", key="email_for_reset")
        #     reset_password(st.session_state.reset_email)
        #     if st.button("Back to Login", use_container_width=True, key="back_btn"):
        #         st.session_state.show_reset = False
        #         st.session_state.reset_email = ""

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