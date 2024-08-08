from fastapi import APIRouter, Body, Depends, HTTPException
from typing import Any

from src.users import models as users_models
from src.quiz import schemas
from src.quiz import dependencies as deps

router = APIRouter()

@router.post("/generation", response_model=schemas.Quiz)
async def generate_quiz(
    *,
    document: str = Body(...),
    quiz_content: list = Body(...),
    quiz_type: list = Body(...),
    number: int = Body(...),
    current_user: users_models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Generate quiz
    """


