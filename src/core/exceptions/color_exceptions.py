from core.enums import ErrorCode
from core.exceptions.base_exception import BaseAPIException


class ColorNotFound(BaseAPIException):
    status_code = 404
    code = ErrorCode.COLOR_NOT_FOUND
    def __init__(self, id: int):
        super().__init__(
            message=f"Color with id {id} not found"
        )

