from typing import Optional, List
import requests
from fastapi import APIRouter, HTTPException, status, Depends
from datetime import datetime

from app.utils.auth_helper import JWTBearer
from app.settings import BANK_API_URL

router = APIRouter(tags=['Anomaly Detector'])

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"})
parameters_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Invalid Parameters",
    headers={"WWW-Authenticate": "Bearer"})


@router.get("/users/{username}/bankaccounts/balance/",status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())])
async def get_monthly_balance_by_user(username: str, from_year: int, from_month: int, to_year: int, to_month: int):
    if JWTBearer.authenticated_username != username:
        raise credentials_exception
    try:
        from_date = datetime(from_year, from_month, 1)
        to_date = datetime(to_year, to_month, 1)
        if from_date < to_date:
            try:
                res = requests.get(f"{BANK_API_URL}/users/{username}/bankaccounts/balance/?month=1&year=2021", 
                headers={'Authorization':f'Bearer {JWTBearer.jwtoken}'})
            except Exception as e:
                raise 
        else:
            return parameters_exception
    except Exception as e:
        raise parameters_exception
    return ["tal communications", "Hot TV"]