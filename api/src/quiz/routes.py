from fastapi import APIRouter, Body, Depends, HTTPException
from typing import Any
from fastapi.responses import StreamingResponse

from src.users import models as users_models
from src.quiz import schemas
from src.quiz import dependencies as deps
from src.quiz.utils.utils import batch_generate_gpt4o_quiz, stream_generate_gpt4o_quiz, batch_translate_gpt4o_quiz, stream_translate_gpt4o_quiz

router = APIRouter()

#batch 퀴즈 생성 API
@router.post("/batch_generation", response_model=schemas.Quiz)
async def batch_generate_quiz(
    *,
    openai_api_key: str = Body(...),
    document: str = Body(...),
    quiz_content: list = Body(...),
    quiz_type: list = Body(...),
    number: int = Body(...),
    current_user: users_models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Generate batch quiz
    """

    data = await batch_generate_gpt4o_quiz(
        openai_api_key = openai_api_key,
        document = document,
        quiz_content = quiz_content,
        quiz_type = quiz_type,
        number = number,
    )

    return {
        "results": data
    }

#stream 퀴즈 생성 API
@router.post("/stream_generation", response_model=schemas.Quiz)
async def stream_generate_quiz(
    *,
    openai_api_key: str = Body(...),
    document: str = Body(...),
    quiz_content: list = Body(...),
    quiz_type: list = Body(...),
    number: int = Body(...),
    current_user: users_models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Generate streaming quiz
    """

    data = await stream_generate_gpt4o_quiz(
        openai_api_key = openai_api_key,
        document = document,
        quiz_content = quiz_content,
        quiz_type = quiz_type,
        number = number,
    )

    return StreamingResponse(data(), media_type="text/event-stream")

#batch 번역 API
@router.post("/batch_translation", response_model=schemas.Quiz)
async def batch_translate_quiz(
    *,
    openai_api_key: str = Body(...),
    quiz: str = Body(...),
    language: str = Body(...),
    current_user: users_models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Translate batch quiz
    """

    data = await batch_translate_gpt4o_quiz(
        openai_api_key = openai_api_key,
        quiz = quiz,
        language = language,
    )

    return {
        "results": data
    }

#stream 번역 API
@router.post("/stream_translation", response_model=schemas.Quiz)
async def stream_translate_quiz(
    *,
    openai_api_key: str = Body(...),
    quiz: str = Body(...),
    language: str = Body(...),
    current_user: users_models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Translate streaming quiz
    """

    data = await stream_translate_gpt4o_quiz(
        openai_api_key = openai_api_key,
        quiz = quiz,
        language = language,
    )

    return StreamingResponse(data(), media_type="text/event-stream")