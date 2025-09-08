# import streamlit as st

# def show():
#     st.title("📜 History Page")

#     st.markdown("### Dashboard History")
#     if "dashboard_history" in st.session_state and st.session_state.dashboard_history:
#         for item in st.session_state.dashboard_history:
#             st.write(f"- {item}")
#     else:
#         st.info("No dashboard history available.")

#     st.markdown("### Chat History")
#     if "chat_history" in st.session_state and st.session_state.chat_history:
#         for entry in st.session_state.chat_history:
#             if len(entry) == 3:
#                 sender, msg, timestamp = entry
#                 st.write(f"**{sender}:** {msg} ({timestamp.strftime('%H:%M')})")
#             elif len(entry) == 2:
#                 sender, msg = entry
#                 st.write(f"**{sender}:** {msg}")
#     else:
#         st.info("No chat history available.")

import streamlit as st

def show(user_dict):
    st.title("📜 History Page")

    st.markdown("### Dashboard History")
    if "dashboard_history" in user_dict and user_dict["dashboard_history"]:
        for item in user_dict["dashboard_history"]:
            st.write(f"- {item}")
    else:
        st.info("No dashboard history available.")

    st.markdown("### Chat History")
    if "chat_history" in user_dict and user_dict["chat_history"]:
        for entry in user_dict["chat_history"]:
            if len(entry) == 3:
                sender, msg, timestamp = entry
                st.write(f"**{sender}:** {msg} ({timestamp.strftime('%H:%M')})")
            elif len(entry) == 2:
                sender, msg = entry
                st.write(f"**{sender}:** {msg}")
    else:
        st.info("No chat history available.")
