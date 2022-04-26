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