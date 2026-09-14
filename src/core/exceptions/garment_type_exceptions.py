from core.enums import ErrorCode
from core.exceptions.base_exception import BaseAPIException


class GarmentTypeNotFound(BaseAPIException):
    status_code = 404
    code = ErrorCode.GARMENT_TYPE_NOT_FOUND
    def __init__(self, id: int):
        super().__init__(
            message=f"Garment type with id {id} not found"
        )

