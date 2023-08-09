import streamlit as st
from component.page_meta import page_meta
from utils.switch_page import switch_page

page_meta(page_title='Welcome', page_icon='👋', show_title=False)

st.markdown(
    f'''
    # License Plate Recognizer 👋

    Key Features:

    1. {switch_page(title='**Recognition in image**', page='/Photo')}
    2. {switch_page(title='**Recognition in video**', page='/Video')}
    '''
    , unsafe_allow_html=True
)