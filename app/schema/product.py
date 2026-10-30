from app.databases.model import ProductCategory
from enum import Enum
from pydantic import Field
from pydantic import BaseModel
import random

def random_warehouse() -> int:
    return random.randint(1,5)


class ProductStatus(str, Enum):
    active = 'active'
    low_stock = 'low_stock'
    out_of_stock = 'out_of_stock'

class BaseProduct(BaseModel):
    name : str = Field(
        description='Product Title', 
        min_length=2, max_length=50
        )
    
    price : float = Field(
        description="Price is USD",
        gt = 0,
        lt=1000
    )
    
    stock : int = Field(
        description="Unit available in warehouse",
        gt=0
    )

    category: ProductCategory | None = Field(default=None)

    # warehouse: int = Field(
    #     description="Warehouse code (1-5)",
    #     # default=1
    #     default_factory=random_warehouse
    # )


class ProductCreate(BaseProduct):
    pass

class ProductRead(BaseProduct):
    # status: ProductStatus
    pass

class ProductUpdate(BaseModel):
    name : str | None= Field(
        default= None,
        description='Product Title', 
        min_length=3, max_length=50
        )
    
    price : float | None= Field(
        default= None,
        description="Price is USD",
        gt = 0,
        lt=1000
    )
    
    stock : int | None= Field(
        default= None,
        description="Unit available in warehouse",
        gt=0
    )

    # warehouse: int | None = Field(
    #     default= None,
    #     description="Warehouse code (1-5)",
    #     # default=1
    #     # default_factory=random_warehouse
    # )