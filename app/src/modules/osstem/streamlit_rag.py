import streamlit as st
# from modules.validation.key_validation import get_api_key_check
from modules.validation.form_validation import validate_text
import json

# #modal
# @st.dialog(" ", width="small")
# def open_openaiapikey_modal(old_key=None):
#     if old_key:
#         value = old_key
#     else:
#         value = None
#     openai_api_key = st.text_input("OpenAI API KEY", value=value, key="chatbot_api_key", type="password")
#     "[OpenAI API key 알아보기] (https://platform.openai.com/account/api-keys)"
#     key_message_placeholder = st.container()
#     st.markdown(" ")
#     col1, col2 = st.columns(2)
#     with col1:
#         if st.button("적용", type="primary", use_container_width=True, key="modal_openaiapikey_button"):
#             if validate_openai_api_key(openai_api_key):
#                 st.session_state["key_status"] = True
#                 st.session_state["openai_api_key"] = openai_api_key
#                 st.rerun()
#             else:
#                 key_message_placeholder.error("OpenAI API KEY를 정확히 입력하세요")
#     with col2:
#         if st.button("닫기", type="secondary", use_container_width=True):
#             st.rerun()
