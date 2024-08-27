import streamlit as st
from modules.validation.key_validation import validate_openai_api_key
from modules.validation.form_validation import validate_text
from modules.quiz.api_quiz import get_quiz, translate_quiz

def sync_translation_interface():
    with st.container(height=450):
        with st.popover('번역 언어',use_container_width=True):
            st.selectbox('From',['English'])
            language = st.selectbox('To',["Vietnamese", "Japanese", "Chinese"])
        messages = st.container(height=350)
    if prompt := st.chat_input("번역할 문장을 입력해 주세요"):
        messages.chat_message("user").write(prompt)
        assistant_message = messages.chat_message("assistant").empty()
            
        translated_quiz = translate_quiz(
            token_type = st.session_state["token_type"], 
            access_token = st.session_state["access_token"],
            openai_api_key = st.session_state["openai_api_key"],
            quiz = prompt,
            language = language)
        messages.chat_message("assistant").write(translated_quiz["results"])

def async_translation_interface():
    with st.container(height=450):
        with st.popover('번역 언어', use_container_width=True):
            st.selectbox('From', ['English'])
            language = st.selectbox('To', ["Vietnamese", "Japanese", "Chinese"])
        messages = st.container(height=350)

    if prompt := st.chat_input("번역할 문장을 입력해 주세요"):
        messages.chat_message("user").write(prompt)
        
        # 번역 결과를 위한 빈 메시지 생성
        assistant_message = messages.chat_message("assistant").empty()
        
        translated_text = ""
        try:
            for chunk in translate_quiz(
                token_type=st.session_state["token_type"], 
                access_token=st.session_state["access_token"],
                openai_api_key=st.session_state["openai_api_key"],
                quiz=prompt,
                language=language
            ):
                if chunk.startswith("Error:"):
                    assistant_message.error(chunk)
                    break
                if chunk.startswith("data: "):  # SSE 형식에서 데이터 추출
                    chunk = chunk[6:]  # "data: " 제거
                translated_text += chunk
                # 실시간으로 번역 결과 업데이트
                assistant_message.markdown(translated_text)
        except Exception as e:
            assistant_message.error(f"An error occurred: {str(e)}")

def async_generation_interface():
    username = st.session_state["user_info"]["username"]
    with st.container(border=True, height=450):
        if "quiz_messages" not in st.session_state:
            st.session_state["quiz_messages"] = [{"role": "assistant", "content": f"안녕하세요 {username} 님 !  \n '퀴즈 생성' 버튼을 클릭하여 퀴즈를 생성해 주세요!"}]
        
        if st.session_state["quiz_messages"]:
            for idx, msg in enumerate(st.session_state["quiz_messages"]):
                with st.chat_message(name=msg["role"], avatar="/app/src/images/bot_icon_2.jpg"): #avatar="https://raw.githubusercontent.com/dataprofessor/streamlit-chat-avatar/master/bot-icon.png"
                    st.markdown(msg["content"])
        
        if st.session_state["quiz_ready"]==True:

            messages = st.empty()
            assistant_message = messages.chat_message("assistant", avatar="/app/src/images/bot_icon_2.jpg").empty()

            generated_text = ""    
            try:
                for chunk in get_quiz(
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
                        chunk = chunk[6:]  # "data: " 제거
                    generated_text += chunk
                    # 실시간으로 생성 결과 업데이트
                    assistant_message.markdown(generated_text)
                
            except Exception as e:
                assistant_message.error(f"An error occurred: {str(e)}")

            st.session_state["quiz_messages"].append({"role": "assistant", "content": generated_text})

            st.session_state['quiz_ready'] = False

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
    #with st.form("quiz_generator_form"):
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
    #with st.container():
    st.markdown("퀴즈 개수를 선택하세요")
    number = st.slider(" ", 1, 10, 3,label_visibility="collapsed")

    #submitted = st.form_submit_button("생성 시작", type="primary", use_container_width=True)
    submitted = st.button("생성 시작",type="primary", use_container_width=True)
    if submitted:
        #valid = False
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

            st.rerun()
        