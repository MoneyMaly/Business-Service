from pymongo import MongoClient
from uuid import uuid4

# from app.models import BankAccountBalance, BankAccountByUsername
from app.settings import DATABASE_SERVER, DATABASE_USER, DATABASE_PASSWORD, DATABASE_PORT, DATABASE_NAME
from app.models import UserDeal

client = None
db = None

async def create_offer(new_deal: UserDeal):
    offer = await db["BusinessOffers"].insert_one(new_deal.__dict__)
    return True

async def get_offers(username: str, account_number: str, offer_status: str):
    offers = await db["BusinessOffers"].find({"status":offer_status, "account_number": account_number, "username": username}).to_list(length=10)
    return list(offers)

# async def get_bank_accounts_list_by_username(username: str):
#     bank_accounts = await db["UsersBankAccounts"].find({"username":username}).to_list(length=5)
#     return list(bank_accounts)

# async def create_user_bank_account(bank_account: BankAccountByUsername):
#     bank_accounts = await db["UsersBankAccounts"].insert_one(bank_account.__dict__)
#     return True

# async def get_monthly_balance(bank_accounts_list, year: int, month: int):
#     accounts_monthly_balance_list = []
#     for bank_account in bank_accounts_list:
#         account_monthly_balance = await db["BankAccounts"].find_one({"owner": bank_account["owner"], \
#         "ssn": bank_account["ssn"], "account_number":bank_account["account_number"], "year": year, "month": month})
#         try:
#             for transaction in account_monthly_balance['expenses_and_revenues']:
#                 accounts_monthly_balance_list.append(transaction)
#         except Exception:
#             pass
#     return accounts_monthly_balance_list