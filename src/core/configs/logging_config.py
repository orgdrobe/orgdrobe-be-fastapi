import structlog
import logging
import sys
from asgi_correlation_id import correlation_id

def configure_logging():
    def add_correlation(logger, method_name, event_dict):
        request_id = correlation_id.get()
        if request_id:
            event_dict["trace_id"] = request_id
        return event_dict

    def order_keys(logger, method_name, event_dict):
        keys_order = ["event", "trace_id", "level", "timestamp", "error_code", "error_message"]
        new_dict = {}
        for key in keys_order:
            if key in event_dict:
                new_dict[key] = event_dict.pop(key)
        new_dict.update(event_dict)
        return new_dict

    structlog.configure(
        processors=[
            add_correlation,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.CallsiteParameterAdder(
                {
                    structlog.processors.CallsiteParameter.FILENAME,
                    structlog.processors.CallsiteParameter.FUNC_NAME,
                    structlog.processors.CallsiteParameter.LINENO,
                }
            ),
            order_keys,
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
    )

    handler = logging.StreamHandler(sys.stdout)
    formatter = structlog.stdlib.ProcessorFormatter(
        processor=structlog.processors.JSONRenderer(),
    )
    handler.setFormatter(formatter)
    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.addHandler(handler)
    root_logger.setLevel(logging.INFO)

    # uncomment when PRODUCTION
    # uvicorn_loggers = [
    #     "uvicorn",
    #     "uvicorn.error",
    #     "uvicorn.access",
    # ]

    # for logger_name in uvicorn_loggers:
    #     logger = logging.getLogger(logger_name)
    #     logger.handlers.clear()
    #     logger.propagate = True