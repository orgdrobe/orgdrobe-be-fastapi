from pydantic import ConfigDict

from schemas.base_model import CamelCaseBaseModel

class NewMasterCategory(CamelCaseBaseModel):
    name: str
    description: str | None = None

class UpdateMasterCategory(CamelCaseBaseModel):
    name: str | None = None
    description: str | None = None

class MasterCategoryOut(CamelCaseBaseModel):
    id: int
    name: str
    description: str | None = None

    model_config = ConfigDict(from_attributes=True)
