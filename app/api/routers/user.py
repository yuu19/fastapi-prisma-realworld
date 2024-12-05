from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["users"])
@router.get("/user/")
