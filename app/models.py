from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

class MonthlyPayment(BaseModel):
    month: int
    year: int
    date: datetime
    price: int

class DealPayment(BaseModel):
    company: str
    # can be Communication, TV, insurance
    sector: str
    payments: list

class CompanyMonthlyPrice(BaseModel):
    company: str
    price: int
    year: int
    month: int

class Deal(BaseModel):
    company: str
    # can be Communication, TV, insurance
    sector: str
    extra_info: dict

class UserDeal(Deal):
    username: str
    account_number: str
    new_price: Optional[int] = 0
    status: Optional[str] = "Open"
    business_phone: Optional[str] = 100