from typing import Annotated
from fastapi import Depends
from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session

# create the database engine
engine = create_engine("sqlite:///database.db", echo=True, 
                               connect_args={"check_same_thread": False}) # echo use har query dikhae ga terminal pr

def create_db_table():
    SQLModel.metadata.create_all(engine)

create_db_table()

def get_session():
    with Session(engine) as session:
        yield session # ye session ko caller (jaise FastAPI endpoint) ko deta hai; with block khatam hone par session automatically close ho jata hai.


sessiondep = Annotated[Session, Depends(get_session)]
# Example purpose
# To Read a data
# product = session.get(Product, 1)
# print(product)

# to create product
# product = Product(name="Product 1", price=10, stock=10, category= ProductCategory.accessories)

# session.add(product)
# session.commit()
# session.refresh(product)
# print(product)