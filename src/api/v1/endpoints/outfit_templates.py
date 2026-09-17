from fastapi import APIRouter

router = APIRouter()

from pydantic import BaseModel
class TempData(BaseModel):
    pass

@router.get("/", response_model=list[TempData])
async def outfit_templates_all():
    return None

@router.get("/parameters", response_model=list[TempData])
async def outfit_templates_parameters():
    return None

@router.get("/{id}/parameters", response_model=list[TempData])
async def outfit_template_parameters_by_template_id(id: int):
    return None
