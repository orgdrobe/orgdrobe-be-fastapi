from pydantic import ConfigDict, Field

from schemas.base_model import CamelCaseBaseModel
from schemas.garment import GarmentOut


class OutfitColor(CamelCaseBaseModel):
    red: int = Field(ge=0, le=255)
    green: int = Field(ge=0, le=255)
    blue: int = Field(ge=0, le=255)
    is_primary: bool


class OutfitColorOut(OutfitColor):
    id: int

    model_config = ConfigDict(from_attributes=True)


class NewOutfit(CamelCaseBaseModel):
    name: str
    description: str | None = None
    garment_ids: list[int]
    colors: list[OutfitColor]


class UpdateOutfit(CamelCaseBaseModel):
    name: str | None = None
    description: str | None = None
    garment_ids: list[int] | None = None
    colors: list[OutfitColor] | None = None


class OutfitOut(CamelCaseBaseModel):
    id: int
    name: str
    description: str | None = None
    user_id: int

    garments: list[GarmentOut]
    colors: list[OutfitColorOut]

    model_config = ConfigDict(from_attributes=True)

