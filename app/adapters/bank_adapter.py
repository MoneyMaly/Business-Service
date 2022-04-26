from typing import Optional, List
import requests
from fastapi import APIRouter, HTTPException, status, Depends
from datetime import datetime
from dateutil.relativedelta import *
import json

from app.utils.auth_helper import JWTBearer
from app.settings import BANK_API_URL

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


async def get_deals_list(username: str, account_number: str):
    try:
        deals_response = requests.get(f"{BANK_API_URL}/users/{username}/bankaccounts/{account_number}/deals", 
        headers={'Authorization':f'Bearer {JWTBearer.jwtoken}'})
        return json.loads(deals_response.text)
    except Exception as e:
        raise Internal_exception

async def get_deal_monthly_price(username: str, account_number: str, company:str, current_year:int, current_month: int):
    try:
        deal_price_response = requests.get(f"{BANK_API_URL}/users/{username}/bankaccounts/{account_number}/company/{company}/?month={current_month}&year={current_year}", 
        headers={'Authorization':f'Bearer {JWTBearer.jwtoken}'})
        return json.loads(deal_price_response.text)
    except Exception as e:
        raise Internal_exception 