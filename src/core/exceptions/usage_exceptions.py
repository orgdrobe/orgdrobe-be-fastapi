from core.enums import ErrorCode
from core.exceptions.base_exception import BaseAPIException


class UsageNotFound(BaseAPIException):
    status_code = 404
    code = ErrorCode.USAGE_NOT_FOUND
    def __init__(self, id: int):
        super().__init__(
            message=f"Usage with id {id} not found"
        )

