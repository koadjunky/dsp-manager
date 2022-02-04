from fastapi import APIRouter

from dsp_be.routes import common, factories, planets, stars

api_router = APIRouter()
api_router.include_router(common.router, tags=["root"])
api_router.include_router(stars.router, tags=["dsp"], prefix="/dsp/api/stars")
api_router.include_router(planets.router, tags=["dsp"], prefix="/dsp/api/planets")
api_router.include_router(factories.router, tags=["dsp"], prefix="/dsp/api/factories")
