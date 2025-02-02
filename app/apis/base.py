from fastapi import APIRouter

from app.apis.v1 import route_login
from app.apis.v1 import route_user

api_router = APIRouter()

api_router.include_router(route_login.router, prefix="/auth", tags=["Login"])
api_router.include_router(route_user.router, prefix="/users", tags=["Users"])
