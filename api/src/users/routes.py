from typing import Any, List
from typing_extensions import Annotated
from fastapi import APIRouter, Depends, HTTPException, Body
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
#from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from functools import lru_cache
from src import config
@lru_cache
def get_settings():
    return config.Settings()

from src.users import schemas
from src.users import models
from src.users.models import user as crud_user #object
from src.users import dependencies as deps
from src.auth.utils import send_new_account_email
import openai

router = APIRouter()

'''
@router.get("/", tags=["users"])
async def users():
    return {"hello users"}
'''

@router.get("/", response_model=List[schemas.User])
async def get_users(
    db: AsyncSession = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Get users.
    """
    users = await crud_user.get_multi(db, skip=skip, limit=limit)
    return users


@router.post("/", response_model=schemas.User)
async def create_user(
    *,
    db: AsyncSession = Depends(deps.get_db),
    user_in: schemas.UserCreate,
    settings: Annotated[config.Settings, Depends(get_settings)],
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new user.
    """
    user = await crud_user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail= "사용할 수 없는 이메일 아이디입니다. 다른 이메일을 입력해 주세요.", #"The user with this username already exists in the system.",
        )
    user = await crud_user.create(db, obj_in=user_in)
    if settings.EMAILS_ENABLED and user_in.email:
        send_new_account_email(
            email_to=user_in.email, username=user_in.email, password=user_in.password
        )
    return user


@router.put("/me", response_model=schemas.User)
async def update_user_me(
    *,
    db: AsyncSession = Depends(deps.get_db),
    password: str = Body(None),
    username: str = Body(None),
    email: EmailStr = Body(None),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Update current user info.
    """
    current_user_data = jsonable_encoder(current_user)
    user_in = schemas.UserUpdate(**current_user_data)
    if password is not None:
        user_in.password = password
    if username is not None:
        user_in.username = username
    if email is not None:
        user_in.email = email
    user = await crud_user.update(db, db_obj=current_user, obj_in=user_in)
    return user


@router.get("/me", response_model=schemas.User)
async def get_user_me(
    db: AsyncSession = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get current user.
    """
    return current_user


@router.post("/signup", response_model=schemas.User)
async def create_user_open_signup(
    *,
    db: AsyncSession = Depends(deps.get_db),
    settings: Annotated[config.Settings, Depends(get_settings)],
    email: EmailStr = Body(...),
    password: str = Body(...),
    username: str = Body(None),
) -> Any:
    """
    Create new user without the need to be logged in.
    """
    if not settings.USERS_OPEN_REGISTRATION:
        raise HTTPException(
            status_code=400, #403
            detail= "권한이 없습니다. 관리자에게 문의하세요.", #"new user is forbidden to sign up" #"Open user registration is forbidden on this server" 
        )
    
    user = await crud_user.get_by_email(db, email=email)
    if user:
        raise HTTPException(
            status_code=400,
            detail= "사용할 수 없는 이메일 아이디입니다. 다른 이메일을 입력해 주세요.", #"The user with this email address already exists"
        )
    
    user_in = schemas.UserCreate(password=password, email=email, username=username)
    user = await crud_user.create(db, obj_in=user_in)
    return user


@router.get("/{user_id}", response_model=schemas.User)
async def get_user_by_id(
    user_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
    db: AsyncSession = Depends(deps.get_db),
) -> Any:
    """
    Get a user by id.
    """
    user = await crud_user.get(db, id=user_id)
    if user == current_user:
        return user
    if not crud_user.is_superuser(current_user):
        raise HTTPException(
            status_code=400,
            detail="권한이 없습니다. 관리자에게 문의하세요.", #"The user doesn't have enough privileges"
        )
    return user


@router.put("/{user_id}", response_model=schemas.User)
async def update_user_by_id(
    *,
    db: AsyncSession = Depends(deps.get_db),
    user_id: int,
    user_in: schemas.UserUpdate,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update a user by id.
    """
    user = await crud_user.get(db, id=user_id)
    user = await crud_user.update(db, db_obj=user, obj_in=user_in)
    return user

#
@router.delete("/{user_id}", response_model=schemas.User)
async def delete_user_by_id(
    user_id: int,
    current_user: models.User = Depends(deps.get_current_active_superuser),
    db: AsyncSession = Depends(deps.get_db),
) -> Any:
    """
    Delete a user by id.
    """
    user = await crud_user.get(db, id=user_id)
    user = await crud_user.remove(db, id=user_id)
    return user

#OPENAI API KEY 확인
@router.post("/api_key_check", response_model=schemas.Api_Key_Check)
async def api_key_check(
    *,
    openai_api_key: str = Body(..., embed=True),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Check API KEY
    """
    try:
        # OpenAI API 키를 설정
        openai.api_key = openai_api_key
        # 간단한 요청을 보내서 키가 유효한지 확인 (예: 모델 리스트 가져오기)
        openai.models.list()
        # 요청이 성공하면 True 반환
        return {
            "results": "OPENAI_API_KEY is valid"
        }
    except openai.AuthenticationError:
        # API 키가 유효하지 않은 경우
        return {
            "results": "OPENAI_API_KEY is invalid"
        }
    except Exception as e:
        # 기타 오류 처리
        return {
            "results": f"API error occurred: {str(e)}"
        }