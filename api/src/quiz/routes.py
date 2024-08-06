from fastapi import APIRouter, HTTPException


router = APIRouter()

@router.get("/", tags=["quiz"])
async def quiz():
    try:
        return {"hello quiz"}
    except:
        raise HTTPException(status_code=500,
                            detail="요청을 처리할 수 없습니다. 다시 시도해 주세요.")

