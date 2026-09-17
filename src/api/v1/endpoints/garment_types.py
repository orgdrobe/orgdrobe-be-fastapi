from fastapi import APIRouter

router = APIRouter()

from pydantic import BaseModel
class TempData(BaseModel):
    pass

@router.get("/", response_model=list[TempData])
async def garment_types_all(db: TempData, current_user: TempData):
    return None

@router.get("/{id}", response_model=TempData)
async def garment_type_by_id(id: int, db: TempData, current_user: TempData):
    return None