from core.enums import ErrorCode
from core.exceptions.base_exception import BaseAPIException


class ImageFileTooLarge(BaseAPIException):
    status_code = 413
    code = ErrorCode.IMAGE_FILE_TOO_LARGE

    def __init__(self, max_size_bytes: int, actual_size_bytes: int):
        max_size_mb = max_size_bytes / (1024 * 1024)
        actual_size_mb = actual_size_bytes / (1024 * 1024)
        super().__init__(
            message=f"Image file size exceeds limit of {max_size_mb:.1f} MB (got {actual_size_mb:.2f} MB)",
            details={
                "max_size_bytes": max_size_bytes,
                "actual_size_bytes": actual_size_bytes,
            },
        )


class InvalidImageFormat(BaseAPIException):
    status_code = 415
    code = ErrorCode.IMAGE_INVALID_TYPE

    def __init__(self, detected_mime: str | None, allowed_mimes: list[str] | tuple[str, ...]):
        allowed_list = list(allowed_mimes)
        super().__init__(
            message=f"Unsupported image format: '{detected_mime or 'unknown'}'. Allowed formats: {', '.join(allowed_list)}",
            details={
                "detected_mime": detected_mime,
                "allowed_mimes": allowed_list,
            },
        )


class CorruptedImage(BaseAPIException):
    status_code = 400
    code = ErrorCode.IMAGE_CORRUPTED

    def __init__(self, reason: str = "Image file is malformed or corrupted"):
        super().__init__(
            message=reason,
            details={"reason": reason},
        )


class ImageDecompressionBomb(BaseAPIException):
    status_code = 400
    code = ErrorCode.IMAGE_DECOMPRESSION_BOMB

    def __init__(self, max_pixels: int):
        super().__init__(
            message=f"Image resolution exceeds allowed maximum of {max_pixels:,} pixels (possible decompression bomb)",
            details={"max_pixels": max_pixels},
        )
