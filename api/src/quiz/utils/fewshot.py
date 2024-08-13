import random
def sample_fewshot(tag1_list, tag2_list,number):
    fewshot = [
        {
            "tag": ['vocabulary_focused', 'multiple_choice'],
            "example": "Choose the meaning of 염색?\n\
            ① Painting  ② Dyeing  ③ Cooking  ④ Drinking\n",
            "answer": "② Dyeing\n",
            "explain": "염색 is a Korean word that specifically means 'Dyeing.' It refers to the process of changing the color of something, usually fabric or hair, which is why the correct answer is ② Dyeing.\n"
        },
        {
            "tag": ['sentence_example', 'multiple_choice'],
            "example": "Choose the meaning of '나 좋아하는 사람이 생겼어'?\n\
            ① I have someone I like  ② I like people  ③ I want to be someone you like  ④ I am a popular person\n",
            "answer": "① I have someone I like\n",
            "explain": "The phrase '나 좋아하는 사람이 생겼어' translates to 'I have someone I like.' This sentence expresses the idea that the speaker has developed feelings for someone, making the correct answer ①.\n"
        },
        {
            "tag": ['cultural_information', 'multiple_choice'],
            "example": "Choose the meaning of '머리 잘라 주세요'?\n\
            ① please cut my head  ② please cut my hair  ③ Can you trim my brain  ④ I need my scalp shortened\n",
            "answer": "② please cut my hair\n",
            "explain": "In Korean, '머리 잘라 주세요' literally means 'please cut my hair.' While '머리' can mean 'head,' in this context, it refers to 'hair,' hence the correct answer is ②.\n"
        },
        {
            "tag": ['word_order', 'multiple_choice'],
            "example": "What is the correct Korean sentence order for 'I can fly'?\n\
            A. 나는 B. 날 수 있다 C. 하늘을\n\
            ① A-B-C  ② A-C-B  ③ B-A-C  ④ C-B-A",
            "answer": "② A-C-B\n",
            "explain": "The correct sentence order in Korean is '나는 하늘을 날 수 있다,' which translates to 'I can fly in the sky.' Therefore, the correct answer is ② A-C-B.\n"
        },
        {
            "tag": ['vocabulary_focused', 'true_or_false'],
            "example": "'염색' means 'Dyeing' O or X\n",
            "answer": "O\n",
            "explain": "'염색' is indeed the Korean word for 'Dyeing,' which is why the correct answer is O.\n"
        },
        {
            "tag": ['sentence_example', 'true_or_false'],
            "example": "'나~ 좋아하는 사람이 생겼어~' means the positive phrase 'I have someone I like.' O or X\n",
            "answer": "O\n",
            "explain": "The phrase '나~ 좋아하는 사람이 생겼어~' is a casual way to say 'I have someone I like,' which is a positive statement. Therefore, the correct answer is O.\n"
        },
        {
            "tag": ['cultural_information', 'true_or_false'],
            "example": "Cyworld users could buy music with a virtual currency called 'Dotori' and use it as background music on their mini-homepage. O or X\n",
            "answer": "O\n",
            "explain": "Cyworld, a popular social networking site in Korea, allowed users to buy music with 'Dotori,' a virtual currency, to personalize their mini-homepages. Hence, the answer is O.\n"
        },
        {
            "tag": ['word_order', 'true_or_false'],
            "example": "The correct order of words in the Korean sentence 'I love you' is '나는 사랑해 너를.' O or X\n",
            "answer": "X\n",
            "explain": "The correct word order for 'I love you' in Korean is '나는 너를 사랑해,' not '나는 사랑해 너를.' Hence, the correct answer is X.\n"
        },
        {
            "tag": ['vocabulary_focused', 'fill_in_the_blank'],
            "example": "What is the Korean word to fill in the blanks?\n\
            학생들이 ____ 떠들어요\n\
            ① 왁자지껄  ② 삐뚤삐뚤  ③ 데굴데굴  ④ 흥얼흥얼\n",
            "answer": "① 왁자지껄\n",
            "explain": "The word '왁자지껄' means 'noisily' or 'boisterously,' which fits the context of students making noise. Thus, the correct answer is ①.\n"
        },
        {
            "tag": ['sentence_example', 'fill_in_the_blank'],
            "example": "What is the Korean word to fill in the blanks?\n\
            티셔츠 사이즈가 맞지 않아 ____.\n\
            (Because the size didn't fit, I returned the T-shirt.)\n\
            ① 환불해요  ② 환불했어요  ③ 환불 할거에요  ④ 환불 할래요\n",
            "answer": "② 환불했어요\n",
            "explain": "The correct verb form is '환불했어요,' which means 'I returned it.' It correctly matches the past tense of the sentence, so the answer is ②.\n"
        },
        {
            "tag": ['cultural_information', 'fill_in_the_blank'],
            "example": "What is the Korean word to fill in the blanks?\n\
            Cyworld users could buy music with a virtual currency called ______ and use it as background music on their mini-homepage.\n",
            "answer": "Dotori\n",
            "explain": "The virtual currency used in Cyworld is called 'Dotori,' which users could use for various personalization options, including background music.\n"
        },
        {
            "tag": ['word_order', 'fill_in_the_blank'],
            "example": "Fill in the blanks with the correct combination of words in the Korean sentence 'I can fly.'\n\
            나는 ___ 을 ___ 수 있다\n\
            ① 날, 하늘  ② 하늘, 날  ③ 바다, 잘  ④ 노래, 날\n",
            "answer": "② 하늘, 날\n",
            "explain": "In the sentence '나는 하늘을 날 수 있다,' the words '하늘' (sky) and '날' (fly) are correctly placed to mean 'I can fly in the sky,' so the correct answer is ②.\n"
        }
    ]
    # 랜덤 샘플링
    fewshot_prompt = []
    for few in fewshot:
        if (few['tag'][0] in tag1_list) and (few['tag'][1] in tag2_list):
            fewshot_prompt.append([few['example'],few['answer'],few['explain']])
    num_fewshot = min(len(fewshot_prompt),int(number))
    final_fewshot_list = random.sample(fewshot_prompt,num_fewshot)
    # 샘플링에 맞게 포맷 변경
    quiz_fewshot='🚀 Quiz\n'
    answer_fewshot='🚀 Answer\n'
    explain_fewshot='🚀 Explain\n'

    for idx, content in enumerate(final_fewshot_list):
        quiz_fewshot = quiz_fewshot + f'🔆 Quiz{idx+1}. ' + content[0]
        answer_fewshot = answer_fewshot + f'🔆 Quiz{idx+1}. ' + content[1]
        explain_fewshot = explain_fewshot + f'🔆 Quiz{idx+1}. ' + content[2]
    final_fewshot = quiz_fewshot + "\n"+answer_fewshot + "\n"+explain_fewshot
    return final_fewshot, 1
import pprint
if __name__=='__main__':
    pprint.pprint(sample_fewshot(['vocabulary_focused','sentence_example','cultural_information','word_order'],['multiple_choice','true_or_false','fill_in_the_blank'],5))
    
