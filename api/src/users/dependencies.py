from typing import Generator
from fastapi import Depends, HTTPException, status
#from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt
from pydantic import ValidationError

from src.db.session import AsyncSessionLocal
from src.users import models
from src.auth.utils import reusable_oauth2
from src.auth.utils import ALGORITHM
from src.auth.schemas import TokenPayload
from src.users.models import user as crud_user #object
from functools import lru_cache
from src import config
@lru_cache
def get_settings():
    return config.Settings()
settings = get_settings()



async def get_db():
    try:
        #db = SessionLocal()
        db = AsyncSessionLocal() #async
        yield db
    finally:
        await db.close()

async def get_current_user(
    db: AsyncSession = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> models.User:
    try:
        payload = jwt.decode(
            token, settings.ACCESS_TOKEN_SECRET, algorithms=[ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=400, #status.HTTP_403_FORBIDDEN
            detail="자격 증명을 확인할 수 없습니다.", #detail="Could not validate credentials",
        )
    user = await crud_user.get(db, id=token_data.sub)
    if not user:
        raise HTTPException(status_code=400, #404
                            detail="사용자를 찾을 수 없습니다.") #detail="User not found"
    return user


def get_current_active_user(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    if not crud_user.is_active(current_user):
        raise HTTPException(status_code=400,
                            detail="비활성 사용자 입니다. 관리자에게 문의하세요.") #detail="Inactive user"
    return current_user


def get_current_active_superuser(
    current_user: models.User = Depends(get_current_active_user),
) -> models.User:
    if not crud_user.is_superuser(current_user):
        raise HTTPException(
            status_code=400,
            detail="권한이 없습니다. 관리자에게 문의하세요." #detail="The user doesn't have enough privileges"
        )
    return current_user