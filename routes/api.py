from fastapi import APIRouter

from .auth import authRoute

apiRoute = APIRouter()

apiRoute.include_router(authRoute,prefix="/auth")
