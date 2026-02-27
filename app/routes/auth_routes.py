from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

auth_router = APIRouter()
from app.controllers.auth_controllers import google_auth

security = HTTPBearer()


@auth_router.get("/google")
def google(credentials: HTTPAuthorizationCredentials = Depends(security)):
    return google_auth(credentials)