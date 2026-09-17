from fastapi import APIRouter

router = APIRouter()

from pydantic import BaseModel
class TempData(BaseModel):
    pass

@router.post("/", response_model=TempData)
async def create_garment(garment_in: TempData, db: TempData, current_user: TempData):
    return None

@router.post("/classify", response_model=TempData)
async def classify_garment_from_image():
   return None

@router.get("/embeddings/check", response_model=TempData)
async def check_garment_embeddings_status(payload: TempData):
    return None

@router.post("/embeddings", response_model=TempData)
async def create_garment_embeddings():
    return None

@router.get("/count", response_model=TempData)
async def get_garments_count():
    return None

@router.post("/filter",response_model=list[TempData])
async def filter_garments():
    return None

@router.get("/", response_model=list[TempData])
async def list_garments():
    return None

@router.get("/{id}", response_model=TempData)
async def read_garment():
   return None

@router.put("/{id}", response_model=TempData)
async def update_garment():
    return None

@router.delete("/{id}")
async def delete_garment():
    return None

@router.get("/{id}/outfits", response_model=list[TempData])
async def get_garment_outfits():
    return None