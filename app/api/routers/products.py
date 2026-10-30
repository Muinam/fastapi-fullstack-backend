from typing import Any
from fastapi import APIRouter, HTTPException, status, Depends
from app.schema.product import ProductCreate, ProductUpdate
from app.databases.session import get_session, sessiondep
from app.databases.model import Product
from sqlmodel import Session

router = APIRouter()

@router.get("/product")
def get_product(id:int, session: sessiondep) -> Product: 
    
    product = session.get(Product, id)
    if not product:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = 'Invalid Product Id'
        )
    
    return product


@router.post("/product")
def Create_product(data: ProductCreate, session:Session = Depends(get_session)) -> dict[str,Any]:

    new_product = Product(**data.model_dump())
    session.add(new_product)
    session.commit()
    session.refresh(new_product)
    return {"id": new_product.id}


@router.patch('/product')
def patch_product(id:int, body: ProductUpdate, session:Session = Depends(get_session)) -> Product:
    
    update = body.model_dump(exclude_none=True)

    product = session.get(Product, id)
    if not product:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = 'Invalid Product Id'
        )

    product.sqlmodel_update(update)
    session.commit()
    session.refresh(product)
    return product
 

@router.delete("/product")
def delete_product(id:int, session:Session = Depends(get_session)) -> dict[str, Any]:

    product = session.get(Product, id)
    if not product:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = 'Invalid Product Id'
        )

    session.delete(product)
    session.commit()

    return {'message': f"product {id} deleted successfully"}