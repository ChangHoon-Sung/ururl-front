import os
import streamlit as st
import requests

BACKEND_URL = os.getenv('BACKEND_URL')

st.title("URURL.LIFE")
st.write('Make your url short and easy to remember!')

prev_origin = ''
origin = st.text_input('your url', key='origin')
button = st.button('Shorten!')
shorten = ''

# You can access the value at any point with:
if button or (prev_origin != origin):
    r = requests.post(f'{BACKEND_URL}/api/generate', json={'origin': st.session_state.get('origin')})
    shorten = f'http://{r.text}'
    st.write(f'[{shorten}]({shorten})')
    st.balloons()

    prev_origin = origin
