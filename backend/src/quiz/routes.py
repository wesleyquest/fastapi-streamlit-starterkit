from fastapi import APIRouter


router = APIRouter()

@router.get("/", tags=["quiz"])
async def quiz():
    return {"hello quiz"}
