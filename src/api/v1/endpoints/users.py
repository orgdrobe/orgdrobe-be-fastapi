from fastapi import APIRouter

router = APIRouter()

from pydantic import BaseModel
class TempData(BaseModel):
    pass

@router.get("/test")
def test_route() -> dict[str,str]:
    return {"message": "Hello world!"}

@router.post("/", response_model=TempData)
async def create_user(payload: TempData, service: TempData):
    return None

@router.get("/", response_model=list[TempData])
async def get_all_users(service: TempData, current_user: TempData):
    return None

@router.get("/users/me", response_model=TempData)
async def get_user_mylesf(service: TempData, current_user: TempData):
    return None

@router.get("/{id}", response_model=TempData)
async def get_user(user_id: int, service: TempData):
    return None

@router.put("/{id}", response_model=TempData) # full update
async def update_user(id: int, user_in: TempData, db: TempData, current_user: TempData):
   return None 

@router.delete("/{id}", response_model=TempData)
async def delete_user(id: int, db: TempData, current_user: TempData):
  return None