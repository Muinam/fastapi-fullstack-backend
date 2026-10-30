# sqlmodel models
from pydantic import EmailStr
from sqlalchemy import table
from datetime import datetime, timezone
from enum import Enum
from sqlmodel import SQLModel, Field

class ProductCategory(str, Enum):
    electronics = "electronics"
    clothing = "clothing"
    accessories= 'accessories'
    peripherals= "peripherals"


# Create Table 
# table ka design/blueprint.
class Product(SQLModel, table=True):
    __tablename__= 'products'
    id: int = Field(default=None, primary_key=True)
    name: str = Field(max_length=30)
    price: float = Field(ge=0)
    stock: int = Field(ge=0)
    category: ProductCategory
    created_at: datetime= Field(default_factory=lambda: datetime.now(timezone.utc))

class Seller(SQLModel, table=True):
    __tablename__= 'sellers'
    id: int = Field(default=None, primary_key=True)
    name: str = Field(max_length=30)
    email:EmailStr 
    password_hash : str
    