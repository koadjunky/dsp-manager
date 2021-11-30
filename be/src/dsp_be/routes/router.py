from fastapi import APIRouter

from dsp_be.routes import common, dsp

api_router = APIRouter()
api_router.include_router(common.router, tags=["root"])
api_router.include_router(dsp.router, tags=["dsp"], prefix="/dsp")
