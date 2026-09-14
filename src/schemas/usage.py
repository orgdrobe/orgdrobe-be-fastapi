from pydantic import ConfigDict

from schemas.base_model import CamelCaseBaseModel


class NewUsage(CamelCaseBaseModel):
    name: str
    description: str | None = None


class UpdateUsage(CamelCaseBaseModel):
    name: str | None = None
    description: str | None = None


class UsageOut(CamelCaseBaseModel):
    id: int
    name: str
    description: str | None = None

    model_config = ConfigDict(from_attributes=True)

