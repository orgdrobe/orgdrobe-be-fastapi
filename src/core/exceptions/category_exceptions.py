from core.enums import ErrorCode
from core.exceptions.base_exception import BaseAPIException


class MasterCategoryNotFound(BaseAPIException):
    status_code = 404
    code = ErrorCode.MASTER_CATEGORY_NOT_FOUND
    def __init__(self, id: int):
        super().__init__(
            message=f"Master category with id {id} not found"
        )

class SubCategoryNotFound(BaseAPIException):
    status_code = 404
    code = ErrorCode.SUB_CATEGORY_NOT_FOUND
    def __init__(self, id: int):
        super().__init__(
            message=f"Sub category with id {id} not found"
        )