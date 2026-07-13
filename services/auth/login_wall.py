import streamlit as st
from services.persistence.exercise_repository import get_or_create_user
def render_login_wall():
    if st.session_state.get("user_id") is not None:
         return True
    
    st.title("🏋️ FitMentor AI")

    st.markdown("""
    ## 👋 Welcome!

    ### Your Personal AI Gym Coach

    Enter your username below to start training with your AI coach.
    """)

    with st.form("login_form", clear_on_submit=False):
        username = st.text_input(
            "Username",
            placeholder="Enter a unique username (e.g., yoggarg)"
        )
        submit_button = st.form_submit_button("Start Session", width="stretch")
         
    if submit_button:
        if not username.strip():
            st.error("Username cannot be empty.")
            return False
        user=get_or_create_user(username)
        st.session_state["username"]=user["username"]
        st.session_state["user_id"]=user["id"]

        st.rerun()
    

    return False


