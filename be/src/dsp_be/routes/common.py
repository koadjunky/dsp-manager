from importlib import resources

from fastapi import APIRouter
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from starlette.responses import RedirectResponse, StreamingResponse

from dsp_be.settings import APP_SETTINGS

router = APIRouter()


@router.get("/", include_in_schema=False)
async def read_root():
    return RedirectResponse("/docs")


@router.get("/favicon.ico", include_in_schema=False)
async def favicon():
    def iterfile():
        with resources.open_binary("branding_service.api.routes", "favicon.ico") as f:
            yield from f

    return StreamingResponse(iterfile(), media_type="image/x-icon")


@router.get("/ping", summary="Healthcheck", status_code=200)
def read_healthcheck():
    return {200: "OK"}


@router.get("/docs", include_in_schema=False)
def overridden_swagger():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title=APP_SETTINGS["title"],
        swagger_favicon_url="/favicon.ico",
    )


@router.get("/redoc", include_in_schema=False)
def overridden_redoc():
    return get_redoc_html(
        openapi_url="/openapi.json",
        title=APP_SETTINGS["title"],
        redoc_favicon_url="/favicon.ico",
    )
