from os import truncate
from typing import Optional, List
import requests
from fastapi import APIRouter, HTTPException, status, Depends
from datetime import datetime
from dateutil.relativedelta import *
import json

from app.utils.auth_helper import JWTBearer
from app.adapters.bank_adapter import get_deals_list, get_deal_monthly_price
from app.models import DealPayment, MonthlyPayment

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

async def detect_anomaly(deal_payment: DealPayment):
    for i in range(0,(len(deal_payment.payments)-1)):
        if deal_payment.payments[i].price < deal_payment.payments[i+1].price:
            return True
    return False

@router.get("/users/{username}/bankaccounts/{account_number}/deals/anomaly",status_code=status.HTTP_200_OK,response_model=List[DealPayment], dependencies=[Depends(JWTBearer())])
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
    deals = await get_deals_list(username, account_number)
    anomaly_list = []
    for deal in deals:
        from_date = datetime(from_year, from_month, 1)
        deal_total_payment = DealPayment(company=deal["company"], sector=deal['sector'], payments=[])
        while from_date <= to_date:
        # get deal current price
            deal_price = await get_deal_monthly_price(username, account_number, deal["company"], from_date.year, from_date.month)
            try:
                if deal_price:
                    monthly_payment = MonthlyPayment(price=deal_price['price'], month=from_date.month, year=from_date.year, date=deal_price['date'] )
                    deal_total_payment.payments.append(monthly_payment)
            except Exception as e:
                raise Internal_exception
            from_date += relativedelta(months=+1)
        if await detect_anomaly(deal_total_payment):
            anomaly_list.append(deal_total_payment)
    return anomaly_list

@router.get("/users/{username}/bankaccounts/{account_number}/deals/companies/{company}/ratio",status_code=status.HTTP_200_OK, dependencies=[Depends(JWTBearer())])
async def get_monthly_balance_by_user(username: str, account_number: str, company: str):
    if JWTBearer.authenticated_username != username:
        raise credentials_exception
    return {"company": company, "percentile"מיקו: 10 }