import random
def sample_fewshot(tag1_list, tag2_list,number):
    fewshot = [
        {
            "tag": ['vocabulary_focused', 'multiple_choice'],
            "example": "Choose the meaning of 염색?\n\
            ① Painting  ② Dyeing  ③ Cooking  ④ Drinking\n",
            "answer": "② Dyeing\n",
            "explain": "염색 is a Korean word that specifically means 'Dyeing.' It refers to the process of changing the color of something, usually fabric or hair, which is why the correct answer is ② Dyeing.\n",
            "sentence_example": ["나는 머리를 염색했어요.",
                                 "그녀는 염색한 머리가 마음에 들어요.",
                                 "염색 후 머리 색이 변했어요."
            ],
            "dialog_example": ["A: 염색한 머리가 예뻐 보여요.",
                               "B: 감사합니다! 새로 염색했어요."
                               ]
        },
        {
            "tag": ['sentence_example', 'multiple_choice'],
            "example": "Choose the meaning of '나 좋아하는 사람이 생겼어'?\n\
            ① I have someone I like  ② I like people  ③ I want to be someone you like  ④ I am a popular person\n",
            "answer": "① I have someone I like\n",
            "explain": "The phrase '나 좋아하는 사람이 생겼어' translates to 'I have someone I like.' This sentence expresses the idea that the speaker has developed feelings for someone, making the correct answer ①.\n",
             "sentence_example": ["나 정말 좋아하는 사람이 생겼어.",
                                  "좋아하는 사람이 생겨서 매일이 즐거워.",
                                  "그는 좋아하는 사람에게 고백하려고 해요."
                                  ],
            "dialog_example": ["A: 나 좋아하는 사람이 생겼어.",
                               "B: 정말? 누구야?"]
        },
        {
            "tag": ['cultural_information', 'multiple_choice'],
            "example": "Choose the meaning of '머리 잘라 주세요'?\n\
            ① please cut my head  ② please cut my hair  ③ Can you trim my brain  ④ I need my scalp shortened\n",
            "answer": "② please cut my hair\n",
            "explain": "In Korean, '머리 잘라 주세요' literally means 'please cut my hair.' While '머리' can mean 'head,' in this context, it refers to 'hair,' hence the correct answer is ②.\n",
            "sentence_example": ["저는 이번 주말에 머리를 자를 거예요.",
                                 "그는 머리를 짧게 잘랐어요.",
                                 "머리 자르는 게 필요해 보여요."],
            "dialog_example": ["A: 머리 어떻게 자를까요?",
                               "B: 짧게 잘라 주세요."]
        },
        {
            "tag": ['word_order', 'multiple_choice'],
            "example": "What is the correct Korean sentence order for 'I can fly'?\n\
            A. 나는 B. 날 수 있다 C. 하늘을\n\
            ① A-B-C  ② A-C-B  ③ B-A-C  ④ C-B-A",
            "answer": "② A-C-B\n",
            "explain": "The correct sentence order in Korean is '나는 하늘을 날 수 있다,' which translates to 'I can fly in the sky.' Therefore, the correct answer is ② A-C-B.\n",
            "sentence_example": ["나는 새처럼 하늘을 날고 싶어요.",
                                  "그녀는 꿈속에서 하늘을 날았어요.",
                                  "하늘을 나는 기분이 들어요."],
            "dialog_example": ["A: 너도 하늘을 날 수 있을 거야.",
                               "B: 그 말이 정말 힘이 돼."]
        },
        {
            "tag": ['vocabulary_focused', 'true_or_false'],
            "example": "'염색' means 'Dyeing' O or X\n",
            "answer": "O\n",
            "explain": "'염색' is indeed the Korean word for 'Dyeing,' which is why the correct answer is O.\n",
             "sentence_example": ["이번에 머리를 염색했어요.",
                                  "염색은 생각보다 시간이 오래 걸려요.",
                                  "다음 주에 머리를 다시 염색할 거예요."],
            "dialog_example": ["A: 머리 색이 예쁘네요, 염색하셨어요?",
                               "B: 네, 염색했어요."]
        },
        {
            "tag": ['sentence_example', 'true_or_false'],
            "example": "'나~ 좋아하는 사람이 생겼어~' means the positive phrase 'I have someone I like.' O or X\n",
            "answer": "O\n",
            "explain": "The phrase '나~ 좋아하는 사람이 생겼어~' is a casual way to say 'I have someone I like,' which is a positive statement. Therefore, the correct answer is O.\n",
            "sentence_example": ["좋아하는 사람이 생기면 매일이 설레요.",
                                 "그녀는 최근에 좋아하는 사람이 생겼어요.",
                                 "좋아하는 사람이 생기면 표현하기가 어려워요."],
            "dialog_example": ["A: 나 좋아하는 사람이 생겼어.",
                               "B: 정말? 축하해!"]
        },
        {
            "tag": ['cultural_information', 'true_or_false'],
            "example": "Cyworld users could buy music with a virtual currency called 'Dotori' and use it as background music on their mini-homepage. O or X\n",
            "answer": "O\n",
            "explain": "Cyworld, a popular social networking site in Korea, allowed users to buy music with 'Dotori,' a virtual currency, to personalize their mini-homepages. Hence, the answer is O.\n",
            "sentence_example": ["싸이월드에서 도토리를 모아 음악을 샀어요.",
                                 "도토리를 모으면 배경 음악을 바꿀 수 있었어요.",
                                 "싸이월드에서 도토리로 여러 아이템을 구매할 수 있었어요."],
            "dialog_example": ["A: 도토리로 뭐 살 거야?",
                               "B: 새로운 배경음악을 사고 싶어."]
        },
        {
            "tag": ['word_order', 'true_or_false'],
            "example": "The correct order of words in the Korean sentence 'I love you' is '나는 사랑해 너를.' O or X\n",
            "answer": "X\n",
            "explain": "The correct word order for 'I love you' in Korean is '나는 너를 사랑해,' not '나는 사랑해 너를.' Hence, the correct answer is X.\n",
            "sentence_example": ["나는 너를 사랑해.",
                                 "그는 그녀를 사랑해.",
                                 "너를 사랑하는 마음은 변하지 않아."],
            "dialog_example": ["A: 어떻게 말해야 해?",
                               "B: '나는 너를 사랑해'라고 말하면 돼."]
        },
        {
            "tag": ['vocabulary_focused', 'fill_in_the_blank'],
            "example": "What is the Korean word to fill in the blanks?\n\
            학생들이 ____ 떠들어요\n\
            ① 왁자지껄  ② 삐뚤삐뚤  ③ 데굴데굴  ④ 흥얼흥얼\n",
            "answer": "① 왁자지껄\n",
            "explain": "The word '왁자지껄' means 'noisily' or 'boisterously,' which fits the context of students making noise. Thus, the correct answer is ①.\n",
            "sentence_example": ["아이들이 왁자지껄하게 떠들고 있어요.",
                                 "교실이 왁자지껄한 소리로 가득 찼어요.",
                                 "그들은 왁자지껄하게 웃으며 놀았어요."],
            "dialog_example": ["A: 왜 이렇게 시끄러워?",
                               "B: 아이들이 왁자지껄하게 떠들고 있어."]
        },
        {
            "tag": ['sentence_example', 'fill_in_the_blank'],
            "example": "What is the Korean word to fill in the blanks?\n\
            티셔츠 사이즈가 맞지 않아 ____.\n\
            (Because the size didn't fit, I returned the T-shirt.)\n\
            ① 환불해요  ② 환불했어요  ③ 환불 할거에요  ④ 환불 할래요\n",
            "answer": "② 환불했어요\n",
            "explain": "The correct verb form is '환불했어요,' which means 'I returned it.' It correctly matches the past tense of the sentence, so the answer is ②.\n",
            "sentence_example": ["구매한 티셔츠를 환불했어요.",
                                 "그녀는 신발이 마음에 들지 않아 환불했어요.",
                                 "제품에 결함이 있어 환불 절차를 진행했어요."],
            "dialog_example": ["A: 티셔츠 사이즈가 맞지 않아서 환불했어요.",
                               "B: 아, 그런 일이 있었군요."]
        },
        {
            "tag": ['cultural_information', 'fill_in_the_blank'],
            "example": "What is the Korean word to fill in the blanks?\n\
            Cyworld users could buy music with a virtual currency called ______ and use it as background music on their mini-homepage.\n",
            "answer": "Dotori\n",
            "explain": "The virtual currency used in Cyworld is called 'Dotori,' which users could use for various personalization options, including background music.\n",
            "sentence_example": ["싸이월드에서 도토리로 배경음악을 구매했어요.",
                                 "도토리를 모아 여러 아이템을 샀어요.",
                                 "도토리로 새로운 음악을 추가했어요."
                                ],
            "dialog_example": ["A: 도토리로 뭐 샀어?",
                               "B: 새로운 배경음악을 샀어."]
        },
        {
            "tag": ['word_order', 'fill_in_the_blank'],
            "example": "Fill in the blanks with the correct combination of words in the Korean sentence 'I can fly.'\n\
            나는 ___ 을 ___ 수 있다\n\
            ① 날, 하늘  ② 하늘, 날  ③ 바다, 잘  ④ 노래, 날\n",
            "answer": "② 하늘, 날\n",
            "explain": "In the sentence '나는 하늘을 날 수 있다,' the words '하늘' (sky) and '날' (fly) are correctly placed to mean 'I can fly in the sky,' so the correct answer is ②.\n",
            "sentence_example": ["나는 하늘을 나는 꿈을 꿨어.",
                                 "그녀는 하늘을 날고 싶어해요.",
                                 "하늘을 날 수 있다니 정말 놀라워요."],
            "dialog_example": ["A: 너도 하늘을 날 수 있기를 바래.",
                            "B: 고마워, 그 말에 힘이 나."]
        }
    ]
    # 랜덤 샘플링
    fewshot_prompt = []
    for few in fewshot:
        if (few['tag'][0] in tag1_list) and (few['tag'][1] in tag2_list):
            fewshot_prompt.append([few['example'],few['answer'],few['explain'],', '.join(few['sentence_example'])+'\n',', '.join(few['dialog_example'])+'\n'])
    num_fewshot = min(len(fewshot_prompt),int(number))
    final_fewshot_list = random.sample(fewshot_prompt,num_fewshot)
    # 샘플링에 맞게 포맷 변경
    quiz_fewshot='🚀 Quiz\n'
    answer_fewshot='🚀 Answer\n'
    explain_fewshot='🚀 Explain\n'
    sentence_fewshot='🚀 Sentence\n'
    dialog_fewshot='🚀 Dialog\n'

    for idx, content in enumerate(final_fewshot_list):
        quiz_fewshot = quiz_fewshot + f'🔆 Quiz{idx+1}. ' + content[0]
        answer_fewshot = answer_fewshot + f'🔆 Quiz{idx+1}. ' + content[1]
        explain_fewshot = explain_fewshot + f'🔆 Quiz{idx+1}. ' + content[2]
        sentence_fewshot = sentence_fewshot + f'🔆 Quiz{idx+1}. ' + content[3]
        dialog_fewshot = dialog_fewshot + f'🔆 Quiz{idx+1}. ' + content[4]



    final_fewshot = quiz_fewshot + "\n"+answer_fewshot + "\n"+explain_fewshot + "\n"+sentence_fewshot + "\n"+dialog_fewshot
    return final_fewshot
import pprint
if __name__=='__main__':
    pprint.pprint(sample_fewshot(['vocabulary_focused','sentence_example','cultural_information','word_order'],['multiple_choice','true_or_false','fill_in_the_blank'],5))
    
