from core.enums import ErrorCode
from core.exceptions.base_exception import BaseAPIException


class SeasonNotFound(BaseAPIException):
    status_code = 404
    code = ErrorCode.SEASON_NOT_FOUND
    def __init__(self, id: int):
        super().__init__(
            message=f"Season with id {id} not found"
        )

