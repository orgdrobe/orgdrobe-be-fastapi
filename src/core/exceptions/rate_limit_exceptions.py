from core.enums import ErrorCode
from core.exceptions.base_exception import BaseAPIException

class RateLimitExceeded(BaseAPIException):
    status_code = 429
    code = ErrorCode.TOO_MANY_REQUESTS 
    message = "Attempt limit exceeded. Please try again later."