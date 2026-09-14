from typing import Sequence
from core.enums import ErrorCode
from core.exceptions.base_exception import BaseAPIException


class GarmentNotFound(BaseAPIException):
    status_code = 404
    code = ErrorCode.GARMENT_NOT_FOUND

    def __init__(self, id: int | Sequence[int]):
        if isinstance(id, (list, tuple, set)):
            id_list = list(id)
            if len(id_list) == 1:
                message = f"Garment with id {id_list[0]} not found"
            else:
                message = f"Garments with ids {id_list} not found"
            details = {"field": "garment_ids", "missing_ids": id_list}
        else:
            message = f"Garment with id {id} not found"
            details = {"field": "garment_id", "missing_ids": [id]}

        super().__init__(
            message=message,
            details=details
        )


class GarmentNameAlreadyExists(BaseAPIException):
    status_code = 409
    code = ErrorCode.GARMENT_NAME_TAKEN

    def __init__(self, name: str):
        super().__init__(
            message=f"Garment with name '{name}' already exists",
            details={"field": "name", "value": name}
        )


