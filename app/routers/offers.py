from os import truncate
from typing import Optional, List
import requests
from fastapi import APIRouter, HTTPException, status, Depends
from datetime import datetime
from dateutil.relativedelta import *
import json

from app.utils.auth_helper import JWTBearer
from app.adapters.bank_adapter import get_deals_anonymously
from app.models import DealPayment, MonthlyPayment

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