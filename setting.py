# import streamlit as st

# def show():
#     st.title("⚙️ Settings Page")

import streamlit as st

def show(user_dict):
    st.title("⚙️ Settings Page")

    # Theme selection (user-specific)
 

    # Button to clear only the current user's data
    if st.button("🗑️ Clear My Chat & Dashboard Data"):
        user_dict["chat_history"] = []
        user_dict["dashboard_df"] = None
        user_dict["dashboard_history"] = []
        st.success("✅ Your data has been cleared!")
        # Safe page refresh without deprecated rerun
        st.session_state["refresh_page"] = st.session_state.get("refresh_page", 0) + 1
