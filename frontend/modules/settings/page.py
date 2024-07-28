import streamlit as st
from st_pages import hide_pages
from time import sleep
from streamlit.runtime.scriptrunner import get_script_run_ctx
from streamlit.source_util import get_pages

#page config
#config
def set_page_config(auth_status):
    if auth_status:
        st.set_page_config(
            page_title="kotact dashboard",
            page_icon="📊",
            #layout="centered",
            initial_sidebar_state="auto",
            #menu_items={
            #    'Get Help': 'https://www.extremelycoolapp.com/help',
            #    'Report a bug': "https://www.extremelycoolapp.com/bug",
            #    'About': "# This is a header. This is an *extremely* cool app!"
            #}
        )
    else:
        st.set_page_config(
            page_title="kotact dashboard",
            page_icon="📊",
            initial_sidebar_state="collapsed",
        )        


def get_current_page_name():
    ctx = get_script_run_ctx()
    if ctx is None:
        raise RuntimeError("Couldn't get script context")

    pages = get_pages("")

    return pages[ctx.page_script_hash]["page_name"]


def make_sidebar(auth_status, user_info):
    with st.sidebar:
        #st.markdown("<div style='text-align: center;'> 회사 로고 </div>", unsafe_allow_html=True)
        st.markdown("**⚉ Kotact Dashboard**  \n version :gray-background[0.1]", unsafe_allow_html=True)
        st.markdown("""<div style="height:0.5px;border:none;color:#D3D3D3;background-color:#D3D3D3;" /> """, unsafe_allow_html=True)
        #st.markdown("")
        if auth_status == True:
            st.markdown("<div style='text-align: center;'> 🟢 </div>", unsafe_allow_html=True)
            st.markdown(f"""<div style='text-align: center;'> {user_info["full_name"]} </div>""", unsafe_allow_html=True)
            st.markdown(f"""<div style='text-align: center; color: grey;'> {user_info["email"]} </div>""", unsafe_allow_html=True)
            
            st.markdown("")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("나의정보", use_container_width=True):
                    st.switch_page("pages/my_profile.py")
            with col2:
                if st.button("로그아웃", use_container_width=True):
                    logout()

            #st.markdown("")
            st.markdown("""<div style="height:0.5px;border:none;color:#D3D3D3;background-color:#D3D3D3;" /> """, unsafe_allow_html=True)
            st.markdown("🏠&nbsp; Home")
            st.page_link("pages/hello.py", label="&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Welcome")
            st.markdown("🚀&nbsp; App")
            st.page_link("pages/quiz_generator.py", label="&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 한국어 퀴즈 생성기")

        elif not auth_status == True:
            st.page_link("main.py", label="로그인")
            st.page_link("pages/signup.py", label="회원가입")

        elif get_current_page_name() != "main":
            # If anyone tries to access a secret page without being logged in,
            # redirect them to the login page
            st.switch_page("main.py")

def logout():
    st.session_state = {}
    st.switch_page("main.py")

