import uvicorn
from fastapi import Depends, FastAPI, Request
from loguru import logger

from dsp_be.event_handlers import start_app_handler, stop_app_handler
from dsp_be.routes.router import api_router
from dsp_be.settings import (
    APP_SETTINGS,
    API_PREFIX,
    DEFAULT_HOST,
    DEFAULT_HOST_PORT,
)


async def logging_dependency(request: Request):
    logger.debug(f"{request.method} {request.url}")
    logger.debug("Params:")
    for name, value in request.path_params.items():
        logger.debug(f"\t{name}: {value}")
    logger.debug("Headers:")
    for name, value in request.headers.items():
        logger.debug(f"\t{name}: {value}")
    form = await request.form()
    logger.debug("Body:")
    logger.debug(f"\t{form}")


def get_app() -> FastAPI:
    app = FastAPI(**APP_SETTINGS)
    app.include_router(
        api_router, prefix=API_PREFIX, dependencies=[Depends(logging_dependency)]
    )

    app.add_event_handler("startup", start_app_handler(app))
    app.add_event_handler("shutdown", stop_app_handler(app))

    return app


app = get_app()

if __name__ == "__main__":
    uvicorn.run(
        "dsp_be.main:app",
        host=DEFAULT_HOST,
        port=DEFAULT_HOST_PORT,
        reload=True,
        reload_dirs=["src"],
    )
