from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timedelta, UTC
from jose import jwt
import os
from google.oauth2 import id_token
from google.auth.transport import requests
from app.db.database import db

security = HTTPBearer()


def google_auth(credentials: HTTPAuthorizationCredentials = Depends(security)):
    id_token = credentials.credentials
    user_info = decode_id_token(id_token)
    if user_info is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = {
        "email": user_info["email"],
        "name": user_info["name"],
        "picture": user_info["picture"],
    }
    user_id = ""
    # check is user already exists
    user_exists = db["users"].find_one({"email": user_info["email"]})
    if user_exists is None:
        user["created_at"] = datetime.now(UTC)
        inserted = db["users"].insert_one(user)
        user_id = inserted.inserted_id
    else:
        user["last_login"] = datetime.now(UTC)
        db["users"].update_one({"email": user_info["email"]}, {"$set": user})
        user_id = user_exists["_id"]

    token = generate_token(str(user_id))
    return {
        "success": True,
        "message": "Authentication Successful",
        "data": {
            "refresh_token": token,
            "user": {
                "id": str(user_id),
                "email": user_info["email"],
                "name": user_info["name"],
                "picture": user_info["picture"],
            },
        },
    }


# ===========helper functions===================


def decode_id_token(token):
    try:
        google_web_client_id = os.getenv("GOOGLE_WEB_CLIENT_ID")
        if google_web_client_id is None:
            google_web_client_id = "secret"

        user_info = id_token.verify_oauth2_token(
            token, requests.Request(), google_web_client_id
        )
        return user_info
    except:
        return None


def generate_token(user_id: str):
    to_encode = {"user_id": user_id, "exp": datetime.utcnow() + timedelta(days=30)}
    s_key = os.getenv("JWT_SECRET_KEY")
    if s_key is None:
        s_key = "secret"
    return jwt.encode(to_encode, s_key, algorithm="HS256")
