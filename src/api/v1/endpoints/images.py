from fastapi import APIRouter

router = APIRouter()

from pydantic import BaseModel
class TempData(BaseModel):
    pass

@router.post("/")
async def upload_image():
     return None

@router.get("/{filename}")
async def get_image_file():
     return None

@router.get("/{filename}/info")
async def get_image_info():
    return None

@router.delete("/{filename}")
async def delete_image():
    return None
