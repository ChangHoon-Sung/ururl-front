import os
import requests
import streamlit as st

st.set_page_config(page_title="Sign Up")

BACKEND_URL = f"http://{os.getenv('BACK_SERVICE_HOST')}:{os.getenv('BACK_SERVICE_PORT')}"
is_finished = False

st.title("👤 Sign Up")
_ = st.empty()
with _.container():
    st.markdown("""Already have an account? <a href="/" target=_self>Home</a>""", unsafe_allow_html=True)
    st.write("Almost done!")
    with st.form("signup_form"):
        st.text_input("username", key="signup_username")
        st.text_input("password", key="signup_password", type="password")
        st.text_input("password check", key="signup_password2", type="password")
        
        signup_sumitted = st.form_submit_button("Sign in")

        if signup_sumitted:
            if not st.session_state["signup_username"]:
                st.error("username required")
            elif st.session_state["signup_password"] != st.session_state["signup_password2"]:
                st.error("password doesn't match")
            else:
                r: requests.Response = requests.post(
                    f"{BACKEND_URL}/api/account/signup",
                    json={
                        "username": st.session_state["signup_username"],
                        "password": st.session_state["signup_password"],
                    },
                )
                if r.status_code == 200:
                    is_finished = True
                elif r.status_code / 100 in (4, 5):
                    st.error(f"{r.status_code} Error: {r.text}")

if is_finished:
    _.empty()
    st.success(f"Sign up success! 🎉")
    st.markdown(f"""Let's go to <a href="/" target="_self"> 🏡 Home</a>""", unsafe_allow_html=True)