
import streamlit as st

# def show(user_dict):
#     st.title("📜 History Page")

#     st.markdown("### Dashboard History")
#     if "dashboard_history" in user_dict and user_dict["dashboard_history"]:
#         for item in user_dict["dashboard_history"]:
#             st.write(f"- {item}")
#     else:
#         st.info("No dashboard history available.")

#     st.markdown("### Chat History")
#     if "chat_history" in user_dict and user_dict["chat_history"]:
#         for entry in user_dict["chat_history"]:
#             if len(entry) == 3:
#                 sender, msg, timestamp = entry
#                 st.write(f"**{sender}:** {msg} ({timestamp.strftime('%H:%M')})")
#             elif len(entry) == 2:
#                 sender, msg = entry
#                 st.write(f"**{sender}:** {msg}")
#     else:
#         st.info("No chat history available.")
def show(user_dict):
    st.title("📜 History Page")

    # ---------------- Dashboard History ----------------
    st.markdown("### 📊 Dashboard History")
    dashboard_history = user_dict.get("dashboard_history", []) if user_dict else []
    if dashboard_history:
        for item in dashboard_history:
            st.markdown(
                f"""
                <div style='background:#F9F9FF; padding:12px; margin:8px 0; 
                            border-radius:10px; border:1px solid #DDD; word-wrap:break-word;'>
                    <b>🕒 {item.get('time').strftime('%Y-%m-%d %H:%M:%S') if item.get('time') else ''}</b><br>
                    <b>Symbol:</b> {item.get('symbol','')} <br>
                    <b>Name:</b> {item.get('name','')} <br>
                    <a href="{item.get('link','')}" target="_blank">🔗 Open Link</a>
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        st.info("No dashboard history available.")

    # ---------------- Chat History ----------------
    st.markdown("### 💬 Chat History")
    chat_history = user_dict.get("chat_history", []) if user_dict else []
    if chat_history:
        for entry in chat_history:
            if len(entry) == 3:
                sender, msg, timestamp = entry

                # Split multiple items by numbers like "1. ", "2. " etc.
                import re
                items = re.split(r'\d+\.\s', msg)
                items = [item.strip() for item in items if item.strip()]

                formatted_msg = ""
                for i, item in enumerate(items, start=1):
                    # Split name and link (assuming '→' or last space before https)
                    if "http" in item:
                        parts = item.rsplit("http", 1)
                        name_part = parts[0].strip()
                        url_part = "http" + parts[1].strip()
                        formatted_msg += f"{i}. {name_part} → <a href='{url_part}' target='_blank'>{url_part}</a><br>"
                    else:
                        formatted_msg += f"{i}. {item}<br>"

                # Bubble colors
                if sender.lower() == "you":
                    bubble_color = "#E0E7FF"
                    align = "right"
                else:
                    bubble_color = "#F0FFF0"
                    align = "left"

                st.markdown(
                    f"""
                    <div style='background:{bubble_color}; padding:10px; border-radius:10px; 
                                margin:6px 0; text-align:{align}; word-break:break-word; overflow-wrap:anywhere;'>
                        <b>{sender}:</b><br>
                        {formatted_msg}
                        <small>{timestamp.strftime('%Y-%m-%d %H:%M')}</small>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            elif len(entry) == 2:
                sender, msg = entry
                st.markdown(
                    f"""
                    <div style='background:#FFFBEA; padding:10px; border-radius:10px; 
                                margin:6px 0; word-break:break-word; overflow-wrap:anywhere;'>
                        <b>{sender}:</b><br>{msg}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
    else:
        st.info("No chat history available.")

    # CSS for timestamp
    st.markdown("""
    <style>
    small { color:#666; font-size:12px; }
    </style>
    """, unsafe_allow_html=True)
