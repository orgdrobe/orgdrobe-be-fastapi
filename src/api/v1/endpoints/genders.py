from fastapi import APIRouter

router = APIRouter()

from pydantic import BaseModel
class TempData(BaseModel):
    pass

@router.get("/", response_model=list[TempData])
async def genders_all():
    return None

@router.get("/{id}", response_model=TempData)
async def gender_by_id():
    return None