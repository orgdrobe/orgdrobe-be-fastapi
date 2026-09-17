from fastapi import APIRouter

router = APIRouter()

from pydantic import BaseModel
class TempData(BaseModel):
    pass

@router.get("/master/", response_model=TempData)
async def master_categories_all(db: TempData, current_user: TempData):
    return None

@router.get("/master/{id}", response_model=TempData)
async def master_category_by_id(id: int, db: TempData, current_user: TempData):
    return None

@router.get("/sub/", response_model=list[TempData])
async def sub_categories_all(db: TempData, current_user: TempData):
    return None

@router.get("/sub/{id}", response_model=TempData)
async def sub_category_by_id(id: int, db: TempData, current_user: TempData):
    return None
