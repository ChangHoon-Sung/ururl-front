import os
import streamlit as st
import requests

BACKEND_URL = os.getenv('BACKEND_URL')

st.set_page_config(page_title='URURL')

st.title("URURL.LIFE")
st.write('Make your url short and easy to share!')

prev_origin = ''
origin = st.text_input('your url', key='origin')
button = st.button('Shorten!')
shorten = ''

# You can access the value at any point with:
if button and (prev_origin != origin):
    r = requests.post(f'{BACKEND_URL}/api/generate', json={'origin': st.session_state.get('origin')})
    if r.status_code == 200 or r.status_code == 201:
        left, _ = st.columns(2)
        left.success(f'ururl is: {r.text}')
        st.balloons()
    elif r.status_code / 100 in (4, 5):
        st.error(f'{r.status_code} Error: {r.text}')

    prev_origin = origin
