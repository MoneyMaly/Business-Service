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

class AccountAnomaly(BaseModel):
    account_number: str
    owner: str
    anomalies_count: Optional[int] = 0
class TotalAnomaly(BaseModel):
    username: str
    accounts_anomaly: list
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

class BusinessDeals(BaseModel):
    business_phone: str
    rejected_count: Optional[int] = 0
    opened_count: Optional[int] = 0
    accepted_count: Optional[int] = 0
    rejected_list: Optional[list] = []
    opened_list: Optional[list] = []
    accepted_list: Optional[list] = []
    offers: Optional[list]= []