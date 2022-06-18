import os
import streamlit as st
import requests

print(f"requested node: {os.getenv('MY_NODE_NAME')}")

# init page settings
BACKEND_URL = f"http://{os.getenv('BACK_SERVICE_HOST')}:{os.getenv('BACK_SERVICE_PORT')}"

st.set_page_config(page_title="URURL")

st.title("URURL.LIFE")
st.write(f"node: {os.getenv('MY_NODE_NAME')}")
st.write("Make your url short and easy to share!")

# init session states
if 'request_session' not in st.session_state.keys():
    st.session_state['request_session'] = requests.Session()

if "user" not in st.session_state.keys():
    st.session_state["user"] = None


# random url generator layout
with st.form("random_form"):
    st.text_input("your url", key="random_origin")
    random_sumitted = st.form_submit_button("Shorten!")

# generate random url
if random_sumitted:
    r = requests.post(
        f"{BACKEND_URL}/api/generate",
        json={"origin": st.session_state.get("random_origin")},
    )
    if r.status_code == 200 or r.status_code == 201:
        left, _ = st.columns(2)
        left.success(f"ururl is: {r.text}")
        st.balloons()
    elif r.status_code / 100 in (4, 5):
        st.error(f"{r.status_code} Error: {r.text}")


# make extra space
for _ in range(2):
    st.text("\n ")


# if logged in, show custom url generator
if st.session_state['user']:
    st.header("Customize!")
    st.write("You can make your own url!")

    with st.form("custom_form"):
        st.text_input("your url", key="custom_origin")
        st.text_input(
            "custom id",
            placeholder = "" if st.session_state['user'] else "signin required",
            key="custom_id",
            disabled=not st.session_state['user'],
        )
        custom_sumitted = st.form_submit_button("Shorten!")

    if custom_sumitted:
        if not st.session_state["custom_id"]:
            st.error("signin required")
        else:
            r = st.session_state['request_session'].post(
                f"{BACKEND_URL}/api/custom/generate",
                json={"origin": st.session_state["custom_origin"], "id": st.session_state["custom_id"]},
            )
            if r.status_code == 200 or r.status_code == 201:
                left, _ = st.columns(2)
                left.success(f"ururl is: {r.text}")
                st.balloons()
            elif r.status_code / 100 in (4, 5):
                st.error(f"{r.status_code} Error: {r.text}")

# signin layout
else:
    st.header("Sign in")
    st.markdown("""Don't have an account? <a href="/Sign_Up" target=_self>Sign up</a>""", unsafe_allow_html=True)
    with st.form("signin_form"):
        st.text_input("username", key="signin_username")
        st.text_input("password", key="signin_password", type="password")
        signin_sumitted = st.form_submit_button("Sign in")

    if signin_sumitted:
        r: requests.Response = st.session_state['request_session'].post(
            f"{BACKEND_URL}/api/account/signin",
            json={
                "username": st.session_state["signin_username"],
                "password": st.session_state["signin_password"],
            },
        )
        if r.status_code == 200:
            st.session_state["request_session"].headers.update({"X-CSRFToken": r.cookies["csrftoken"]})
            st.session_state["user"] = st.session_state['request_session'].cookies.get_dict()
        elif r.status_code / 100 in (4, 5):
            st.error(f"{r.status_code} Error: {r.text}")
        st.experimental_rerun()
