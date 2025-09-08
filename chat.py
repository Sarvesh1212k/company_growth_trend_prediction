
# import streamlit as st
# import mysql.connector
# import hashlib
# import pandas as pd
# import numpy as np
# from datetime import datetime
# from sklearn.linear_model import LinearRegression
# import plotly.express as px
# import yfinance as yf
# import re
# import urllib.parse
# import json
# import os
# import streamlit as st
# import random
# # chat.py
# import streamlit as st
# from datetime import datetime
# import json
# import os

# SESSION_FILE = "session_state.json"

# # ---------------- Session Save Function ----------------
# def save_session():
#     """Save the current session state to a JSON file."""
#     session_data = dict(st.session_state)
#     with open(SESSION_FILE, "w") as f:
#         json.dump(session_data, f, default=str)

# # ---------------- Chat Page ----------------
# def chat_page():
#     st.subheader("💬 Chat with Bot")
#     if "chat_history" not in st.session_state:
#         st.session_state.chat_history = []

#     chat_container = st.container()
#     with chat_container:
#         for i, (sender, msg, timestamp) in enumerate(st.session_state.chat_history):
#             time_str = timestamp.strftime("%H:%M")
#             col1, col2 = st.columns([9, 1])
#             with col1:
#                 if sender == "user":
#                     st.markdown(f"""
#                         <div style='text-align:right; margin:5px 0;'>
#                             <div style='display:inline-block; background:#DCF8C6; padding:10px 15px; border-radius:15px; 
#                             box-shadow:1px 2px 5px rgba(0,0,0,0.1); max-width:70%;'>
#                                 {msg} <span style='font-size:10px; color:gray;'>{time_str}</span>
#                             </div>
#                         </div>
#                     """, unsafe_allow_html=True)
#                 else:
#                     st.markdown(f"""
#                         <div style='text-align:left; margin:5px 0;'>
#                             <div style='display:inline-block; background:#E6E6E6; padding:10px 15px; border-radius:15px; 
#                             box-shadow:1px 2px 5px rgba(0,0,0,0.1); max-width:70%;'>
#                                 🤖 {msg} <span style='font-size:10px; color:gray;'>{time_str}</span>
#                             </div>
#                         </div>
#                     """, unsafe_allow_html=True)
#             with col2:
#                 if st.button("🗑️", key=f"chat_del_{i}"):
#                     st.session_state.chat_history.pop(i)
#                     save_session()
#                     st.rerun()

#     user_input = st.text_input("Type your message...", key="chat_input", placeholder="Ask something...")
#     if st.button("Send", use_container_width=True) and user_input:
#         st.session_state.chat_history.append(("user", user_input, datetime.now()))
#         bot_reply = f"I received: {user_input}"
#         st.session_state.chat_history.append(("bot", bot_reply, datetime.now()))
#         save_session()
#         st.rerun()

#     if st.button("🗑️ Delete All Chat", key="delete_all_chat"):
#         st.session_state.chat_history = []
#         save_session()
#         st.rerun()

# Yahoo-Finance-Ticker-Symbols

# import streamlit as st
# import pandas as pd
# import os
# import re
# import random
# from datetime import datetime

# def show():
#     st.title("💬 Company Link Bot")

#     # ---------------- Load CSV ----------------
#     @st.cache_data
#     def load_companies(file_path="Yahoo-Finance-Ticker-Symbols.csv"):
#         if not os.path.exists(file_path):
#             st.error(f"CSV file not found: {file_path}")
#             return pd.DataFrame(columns=["Symbol", "Company"])
#         df = pd.read_csv(file_path, sep="|", header=None, usecols=[0, 1], names=["Symbol", "Company"])
#         return df

#     companies_df = load_companies()

#     # ---------------- Initialize Chat History ----------------
#     if "chat_history" not in st.session_state:
#         st.session_state.chat_history = []

#     # ---------------- Delete Chat Button ----------------
#     if st.button("🗑️ Delete Chat"):
#         st.session_state.chat_history = []

#     # ---------------- User Input ----------------
#     user_input = st.text_input("Ask me for company link(s):")

#     if user_input:
#         user_text = user_input.strip()
#         response = []

#         if "link" in user_text.lower():
#             company_names = re.split(r',\s*', user_text)
#             links_list = []

#             # Try to match each company name
#             for name in company_names:
#                 if len(name) < 2:
#                     continue
#                 matched = companies_df[companies_df['Company'].str.contains(name, case=False, na=False)]
#                 if not matched.empty:
#                     for _, row in matched.iterrows():
#                         link = f"https://finance.yahoo.com/quote/{row['Symbol']}"
#                         links_list.append(f"{row['Company']} → {link}")

#             # If no matches, pick random companies based on number requested
#             if not links_list:
#                 number_match = re.search(r"\b(\d+)\b", user_text)
#                 count = int(number_match.group(1)) if number_match else 1
#                 count = min(count, len(companies_df))
#                 selected = companies_df.sample(count).dropna(subset=['Company'])
#                 for _, row in selected.iterrows():
#                     link = f"https://finance.yahoo.com/quote/{row['Symbol']}"
#                     links_list.append(f"{row['Company']} → {link}")

#             # Number links
#             numbered_links = [f"{i+1}. {link}" for i, link in enumerate(links_list)]
#             response = "\n".join(numbered_links)
#         else:
#             response = "I can only provide Yahoo Finance links. Please ask for a link."

#         # Append new chat with timestamp
#         st.session_state.chat_history.append(("You", user_text, datetime.now()))
#         st.session_state.chat_history.append(("Bot", response, datetime.now()))

#     # ---------------- Display Chat ----------------
#     displayed = []
#     for entry in st.session_state.chat_history:
#         if len(entry) == 3:
#             sender, msg, timestamp = entry
#         elif len(entry) == 2:
#             sender, msg = entry
#             timestamp = None
#         if (sender, msg) not in displayed:
#             displayed.append((sender, msg))
#             if timestamp:
#                 st.markdown(f"**{sender}:**\n{msg} ({timestamp.strftime('%H:%M')})")
#             else:
#                 st.markdown(f"**{sender}:** {msg} (No timestamp)")

import streamlit as st
import pandas as pd
import os
import re
import random
from datetime import datetime

def show(user_dict):
    st.title("💬 Company Link Bot")

    # ---------------- Load CSV ----------------
    @st.cache_data
    def load_companies(file_path="Yahoo-Finance-Ticker-Symbols.csv"):
        if not os.path.exists(file_path):
            st.error(f"CSV file not found: {file_path}")
            return pd.DataFrame(columns=["Symbol", "Company"])
        df = pd.read_csv(file_path, sep="|", header=None, usecols=[0, 1], names=["Symbol", "Company"])
        return df

    companies_df = load_companies()

    # ---------------- Initialize Chat History ----------------
    if "chat_history" not in user_dict:
        user_dict["chat_history"] = []

    # ---------------- Delete Chat Button ----------------
    if st.button("🗑️ Delete Chat"):
        user_dict["chat_history"] = []

    # ---------------- User Input ----------------
    user_input = st.text_input("Ask me for company link(s):")

    if user_input:
        user_text = user_input.strip()
        response = []

        if "link" in user_text.lower():
            company_names = re.split(r',\s*', user_text)
            links_list = []

            # Try to match each company name
            for name in company_names:
                if len(name) < 2:
                    continue
                matched = companies_df[companies_df['Company'].str.contains(name, case=False, na=False)]
                if not matched.empty:
                    for _, row in matched.iterrows():
                        link = f"https://finance.yahoo.com/quote/{row['Symbol']}"
                        links_list.append(f"{row['Company']} → {link}")

            # If no matches, pick random companies based on number requested
            if not links_list:
                number_match = re.search(r"\b(\d+)\b", user_text)
                count = int(number_match.group(1)) if number_match else 1
                count = min(count, len(companies_df))
                selected = companies_df.sample(count).dropna(subset=['Company'])
                for _, row in selected.iterrows():
                    link = f"https://finance.yahoo.com/quote/{row['Symbol']}"
                    links_list.append(f"{row['Company']} → {link}")

            # Number links
            numbered_links = [f"{i+1}. {link}" for i, link in enumerate(links_list)]
            response = "\n".join(numbered_links)
        else:
            response = "I can only provide Yahoo Finance links. Please ask for a link."

        # Append new chat with timestamp
        user_dict["chat_history"].append(("You", user_text, datetime.now()))
        user_dict["chat_history"].append(("Bot", response, datetime.now()))

    # ---------------- Display Chat ----------------
    displayed = []
    for entry in user_dict["chat_history"]:
        if len(entry) == 3:
            sender, msg, timestamp = entry
        elif len(entry) == 2:
            sender, msg = entry
            timestamp = None
        if (sender, msg) not in displayed:
            displayed.append((sender, msg))
            if timestamp:
                st.markdown(f"**{sender}:**\n{msg} ({timestamp.strftime('%H:%M')})")
            else:
                st.markdown(f"**{sender}:** {msg} (No timestamp)")
