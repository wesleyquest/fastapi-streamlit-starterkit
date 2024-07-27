import streamlit as st
from st_pages import hide_pages
from time import sleep
from streamlit.runtime.scriptrunner import get_script_run_ctx
from streamlit.source_util import get_pages

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

def get_current_page_name():
    ctx = get_script_run_ctx()
    if ctx is None:
        raise RuntimeError("Couldn't get script context")

    pages = get_pages("")

    return pages[ctx.page_script_hash]["page_name"]


def make_sidebar():
    with st.sidebar:
        st.title("💎 로고")
        if st.session_state["auth_status"] == True:
            
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("안녕하세요 !  \n 🐱 000 님")
            with col2:
                if st.button("Log out", use_container_width=False):
                    logout()

            st.write("")
            st.write("")
            #st.page_link("pages/page1.py", label="Secret Company Stuff", icon="🔒")
            st.page_link("pages/hello.py")
            st.page_link("pages/my_profile.py")
            st.page_link("pages/quiz_generator.py")

            st.write("")
            st.write("")


        elif not st.session_state["auth_status"] == True:
            st.page_link("main.py")
            st.page_link("pages/signup.py")

        elif get_current_page_name() != "main":
            # If anyone tries to access a secret page without being logged in,
            # redirect them to the login page
            st.switch_page("main.py")


def logout():
    st.session_state = {}
    st.info("Logged out successfully!")
    sleep(0.5)
    st.switch_page("main.py")

