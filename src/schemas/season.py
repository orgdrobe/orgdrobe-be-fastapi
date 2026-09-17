from pydantic import ConfigDict

from schemas.base_model import CamelCaseBaseModel


class NewSeason(CamelCaseBaseModel):
    name: str
    description: str | None = None


class UpdateSeason(CamelCaseBaseModel):
    name: str | None = None
    description: str | None = None


class SeasonOut(CamelCaseBaseModel):
    id: int
    name: str
    description: str | None = None

    model_config = ConfigDict(from_attributes=True)

