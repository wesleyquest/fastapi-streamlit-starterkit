


async def generate_gpt4o_quiz(
        openai_api_key,
        document,
        quiz_content,
        quiz_type,
        number
):
    results = """
    아래와 같이 퀴즈를 생성했어요.
                        
    Quiz 1. What does the following Korean phrase mean? \n
    머리 잘라 주세요. \n
    ① Cut my head  ② Cut my hair
    \n
    Quiz 2. What was the first act that happened? \n
    머리를 염색하기 전에 커트를 해요. \n
    ① dye my hair ② get a haircut
    \n
    Answer \n
    Quiz 1. ② Cut my hair \n
    Quiz 2. ② get a haircut
    """
    return results








