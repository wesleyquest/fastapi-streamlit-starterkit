from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from functools import lru_cache

from src import config

@lru_cache
def get_settings():
    return config.Settings()

settings = get_settings()

'''
engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI), pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
'''
#async
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
engine = create_async_engine(str(settings.SQLALCHEMY_DATABASE_URI), echo=True)
AsyncSessionLocal = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
)





