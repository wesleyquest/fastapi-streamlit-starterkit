import logging
from sqlalchemy.ext.asyncio import AsyncSession
from functools import lru_cache

from src.users.models import user as crud_user
from src.users.schemas import UserCreate
from src import config

# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28
# example : from app.db import base  # noqa: F401
from src.db import base # noqa: F401

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@lru_cache
def get_settings():
    return config.Settings()

async def init_db(db: AsyncSession) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # Base.metadata.create_all(bind=engine)
    settings = get_settings()
    user = await crud_user.get_by_email(db, email=settings.FIRST_SUPERUSER)

    if not user:
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        user = await crud_user.create(db, obj_in=user_in)  # noqa: F841

    else:
        logger.warning(
            "Skipping creating speruser. User with email "
            f"{settings.FIRST_SUPERUSER} already exists. "
        )

