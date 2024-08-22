from fastapi import APIRouter, Body, Depends, HTTPException
from typing import Any

from src.users import models as users_models
from src.quiz import schemas
from src.quiz import dependencies as deps
from src.quiz.utils.utils import generate_gpt4o_quiz, translate_gpt4o_quiz

router = APIRouter()

@router.post("/generation", response_model=schemas.Quiz)
async def generate_quiz(
    *,
    openai_api_key: str = Body(...),
    document: str = Body(...),
    quiz_content: list = Body(...),
    quiz_type: list = Body(...),
    number: int = Body(...),
    current_user: users_models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Generate quiz
    """

    data = await generate_gpt4o_quiz(
        openai_api_key = openai_api_key,
        document = document,
        quiz_content = quiz_content,
        quiz_type = quiz_type,
        number = number,
    )

    return {
        "results": data
    }

@router.post("/translation", response_model=schemas.Quiz)
async def translate_quiz(
    *,
    openai_api_key: str = Body(...),
    quiz: str = Body(...),
    language: str = Body(...),
    current_user: users_models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Translate quiz
    """

    data = await translate_gpt4o_quiz(
        openai_api_key = openai_api_key,
        quiz = quiz,
        language = language,
    )

    return {
        "results": data
    }


