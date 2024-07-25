import streamlit as st
from st_pages import Page, show_pages, add_page_title, hide_pages, Section, add_indentation


#page config
#config
def set_page_config_sidebar_collapsed():
    st.set_page_config(
        #page_title="Ex-stream-ly Cool App",
        #page_icon="🧊",
        #layout="centered",
        initial_sidebar_state="collapsed", #"expanded"
        #menu_items={
        #    'Get Help': 'https://www.extremelycoolapp.com/help',
        #    'Report a bug': "https://www.extremelycoolapp.com/bug",
        #    'About': "# This is a header. This is an *extremely* cool app!"
        #}
    )

def set_page_config_sidebar_expanded():
    st.set_page_config(
        initial_sidebar_state="expanded"
    )

def show_pages_auth_false():
    add_indentation()
    show_pages(
        [
            Section("Home", icon="🏠"),
            Page("main.py", "로그인"),
            Page("pages/signup.py", "회원가입")
        ]
    )

def show_pages_auth_true():
    add_indentation()
    show_pages(
        [
            Section("Home", icon="🏠"),
            Page("pages/welcome.py", "Welcome"),
            Page("pages/my_profile.py", "My Profile"),
            Section("App", icon="🚀"),
            Page("pages/quiz_generator.py", "한국어 퀴즈 생성")
        ]
    )


#style
def style_global():
    st.markdown("""
        <style>
        div.stButton {text-align:center}
        </style>""", unsafe_allow_html=True)

    st.markdown("""
        <style>
        div.stSpinner > div {
        text-align:center;
        align-items: center;
        justify-content: center;
        }
        </style>""", unsafe_allow_html=True)

    st.markdown("""
        <style>
        .main > .block-container {
            padding-top: 0rem;
            padding-bottom: 0rem;
            padding-left: 5rem;
            padding-right: 5rem;
        }
        </style>""", unsafe_allow_html=True)

