import streamlit as st
from st_pages import Page, show_pages, add_page_title, hide_pages, Section, add_indentation
from time import sleep

from modules.custom.style import style_global
from modules.custom.style import set_page_config_sidebar_collapsed, set_page_config_sidebar_expanded
from modules.custom.style import show_pages_auth_false, show_pages_auth_true

set_page_config_sidebar_expanded()
style_global()
show_pages_auth_true()

with st.sidebar:
    if st.button("로그아웃", use_container_width=False):
        st.session_state = {}
        show_pages_auth_false()
        st.switch_page("main.py")

st.title("Hello", anchor=False)






