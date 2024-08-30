import streamlit as st
from modules.validation.key_validation import validate_openai_api_key
from modules.validation.form_validation import validate_text
from modules.quiz.api_quiz import get_batch_quiz,get_stream_quiz, translate_batch_quiz, translate_stream_quiz
import json

def popover():
    with st.popover('번역 언어', use_container_width=True):
        st.selectbox('From', ['English'])
        language = st.selectbox('To', ["Vietnamese", "Japanese", "Chinese"])
        st.session_state["language"] = language
        quiz_list = [msg['content'] for msg in st.session_state['quiz_messages'][1:]]
        quiz_list.append('직접입력')
        selected_quiz = st.selectbox("Quiz List", quiz_list)
        if selected_quiz != "직접입력":    
            if st.button('생성하기'):
                st.session_state["translated_messages"].append({"role":"user","content":selected_quiz})
                st.session_state["translate_ready"]=True
                st.rerun()
        else:
            if prompt := st.chat_input("번역할 문장을 입력해 주세요"):
                st.session_state["translated_messages"].append({"role":"user","content":prompt})
                st.session_state['translate_ready'] = True
                st.rerun()

#modal
@st.dialog(" ", width="small")
def open_openaiapikey_modal(old_key=None):
    if old_key:
        value = old_key
    else:
        value = None
    openai_api_key = st.text_input("OpenAI API KEY", value=value, key="chatbot_api_key", type="password")
    "[OpenAI API key 알아보기] (https://platform.openai.com/account/api-keys)"
    key_message_placeholder = st.container()
    st.markdown(" ")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("적용", type="primary", use_container_width=True, key="modal_openaiapikey_button"):
            if validate_openai_api_key(openai_api_key):
                st.session_state["key_status"] = True
                st.session_state["openai_api_key"] = openai_api_key
                st.rerun()
            else:
                key_message_placeholder.error("OpenAI API KEY를 정확히 입력하세요")
    with col2:
        if st.button("닫기", type="secondary", use_container_width=True):
            st.rerun()

@st.dialog(" ", width="large")
def open_settings_modal():
    st.markdown("")
    st.markdown("퀴즈를 생성할 문서를 입력하세요")
    document = st.text_area(" ",label_visibility="collapsed")
    document_valid_placeholder = st.container()
    
    #quiz content
    #with st.container():
    st.markdown("퀴즈 콘텐츠를 선택하세요 (1개 이상)")
    col_1, col_2, col_3, col_4 = st.columns(4)
    with col_1: 
        #Vocabulary Focused Quiz: 단어 중심
        tog_content_vocabulary_focused_quiz = st.toggle("단어 중심", value=True)
    with col_2: 
        #Sentence Example Based Quiz: 문장 기반
        tog_content_sentence_example_based_quiz = st.toggle("문장 기반", value=True)
    with col_3:
        #Cultural Information Quiz: 문화 정보
        tog_content_cultural_information_quiz = st.toggle("문화 정보", value=True)
    with col_4:
        #Word Order Quiz: 단어 순서
        tog_content_word_order_quiz = st.toggle("단어 순서", value=True)  
    tog_content_valid_placeholder = st.container()
    #quiz type
    #with st.container():
    st.markdown("퀴즈 타입을 선택하세요 (1개 이상)")
    col_1, col_2, col_3, col_4 = st.columns(4)
    with col_1:
        #Multiple Choice: 객관식
        tog_type_multiple_choice = st.toggle("객관식", value=True)
    with col_2:
        #True Or False: 참거짓
        tog_type_true_or_false = st.toggle("참/거짓", value=True)
    with col_3:
        #Fill In The Blank: 빈칸채우기
        tog_type_fill_in_the_blank = st.toggle("빈칸 채우기", value=True)
    with col_4:
        st.markdown("")
    tog_type_valid_placeholder =  st.container()

    #quiz number
    st.markdown("퀴즈 개수를 선택하세요")
    number = st.slider(" ", 1, 10, 3,label_visibility="collapsed")

    but1, but2 = st.columns(2)
    with but1:
        submitted = st.button("생성 시작",type="primary", use_container_width=True)
        if submitted:
            st.session_state["quiz_ready"] = False
            if validate_text(document):
                if tog_content_vocabulary_focused_quiz | tog_content_sentence_example_based_quiz | tog_content_cultural_information_quiz | tog_content_word_order_quiz:
                    if tog_type_multiple_choice | tog_type_true_or_false | tog_type_fill_in_the_blank:
                        #valid = True
                        st.session_state["quiz_ready"] = True
                    else:
                        tog_type_valid_placeholder.markdown(":red[퀴즈 타입을 1개 이상 선택하세요]")
                else:
                    tog_content_valid_placeholder.markdown(":red[퀴즈 콘텐츠를 1개 이상 선택하세요]")
            else:
                document_valid_placeholder.markdown(":red[퀴즈를 생성할 문서를 입력하세요 (10자 이상)]")

            #if valid:
            if st.session_state["quiz_ready"]:
                #initialization
                st.session_state["quiz"] = {
                    "input": {
                        "document": document,
                        "quiz_content": [],
                        "quiz_type": [],
                        "number": number
                    }
                }
                #document
                #print(document)
                #quiz_content
                st.session_state["quiz"]["input"]["quiz_content"] = []
                #print(tog_content_vocabulary_focused_quiz)
                if tog_content_vocabulary_focused_quiz:
                    st.session_state["quiz"]["input"]["quiz_content"].append("vocabulary_focused")
                #print(tog_content_sentence_example_based_quiz)
                if tog_content_sentence_example_based_quiz:
                    st.session_state["quiz"]["input"]["quiz_content"].append("sentence_example")
                #print(tog_content_cultural_information_quiz)
                if tog_content_cultural_information_quiz:
                    st.session_state["quiz"]["input"]["quiz_content"].append("cultural_information")
                #print(tog_content_word_order_quiz)
                if tog_content_word_order_quiz:
                    st.session_state["quiz"]["input"]["quiz_content"].append("word_order")
                #quiz_type
                st.session_state["quiz"]["input"]["quiz_type"] = []
                #print(tog_type_multiple_choice)
                if tog_type_multiple_choice:
                    st.session_state["quiz"]["input"]["quiz_type"].append("multiple_choice")
                #print(tog_type_true_or_false)
                if tog_type_true_or_false:
                    st.session_state["quiz"]["input"]["quiz_type"].append("true_or_false")
                #print(tog_type_fill_in_the_blank)
                if tog_type_fill_in_the_blank:
                    st.session_state["quiz"]["input"]["quiz_type"].append("fill_in_the_blank")
                st.session_state["rerun"]=True
                st.rerun()
    with but2:
        if st.button("닫기",type="primary", use_container_width=True):
            st.rerun()    

def batch_generation_interface():
    with st.container(border=True, height=450):
        if st.session_state["quiz_messages"]:
            for idx, msg in enumerate(st.session_state["quiz_messages"]):
                with st.chat_message(name=msg["role"], avatar="/app/src/images/bot_icon_2.jpg"): #avatar="https://raw.githubusercontent.com/dataprofessor/streamlit-chat-avatar/master/bot-icon.png"
                    st.markdown(msg["content"])
        
        if st.session_state["quiz_ready"]==True:

            messages = st.empty()
            assistant_message = messages.chat_message("assistant", avatar="/app/src/images/bot_icon_2.jpg").empty()
            with st.spinner('퀴즈를 생성 중입니다...'):
                generated_text = get_batch_quiz(
                    token_type = st.session_state["token_type"], 
                    access_token = st.session_state["access_token"],
                    openai_api_key = st.session_state["openai_api_key"],
                    document = st.session_state["quiz"]["input"]["document"],
                    quiz_content = st.session_state["quiz"]["input"]["quiz_content"],
                    quiz_type = st.session_state["quiz"]["input"]["quiz_type"],
                    number = st.session_state["quiz"]["input"]["number"]
                )
            assistant_message.markdown(generated_text["results"]) 
            
            st.session_state["quiz_messages"].append({"role": "assistant", "content": generated_text["results"]})

            st.session_state['quiz_ready'] = False

def stream_generation_interface():
    with st.container(border=True, height=450):
        if st.session_state["quiz_messages"]:
            for idx, msg in enumerate(st.session_state["quiz_messages"]):
                with st.chat_message(name=msg["role"], avatar="/app/src/images/bot_icon_2.jpg"): #avatar="https://raw.githubusercontent.com/dataprofessor/streamlit-chat-avatar/master/bot-icon.png"
                    st.markdown(msg["content"])
        if st.session_state["quiz_ready"]==True:
            messages = st.empty()
            assistant_message = messages.chat_message("assistant", avatar="/app/src/images/bot_icon_2.jpg").empty()

            generated_text = ""    
            try:
                for chunk in get_stream_quiz(
                    token_type = st.session_state["token_type"], 
                    access_token = st.session_state["access_token"],
                    openai_api_key = st.session_state["openai_api_key"],
                    document = st.session_state["quiz"]["input"]["document"],
                    quiz_content = st.session_state["quiz"]["input"]["quiz_content"],
                    quiz_type = st.session_state["quiz"]["input"]["quiz_type"],
                    number = st.session_state["quiz"]["input"]["number"]
                ):
                    if chunk.startswith("Error:"):
                        assistant_message.error(chunk)
                        break
                    if chunk.startswith("data: "):  # SSE 형식에서 데이터 추출
                        data = json.loads(chunk[6:]) # "data: " 제거
                        text = data['text']
                        generated_text += text + "\n"
                        assistant_message.markdown(generated_text)   
                
            except Exception as e:
                assistant_message.error(f"An error occurred: {str(e)}")

            st.session_state["quiz_messages"].append({"role": "assistant", "content": generated_text})

            st.session_state['quiz_ready'] = False

def batch_translation_interface():
    with st.container(height=450):
        if st.session_state["translated_messages"]:
            for idx, msg in enumerate(st.session_state["translated_messages"]):
                with st.chat_message(name=msg["role"], avatar="/app/src/images/bot_icon_2.jpg"): #avatar="https://raw.githubusercontent.com/dataprofessor/streamlit-chat-avatar/master/bot-icon.png"
                    st.markdown(msg["content"])
        if st.session_state['translate_ready']:
            messages = st.empty()
            assistant_message = messages.chat_message("assistant", avatar="/app/src/images/bot_icon_2.jpg").empty()
            with st.spinner('번역 중입니다...'):
                translated_quiz = translate_batch_quiz(
                    token_type = st.session_state["token_type"], 
                    access_token = st.session_state["access_token"],
                    openai_api_key = st.session_state["openai_api_key"],
                    quiz = st.session_state["translated_messages"][-1]["content"],
                    language = st.session_state["language"])
            assistant_message.markdown(translated_quiz["results"]) 
            st.session_state["translate_ready"]=False
    popover()

def stream_translation_interface():
    with st.container(height=450):        
        if st.session_state["translated_messages"]:
            for idx, msg in enumerate(st.session_state["translated_messages"]):
                with st.chat_message(name=msg["role"], avatar="/app/src/images/bot_icon_2.jpg"): #avatar="https://raw.githubusercontent.com/dataprofessor/streamlit-chat-avatar/master/bot-icon.png"
                    st.markdown(msg["content"])
        if st.session_state['translate_ready']:
            messages = st.empty()
            assistant_message = messages.chat_message("assistant", avatar="/app/src/images/bot_icon_2.jpg").empty()
            translated_text = ""
            try:
                for chunk in translate_stream_quiz(
                    token_type=st.session_state["token_type"], 
                    access_token=st.session_state["access_token"],
                    openai_api_key=st.session_state["openai_api_key"],
                    quiz=st.session_state["translated_messages"][-1]["content"],
                    language=st.session_state["language"]
                ):
                    if chunk.startswith("Error:"):
                        assistant_message.error(chunk)
                        break
                    if chunk.startswith("data: "):  # SSE 형식에서 데이터 추출
                        data = json.loads(chunk[6:])
                        text = data['text'] # "data: " 제거
                        translated_text += text + "\n"
                        # 실시간으로 번역 결과 업데이트
                        assistant_message.markdown(translated_text)
                        
                st.session_state["translated_messages"].append({"role": "assistant", "content": translated_text})
            except Exception as e:
                assistant_message.error(f"An error occurred: {str(e)}")
            st.session_state["translate_ready"]=False
    popover()
