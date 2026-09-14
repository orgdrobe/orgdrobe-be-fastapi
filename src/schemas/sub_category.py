from pydantic import ConfigDict

from schemas.base_model import CamelCaseBaseModel

class NewSubCategory(CamelCaseBaseModel):
    name: str
    description: str | None = None

class UpdateSubCategory(CamelCaseBaseModel):
    name: str | None = None
    description: str | None = None

class SubCategoryOut(CamelCaseBaseModel):
    id: int
    name: str
    description: str | None = None

    model_config = ConfigDict(from_attributes=True)
