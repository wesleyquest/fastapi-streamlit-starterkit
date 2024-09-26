from fastapi import APIRouter, Body, Depends, HTTPException
from typing import Any
from fastapi.responses import StreamingResponse

from src.users import models as users_models
from src.rag import schemas
from src.rag import dependencies as deps

from src.rag.utils.utils import batch_generate_rag
router = APIRouter()

#batch 퀴즈 생성 API
@router.post("/batch_generation", response_model=schemas.Answer)
async def batch_generate_quiz(
    *,
    openai_api_key: str = Body(...),
    query: str = Body(...),
    current_user: users_models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Generate batch answer
    """

    data = await batch_generate_rag(
        openai_api_key = openai_api_key,
        query = query
    )

    return {
        "results": data[0],
        "reference": data[1]
    }
