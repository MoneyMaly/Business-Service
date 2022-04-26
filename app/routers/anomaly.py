from typing import Optional, List
import requests
from fastapi import APIRouter, HTTPException, status, Depends

from app.utils.auth_helper import JWTBearer

router = APIRouter(tags=['Anomaly Detector'])

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"})


@router.get("/users/{username}/bankaccounts/balance/",status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())])
async def get_monthly_balance_by_user(username: str):
    if JWTBearer.authenticated_username != username:
        raise credentials_exception
    try:
        res = requests.get(f"http://192.116.98.107:8082/users/{username}/bankaccounts/balance/?month=1&year=2021", 
        headers={'Authorization':f'Bearer {JWTBearer.jwtoken}'})
    # bank_accounts_list = await get_bank_accounts_list_by_username(username)
    # monthly_balance = await get_monthly_balance(bank_accounts_list, year, month)
    except:
        raise Exception
    return ["tal communications", "Hot TV"]