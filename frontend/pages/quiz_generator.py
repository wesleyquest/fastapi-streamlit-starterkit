import streamlit as st
from st_pages import add_indentation
from modules.custom.style import style_global
from modules.custom.style import set_page_config_sidebar_expanded
from modules.custom.style import show_pages_auth_true, show_pages_auth_false
from openai import OpenAI
import time

set_page_config_sidebar_expanded()
show_pages_auth_true()
style_global()

#var
if "auth_status" not in st.session_state:
    st.session_state["auth_status"] = None
if "key_status" not in st.session_state:
    st.session_state["key_status"] = None

if st.session_state["auth_status"]==True:
    from modules.auth.api_auth import get_user_info
    st.session_state["user_info"] = get_user_info(token_type=st.session_state["token_type"], access_token=st.session_state["access_token"])


@st.experimental_dialog(" ", width="small")
def open_login_modal():
    username = st.text_input("사용자명", placeholder="Username (Email)")
    password = st.text_input("비밀번호", placeholder="Password", type="password")

    if st.button("로그인", type="primary", use_container_width=True, key="modal_log_in_button"):
        from modules.auth.api_auth import get_access_token
        data = get_access_token(username=username, password=password)
        
        if data["access_token"]:
            st.session_state["auth_status"] = True
            st.session_state["access_token"] = data["access_token"]
            st.session_state["token_type"] = data["token_type"]
        else:
            st.session_state["auth_status"] = False
        
        st.rerun()


@st.experimental_dialog(" ", width="small")
def open_logout_modal():
    st.markdown("로그아웃 하시겠습니까 ?")

    email = st.session_state["user_info"]["email"]
    nickname = st.session_state["user_info"]["full_name"]

    st.info(f"Username (Email) : {email}  \n nickname : {nickname}")



    if st.button("로그아웃", type="primary", use_container_width=True, key="modal_log_out_button"):
        st.session_state["auth_status"] = None
        st.session_state["key_status"] = None
        st.rerun()

@st.experimental_dialog(" ", width="small")
def open_openaiapikey_modal():
    openai_api_key = st.text_input("OpenAI API KEY", key="chatbot_api_key", type="password")
    "[OpenAI API key 알아보기] (https://platform.openai.com/account/api-keys)"

    if st.button("적용", type="primary", use_container_width=True, key="modal_openaiapikey_button"):
        st.session_state["key_status"] = True
        st.session_state["openai_api_key"] = openai_api_key
        st.rerun()


# sidebar
with st.sidebar:
    #st.info("    &nbsp;<br /> &nbsp;&nbsp;&nbsp;   \n ㅇㄹ")

    login_placeholder = st.container()
    #logout_placeholder = st.empty()
    key_placeholder = st.container()
    
    if not st.session_state["auth_status"]==True:
        if login_placeholder.button("로그인 (LOG IN)", type="primary", use_container_width=True, key="log_in_button"):
            open_login_modal()

    if not st.session_state["key_status"]==True:
        if key_placeholder.button("OpenAI API KEY 입력", type="primary", use_container_width=True, key="openai_api_key_button"):
            open_openaiapikey_modal()
    else:
        if key_placeholder.button("OpenAI API KEY 수정", type="secondary", use_container_width=True, key="openai_api_key_2_button"):
            open_openaiapikey_modal()



#info
st.markdown(" ")
status_col_1, status_col_2 = st.columns(2)
with status_col_1:
    if not st.session_state["auth_status"]==True:
        st.info("🔴 &nbsp;&nbsp; LOG IN  \n &nbsp;&nbsp;")
    else :
        nickname = st.session_state["user_info"]["full_name"]
        st.info(f"🟢 &nbsp;&nbsp; LOG IN  : ( {nickname} )")
with status_col_2:
    if not st.session_state["key_status"]==True:
        st.info("🔴 &nbsp;&nbsp; API KEY  \n &nbsp;&nbsp;")
    else:
        from modules.security.encryption import str_to_asterisk
        openai_api_key_enc = str_to_asterisk(st.session_state["openai_api_key"])
        st.info(f"🟢 &nbsp;&nbsp; API KEY  : ( {openai_api_key_enc} )")



# main
login_info_placeholder=st.container()
key_info_placeholder=st.container()
st.title("🚀 Kotact Quiz Generator", anchor=False)
st.caption("version 0.1")


@st.experimental_dialog("Settings", width="large")
def open_settings_modal():
    #quiz document
    st.markdown(":blue-background[**1. 퀴즈 생성용 문서를 입력하세요 (Input document)**]")
    with st.container():
        st.text_area(" ",label_visibility="collapsed")
    #quiz content
    st.markdown(":blue-background[**2. 퀴즈 콘텐츠를 선택하세요 (Select quiz content)**]")
    with st.container():
        col_1, col_2, col_3, col_4 = st.columns(4)
        with col_1: 
            #Vocabulary Focused Quiz: 단어 중심
            tog_vocabulary_focused_quiz = st.toggle("단어 중심", value=True)
        with col_2: 
            #Sentence Example Based Quiz: 문장 기반
            tog_sentence_example_based_quiz = st.toggle("문장 기반", value=True)
        with col_3:
            #Cultural Information Quiz: 문화 정보
            tog_cultural_information_quiz = st.toggle("문화 정보", value=True)
        with col_4:
            #Word Order Quiz: 단어 순서
            tog_word_order_quiz = st.toggle("단어 순서", value=True)
    #quiz type
    st.markdown(":blue-background[**3. 퀴즈 타입을 선택하세요 (Select quiz type)**]")
    with st.container():
        col_1, col_2, col_3, col_4 = st.columns(4)
        with col_1:
            #Multiple Choice: 객관식
            on_1 = st.toggle("객관식", value=True)
        with col_2:
            #True Or False: 참거짓
            on_2 = st.toggle("참/거짓", value=True)
        with col_3:
            #Fill In The Blank: 빈칸채우기
            on_3 = st.toggle("빈칸 채우기", value=True)
        with col_4:
            st.write("")
    if st.button("생성 시작", type="primary", use_container_width=True):
        #st.session_state.vote = {"item": item, "reason": reason}

        #st.session_state["quiz_messages"] = [{"role": "assistant", "content": "this is quiz"}]
        with st.spinner("..."):
            time.sleep(1)
            st.session_state.quiz_messages.append({"role": "assistant", "content": "아래와 같이 퀴즈를 생성했어요."})
            st.rerun()

def reset_conversation():
  #message 초기화
  st.session_state.quiz_messages = [st.session_state.quiz_messages[0]]
  ##st.session_state.chat_history = None



#message
if st.session_state["auth_status"]==True:
    if login_placeholder.button("로그아웃 (LOG OUT)", type="secondary", use_container_width=True, key="log_out_button"):
        open_logout_modal()

elif st.session_state["auth_status"] == False:
    #login_info_placeholder.error("🔴 :red[로그인 실패 !  사용자명 또는 비밀번호가 잘못 됐어요]")
    login_info_placeholder.code("""🔴 로그인 실패 ! 사용자명과 비밀번호를 확인해 주세요""")

else:
    #login_info_placeholder.info("👈 로그인을 진행해 주세요")
    login_info_placeholder.code("""👈 로그인을 진행해 주세요""")


if not st.session_state["key_status"]==True:
    #key_info_placeholder.info(f"👈 OpenAI API KEY를 입력하세요")
    key_info_placeholder.code("""👈 OpenAI API KEY를 입력하세요""")




#quiz generator
if (st.session_state["auth_status"]==True) & (st.session_state["key_status"]==True):

    nickname = st.session_state["user_info"]["full_name"]

    
    with st.container():
        col_1, col_2 = st.columns(2)
        with col_1:
            if st.button("퀴즈 생성", type="primary", use_container_width=True):
                open_settings_modal()

        with col_2:
            st.button('퀴즈 삭제', on_click=reset_conversation, use_container_width=True)

    #빈칸
    with st.container():
        st.markdown(" ")


    if "quiz_messages" not in st.session_state:
        st.session_state["quiz_messages"] = [{"role": "assistant", "content": f"안녕하세요 {nickname} 님 !  \n '퀴즈 생성' 버튼을 클릭하여 퀴즈를 생성해 주세요!"}]

    if st.session_state.quiz_messages:
        #반대 순서로 보기('reversed')
        for msg in reversed(st.session_state.quiz_messages):
            st.chat_message(msg["role"]).write(msg["content"])




