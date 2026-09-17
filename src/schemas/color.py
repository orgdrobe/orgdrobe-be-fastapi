from pydantic import ConfigDict, Field

from schemas.base_model import CamelCaseBaseModel


class NewColor(CamelCaseBaseModel):
    red: int = Field(ge=0, le=255)
    green: int = Field(ge=0, le=255)
    blue: int = Field(ge=0, le=255)


class UpdateColor(CamelCaseBaseModel):
    red: int | None = Field(default=None, ge=0, le=255)
    green: int | None = Field(default=None, ge=0, le=255)
    blue: int | None = Field(default=None, ge=0, le=255)


class ColorOut(CamelCaseBaseModel):
    id: int
    red: int
    green: int
    blue: int

    model_config = ConfigDict(from_attributes=True)

