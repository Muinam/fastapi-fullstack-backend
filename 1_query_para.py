from itertools import product
from fastapi import FastAPI, HTTPException, status
from typing import Any

app = FastAPI()

product = {
    1:{"name" : "Laptop", "price" : 50000,  "stock":22},
    2:{"name" : "Mouse", "price" : 200, "stock":55},
    3:{"name" : "Keyboard", "price" : 500, "stock":44},
    4:{"name" : "Monitor", "price" : 10000, "stock":12},
    5:{ "name" : "Webcam", "price" : 1000, "stock":15},
}

# Step 2: Query Parameter

@app.get("/product/{field}") # path and query parameter used at once
def get_product_field(field:str, id:int) -> dict[str,Any]:
    
    return {
        field: product[id][field]
    }


@app.get("/Product")
def get_product(id:int) -> dict[str,Any]:
    if id not in product:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = 'Invalid Product Id'
        )
        return product[id]
    return product

# Post endpoint
@app.post("/product")
def Create_product(name:str, price:float, stock:int) -> dict[str,Any]:
    if price <=0 or stock <= 0: # error handling
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