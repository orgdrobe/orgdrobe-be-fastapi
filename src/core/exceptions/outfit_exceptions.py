from core.enums import ErrorCode
from core.exceptions.base_exception import BaseAPIException


class OutfitNotFound(BaseAPIException):
    status_code = 404
    code = ErrorCode.OUTFIT_NOT_FOUND
    def __init__(self, id: int):
        super().__init__(
            message=f"Outfit with id {id} not found"
        )


class OutfitNameAlreadyExists(BaseAPIException):
    status_code = 409
    code = ErrorCode.OUTFIT_NAME_TAKEN

    def __init__(self, name: str):
        super().__init__(
            message=f"Outfit with name '{name}' already exists",
            details={"field": "name", "value": name}
        )


