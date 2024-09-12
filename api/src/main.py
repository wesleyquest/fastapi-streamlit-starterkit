from fastapi import FastAPI
from functools import lru_cache
from fastapi import Depends, APIRouter
from typing_extensions import Annotated
from fastapi.middleware.cors import CORSMiddleware

from src import config
from src.quiz.routes import router as quiz_router
from src.users.routes import router as users_router
from src.auth.routes import router as auth_router
from src.rag.routes import router as rag_router

@lru_cache
def get_settings():
    return config.Settings()

settings = get_settings()

app = FastAPI(title='starterkit API') #, root_path="/api/"

#root router
router = APIRouter()

@router.get("/")
async def default(settings: Annotated[config.Settings, Depends(get_settings)]):
    return f"Hello! This is {settings.API_NAME}"

#startup
@app.on_event("startup")
def on_startup():

    print("Hello FastAPI")


#middleware
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"], #{"OPTIONS", "GET", "POST", "DELETE", "PUT"}
        allow_headers=["*"],
    )

#routes
app.include_router(router)
app.include_router(auth_router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(users_router, prefix=f"{settings.API_V1_STR}/users", tags=["users"])
app.include_router(quiz_router, prefix=f"{settings.API_V1_STR}/quiz", tags=["quiz"])
app.include_router(rag_router, prefix=f"{settings.API_V1_STR}/rag", tags=["rag"])


'''
import uvicorn

if __name__ == "__main__":
    uvicorn.run("app.api:app", host="0.0.0.0", port=8081, reload=True)
'''
 


