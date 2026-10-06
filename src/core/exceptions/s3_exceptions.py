from core.enums import ErrorCode
from core.exceptions.base_exception import BaseAPIException


class S3StorageError(BaseAPIException):
    status_code = 500
    code = ErrorCode.S3_STORAGE_ERROR

    def __init__(self, message: str = "An S3 storage error occurred"):
        super().__init__(
            message=message,
            details={"error": message},
        )


class S3ObjectNotFound(BaseAPIException):
    status_code = 404
    code = ErrorCode.S3_OBJECT_NOT_FOUND

    def __init__(self, bucket: str, key: str):
        super().__init__(
            message=f"Object '{key}' not found in bucket '{bucket}'",
            details={"bucket": bucket, "key": key},
        )
