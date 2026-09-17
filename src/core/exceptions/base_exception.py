from typing import Optional, Any
from core.enums.error_codes import ErrorCode

class BaseAPIException(Exception):
    status_code: int = 500
    code: ErrorCode = ErrorCode.INTERNAL_SERVER_ERROR
    message: str = "An unexpected error occurred."
    headers: Optional[dict[str, str]] = None
    # TODO: add module= auth, 

    def __init__(self, message: Optional[str] = None, details: Optional[Any] = None, headers: Optional[dict[str,str]] = None) -> None:
        if message is not None:
            self.message = message
        if headers is not None:
            self.headers = headers
            
        self.details = details
        super().__init__(self.message)
