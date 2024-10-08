import streamlit as st
from modules.validation.form_validation import validate_text
from modules.quiz.api_quiz import get_batch_quiz, translate_batch_quiz, translate_stream_quiz
import json

def expander():
    col1,col2,col3 = st.columns([2,2,1])
    with col1:
        if prompt := st.chat_input("번역할 문장을 입력해 주세요",disabled=not bool(st.session_state["key_status"])):
            st.session_state["translated_messages"].append({"role":"user","content":prompt,"answer":"","typing":True})
            st.session_state['translate_ready'] = True
            st.rerun()
    with col2:
        quiz_list = [[msg['content'],msg['explain']] for msg in st.session_state['quiz_messages'][2:]]
        selected_quiz = st.selectbox("Quiz List", quiz_list, index=None, placeholder="Quiz를 선택해 주세요",label_visibility='collapsed')
        selected_language = st.session_state["language"]
        if selected_quiz != None:
            with st.container(border=True):
                st.markdown(f"<p style='text-align: center;'> 선택된 퀴즈를 {selected_language}로 번역하시겠습니까?</p>",unsafe_allow_html=True)
                if st.button("번역",use_container_width=True):
                    st.session_state["translated_messages"].append({"role":"user","content":selected_quiz[0], "answer":selected_quiz[1],"typing":False})
                    st.session_state["translate_ready"]=True
                    st.rerun()

    with col3:
        with st.popover('번역 옵션',use_container_width=True):
            st.selectbox('From', ['English'])
            language_list = {"Vietnamese":0,"Japanese":1,"Chinese":2}
            index = language_list[st.session_state["language"]]
            language = st.selectbox('To', ["Vietnamese", "Japanese", "Chinese"],index=index)
            st.session_state["language"] = language

            if st.toggle("Activate Streaming", value=st.session_state["stream"]):
                st.session_state["stream"]=True
            else:
                st.session_state["stream"] = False

@st.dialog(" ", width="large")
def open_answer_modal(answer):
    st.markdown("")
    for i in range(len(answer)):
        with st.container(border=True):
            st.markdown(answer[i])

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
                #quiz_content
                st.session_state["quiz"]["input"]["quiz_content"] = []
                if tog_content_vocabulary_focused_quiz:
                    st.session_state["quiz"]["input"]["quiz_content"].append("vocabulary_focused")
                if tog_content_sentence_example_based_quiz:
                    st.session_state["quiz"]["input"]["quiz_content"].append("sentence_example")
                if tog_content_cultural_information_quiz:
                    st.session_state["quiz"]["input"]["quiz_content"].append("cultural_information")
                if tog_content_word_order_quiz:
                    st.session_state["quiz"]["input"]["quiz_content"].append("word_order")
                #quiz_type
                st.session_state["quiz"]["input"]["quiz_type"] = []
                if tog_type_multiple_choice:
                    st.session_state["quiz"]["input"]["quiz_type"].append("multiple_choice")
                if tog_type_true_or_false:
                    st.session_state["quiz"]["input"]["quiz_type"].append("true_or_false")
                if tog_type_fill_in_the_blank:
                    st.session_state["quiz"]["input"]["quiz_type"].append("fill_in_the_blank")
                st.session_state["rerun"]=True
                st.rerun()
    with but2:
        if st.button("닫기",type="primary", use_container_width=True):
            st.rerun()    

def batch_generation_interface():
    with st.container(border=True, height=500):
        if st.session_state["quiz_messages"]:
            for idx, msg in enumerate(st.session_state["quiz_messages"]):
                if msg["role"]=="user":
                    with st.chat_message(name=msg["role"], avatar="/app/src/images/user_icon_1.png"): #avatar="https://raw.githubusercontent.com/dataprofessor/streamlit-chat-avatar/master/bot-icon.png"
                        st.markdown(msg["content"])
                        if (idx !=0) and (idx!=1):
                            if st.button("해설보기",key=f"explanation_button_{idx}",use_container_width=True):
                                open_answer_modal(msg["explain"])
                else:
                    with st.chat_message(name=msg["role"], avatar="/app/src/images/bot_icon_2.jpg"): #avatar="https://raw.githubusercontent.com/dataprofessor/streamlit-chat-avatar/master/bot-icon.png"
                        st.markdown(msg["content"])
                        if (idx !=0) and (idx!=1):
                            if st.button("해설보기",key=f"explanation_button_{idx}",use_container_width=True):
                                open_answer_modal(msg["explain"])
                        
        if st.session_state["quiz_ready"]==True:

            assistant_message = st.chat_message("assistant", avatar="/app/src/images/bot_icon_2.jpg").empty()
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

            generated_quiz = generated_text["results"]
            generated_answer = generated_text["answer"]

            with assistant_message:
                with st.container():
                    st.markdown(generated_quiz)
                    if st.button("해설보기", key = "generate_tmp",use_container_width=True):
                        open_answer_modal(generated_answer)

            st.session_state["quiz_messages"].append({"role": "assistant", "content": generated_quiz,"explain":generated_answer})

            st.session_state['quiz_ready'] = False
            st.rerun()

def batch_translation_interface():
    with st.container(height=500):
        if st.session_state["translated_messages"]:
            for idx, msg in enumerate(st.session_state["translated_messages"]):
                if msg["role"]=="user":
                    with st.chat_message(name=msg["role"], avatar="/app/src/images/user_icon_1.png"): #avatar="https://raw.githubusercontent.com/dataprofessor/streamlit-chat-avatar/master/bot-icon.png"
                        st.markdown(msg["content"])
                        #if idx !=0:
                        if msg["typing"]==False:
                            if st.button("해설보기",key=f"batch_explanation_button_{idx}",use_container_width=True):
                                open_answer_modal(msg["answer"])
                else:
                    with st.chat_message(name=msg["role"], avatar="/app/src/images/bot_icon_2.jpg"): #avatar="https://raw.githubusercontent.com/dataprofessor/streamlit-chat-avatar/master/bot-icon.png"
                        st.markdown(msg["content"])
                        #if idx !=0:
                        if msg["typing"]==False:
                            if st.button("해설보기",key=f"batch_explanation_button_{idx}",use_container_width=True):
                                open_answer_modal(msg["answer"])
                            
        if st.session_state['translate_ready']:
            assistant_message = st.chat_message("assistant", avatar="/app/src/images/bot_icon_2.jpg").empty()
            
            with st.spinner('번역 중입니다...'):
                translated_text = translate_batch_quiz(
                    token_type = st.session_state["token_type"], 
                    access_token = st.session_state["access_token"],
                    openai_api_key = st.session_state["openai_api_key"],
                    quiz = st.session_state["translated_messages"][-1]["content"],
                    answer = "\n".join(st.session_state["translated_messages"][-1]["answer"]),
                    language = st.session_state["language"])
            if st.session_state["translated_messages"][-1]["typing"]==False:
                translated_quiz = "🚀" + translated_text["results"].split("🚀")[1]
                translated_answer = ["🚀" + text for text in translated_text["results"].split("🚀")[2:]]
            else:
                translated_quiz = translated_text["results"]
                translated_answer = ""
            with assistant_message:
                with st.container():
                    st.markdown(translated_quiz)
                    if st.session_state["translated_messages"][-1]["typing"]==False:
                        if st.button("해설보기",key="translate_tmp",use_container_width=True):
                            open_answer_modal(translated_answer)

            
            if st.session_state["translated_messages"][-1]["typing"]:
                st.session_state["translated_messages"].append({"role": "assistant", "content": translated_quiz, "answer":translated_answer,"typing":True})
            else:
                st.session_state["translated_messages"].append({"role": "assistant", "content": translated_quiz, "answer":translated_answer,"typing":False})
            st.session_state["translate_ready"]=False
            st.rerun()
    expander()

def stream_translation_interface():
    with st.container(height=500):        
        if st.session_state["translated_messages"]:
            for idx, msg in enumerate(st.session_state["translated_messages"]):
                if msg["role"]=="user":
                    with st.chat_message(name=msg["role"], avatar="/app/src/images/user_icon_1.png"): #avatar="https://raw.githubusercontent.com/dataprofessor/streamlit-chat-avatar/master/bot-icon.png"
                        st.markdown(msg["content"])
                        if msg["typing"]==False:
                            if st.button("해설보기",key=f"batch_explanation_button_{idx}",use_container_width=True):
                                open_answer_modal(msg["answer"])
                else:    
                    with st.chat_message(name=msg["role"], avatar="/app/src/images/bot_icon_2.jpg"): #avatar="https://raw.githubusercontent.com/dataprofessor/streamlit-chat-avatar/master/bot-icon.png"
                        st.markdown(msg["content"])
                        if msg["typing"]==False:
                            if st.button("해설보기",key=f"stream_explanation_button_{idx}",use_container_width=True):
                                open_answer_modal(msg["answer"])
                        
        if st.session_state['translate_ready']:
            assistant_message = st.chat_message("assistant", avatar="/app/src/images/bot_icon_2.jpg").empty()
            
            answer = False
            with assistant_message:
                with st.container():
                    messages = st.empty()
                    translated_text = ""
                    translated_answer = ""
                    try:
                        for chunk in translate_stream_quiz(
                            token_type=st.session_state["token_type"], 
                            access_token=st.session_state["access_token"],
                            openai_api_key=st.session_state["openai_api_key"],
                            quiz=st.session_state["translated_messages"][-1]["content"],
                            answer="\n".join(st.session_state["translated_messages"][-1]["answer"]),
                            language=st.session_state["language"]
                        ):
                            if chunk.startswith("Error:"):
                                assistant_message.error(chunk)
                                break
                            if chunk.startswith("data: "):  # SSE 형식에서 데이터 추출
                                data = json.loads(chunk[6:])
                                text = data['text'] # "data: " 제거
                                #translated_text += text + "\n"

                                if answer==False:
                                    translated_text += text + "\n"
                                    if translated_text.count("🚀")==2:
                                        answer=True
                                        translated_answer += translated_text[translated_text.find("🚀",2):] + "\n"
                                        translated_text = translated_text[:translated_text.find("🚀",2)]
                                        
                                else:
                                    translated_answer += text + "\n"

                                # 실시간으로 번역 결과 업데이트
                                messages.markdown(translated_text)

                        translated_answer = ["🚀" + txt for txt in translated_answer.split("🚀")][1:]
                        if st.session_state["translated_messages"][-1]["typing"]==False:
                            explain = st.button("해설보기",key="translate_tmp",use_container_width=True)
                            if explain:
                                open_answer_modal(translated_answer)

                        if st.session_state["translated_messages"][-1]["typing"]:
                            st.session_state["translated_messages"].append({"role": "assistant", "content": translated_text, "answer":"","typing":True})
                        else:
                            st.session_state["translated_messages"].append({"role": "assistant", "content": translated_text, "answer":translated_answer,"typing":False})
                    except Exception as e:
                        assistant_message.error(f"An error occurred: {str(e)}")
                st.session_state["translate_ready"]=False
                st.rerun()
    expander()
