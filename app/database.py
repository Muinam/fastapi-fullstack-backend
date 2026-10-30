# sqlite3 database connection using python
from contextlib import contextmanager
from typing import Any
from app.schema.product import ProductCreate, ProductUpdate
import sqlite3

class Database:

    # Initialize DB
    def connect_to_db(self):
        self.conn = sqlite3.connect("products.db", check_same_thread=False) # check_same_thread is liya use kiya fastapi or db same thread par nhi chala conflic create na ho
        self.cur = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS products(
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                stock INTEGER NOT NULL
            )
        ''')

    def create(self, product: ProductCreate):
        self.cur.execute('SELECT MAX(id) FROM products')
        result = self.cur.fetchone()

        new_id = (result[0] or 0) + 1

        # :id, :name, :price, :stock  placeholder ka tor pr use krta h
        self.cur.execute('''
            INSERT INTO products (id, name, price, stock) 
            VALUES (:id, :name, :price, :stock)
        ''', {"id": new_id, **product.model_dump()})

        self.conn.commit()
        return new_id

    def get(self, id: int)-> dict[str,Any]:
        self.cur.execute('SELECT * FROM products WHERE id = :id',
        {"id":id})

        result = self.cur.fetchone()
        if result:
            return{
                'id': result[0],
                'name':result[1],
                'price':result[2],
                'stock':result[3]
            }
        return None

    
    def update(self, id:int, product_update:ProductUpdate):
        
        updated_fields = product_update.model_dump(exclude_none=True) # only store jo update hui hai
        
        set_clause = ",".join(f"{key} = :{key}" for key in updated_fields )  # set clause for update query

        self.cur.execute(f"""
        UPDATE products SET {set_clause} WHERE id = :id""",
        { "id":id,  **updated_fields })

        self.conn.commit()

        return self.get(id)

    def delete(self ,id:int):
        self.cur.execute('''
            DELETE FROM products WHERE id = :id
        ''',{"id":id})

        self.conn.commit()

        return self.cur.rowcount > 0

    
    def close(self):
        self.conn.close()


    # custom manager function        
    # def __enter__(self): 
    #     self.connect_to_db()
    #     self.create_table()
    #     return self

    # def __exit__(self, *args):
    #     self.close()

    # with Database() as db:
    # prod = ProductCreate(
    #     name = "top",
    #     price = 120.0,
    #     stock = 8
    # )
    # new = db.create(prod)
    # print(db.get(new))

@contextmanager
def manage_db():
    db = Database()
    db.connect_to_db()
    db.create_table()
    try:
        yield db
    finally:
        db.close()

with manage_db() as db:
    print(db.get(1))
