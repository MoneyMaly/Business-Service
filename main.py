from urllib.parse import quote_plus
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor import motor_asyncio
from passlib.context import CryptContext
from starlette.responses import JSONResponse

from app.routers import anomaly
from app.adapters import  db_adapter
from app.settings import DATABASE_USER, DATABASE_PORT, DATABASE_PASSWORD, DATABASE_SERVER, DATABASE_NAME

app = FastAPI(title='Business Service API')

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
# routers
app.include_router(anomaly.router)

@app.exception_handler(Exception)
async def exception_handler(request, exception: Exception):
    return JSONResponse(status_code=500, content={'detail': type(exception).__name__})

async def setup_db():
    url = f'mongodb://{DATABASE_USER}:{quote_plus(DATABASE_PASSWORD)}@{DATABASE_SERVER}:{DATABASE_PORT}' \
          f'/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@money-maly@'
    db_adapter.client = motor_asyncio.AsyncIOMotorClient(url, w='majority', socketTimeoutMS=5000, j=True, wtimeout=5000)
    return db_adapter.client[DATABASE_NAME]

@app.on_event('startup')
async def before_server_start():
    try:
        db_adapter.db = await setup_db()
    except:
        pass


@app.on_event('shutdown')
async def before_server_stop():
    db_adapter.client.close()

if __name__ == '__main__':  # For Debugging
    uvicorn.run(app, host='0.0.0.0', port=5000) 