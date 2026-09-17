from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from asgi_correlation_id import CorrelationIdMiddleware


from core.configs import application_config, configure_logging
from core.exceptions.base_exception import BaseAPIException
from core.exceptions.handlers import base_api_exception_handler, global_exception_handler
from api.v1 import router as v1_router

configure_logging()

app = FastAPI()

app.add_exception_handler(BaseAPIException, base_api_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*", # TODO: move to env
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(CorrelationIdMiddleware)



app.include_router(v1_router, prefix="/api/v1")


if __name__ == "__main__":
    # only for development
    import webbrowser
    import uvicorn

    port = application_config.PORT

    if application_config.ENV == "DEV":
        webbrowser.open_new(f"http://localhost:{port}/docs")
        
    uvicorn.run("main:app", port=port, reload=True)