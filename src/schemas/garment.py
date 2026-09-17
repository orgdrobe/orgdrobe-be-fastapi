from pydantic import ConfigDict, Field

from schemas.base_model import CamelCaseBaseModel
from schemas.gender import GenderOut
from schemas.master_category import MasterCategoryOut
from schemas.sub_category import SubCategoryOut
from schemas.garment_type import GarmentTypeOut
from schemas.season import SeasonOut
from schemas.usage import UsageOut

class GarmentColorBase(CamelCaseBaseModel):
    red: int = Field(ge=0, le=255)
    green: int = Field(ge=0, le=255)
    blue: int = Field(ge=0, le=255)
    is_primary: bool


class NewGarment(CamelCaseBaseModel):
    name: str
    description: str | None = None
    gender_id: int
    category_master_id: int
    category_sub_id: int
    garment_type_id: int
    season_id: int
    usage_id: int

    colors: list[GarmentColorBase]


class UpdateGarment(CamelCaseBaseModel):
    name: str | None = None
    description: str | None = None
    gender_id: int | None = None
    category_master_id: int | None = None
    category_sub_id: int | None = None
    garment_type_id: int | None = None
    season_id: int | None = None
    usage_id: int | None = None
    colors: list[GarmentColorBase] | None = None


class GarmentColorOut(GarmentColorBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)


class GarmentOut(CamelCaseBaseModel):
    id: int
    name: str
    description: str | None = None
    user_id: int
    
    gender: GenderOut
    category_master: MasterCategoryOut
    category_sub: SubCategoryOut
    garment_type: GarmentTypeOut
    season: SeasonOut
    usage: UsageOut
    
    colors: list[GarmentColorOut]

    model_config = ConfigDict(from_attributes=True)
