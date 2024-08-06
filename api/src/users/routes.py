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
    try:
        users = await crud_user.get_multi(db, skip=skip, limit=limit)
        return users
    except:
        raise HTTPException(status_code=500,
                            detail="요청을 처리할 수 없습니다. 다시 시도해 주세요.")


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
    try:
        user = await crud_user.get_by_email(db, email=user_in.email)
        if user:
            raise HTTPException(
                status_code=400,
                detail="The user with this username already exists in the system.",
            )
        user = await crud_user.create(db, obj_in=user_in)
        if settings.EMAILS_ENABLED and user_in.email:
            send_new_account_email(
                email_to=user_in.email, username=user_in.email, password=user_in.password
            )
        return user
    except:
        raise HTTPException(status_code=500,
                            detail="요청을 처리할 수 없습니다. 다시 시도해 주세요.")


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
    try:
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
    except:
        raise HTTPException(status_code=500,
                            detail="요청을 처리할 수 없습니다. 다시 시도해 주세요.")


@router.get("/me", response_model=schemas.User)
async def get_user_me(
    db: AsyncSession = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get current user.
    """
    try:
        return current_user
    except:
        raise HTTPException(status_code=500,
                            detail="요청을 처리할 수 없습니다. 다시 시도해 주세요.")


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
    try:
        if not settings.USERS_OPEN_REGISTRATION:
            raise HTTPException(
                status_code=403,
                detail="new user is forbidden to sign up" #"Open user registration is forbidden on this server" 
            )
        
        user = await crud_user.get_by_email(db, email=email)
        if user:
            raise HTTPException(
                status_code=400,
                detail="The user with this email address already exists"
            )
        
        user_in = schemas.UserCreate(password=password, email=email, username=username)
        user = await crud_user.create(db, obj_in=user_in)
        return user
    except:
        raise HTTPException(status_code=500,
                            detail="요청을 처리할 수 없습니다. 다시 시도해 주세요.")


@router.get("/{user_id}", response_model=schemas.User)
async def get_user_by_id(
    user_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
    db: AsyncSession = Depends(deps.get_db),
) -> Any:
    """
    Get a user by id.
    """
    try:
        user = await crud_user.get(db, id=user_id)
        if user == current_user:
            return user
        if not crud_user.is_superuser(current_user):
            raise HTTPException(
                status_code=400, detail="The user doesn't have enough privileges"
            )
        return user
    except:
        raise HTTPException(status_code=500,
                            detail="요청을 처리할 수 없습니다. 다시 시도해 주세요.")


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
    try:
        user = await crud_user.get(db, id=user_id)
        if not user:
            raise HTTPException(
                status_code=404,
                detail="The user with this username does not exist in the system",
            )
        user = await crud_user.update(db, db_obj=user, obj_in=user_in)
        return user
    except:
        raise HTTPException(status_code=500,
                            detail="요청을 처리할 수 없습니다. 다시 시도해 주세요.")

