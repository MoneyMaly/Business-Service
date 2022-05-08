from os import truncate
from typing import Optional, List
import requests
from fastapi import APIRouter, HTTPException, status, Depends
from datetime import datetime
from dateutil.relativedelta import *
import json

from app.utils.auth_helper import JWTBearer
from app.adapters.bank_adapter import get_deals_anonymously, get_deal_by_id
from app.adapters.db_adapter import create_offer, get_offers, update_offer, get_offers_for_business
from app.models import DealPayment, MonthlyPayment, UserDeal, BusinessDeals

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

@router.get("/offers/business_phone/{phone}",status_code=status.HTTP_200_OK, response_model=BusinessDeals, response_model_exclude=['_id'], dependencies=[Depends(JWTBearer())])
async def get_business_offer(phone: str):
    if JWTBearer.role != "business":
        raise credentials_exception
    business_deals = BusinessDeals(business_phone=phone)
    business_deals.offers =  await get_offers_for_business(phone)
    for offer in business_deals.offers:
        if offer['status'] == 'Rejected':
            business_deals.rejected_list.append(offer.copy())
        if offer['status'] == 'Open':
            business_deals.opened_list.append(offer.copy())
        if offer['status'] == 'Accepted':
            business_deals.accepted_list.append(offer.copy())
    business_deals.accepted_count = len(business_deals.accepted_list)
    business_deals.opened_count = len(business_deals.opened_list)
    business_deals.rejected_count = len(business_deals.rejected_list)
    return business_deals

@router.post("/deals/deal_id/{id}/prices/{price}",status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())])
async def create_deal_for_offer(id: str, price : int, business_phone: str ):
    if JWTBearer.role != "business":
        raise credentials_exception
    deal = await get_deal_by_id(id)
    deal = UserDeal(**deal)
    deal.new_price = price
    deal.business_phone = business_phone
    offer = await create_offer(deal)
    return True

@router.get("/users/{username}/offers/offer_status/{offer_status}", response_model=List[UserDeal], response_model_exclude=['_id'] ,status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())])
async def get_users_offers(username: str, offer_status: str):
    if JWTBearer.authenticated_username != username:
        raise credentials_exception
    offers = await get_offers(username, offer_status)
    return offers

@router.put("/users/{username}/bankaccounts/{account_number}/offers/companies/{company}/offer_status/{offer_status}",status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())])
async def update_users_offers_status(username: str, account_number: str, offer_status: str, company: str, new_price: int, business_phone: str):
    if JWTBearer.authenticated_username != username:
        raise credentials_exception
    offers = await update_offer(username, account_number, offer_status, company, new_price, business_phone)
    return offers