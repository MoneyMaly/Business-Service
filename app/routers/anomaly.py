from typing import Optional, List
import requests
from fastapi import APIRouter, HTTPException, status, Depends
from datetime import datetime
from dateutil.relativedelta import *
import json

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
Internal_exception = HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Internal server error",
    headers={"WWW-Authenticate": "Bearer"})


@router.get("/users/{username}/bankaccounts/{account_number}/deals/anomaly",status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())])
async def get_monthly_balance_by_user(username: str, account_number: str, from_year: int, from_month: int, to_year: int, to_month: int):
    if JWTBearer.authenticated_username != username:
        raise credentials_exception
        #Validate dates
    try:
        from_date = datetime(from_year, from_month, 1)
        to_date = datetime(to_year, to_month, 1)
        if from_date > to_date:
            return parameters_exception
    except Exception as e:
            return parameters_exception
    # Get users deals
    try:
        deals_response = requests.get(f"{BANK_API_URL}/users/{username}/bankaccounts/{account_number}/deals", 
        headers={'Authorization':f'Bearer {JWTBearer.jwtoken}'})

        deals = json.loads(deals_response.text)
        for deal in deals:
            deal_prices = []
            while from_date <= to_date:
            # get deal current price
                deal_price_response = requests.get(f"{BANK_API_URL}/users/{username}/bankaccounts/{account_number}/company/{deal['company']}/?month={from_date.month}&year={from_date.year}", 
                headers={'Authorization':f'Bearer {JWTBearer.jwtoken}'})
                deal_price = json.loads(deal_price_response.text)
                if deal_price:
                    deal_prices.append(deal_price['price'])
                from_date += relativedelta(months=+1)
    except Exception as e:
        return Internal_exception    
    return deal_prices


# res = requests.get(f"{BANK_API_URL}/users/{username}/bankaccounts/balance/?month=1&year=2022", 
# headers={'Authorization':f'Bearer {JWTBearer.jwtoken}'}