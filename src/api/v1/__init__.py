from fastapi import APIRouter

from .endpoints import auth, users, categories, colors, garment_types, garments, genders, images, outfit_templates, outfits, seasons, usage

router = APIRouter()
router.include_router(auth.router, prefix="/auth", tags=["Auth"])
router.include_router(users.router, prefix="/users", tags=["Users"])
router.include_router(categories.router, prefix="/categories", tags=["Categories"])
router.include_router(colors.router, prefix="/colors", tags=["Colors"])
router.include_router(garment_types.router, prefix="/garment-types", tags=["Garment-types"])
router.include_router(garments.router, prefix="/garments", tags=["Garments"])
router.include_router(genders.router, prefix="/genders", tags=["Genders"])
router.include_router(images.router, prefix="/images", tags=["Images"])
router.include_router(outfit_templates.router, prefix="/outfit-templates", tags=["Outfit-templates"])
router.include_router(outfits.router, prefix="/outfits", tags=["Outfits"])
router.include_router(seasons.router, prefix="/seasons", tags=["Seasons"])
router.include_router(usage.router, prefix="/uses", tags=["Uses"])

