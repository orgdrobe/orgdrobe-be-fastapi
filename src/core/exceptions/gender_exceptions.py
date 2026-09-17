from core.enums import ErrorCode
from core.exceptions.base_exception import BaseAPIException


class GenderNotFound(BaseAPIException):
    status_code = 404
    code = ErrorCode.GENDER_NOT_FOUND
    def __init__(self, id: int):
        super().__init__(
            message=f"Gender with id {id} not found"
        )

