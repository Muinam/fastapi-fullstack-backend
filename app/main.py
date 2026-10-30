from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.databases.session import create_db_table
from app.api.routers import products, seller


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_table()
    yield


# db = Database() ----> db.py
app = FastAPI(lifespan=lifespan)

app.include_router(products.router, tags=['Products'])
app.include_router(seller.router, tags=['Sellers'])