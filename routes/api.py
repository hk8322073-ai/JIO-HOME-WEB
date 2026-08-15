from fastapi import APIRouter,Depends

from .auth import authRoute
from .dashboard import dashboardRoute
from utils.utility import verify_auth

apiRoute = APIRouter()

apiRoute.include_router(authRoute,prefix="/auth")
apiRoute.include_router(dashboardRoute,prefix="/dashboard",dependencies=[Depends(verify_auth)])
