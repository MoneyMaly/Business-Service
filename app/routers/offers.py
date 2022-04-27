from os import truncate
from typing import Optional, List
import requests
from fastapi import APIRouter, HTTPException, status, Depends
from datetime import datetime
from dateutil.relativedelta import *
import json

from app.utils.auth_helper import JWTBearer
from app.adapters.bank_adapter import get_deals_anonymously, get_deal_by_id
from app.adapters.db_adapter import create_offer, get_offers
from app.models import DealPayment, MonthlyPayment, UserDeal

router = APIRouter(tags=['Business Offers'])

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

@router.get("/deals/sectors/{sector}",status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())])
async def get_deals_for_offer(sector: str):
    if JWTBearer.role != "business":
        raise credentials_exception
    deals = await get_deals_anonymously(sector)
    return {"deals": deals }

@router.post("/deals/deal_id/{id}/prices/{price}",status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())])
async def get_deals_for_offer(id: str, price : int, business_phone: str ):
    if JWTBearer.role != "business":
        raise credentials_exception
    deal = await get_deal_by_id(id)
    deal = UserDeal(**deal)
    deal.new_price = price
    deal.business_phone = business_phone
    offer = await create_offer(deal)
    return True

@router.get("/users/{username}/bankaccounts/{account_number}/offers/offer_status/{offer_status}", response_model=List[UserDeal], response_model_exclude=['_id'] ,status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())])
async def get_users_offers(username: str, account_number: str, offer_status: str):
    if JWTBearer.authenticated_username != username:
        raise credentials_exception
    offers = await get_offers(username, account_number, offer_status)
    return offers 