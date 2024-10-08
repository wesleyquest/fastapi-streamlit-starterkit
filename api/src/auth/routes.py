from typing import Any
from typing_extensions import Annotated
from datetime import timedelta
from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
#from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

#from src import crud, models, schemas
from src.users import models as users_models
from src.users.models import user as crud_user #object
from src.users import schemas as users_schemas
from src.auth import schemas as auth_schemas
#from src.api import deps
from src.auth import dependencies as deps
#from app.core import security
from src.auth import utils
from functools import lru_cache
from src import config

@lru_cache
def get_settings():
    return config.Settings()
settings = get_settings()


router = APIRouter()

@router.post("/login/access-token", response_model=auth_schemas.Token)
async def login_access_token(
    db: AsyncSession = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = await crud_user.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400,
                            detail="이메일 또는 비밀번호가 일치하지 않습니다.") #detail="Incorrect email or password"
    elif not crud_user.is_active(user):
        raise HTTPException(status_code=400,
                            detail="비활성 사용자 입니다. 관리자에게 문의하세요.") #detail="Inactive user"
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": utils.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


@router.post("/login/test-token", response_model=users_schemas.User)
def test_token(current_user: users_models.User = Depends(deps.get_current_user)) -> Any:
    """
    Test access token
    """
    return current_user


@router.post("/password-recovery/{email}", response_model=auth_schemas.Msg)
async def recover_password(email: str, db: AsyncSession = Depends(deps.get_db)) -> Any:
    """
    Password Recovery
    """
    user = await crud_user.get_by_email(db, email=email)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="가입하신 이메일 정보가 없습니다." #detail="The user with this email does not exist in the system.",
        )
    password_reset_token = utils.generate_password_reset_token(email=email)
    utils.send_reset_password_email(
        email_to=user.email, email=email, token=password_reset_token
    )
    return {"detail": "패스워드 재설정 메일을 보냈습니다."} #return {"detail": "Password recovery email sent"}



@router.post("/reset-password", response_model=auth_schemas.Msg)
async def reset_password(
    token: str = Body(...),
    new_password: str = Body(...),
    db: AsyncSession = Depends(deps.get_db),
) -> Any:
    """
    Reset password
    """
    email = utils.verify_password_reset_token(token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid token")
    user = await crud_user.get_by_email(db, email=email)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="가입하신 이메일 정보가 없습니다." #detail="The user with this username does not exist in the system.",
        )
    elif not crud_user.is_active(user):
        raise HTTPException(status_code=400, detail="Inactive user")
    hashed_password = utils.get_password_hash(new_password)
    user.hashed_password = hashed_password
    db.add(user)
    await db.commit()
    return {"detail": "패스워드를 변경하였습니다."} #return {"msg": "Password updated successfully"}

