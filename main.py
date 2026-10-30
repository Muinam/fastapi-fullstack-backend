# fastapi devf
from typing import Any
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

class Product(BaseModel):
    name: str
    price: float
    stock: int

product = {
    1:{"name" : "Laptop", "price" : 50000,  "stock":22},
    2:{"name" : "Mouse", "price" : 200, "stock":55},
    3:{"name" : "Keyboard", "price" : 500, "stock":44},
    4:{"name" : "Monitor", "price" : 10000, "stock":12},
    5:{"name" : "Webcam", "price" : 1000, "stock":15},
}

# Step 2: Query Parameter

@app.get("/product/{field}") # path and query parameter used at once
def get_product_field(field:str, id:int) -> dict[str,Any]:
    
    return {
        field: product[id][field]
    }


@app.get("/product")
def get_product(id:int | None= None) -> dict[str,Any]: 
    # id a skti ha ya koi bhi id ni skti null bhi ho skti h
    if not id:
        id = max(product.keys())
        return product[id]

    if id not in product:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = 'Invalid Product Id'
        )
        return product[id]
    return product[id]

# Post endpoint using quey parameter
@app.post("/product")
def Create_product(data: Product) -> Product: # Product schema pydantic 
    name = data.name
    price = data.price
    stock = data.stock
    if price <=0 or stock <= 0:
        raise HTTPException(
            status_code = status.HTTP_406_NOT_ACCEPTABLE,
            detail = 'Product price and stock should be greater than 0'
        )

    new_id = max(product.keys()) + 1
    product[new_id] = {
        'name' : name,
        'price': price,
        'stock': stock
    }
    return product[new_id]

# Query or body parameter dono comhine bhi use kr skta h
# Post endpoint using Request body
@app.post("/product_request")
def Create_product(data: dict[str,Any]) -> dict[str,Any]:
    name = data['name']
    price = data['price']
    stock = data['stock']
    if price <=0 or stock <= 0:
        raise HTTPException(
            status_code = status.HTTP_406_NOT_ACCEPTABLE,
            detail = 'Product price and stock should be greater than 0'
        )

    new_id = max(product.keys()) + 1
    product[new_id] = {
        'name' : name,
        'price': price,
        'stock': stock
    }
    return {'id': new_id}



# update the exiting product 
@app.put("/product")
def replace_product(id:int, name:str, price:float, stock:int) -> dict[str,Any]:

    if id not in product:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = 'Invalid Product Id'
        )

    product[id] ={ 
        'name' : name,
        'price': price,
        'stock': stock
    }
    return product[id]



@app.patch('/product')
def patch_product(id:int, name:str | None =None, price:float| None=None, stock:int| None =None,) -> dict[str,Any]:

    if id not in product:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = 'Invalid Product Id'
        )

    products = product[id]

    if name is not None:
        products['name'] = name

    if price is not None:
        products['price'] = price

    if stock is not None:
        products['stock'] = stock

    product[id] = products

    return product[id]


@app.delete("/product")
def delete_product(id:int) -> dict[str, Any]:

    if id not in product:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = 'Invalid Product Id'
        )

    del product[id]

    return {"message": f"Product {id} deleted successfully"}


shipments = {
   1: {"id": 1, "weight": 1.2, "content": "Wood Table", "status": "Shipped"},
   2: {"id": 2, "weight": 2.5, "content": "Office Chair", "status": "Pending"},
   3: {"id": 3, "weight": 3.0, "content": "Bookshelf", "status": "Delivered"},
   4: {"id": 4, "weight": 0.8, "content": "Desk Lamp", "status": "Shipped"},
   5: {"id": 5, "weight": 4.2, "content": "Dining Table", "status": "Processing"},
   6: {"id": 6, "weight": 1.5, "content": "Wooden Stool", "status": "Delivered"}
}

# Step 1
@app.get("/shipment/latest") 
def get_shipment_latest() -> dict[str,Any]:
    id = max(shipments.keys())
    return shipments[id]


# Path Parameter
# for specific data fetch
@app.get("/shipment/{id}") # Path Parameter woh variable hota hai jo URL ke path ke andar define hota hai aur jiski value URL se receive hoti ha
# to complex
# def get_shipment_id(id: int) -> dict[str, int |str |float]: # int data type validation

def get_shipment_id(id: int) -> dict[str,Any]:
    
    if id not in shipments:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail = "Invalid Shipment Id"
        )

    return shipments[id]


@app.get("/shipment")
def get_shipment():
    return shipments


@app.get("/")
async def root():
    return {"message": "Hello World"}