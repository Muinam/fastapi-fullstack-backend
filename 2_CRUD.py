from fastapi import FastAPI, HTTPException,status
from typing import Any

app = FastAPI()

product = {
    1:{"name" : "Laptop", "price" : 50000,  "stock":22},
    2:{"name" : "Mouse", "price" : 200, "stock":55},
    3:{"name" : "Keyboard", "price" : 500, "stock":44},
    4:{"name" : "Monitor", "price" : 10000, "stock":12},
    5:{"name" : "Webcam", "price" : 1000, "stock":15},
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


@app.put() # full Data Update
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


# Specific Field Update
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

    return {"message": "Product deleted successfully"}