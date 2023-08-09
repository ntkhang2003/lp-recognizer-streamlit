import streamlit as st


def page_meta(page_title: str, page_icon, layout='wide', show_title=True, is_under_construction=False):
    st.set_page_config(page_title=f'lp-recognizer | {page_title}', page_icon=page_icon, layout=layout)

    with st.sidebar:
        st.info('Select type of file')
        st.markdown('Created by [ntkhang](https://github.com/ntkhang2003)'
                    '<br/> © All right reserved',
                    unsafe_allow_html=True)
        st.markdown('[![Star](https://img.shields.io/github/stars/ntkhang2003/lp-recognizer-streamlit.svg?logo=github&style=social)](https://github.com/ntkhang2003/lp-recognizer-streamlit)')
    if show_title:
        st.title(page_title)
    if is_under_construction:
        st.image('https://media.istockphoto.com/id/1283050796/vector/flat-design-under-construction-concept.jpg?s=612x612&w=0&k=20&c=CATQe8sEl7YdpwxZ4VHwYh5FjHY9MkbyRNhALyslZwA=')