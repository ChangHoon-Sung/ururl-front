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
    shorten = f'{r.text}'
    st.write(f'[{shorten}]({shorten})')
    st.balloons()

    prev_origin = origin
