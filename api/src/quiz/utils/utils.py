import os
from langchain.chat_models import ChatOpenAI
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import load_prompt
from src.quiz.utils.fewshot import sample_fewshot
import json
import random
# random content, type 세트 만들기

async def make_set(quiz_content,quiz_type,number):
    set_type = [(q_content,q_type) for q_content in quiz_content for q_type in quiz_type]
    q_set = []
    if len(set_type)>= number:
        # 각 quiz_type을 최대한 골고루 선택하기 위한 알고리즘
        quiz_type_cycle = iter(random.sample(quiz_type, len(quiz_type)))  # quiz_type을 섞어서 순환
        while len(q_set) < number:
            q_content = random.choice(quiz_content)  # 랜덤하게 quiz_content 선택
            q_type = next(quiz_type_cycle, None)  # quiz_type을 순차적으로 선택
            
            if q_type is None:  # quiz_type을 모두 순환했으면 다시 섞어서 순환
                quiz_type_cycle = iter(random.sample(quiz_type, len(quiz_type)))
                q_type = next(quiz_type_cycle)
            
            # 중복되지 않게 조합을 추가
            if (q_content, q_type) not in q_set:
                q_set.append((q_content, q_type))
    else:
        for _ in range(number//len(set_type)):
            q_set += set_type
        q_set += random.sample(set_type,k=number%len(set_type))
    random.shuffle(q_set)
    return q_set

# async def quiz_format(text):
#     start = text.find('[')  # '['로 시작하는 부분을 찾음
#     end = text.rfind(']')   # ']'로 끝나는 부분을 찾음
#     if start != -1 and end != -1:
#         json_data = text[start:end+1]  # JSON 부분만 추출
#         try:
#             parsed_data = json.loads(json_data)
        
#         except json.JSONDecodeError as e:
#             print("Failed to parse JSON:", e)
#             return None
#     else:
#         print("No valid JSON found in the result.")
#         return None

#     quiz = "🚀 **Quiz**\n\n"
#     answer = "🚀 **Answer**\n\n"
#     explain = "🚀 **Explain**\n\n"
#     sentence = "🚀 **Sentence**\n\n"
#     dialog = "🚀 **Dialog**\n\n"

#     for idx, data in enumerate(parsed_data,start=1):
#         quiz += f"🔆 Quiz {idx}. " + data["quiz"] + "\n\n"
#         if data["type"] !="fill_in_the_blank":
#             for choice in data["choice"]:
#                 quiz += choice + "\n\n"
#         answer += f"🔆 Quiz {idx}. " + data["answer"]  + "\n\n"
#         explain += f"🔆 Quiz {idx}. " + data["explain"] + "\n\n"
#         sentence += f"🔆 Quiz {idx}. " + "\n\n"
#         for i, sen in enumerate(data["sentence"],start=1):
#             sentence += f"Example {i}. "  + sen + "\n\n"
#         dialog += f"🔆 Quiz {idx}. " +"\n\n"
#         for i, dia in enumerate(data["dialog"],start=1):
#             dialog += dia + "\n\n"
#     # output = quiz + answer + explain + sentence + dialog
#     # print(output)
#     # return output
#     output_quiz = quiz 
#     output_answer = answer + explain + sentence + dialog
#     output = [output_quiz, output_answer]
#     return output

async def quiz_format(text):
    start = text.find('[')  # '['로 시작하는 부분을 찾음
    end = text.rfind(']')   # ']'로 끝나는 부분을 찾음
    if start != -1 and end != -1:
        json_data = text[start:end+1]  # JSON 부분만 추출
        try:
            parsed_data = json.loads(json_data)
        
        except json.JSONDecodeError as e:
            print("Failed to parse JSON:", e)
            return None
    else:
        print("No valid JSON found in the result.")
        return None

    quiz = "🚀 **Quiz**\n\n"
    answer_list = []

    for idx, data in enumerate(parsed_data,start=1):
        quiz += f"🔆 Quiz {idx}. " + data["quiz"] + "\n\n"
        if data["type"] !="fill_in_the_blank":
            for choice in data["choice"]:
                quiz += choice + "\n\n"

        text = f"🚀 **Quiz {idx}**\n\n"
        text += "🔆 **Answer:** " + data["answer"] + "\n\n"
        text += "🔆 **Explain:** " + data["explain"] + "\n\n"
        text += "🔆 **Sentence:** " + "\n\n"
        for i, sen in enumerate(data["sentence"],start=1):
            text += f"Example {i}. "  + sen + "\n\n"
        text += "🔆 **Dialog:** " + "\n\n"
        for i, dia in enumerate(data["dialog"],start=1):
            text += dia + "\n\n"
        answer_list.append(text)
    output_quiz = quiz
    output_answer = answer_list
    output = [output_quiz, output_answer]

    return output
    
# async def make_set(quiz_content,quiz_type,number):
#     set_type = [(q_content,q_type) for q_content in quiz_content for q_type in quiz_type]
#     q_set = []
#     if len(set_type)>= number:
#         q_set = random.sample(set_type,k=number)
#     else:
#         for _ in range(number//len(set_type)):
#             q_set += set_type
#         q_set += random.sample(set_type,k=number%len(set_type))
#     random.shuffle(q_set)
#     return q_set

# batch 퀴즈 생성

async def batch_generate_gpt4o_quiz(
        openai_api_key,
        document,
        quiz_content,
        quiz_type,
        number
):

    llm = ChatOpenAI(model_name = "gpt-4o",streaming=True, callbacks=[StreamingStdOutCallbackHandler()],
                    temperature = 0.56,
                    openai_api_key= openai_api_key)
    #prompt = load_prompt(os.path.join('/app/src/quiz/utils/prompt', 'quiz_generator_pythonic.yaml'))
    prompt = load_prompt(os.path.join('/app/src/quiz/utils/prompt', 'quiz_generator_json.yaml'))
    topic = document.split('\n')[0]
    reference = '\n'.join(document.split('\n')[1:])
    q_set= await make_set(quiz_content,quiz_type,number)
    print(q_set)
    #input_data = {"topic": topic,"reference": reference,"quiz_content":quiz_content,"quiz_type":quiz_type,"number":number,"set":q_set}
    input_data = {"topic": topic,"reference": reference,"number":number,"set":q_set}

    chain = (
        prompt
        | llm
        | StrOutputParser()
    )

    #results = chain.invoke(input_data).replace("A:", "\n    A:").replace("B:","\n    B:").replace("①","\n    ①").replace("②","    ②").replace("③","    ③").replace("④","    ④")
    response = chain.invoke(input_data)
    results = await quiz_format(response)
    return results

# async def batch_generate_gpt4o_quiz(
#         openai_api_key,
#         document,
#         quiz_content,
#         quiz_type,
#         number
# ):

#     llm = ChatOpenAI(model_name = "gpt-4o", streaming=True, callbacks=[StreamingStdOutCallbackHandler()],
#                     temperature = 0,
#                     openai_api_key= openai_api_key)
#     #prompt = load_prompt(os.path.join('/app/src/quiz/utils/prompt', 'quiz_generator_pythonic.yaml'))
#     prompt = load_prompt(os.path.join('/app/src/quiz/utils/prompt', 'quiz_generator_pythonic_for_develop.yaml'))
#     topic = document.split('\n')[0]
#     reference = '\n'.join(document.split('\n')[1:])
#     q_set= await make_set(quiz_content,quiz_type,number)
#     input_data = {"topic": topic,"reference": reference,"quiz_content":quiz_content,"quiz_type":quiz_type,"number":number,"set":q_set}

#     chain = (
#         prompt
#         | llm
#         | StrOutputParser()
#     )

#     #results = chain.invoke(input_data).replace("A:", "\n    A:").replace("B:","\n    B:").replace("①","\n    ①").replace("②","    ②").replace("③","    ③").replace("④","    ④")
#     results = chain.invoke(input_data)
#     return results

# stream 퀴즈 생성
# async def stream_generate_gpt4o_quiz(
#         openai_api_key,
#         document,
#         quiz_content,
#         quiz_type,
#         number
# ):

#     llm = ChatOpenAI(model_name = "gpt-4o", streaming=True, callbacks=[StreamingStdOutCallbackHandler()],
#                     temperature = 0,
#                     openai_api_key= openai_api_key)
#     #prompt = load_prompt(os.path.join('/app/src/quiz/utils/prompt', 'quiz_generator_pythonic.yaml'))
#     prompt = load_prompt(os.path.join('/app/src/quiz/utils/prompt', 'quiz_generator_pythonic_for_develop.yaml'))
#     topic = document.split('\n')[0]
#     reference = '\n'.join(document.split('\n')[1:])
#     q_set= await make_set(quiz_content,quiz_type,number)
#     input_data = {"topic": topic,"reference": reference,"quiz_content":quiz_content,"quiz_type":quiz_type,"number":number,"set":q_set}

#     chain = (
#         prompt
#         | llm
#         | StrOutputParser()
#     )

#     async def generate():
#         buffer = ""
#         async for chunk in chain.astream(input_data):
#             buffer += chunk
#             lines = buffer.split('\n')
            
#             # Process all complete lines
#             for line in lines[:-1]:
#                 #line = line.replace("🔆", "\n  🔆").replace("A:", "\n    A:").replace("B:","\n    B:").replace("①","\n    ①").replace("②","    ②").replace("③","    ③").replace("④","    ④")
#                 yield f"data: {json.dumps({'text': line})}\n\n"
            
#             # Keep the last (possibly incomplete) line in the buffer
#             buffer = lines[-1]

#         # Yield any remaining content in the buffer
#         if buffer:
#             #buffer = buffer.replace("🔆", "\n  🔆").replace("A:", "\n    A:").replace("B:","\n    B:").replace("①","\n    ①").replace("②","    ②").replace("③","    ③").replace("④","    ④")
#             yield f"data: {json.dumps({'text': buffer})}\n\n"
#     return generate

# batch 번역
async def batch_translate_gpt4o_quiz(
        openai_api_key,
        quiz,
        answer,
        language
):
    llm = ChatOpenAI(model_name = "gpt-4o", streaming=True, callbacks=[StreamingStdOutCallbackHandler()],
                    temperature = 0,
                    openai_api_key= openai_api_key)
    prompt = load_prompt(os.path.join('/app/src/quiz/utils/prompt', 'quiz_translator.yaml'))
    input_data = {"quiz": quiz,"answer":answer,"language":language}
    chain = (
        prompt
        | llm
        | StrOutputParser()
    )

    results=chain.invoke(input_data)
    return results

# stream 번역
async def stream_translate_gpt4o_quiz(
        openai_api_key,
        quiz,
        answer,
        language
):
    llm = ChatOpenAI(model_name = "gpt-4o", streaming=True, callbacks=[StreamingStdOutCallbackHandler()],
                    temperature = 0,
                    openai_api_key= openai_api_key)
    prompt = load_prompt(os.path.join('/app/src/quiz/utils/prompt', 'quiz_translator.yaml'))
    input_data = {"quiz": quiz,"answer":answer,"language":language}
    chain = (
        prompt
        | llm
        | StrOutputParser()
    )

    async def generate():
        buffer=""
        async for chunk in chain.astream(input_data):
            buffer +=chunk
            lines = buffer.split("\n")

            for line in lines[:-1]:
                yield f"data: {json.dumps({'text': line})}\n\n"
            buffer = lines[-1]

        # Yield any remaining content in the buffer
        if buffer:
            yield f"data: {json.dumps({'text': buffer})}\n\n"

    return generate
    #########################################################################################################
    # fewshot prompt
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
