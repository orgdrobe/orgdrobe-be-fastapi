from pydantic import ConfigDict

from schemas.base_model import CamelCaseBaseModel


class NewGarmentType(CamelCaseBaseModel):
    name: str
    description: str | None = None


class UpdateGarmentType(CamelCaseBaseModel):
    name: str | None = None
    description: str | None = None


class GarmentTypeOut(CamelCaseBaseModel):
    id: int
    name: str
    description: str | None = None

    model_config = ConfigDict(from_attributes=True)

