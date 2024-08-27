import os
from langchain.chat_models import ChatOpenAI
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import load_prompt
from src.quiz.utils.fewshot import sample_fewshot


async def generate_gpt4o_quiz(
        openai_api_key,
        document,
        quiz_content,
        quiz_type,
        number
):
    # fewshot
    # llm = ChatOpenAI(model_name = "gpt-4o", streaming=True, callbacks=[StreamingStdOutCallbackHandler()],
    #                 temperature = 0,
    #                 openai_api_key= openai_api_key)
    # prompt = load_prompt(os.path.join('/app/src/quiz/utils/prompt', 'quiz_generator.yaml'))
    # topic = document.split('\n')[0]
    # reference = '\n'.join(document.split('\n')[1:])
    # quiz_content_list = {'vocabulary_focused':'create quizzes based on words',
    #                 'sentence_example':'create quizzes based on sentences',
    #                 'cultural_information':'create quizzes based on culture',
    #                 'word_order':'create quizzes based on the order of words'}
    # quiz_content_prompt = ''
    # for i in quiz_content:
    #     quiz_content_prompt = quiz_content_prompt + '-'+ quiz_content_list[i] + '\n'
    # quiz_type_list={'multiple_choice':'create multiple choice quizzes',
    #        'true_or_false':'create true/false quizzes',
    #        'fill_in_the_blank':'create fill-in-the-blank quizzes'}
    
    # quiz_type_prompt = ''
    # for i in quiz_type:
    #     quiz_type_prompt = quiz_type_prompt + '-'+ quiz_type_list[i] + '\n'

    # fewshot_prompt = sample_fewshot(quiz_content,quiz_type,number)
    # input_data = {"topic": topic,"reference": reference,"quiz_content":quiz_content,"quiz_type":quiz_type,"fewshot":fewshot_prompt,"number":number}
    # rag_chain = (
    #     prompt
    #     | llm
    #     | StrOutputParser()
    # )

    # results = rag_chain.invoke(input_data)
    # return results

    # sync
    # llm = ChatOpenAI(model_name = "gpt-4o", streaming=True, callbacks=[StreamingStdOutCallbackHandler()],
    #                 temperature = 0,
    #                 openai_api_key= openai_api_key)
    # prompt = load_prompt(os.path.join('/app/src/quiz/utils/prompt', 'quiz_generator_pythonic.yaml'))
    # topic = document.split('\n')[0]
    # reference = '\n'.join(document.split('\n')[1:])

    # input_data = {"topic": topic,"reference": reference,"quiz_content":quiz_content,"quiz_type":quiz_type,"number":number}

    # chain = (
    #     prompt
    #     | llm
    #     | StrOutputParser()
    # )

    # results = chain.invoke(input_data)
    # return results

    llm = ChatOpenAI(model_name = "gpt-4o", streaming=True, callbacks=[StreamingStdOutCallbackHandler()],
                    temperature = 0,
                    openai_api_key= openai_api_key)
    prompt = load_prompt(os.path.join('/app/src/quiz/utils/prompt', 'quiz_generator_pythonic.yaml'))
    topic = document.split('\n')[0]
    reference = '\n'.join(document.split('\n')[1:])

    input_data = {"topic": topic,"reference": reference,"quiz_content":quiz_content,"quiz_type":quiz_type,"number":number}

    chain = (
        prompt
        | llm
        | StrOutputParser()
    )

    async def generate():
        async for chunk in chain.astream(input_data):
            yield f"data: {chunk}\n\n"
    return generate
# async def translate_gpt4o_quiz(
#         openai_api_key,
#         quiz,
#         language
# ):
#     llm = ChatOpenAI(model_name = "gpt-4o", streaming=True, callbacks=[StreamingStdOutCallbackHandler()],
#                     temperature = 0,
#                     openai_api_key= openai_api_key)
#     prompt = load_prompt(os.path.join('/app/src/quiz/utils/prompt', 'quiz_translator.yaml'))
#     input_data = {"quiz": quiz,"language":language}
#     chain = (
#         prompt
#         | llm
#         | StrOutputParser()
#     )

#     results=chain.invoke(input_data)
#     return results

async def translate_gpt4o_quiz(
        openai_api_key,
        quiz,
        language
):
    llm = ChatOpenAI(model_name = "gpt-4o", streaming=True, callbacks=[StreamingStdOutCallbackHandler()],
                    temperature = 0,
                    openai_api_key= openai_api_key)
    prompt = load_prompt(os.path.join('/app/src/quiz/utils/prompt', 'quiz_translator.yaml'))
    input_data = {"quiz": quiz,"language":language}
    chain = (
        prompt
        | llm
        | StrOutputParser()
    )

    async def generate():
        async for chunk in chain.astream(input_data):
            yield f"data: {chunk}\n\n"
    return generate

    

