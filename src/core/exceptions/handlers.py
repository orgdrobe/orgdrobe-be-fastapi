from typing import cast

import structlog
from fastapi import Request
from fastapi.responses import JSONResponse
from asgi_correlation_id import correlation_id

from schemas.errors import ErrorResponse, ErrorContent
from core.exceptions.base_exception import BaseAPIException

logger = structlog.get_logger()

async def base_api_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    exc = cast(BaseAPIException, exc) # need only for mypy

    trace_id = correlation_id.get()

    logger.error(
        "business_exception_occurred",
        error_code=exc.code,
        error_message=exc.message,
        details=exc.details,
        path=request.url.path,
        trace_id=trace_id,
        method=request.method,
        status_code=exc.status_code
    )

    content = ErrorResponse(
        error=ErrorContent(
            code=exc.code,
            message=exc.message,
            details=exc.details,
            trace_id=trace_id
        )
    ).model_dump()

    return JSONResponse(
        status_code=exc.status_code,
        content=content,
        headers=exc.headers
    )

async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    trace_id = correlation_id.get()
    
    logger.error(
        "global_exception_occurred",
        error_code="INTERNAL_SERVER_ERROR",
        error_message="An error has occurred on the server. Please contact support.",
        details=str(exc),
        path=request.url.path,
        trace_id=trace_id,
        method=request.method
        # TODO: add user id, and role
    )

    content = ErrorResponse(
        error=ErrorContent(
            code="INTERNAL_SERVER_ERROR",
            message="An error has occurred on the server. Please contact support.",
            trace_id=trace_id
        )
    ).model_dump()

    return JSONResponse(status_code=500, content=content)