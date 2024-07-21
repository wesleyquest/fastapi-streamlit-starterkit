from openai import OpenAI
import streamlit as st
import time

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


with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"

    
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

        #st.session_state["messages"] = [{"role": "assistant", "content": "this is quiz"}]
        with st.spinner("..."):
            time.sleep(1)
            st.session_state.messages.append({"role": "assistant", "content": "아래와 같이 퀴즈를 생성했어요."})
            st.rerun()

def reset_conversation():
  #message 초기화
  st.session_state.messages = [st.session_state.messages[0]]
  ##st.session_state.chat_history = None

with st.container():
    col_1, col_2 = st.columns(2)
    with col_1:
        if st.button("퀴즈 생성", type="primary", use_container_width=True):
            open_settings_modal()

    with col_2:
        st.button('퀴즈 삭제', on_click=reset_conversation, use_container_width=True)

with st.container():
    st.markdown(" ")


if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "안녕하세요! 코택트 퀴즈 생성기입니다.  \n 버튼을 클릭하여 퀴즈를 생성해 주세요!"}]

if st.session_state.messages:
    #반대 순서로 보기('reversed')
    for msg in reversed(st.session_state.messages):
        st.chat_message(msg["role"]).write(msg["content"])





