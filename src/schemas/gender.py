from pydantic import ConfigDict

from schemas.base_model import CamelCaseBaseModel


class NewGender(CamelCaseBaseModel):
    name: str
    description: str | None = None


class UpdateGender(CamelCaseBaseModel):
    name: str | None = None
    description: str | None = None


class GenderOut(CamelCaseBaseModel):
    id: int
    name: str
    description: str | None = None

    model_config = ConfigDict(from_attributes=True)

