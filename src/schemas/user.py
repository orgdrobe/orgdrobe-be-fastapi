from pydantic import ConfigDict

from schemas.base_model import CamelCaseBaseModel


class UserAvatarOut(CamelCaseBaseModel):
    url: str

    model_config = ConfigDict(from_attributes=True)

