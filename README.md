# 🚀 FastAPI Lecture — Complete Guide

> Python ke sab se fast web framework ka complete reference — basics se le kar JWT Authentication, Redis Token Blacklisting, aur production-ready project structure tak.

---

## 📑 Table of Contents

1. [API Fundamentals](#1--api-fundamentals)
2. [HTTP Methods (CRUD)](#2--http-methods-crud)
3. [Request & Response Anatomy](#3--request--response-anatomy)
4. [What is FastAPI?](#4--what-is-fastapi)
5. [Routes & Decorators](#5--routes--decorators)
6. [Path Parameters](#6--path-parameters)
7. [Query Parameters](#7--query-parameters)
8. [Request Body](#8--request-body)
9. [Pydantic — Data Validation](#9--pydantic--data-validation)
10. [Field, Literal, Default & Default Factory](#10--field-literal-default--default-factory)
11. [Field Validator & Model Validator](#11--field-validator--model-validator)
12. [Nested Pydantic Models](#12--nested-pydantic-models)
13. [Enum — Fixed Choices](#13--enum--fixed-choices)
14. [Sync vs Async](#14--sync-vs-async)
15. [Context Manager](#15--context-manager)
16. [Database — SQLite3 (Raw SQL)](#16--database--sqlite3-raw-sql)
17. [SQLModel & SQLAlchemy (ORM)](#17--sqlmodel--sqlalchemy-orm)
18. [Dependency Injection](#18--dependency-injection)
19. [Project Structure](#19--project-structure)
20. [Lifespan Events](#20--lifespan-events)
21. [APIRouter — Modular Routing](#21--apirouter--modular-routing)
22. [Response Model & Status Codes](#22--response-model--status-codes)
23. [Error Handling — HTTPException](#23--error-handling--httpexception)
24. [Password Hashing — Passlib & Bcrypt](#24--password-hashing--passlib--bcrypt)
25. [Authentication — OAuth2 & JWT](#25--authentication--oauth2--jwt)
26. [Token Blacklisting — Redis Logout](#26--token-blacklisting--redis-logout)
27. [Environment Variables — pydantic-settings](#27--environment-variables--pydantic-settings)
28. [CORS Middleware](#28--cors-middleware)
29. [Common Errors & Solutions](#29--common-errors--solutions)
30. [Project File Reference](#30--project-file-reference)

---

## 1. 🌐 API Fundamentals

**API (Application Programming Interface):** Ek program ko doosre program se internet ke zariye baat karne deta hai — bina browser ya UI ke.

| Term | Meaning |
|------|---------|
| **Client** | Woh program jo request bhejta hai (browser, mobile app, Postman) |
| **Server** | Woh machine jo sunta hai, process karta hai, aur reply deta hai |
| **Endpoint** | Resource ka address, e.g. `/products`, `/seller/login` |
| **REST** | Design rules ka set jo APIs banane ke liye follow kiya jata hai |
| **RESTful API** | Ek API jo REST ke un rules ko follow karti hai |

### REST ke Core Rules
1. **Client-Server Architecture** — Client aur Server alag hote hain
2. **Statelessness** — Har request independent hoti hai, server koi session store nahi karta
3. **Uniform Interface** — Consistent URL pattern (`/products/1`, `/sellers/5`)
4. **Resource-Based** — Har cheez ek resource hai jo URL se identify hoti hai

---

## 2. 📬 HTTP Methods (CRUD)

| Method | Operation | Description | Example |
|--------|-----------|-------------|---------|
| `GET` | **Read** | Data padhna (fetch karna) | `GET /products?id=1` |
| `POST` | **Create** | Naya data banana | `POST /products` (body mein data) |
| `PUT` | **Replace** | Poora record replace karna | `PUT /products?id=1` (full body) |
| `PATCH` | **Update** | Sirf specific fields update karna | `PATCH /products?id=1` (partial body) |
| `DELETE` | **Delete** | Data mitaana (remove karna) | `DELETE /products?id=1` |

### PUT vs PATCH ka Farq
```
PUT    → Poora object bhejo    → {"name":"Mouse", "price":200, "stock":55}
PATCH  → Sirf jo badalna ho    → {"price": 250}
```

---

## 3. 📨 Request & Response Anatomy

### Request ke 4 Parts
```
┌──────────────────────────────────────────┐
│  1. Method      →  GET, POST, PUT, etc.  │
│  2. Endpoint    →  /seller/login         │
│  3. Headers     →  Content-Type, Token   │
│  4. Body        →  JSON data (POST/PUT)  │
└──────────────────────────────────────────┘
```

### Response ke 3 Parts
```
┌──────────────────────────────────────────┐
│  1. Status Code →  200, 404, 500, etc.   │
│  2. Headers     →  Content-Type, etc.    │
│  3. Body        →  JSON response data    │
└──────────────────────────────────────────┘
```

### Status Codes
| Range | Category | Examples |
|-------|----------|----------|
| `2xx` | ✅ Success | `200 OK`, `201 Created`, `204 No Content` |
| `3xx` | ↪️ Redirection | `301 Moved Permanently`, `304 Not Modified` |
| `4xx` | ❌ Client Error | `400 Bad Request`, `401 Unauthorized`, `404 Not Found`, `422 Validation Error` |
| `5xx` | 💥 Server Error | `500 Internal Server Error`, `503 Service Unavailable` |

---

## 4. ⚡ What is FastAPI?

A Python web framework for building APIs — **fast to run** aur **fast to write**.

### 3 Simple Steps
```python
from fastapi import FastAPI
app = FastAPI()

# Step 1: Write a function
# Step 2: Add a decorator (method + path)
@app.get("/")
async def root():
    # Step 3: Return data (FastAPI sends it as JSON)
    return {"message": "Hello World"}
```

### Free Built-in Features
| Feature | Description |
|---------|-------------|
| **Data Validation** | Pydantic se powered — automatic type checking |
| **Automatic Docs** | `/docs` (Swagger UI) aur `/redoc` — kuch likhne ki zaroorat nahi |
| **Dependency Injection** | Framework mein built-in hai |
| **Async Support** | `async/await` for scalable apps |

### Built on
- **Starlette** → Web toolkit (routing, middleware, ASGI)
- **Pydantic** → Data validation aur serialization

---

## 5. 🎯 Routes & Decorators

**Decorator** woh `@` syntax hai jo kisi function ko kisi specific HTTP method aur path se jodta hai.

```python
@app.get("/hello")
# Matlab: Jab GET request "/hello" par aaye, neeche wala function chalao
def say_hello():
    return {"message": "Hello!"}
```

### Rules
- Route path hamesha **forward slash `/`** se start hota hai
- Ek function par ek ya zyada decorators lag sakte hain
- Path case-sensitive hota hai (`/Hello` ≠ `/hello`)

---

## 6. 🔗 Path Parameters

Path parameter URL path ke andar ka variable hota hai — **kis specific resource ki baat ho rahi hai?**

```python
# Client bhejta hai: GET /shipment/3
@app.get("/shipment/{id}")
def get_shipment(id: int):    # {id} URL se auto-extract hota hai
    return shipments[id]
```

**Jab client ki taraf se koi cheez URL mein aaye, usko path parameter kehte hain.**

### ⚠️ Path Order Matters!
```python
@app.get("/shipment/latest")   # ← Pehle ye define karo
@app.get("/shipment/{id}")     # ← Phir ye, warna "latest" ko id samjhega
```

---

## 7. 🔍 Query Parameters

Query parameter URL mein `?` ke baad key-value pair hota hai — **data ko filter ya customize kaise karna hai?**

```python
# Client bhejta hai: GET /product?id=3
@app.get("/product")
def get_product(id: int):    # URL se ?id=3 auto-extract hota hai
    return product[id]

# Optional query parameter:
@app.get("/product")
def get_product(id: int | None = None):    # id zaruri nahi
    if not id:
        return all_products
    return product[id]
```

### Path + Query Combined
```python
# GET /product/name?id=3 → field="name", id=3
@app.get("/product/{field}")
def get_product_field(field: str, id: int):
    return {field: product[id][field]}
```

---

## 8. 📦 Request Body

Jab client se server ko data bhejna ho (jaise naya product banana), toh wo **request body** mein JSON ke tor par bhejte hain. POST, PUT aur PATCH mein use hota hai.

```python
# Raw dict approach (not recommended):
@app.post("/product")
def create(data: dict[str, Any]):
    name = data['name']       # No validation!

# ✅ Pydantic approach (recommended):
@app.post("/product")
def create(data: ProductCreate):
    name = data.name           # Validated automatically!
```

---

## 9. ✅ Pydantic — Data Validation

Pydantic Python ki sab se popular data validation library hai. Type hints use karke schema define karo, Pydantic validate karega.

### Why Pydantic?
- **Type Hints Powered** — Python 3.10+ annotations se schema control hota hai
- **Speed** — Core logic Rust mein likhi hai
- **JSON Schema** — Models automatically JSON Schema emit karte hain

### Basic Model
```python
from pydantic import BaseModel, EmailStr

class Student(BaseModel):
    name: str                             # Required string
    age: int                              # Required integer
    cgpa: float                           # Required float
    email: EmailStr                       # Valid email format
    hostel: bool                          # True/False
    interests: list[str]                  # List of strings
    contact: dict[str, str] | None = None # Optional dictionary
```

### Pydantic ka Use (3 Steps)
```python
# 1. Model define karo
class Product(BaseModel):
    name: str
    price: float

# 2. Object banao (validation yahan hoti hai)
p = Product(name="Mouse", price=200)

# 3. Function mein pass karo
def save_product(product: Product):
    print(product.name)     # attribute access
    print(product.model_dump())  # → dict
    print(product.model_dump_json())  # → JSON string
```

---

## 10. 🔧 Field, Literal, Default & Default Factory

### Field() — Validation Constraints
```python
from pydantic import Field

class Product(BaseModel):
    name: str = Field(
        min_length=2,                    # Minimum 2 characters
        max_length=50,                   # Maximum 50 characters
        description="Product Title"      # Docs mein dikhega
    )
    price: float = Field(
        gt=0,                            # Greater than 0
        lt=1000,                         # Less than 1000
        description="Price in USD"
    )
    stock: int = Field(ge=0)             # Greater than or equal to 0
```

### Literal — Fixed Allowed Values
```python
from typing import Literal

class Student(BaseModel):
    gender: Literal["male", "female"]
    # Sirf "male" ya "female" allowed — koi aur value error degi
```

### Default — Predefined Value
```python
class Product(BaseModel):
    name: str = Field(default="N/A")     # Agar value na do toh "N/A"
    category: str | None = Field(default=None)  # Optional field
```

### Default Factory — Dynamic Default
```python
import random

def random_warehouse() -> int:
    return random.randint(1, 5)

class Product(BaseModel):
    warehouse: int = Field(default_factory=random_warehouse)
    # Har naye instance mein naya random value generate hoga
```

---

## 11. 🔬 Field Validator & Model Validator

### Field Validator — Single Field Validation
```python
from pydantic import field_validator

class Student(BaseModel):
    name: str
    email: EmailStr

    @field_validator('email')
    @classmethod
    def email_must_be_edu(cls, value):
        if not str(value).endswith('.edu'):
            raise ValueError("Email must be .edu domain")
        return value

    @field_validator('name')
    @classmethod
    def name_to_upper(cls, value):
        return value.upper()    # Transform + return
```

### Model Validator — Multiple Fields Together
```python
from pydantic import model_validator

class Student(BaseModel):
    age: int
    contact_detail: dict | None = None

    @model_validator(mode='after')
    def validate_contact(model):
        # Agar age > 20 hai toh contact zaroori hai
        if model.age > 20 and not model.contact_detail:
            raise ValueError("Student must have contact info")
        return model
```

**Farq:** `field_validator` = ek field, `model_validator` = poore model ka combined check.

---

## 12. 🪆 Nested Pydantic Models

Ek Pydantic model ke andar doosra Pydantic model rakh sakte hain:

```python
class Address(BaseModel):
    city: str
    pin_code: int

class Student(BaseModel):
    name: str
    gender: Literal["male", "female"]
    address: Address              # Nested model

# Usage:
data = {
    "name": "Abdullah",
    "gender": "male",
    "address": {                  # Nested dict auto-validate hoga
        "city": "Karachi",
        "pin_code": 123456
    }
}
student = Student(**data)

# Convert back:
student.model_dump()          # → Python dict
student.model_dump_json()     # → JSON string
```

---

## 13. 🏷️ Enum — Fixed Choices

Enum tab use hota hai jab user ko sirf **allowed values** mein se choose karna ho.

```python
from enum import Enum

class ProductCategory(str, Enum):
    electronics = "electronics"
    clothing = "clothing"
    accessories = "accessories"
    peripherals = "peripherals"

class Product(SQLModel, table=True):
    category: ProductCategory     # Sirf enum values allowed
```

**`str, Enum`** likhne ka faida: JSON serialization aur Swagger docs mein properly dikhta hai.

---

## 14. ⚡ Sync vs Async

### Synchronous (Blocking)
```python
def get_data():
    result = db.query()     # ← Poora program yahan rukta hai jab tak query complete na ho
    return result
```
Tasks ek ke baad ek chalte hain. Agar koi task slow ho, sab ruk jata hai.

### Asynchronous (Non-Blocking)
```python
async def get_data():
    result = await db.query()  # ← Event loop doosre kaam karta hai jab tak ye complete ho
    return result
```
Tasks concurrently chalte hain. Waiting period mein Python doosra kaam karta hai.

### Key Terms
| Term | Meaning |
|------|---------|
| `async` | Function ko asynchronous banata hai |
| `await` | Async operation complete hone ka wait karta hai bina block kiye |
| **Event Loop** | Scheduler jo async tasks manage karta hai |
| **Blocking** | Ek task doosron ko rok leta hai |
| **Non-Blocking** | Ek task wait karte hue doosre kaam chalte rahte hain |

### FastAPI mein Usage
```python
# Sync endpoint (simple database calls):
@app.get("/product")
def get_product():
    return db.get(1)

# Async endpoint (I/O heavy, external APIs):
@app.get("/product")
async def get_product():
    return await db.async_get(1)
```

---

## 15. 📦 Context Manager

Ek object jo resources (files, database connections) ko **automatically open aur close** karta hai.

```python
# Built-in example:
with open("file.txt") as f:
    data = f.read()
# File automatically close ho jati hai

# Database connection context manager:
from contextlib import contextmanager

@contextmanager
def manage_db():
    db = Database()
    db.connect_to_db()
    try:
        yield db          # ← Caller ko db deta hai
    finally:
        db.close()        # ← Guarantee: hamesha close hoga

# Usage:
with manage_db() as db:
    print(db.get(1))
```

### Async Context Manager (FastAPI Lifespan)
```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_table()     # ← App start hone par
    yield                 # ← App chal rahi hai
    # cleanup here        # ← App band hone par
```

---

## 16. 🗄️ Database — SQLite3 (Raw SQL)

SQLite3 Python mein built-in hai — koi installation zaruri nahi.

```python
import sqlite3

# Connect (ya create) database
conn = sqlite3.connect("products.db", check_same_thread=False)
cursor = conn.cursor()

# Create Table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS products(
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        price REAL NOT NULL,
        stock INTEGER NOT NULL
    )
''')

# CRUD Operations:
# Create: INSERT INTO products VALUES (...)
# Read:   SELECT * FROM products WHERE id = :id
# Update: UPDATE products SET stock = :stock WHERE id = :id
# Delete: DELETE FROM products WHERE id = :id

conn.commit()    # Changes save karo
conn.close()     # Connection band karo
```

### SQL Injection Protection
```python
# ❌ WRONG — SQL Injection ka khattra:
cursor.execute(f"SELECT * FROM products WHERE id = {user_input}")

# ✅ RIGHT — Parameterized query:
cursor.execute("SELECT * FROM products WHERE id = :id", {"id": user_input})
```

---

## 17. 🧩 SQLModel & SQLAlchemy (ORM)

**ORM (Object Relational Mapping):** Python classes aur objects se database tables aur rows ko handle karna — raw SQL likhne ki zaroorat nahi.

### SQLModel = SQLAlchemy + Pydantic
```python
from sqlmodel import SQLModel, Field

# table=True: ye class ek actual database table hai
class Product(SQLModel, table=True):
    __tablename__ = 'products'
    id: int = Field(default=None, primary_key=True)
    name: str = Field(max_length=30)
    price: float = Field(ge=0)
    stock: int = Field(ge=0)
    category: ProductCategory
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
```

### Engine & Session
```python
from sqlalchemy import create_engine
from sqlmodel import Session

# Engine = Database ka connection pool
engine = create_engine("sqlite:///database.db", echo=True)
# echo=True: har SQL query terminal par dikhegi

# Session = Ek conversation with the database
def get_session():
    with Session(engine) as session:
        yield session
# yield session: caller ko session deta hai
# with block khatam hone par session automatically close hota hai
```

### CRUD with SQLModel
```python
# CREATE
new_product = Product(name="Mouse", price=200, stock=55)
session.add(new_product)
session.commit()
session.refresh(new_product)    # DB se updated data wapas laao (e.g. auto ID)

# READ (by primary key)
product = session.get(Product, 1)

# READ (by filter/column)
from sqlmodel import select
statement = select(Product).where(Product.name == "Mouse")
product = session.exec(statement).first()

# UPDATE
product.price = 250
session.commit()
session.refresh(product)

# DELETE
session.delete(product)
session.commit()
```

### ⚠️ session.get() vs select()
```python
session.get(Model, primary_key)              # Sirf Primary Key (ID) se search
select(Model).where(Model.column == value)   # Kisi bhi column se search (filter)
```

---

## 18. 💉 Dependency Injection

FastAPI mein **Depends()** use hota hai taake shared logic (database session, auth check) automatically inject ho jaye.

```python
from fastapi import Depends
from typing import Annotated

# Method 1: Depends() directly
@app.get("/product")
def get_product(session: Session = Depends(get_session)):
    ...

# Method 2: Annotated (recommended, cleaner)
sessiondep = Annotated[Session, Depends(get_session)]

@app.get("/product")
def get_product(session: sessiondep):
    ...
```

### Dependency Chain
FastAPI mein dependencies nested bhi ho sakti hain — ek dependency doosri dependency use kar sakti hai.

---

## 19. 📁 Project Structure

```
fastapi-lecture/
├── .env                        # Environment variables (SECRET keys)
├── .gitignore                  # Git ignore rules
├── app/
│   ├── main.py                 # FastAPI app, lifespan, router includes
│   ├── config.py               # pydantic-settings (.env se values load)
│   ├── api/
│   │   └── routers/
│   │       ├── products.py     # Product CRUD endpoints
│   │       └── seller.py       # Seller auth (signup, login, logout, dashboard)
│   ├── core/
│   │   ├── security.py         # OAuth2 scheme setup
│   │   └── redis.py            # Redis client & token blacklist helpers
│   ├── databases/
│   │   ├── model.py            # SQLModel table definitions
│   │   └── session.py          # Engine, session, dependency
│   └── schema/
│       ├── product.py          # Pydantic schemas for Product
│       └── seller.py           # Pydantic schemas for Seller
├── main.py                     # Early practice file (basic endpoints)
├── 1_query_para.py             # Practice: Path & Query parameters
├── 2_CRUD.py                   # Practice: Full CRUD with in-memory dict
├── 3_pydantic.py               # Practice: Pydantic validation
├── 4_nested_pydantic.py        # Practice: Nested models & Literal
├── databases.py                # Practice: Raw SQLite3
└── database.db                 # SQLite database file
```

---

## 20. 🔄 Lifespan Events

App start aur shutdown ke waqt kuch kaam karana ho (jaise tables banana), toh lifespan use hota hai.

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- STARTUP (app start hone se pehle) ---
    create_db_table()
    print("Database tables created!")
    yield
    # --- SHUTDOWN (app band hone par) ---
    print("Cleanup done!")

app = FastAPI(lifespan=lifespan)
```

---

## 21. 🛣️ APIRouter — Modular Routing

Bade projects mein sab endpoints ek file mein nahi rakhte. **APIRouter** se endpoints alag files mein organize hote hain.

```python
# app/api/routers/products.py
from fastapi import APIRouter
router = APIRouter()

@router.get("/product")
def get_product(): ...

# app/api/routers/seller.py
router = APIRouter(prefix="/seller", tags=['Sellers'])

@router.post("/Signup")
async def register_seller(): ...

# app/main.py — Sab routers ko main app mein jodo:
app.include_router(products.router, tags=['Products'])
app.include_router(seller.router, tags=['Sellers'])
```

### `prefix` aur `tags`
- **prefix** = Sab endpoints ke aage yeh path lagta hai (`/seller/login`)
- **tags** = Swagger docs mein grouping ke liye

---

## 22. 📤 Response Model & Status Codes

### Response Model — Control Response Shape
```python
class SellerRead(BaseModel):
    name: str
    email: EmailStr
    # password_hash NAHI hai — toh response mein nahi jayega!

@router.post("/Signup", response_model=SellerRead, status_code=201)
async def register_seller(data: SellerCreate):
    ...
    return new_seller    # FastAPI sirf name & email bhejega
```

**Faida:** Sensitive fields (password, hash) response mein leak nahi hote.

### Common Status Codes
```python
from fastapi import status

status.HTTP_200_OK              # Default GET
status.HTTP_201_CREATED         # Naya resource bana
status.HTTP_204_NO_CONTENT      # Success, koi body nahi
status.HTTP_400_BAD_REQUEST     # Client ki galti
status.HTTP_401_UNAUTHORIZED    # Login required / invalid token
status.HTTP_404_NOT_FOUND       # Resource nahi mila
status.HTTP_422_UNPROCESSABLE_ENTITY  # Validation fail
status.HTTP_500_INTERNAL_SERVER_ERROR # Server crash
```

---

## 23. ⚠️ Error Handling — HTTPException

```python
from fastapi import HTTPException, status

@app.get("/product")
def get_product(id: int):
    product = session.get(Product, id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"      # Client ko ye message milega
        )
    return product
```

**`raise HTTPException`** — Function turant ruk jata hai aur error response client ko bhej deta hai.

---

## 24. 🔐 Password Hashing — Passlib & Bcrypt

Passwords database mein **kabhi plain text** mein store nahi karte. Hamesha **hash** karo.

```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"])

# Password hash karo (Signup ke waqt):
hashed = pwd_context.hash("mypassword123")
# → "$2b$12$LH73smP1ax1Wms/zGgIbCO..."

# Password verify karo (Login ke waqt):
is_correct = pwd_context.verify("mypassword123", hashed)
# → True
```

### ⚠️ Version Compatibility
```
passlib==1.7.4  →  bcrypt<=4.0.1 chahiye
bcrypt 4.1+ / 5.0+  →  passlib se compatible NAHI hai
```
**Fix:** `pip install "bcrypt<=4.0.1"`

---

## 25. 🔑 Authentication — OAuth2 & JWT

### Flow Diagram
```
┌─────────┐    email + password     ┌─────────┐
│  Client  │ ─────────────────────→ │  Server  │
│ (Browser)│                        │ (FastAPI)│
│          │ ←───────────────────── │          │
│          │    JWT access_token    │          │
│          │                        │          │
│          │  Authorization: Bearer │          │
│          │  <token>               │          │
│          │ ─────────────────────→ │          │
│          │                        │  Verify  │
│          │ ←───────────────────── │  Token   │
│          │    Protected Data      │          │
└─────────┘                        └─────────┘
```

### Step 1: OAuth2 Scheme Setup
```python
# app/core/security.py
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/seller/login")
# tokenUrl: Swagger docs ko batata hai ke login kahan hai
```

### Step 2: Login — Token Generate Karna
```python
import jwt, uuid
from datetime import datetime, timezone, timedelta

@router.post("/login")
def login(request_from: Annotated[OAuth2PasswordRequestForm, Depends()], session: sessiondep):
    # 1. Email se seller dhoondho
    seller = session.exec(select(Seller).where(Seller.email == request_from.username)).first()

    # 2. Password verify karo
    if not pwd_context.verify(request_from.password, seller.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect password")

    # 3. JWT Token banao
    token = jwt.encode(
        payload={
            "user": {"id": seller.id, "jwt": str(uuid.uuid4())},
            "exp": datetime.now(timezone.utc) + timedelta(minutes=5)
        },
        key=SECRET_KEY,
        algorithm="HS256"
    )
    return {"access_token": token, "token_type": "bearer"}
    #                                          ↑ ZAROORI: "bearer" hona chahiye
```

### Step 3: Protected Route — Token Verify Karna
```python
@router.get("/dashboard", response_model=SellerRead)
def get_dashboard(token: Annotated[str, Depends(oauth2_scheme)], session: sessiondep):
    payload = jwt.decode(token, key=SECRET_KEY, algorithms=["HS256"])
    user_id = payload["user"]["id"]
    seller = session.exec(select(Seller).where(Seller.id == user_id)).first()
    return seller
```

### JWT Token Anatomy
```
Header.Payload.Signature

eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyIjp7ImlkIjoxfSwiZXhwIjoxNjk5fQ.abc123
         ↑                          ↑                              ↑
      Algorithm              User data + Expiry               Signature
```

### ⚠️ Important Notes
| Rule | Reason |
|------|--------|
| `token_type` must be `"bearer"` | OAuth2 standard + Swagger UI compatibility |
| `OAuth2PasswordRequestForm` needs `Depends()` | Ye Pydantic model nahi, dependency hai |
| `jwt.decode()` mein `algorithms` list hai | `algorithms=["HS256"]` (plural, list) |
| `exp` claim UTC time mein hona chahiye | `datetime.now(timezone.utc)` |

---

## 26. 🚪 Token Blacklisting — Redis Logout

JWT tokens stateless hain — server unhe revoke nahi kar sakta. **Redis** use karke token ko blacklist karte hain.

### Redis Setup
```python
# app/core/redis.py
import redis
from redis.exceptions import RedisError

redis_client = redis.Redis(
    host="localhost", port=6379,
    db=0, decode_responses=True,
    protocol=2      # Older Redis versions ke liye compatibility
)

def add_token_to_blacklist(jti: str, expire_seconds: int = 604800):
    redis_client.set(f"blacklist_{jti}", "true", ex=expire_seconds)

def is_token_blacklisted(jti: str) -> bool:
    return bool(redis_client.exists(f"blacklist_{jti}"))
```

### Logout Endpoint
```python
@router.post("/logout")
def logout(token: Annotated[str, Depends(oauth2_scheme)]):
    payload = jwt.decode(token, key=SECRET_KEY, algorithms=["HS256"])
    jti = payload["user"]["jwt"]       # Token ka unique ID

    # Redis mein blacklist karo (token expire hone tak)
    exp = payload.get("exp")
    remaining = max(int(exp - datetime.now(timezone.utc).timestamp()), 1)
    add_token_to_blacklist(jti, expire_seconds=remaining)

    return {"message": "Logout successful"}
```

### Protected Route mein Check
```python
@router.get("/dashboard")
def dashboard(token: Annotated[str, Depends(oauth2_scheme)]):
    payload = jwt.decode(token, ...)
    jti = payload["user"]["jwt"]

    # ← YEH CHECK zaroori hai:
    if is_token_blacklisted(jti):
        raise HTTPException(status_code=401, detail="Token has been revoked")

    # ... baaki logic
```

### Flow
```
Login  → Token mein unique "jwt" (UUID) daalo
Logout → Us UUID ko Redis mein store karo (blacklist)
Request → Pehle check karo: kya ye UUID blacklisted hai?
           Haan → 401 Unauthorized
           Nahi → Request proceed karo
```

---

## 27. ⚙️ Environment Variables — pydantic-settings

Sensitive values (secret keys, passwords) code mein nahi, `.env` file mein rakhte hain.

### `.env` File
```env
JWT_SECRET_KEY=my-super-secret-key-here
JWT_ALGORITHM=HS256
```

### Config Class
```python
from pydantic_settings import BaseSettings, SettingsConfigDict

class SecuritySettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",          # .env file ka path
        env_ignore_empty=True,    # Empty values ignore karo
        extra="ignore"            # Extra variables ignore karo
    )
    JWT_SECRET_KEY: str           # .env mein SAME naam hona chahiye
    JWT_ALGORITHM: str

security_settings = SecuritySettings()
```

### ⚠️ Variable Names Match Hone Chahiye
```
.env file:     JWT_SECRET_KEY=INAM
Config class:  JWT_SECRET_KEY: str     ✅ Match

.env file:     SECRET_KEY=INAM
Config class:  JWT_SECRET_KEY: str     ❌ Mismatch → ValidationError
```

---

## 28. 🌍 CORS Middleware

Agar aapka frontend (React/Next.js) alag port par chal raha hai, toh browser CORS policy ki wajah se API call block karega. **CORSMiddleware** se solve hota hai.

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],         # Sab HTTP methods allow
    allow_headers=["*"],         # Sab headers allow
)
```

> **Note:** Is project mein abhi CORS use nahi hua hai, lekin jab frontend connect karoge toh zaroori hoga.

---

## 29. 🐛 Common Errors & Solutions

| Error | Wajah | Solution |
|-------|-------|----------|
| `TypeError: Boolean value of this clause is not defined` | `session.get()` mein filter expression pass kiya | `select().where()` use karo, `session.get()` sirf primary key ke liye |
| `FastAPIError: Invalid args for response field` | `OAuth2PasswordRequestForm` bina `Depends()` ke use kiya | `Annotated[OAuth2PasswordRequestForm, Depends()]` likho |
| `ValueError: password cannot be longer than 72 bytes` | `bcrypt>=4.1` aur `passlib==1.7.4` ka mismatch | `pip install "bcrypt<=4.0.1"` |
| `ValidationError: Field required` | `.env` file ke variable names config class se match nahi karte | Dono jagah **exact same naam** rakho |
| `AttributeError: datetime has no attribute timezone` | `from datetime import datetime` ke baad `datetime.timezone.utc` likha | `from datetime import timezone` alag import karo |
| `ResponseValidationError: Input should be a valid dictionary` | `response_model=SellerRead` laga tha lekin raw string return kiya | Token decode karke dict/object return karo |
| `TypeError: list indices must be integers, not str` | `payload.get(["user"]["id"])` — list banake string index kiya | `payload.get("user")` phir `.get("id")` use karo |
| `SyntaxError: non-default argument follows default argument` | `Depends()` wala parameter pehle, normal parameter baad mein | `Annotated` use karo ya parameter order fix karo |
| `401 Unauthorized` on Swagger UI | `token_type` `"jwt"` likha tha ya token header nahi bheja | `token_type` hamesha `"bearer"` rakho, Swagger UI mein Authorize button use karo |

---

## 30. 📂 Project File Reference

| File | Purpose |
|------|---------|
| [`app/main.py`](app/main.py) | FastAPI app instance, lifespan events, router registration |
| [`app/config.py`](app/config.py) | Environment variable loading via pydantic-settings |
| [`app/databases/model.py`](app/databases/model.py) | SQLModel table definitions (Product, Seller) |
| [`app/databases/session.py`](app/databases/session.py) | Database engine, session factory, sessiondep |
| [`app/schema/product.py`](app/schema/product.py) | Pydantic schemas: ProductCreate, ProductRead, ProductUpdate |
| [`app/schema/seller.py`](app/schema/seller.py) | Pydantic schemas: BaseSeller, SellerCreate, SellerRead |
| [`app/api/routers/products.py`](app/api/routers/products.py) | Product CRUD endpoints (GET, POST, PATCH, DELETE) |
| [`app/api/routers/seller.py`](app/api/routers/seller.py) | Seller auth: Signup, Login (JWT), Dashboard, Logout |
| [`app/core/security.py`](app/core/security.py) | OAuth2PasswordBearer scheme |
| [`app/core/redis.py`](app/core/redis.py) | Redis client, token blacklist helpers |
| [`main.py`](main.py) | Practice: Basic endpoints, path/query params, CRUD |
| [`1_query_para.py`](1_query_para.py) | Practice: Path + Query parameters combined |
| [`2_CRUD.py`](2_CRUD.py) | Practice: Full CRUD with in-memory dictionary |
| [`3_pydantic.py`](3_pydantic.py) | Practice: Pydantic validation, field/model validators |
| [`4_nested_pydantic.py`](4_nested_pydantic.py) | Practice: Nested models, Literal, model_dump |
| [`databases.py`](databases.py) | Practice: Raw SQLite3 CRUD |
| [`app/database.py`](app/database.py) | Practice: SQLite3 with context manager class |

---

## 🏃 Quick Start

```bash
# 1. Virtual environment banao
python -m venv venv
.\venv\Scripts\activate          # Windows

# 2. Dependencies install karo
pip install fastapi uvicorn sqlmodel pydantic[email] pydantic-settings
pip install passlib "bcrypt<=4.0.1" PyJWT redis python-multipart

# 3. .env file banao
echo JWT_SECRET_KEY=your-secret-key-here > .env
echo JWT_ALGORITHM=HS256 >> .env

# 4. Redis start karo (Windows pe redis-server.exe)
redis-server

# 5. Server chalao
uvicorn app.main:app --reload

# 6. Docs dekho
# → http://127.0.0.1:8000/docs
```

---

## 📦 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `fastapi` | Latest | Web framework |
| `uvicorn` | Latest | ASGI server |
| `sqlmodel` | Latest | ORM (SQLAlchemy + Pydantic) |
| `pydantic[email]` | Latest | Email validation (`EmailStr`) |
| `pydantic-settings` | Latest | `.env` file loading |
| `passlib` | 1.7.4 | Password hashing |
| `bcrypt` | ≤4.0.1 | Bcrypt algorithm (passlib compatible) |
| `PyJWT` | Latest | JWT token encode/decode |
| `redis` | Latest | Token blacklisting |
| `python-multipart` | Latest | Form data parsing (`OAuth2PasswordRequestForm`) |

---

> **📝 Note:** Yeh notes lecture ke practice code aur final production-ready `app/` folder dono cover karti hain.
