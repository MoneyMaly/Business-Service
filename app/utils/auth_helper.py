from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from passlib.context import CryptContext
import time

from app.settings import APP_SECRET_KEY, ALGORITHM

#region verify token
class JWTBearer(HTTPBearer):
    authenticated_username = None
    jwtoken = None
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)


    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid: bool = False

        try:
            decoded_token =  jwt.decode(jwtoken, APP_SECRET_KEY, algorithms=[ALGORITHM])
            if not decoded_token["exp"] >= time.time():
                raise
            JWTBearer.authenticated_username =  decoded_token["username"]
            JWTBearer.jwtoken = jwtoken
        except:
            decoded_token = None
        if decoded_token:
            isTokenValid = True
        return isTokenValid

#endregion 