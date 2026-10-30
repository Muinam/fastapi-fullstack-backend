# 🚀 FastAPI Lecture — Complete Guide

> A complete reference for Python's fastest web framework — from basics to JWT Authentication, Redis Token Blacklisting, and production-ready project structure.

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

**API (Application Programming Interface):** Lets one program talk to another program over the internet, without using a browser or UI.

| Term | Meaning |
|------|---------|
| **Client** | The program that sends the request (browser, mobile app, Postman) |
| **Server** | The machine that listens, processes, and replies |
| **Endpoint** | The address of a resource, e.g. `/products`, `/seller/login` |
| **REST** | A set of design rules for building APIs |
| **RESTful API** | An API that follows those REST rules |

### Core Rules of REST
1. **Client-Server Architecture** — Client and Server are separate
2. **Statelessness** — Every request is independent, the server does not store any session
3. **Uniform Interface** — Consistent URL patterns (`/products/1`, `/sellers/5`)
4. **Resource-Based** — Everything is a resource identified by a URL

---

## 2. 📬 HTTP Methods (CRUD)

| Method | Operation | Description | Example |
|--------|-----------|-------------|---------|
| `GET` | **Read** | Fetch data | `GET /products?id=1` |
| `POST` | **Create** | Create new data | `POST /products` (data in body) |
| `PUT` | **Replace** | Replace the entire record | `PUT /products?id=1` (full body) |
| `PATCH` | **Update** | Update only specific fields | `PATCH /products?id=1` (partial body) |
| `DELETE` | **Delete** | Remove data | `DELETE /products?id=1` |

### PUT vs PATCH Difference
```
PUT    → Send the full object     → {"name":"Mouse", "price":200, "stock":55}
PATCH  → Send only what changed   → {"price": 250}
```

---

## 3. 📨 Request & Response Anatomy

### 4 Parts of a Request
```
┌──────────────────────────────────────────┐
│  1. Method      →  GET, POST, PUT, etc.  │
│  2. Endpoint    →  /seller/login         │
│  3. Headers     →  Content-Type, Token   │
│  4. Body        →  JSON data (POST/PUT)  │
└──────────────────────────────────────────┘
```

### 3 Parts of a Response
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

A Python web framework for building APIs — **fast to run** and **fast to write**.

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
| **Data Validation** | Powered by Pydantic — automatic type checking |
| **Automatic Docs** | `/docs` (Swagger UI) and `/redoc` — no extra code needed |
| **Dependency Injection** | Built into the framework |
| **Async Support** | `async/await` for scalable apps |

### Built on
- **Starlette** → Web toolkit (routing, middleware, ASGI)
- **Pydantic** → Data validation and serialization

---

## 5. 🎯 Routes & Decorators

A **Decorator** is the `@` syntax that connects a function to a specific HTTP method and path.

```python
@app.get("/hello")
# Means: When a GET request arrives at /hello, run the function below
def say_hello():
    return {"message": "Hello!"}
```

### Rules
- A route path must always start with a **forward slash `/`**
- One function can have one or more decorators
- Paths are case-sensitive (`/Hello` ≠ `/hello`)

---

## 6. 🔗 Path Parameters

A path parameter is a variable inside the URL path — it identifies **which specific resource** you are referring to.

```python
# Client sends: GET /shipment/3
@app.get("/shipment/{id}")
def get_shipment(id: int):    # {id} is auto-extracted from the URL
    return shipments[id]
```

**When a value comes from the client as part of the URL, it is called a path parameter.**

### ⚠️ Path Order Matters!
```python
@app.get("/shipment/latest")   # ← Define this first
@app.get("/shipment/{id}")     # ← Then this, otherwise "latest" will be treated as an id
```

---

## 7. 🔍 Query Parameters

A query parameter is a key-value pair passed in the URL after the `?` symbol — it tells the API **how to filter or customize** the returned data.

```python
# Client sends: GET /product?id=3
@app.get("/product")
def get_product(id: int):    # ?id=3 is auto-extracted from the URL
    return product[id]

# Optional query parameter:
@app.get("/product")
def get_product(id: int | None = None):    # id is not required
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

When the client needs to send data to the server (like creating a new product), the data is sent as a **request body** in JSON format. Used with POST, PUT, and PATCH methods.

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

Pydantic is the most widely used data validation library for Python. It uses type hints to define schemas and validates data automatically.

### Why Pydantic?
- **Powered by Type Hints** — Schema validation is controlled by Python 3.10+ type annotations
- **Speed** — Core validation logic is written in Rust
- **JSON Schema** — Models automatically emit JSON Schema for easy integration

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

### Using Pydantic (3 Steps)
```python
# 1. Define the model
class Product(BaseModel):
    name: str
    price: float

# 2. Create an object (validation happens here)
p = Product(name="Mouse", price=200)

# 3. Pass it to a function
def save_product(product: Product):
    print(product.name)              # Attribute access
    print(product.model_dump())      # → Python dict
    print(product.model_dump_json()) # → JSON string
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
        description="Product Title"      # Shown in docs
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
    # Only "male" or "female" are allowed — any other value raises an error
```

### Default — Predefined Value
```python
class Product(BaseModel):
    name: str = Field(default="N/A")     # If no value is given, defaults to "N/A"
    category: str | None = Field(default=None)  # Optional field
```

### Default Factory — Dynamic Default
```python
import random

def random_warehouse() -> int:
    return random.randint(1, 5)

class Product(BaseModel):
    warehouse: int = Field(default_factory=random_warehouse)
    # A new random value is generated for each new instance
```

---

## 11. 🔬 Field Validator & Model Validator

### Field Validator — Validate a Single Field
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
        return value.upper()    # Transform and return
```

### Model Validator — Validate Multiple Fields Together
```python
from pydantic import model_validator

class Student(BaseModel):
    age: int
    contact_detail: dict | None = None

    @model_validator(mode='after')
    def validate_contact(model):
        # If age > 20, contact info is required
        if model.age > 20 and not model.contact_detail:
            raise ValueError("Student must have contact info")
        return model
```

**Difference:** `field_validator` = one field at a time, `model_validator` = combined check across the whole model.

---

## 12. 🪆 Nested Pydantic Models

You can place one Pydantic model inside another:

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
    "address": {                  # Nested dict is auto-validated
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

Enum is used when the user should only be able to pick from a set of **allowed values**.

```python
from enum import Enum

class ProductCategory(str, Enum):
    electronics = "electronics"
    clothing = "clothing"
    accessories = "accessories"
    peripherals = "peripherals"

class Product(SQLModel, table=True):
    category: ProductCategory     # Only enum values are allowed
```

**`str, Enum`** is used so that the values properly show in JSON serialization and Swagger docs.

---

## 14. ⚡ Sync vs Async

### Synchronous (Blocking)
```python
def get_data():
    result = db.query()     # ← The entire program stops here until the query finishes
    return result
```
Tasks run one after another. If any task is slow, everything stops.

### Asynchronous (Non-Blocking)
```python
async def get_data():
    result = await db.query()  # ← The event loop handles other work while this completes
    return result
```
Tasks run concurrently. While one task is waiting, Python works on other tasks.

### Key Terms
| Term | Meaning |
|------|---------|
| `async` | Makes a function asynchronous |
| `await` | Waits for an async operation to finish without blocking |
| **Event Loop** | The scheduler that manages async tasks |
| **Blocking** | One task holds up all others |
| **Non-Blocking** | Other tasks keep running while one task waits |

### Usage in FastAPI
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

An object designed to **automatically handle setup and teardown** of resources (files, database connections).

```python
# Built-in example:
with open("file.txt") as f:
    data = f.read()
# File is automatically closed

# Database connection context manager:
from contextlib import contextmanager

@contextmanager
def manage_db():
    db = Database()
    db.connect_to_db()
    try:
        yield db          # ← Gives the db to the caller
    finally:
        db.close()        # ← Guaranteed: always closes

# Usage:
with manage_db() as db:
    print(db.get(1))
```

### Async Context Manager (FastAPI Lifespan)
```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_table()     # ← Runs when app starts
    yield                 # ← App is running
    # cleanup here        # ← Runs when app shuts down
```

---

## 16. 🗄️ Database — SQLite3 (Raw SQL)

SQLite3 is built into Python — no installation needed.

```python
import sqlite3

# Connect to (or create) a database
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

conn.commit()    # Save the changes
conn.close()     # Close the connection
```

### SQL Injection Protection
```python
# ❌ WRONG — Vulnerable to SQL Injection:
cursor.execute(f"SELECT * FROM products WHERE id = {user_input}")

# ✅ RIGHT — Parameterized query (safe):
cursor.execute("SELECT * FROM products WHERE id = :id", {"id": user_input})
```

---

## 17. 🧩 SQLModel & SQLAlchemy (ORM)

**ORM (Object Relational Mapping):** Lets you work with database tables and rows using Python classes and objects — no raw SQL needed.

### SQLModel = SQLAlchemy + Pydantic
```python
from sqlmodel import SQLModel, Field

# table=True means this class represents an actual database table
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

# Engine = The connection pool to the database
engine = create_engine("sqlite:///database.db", echo=True)
# echo=True: prints every SQL query to the terminal

# Session = A single conversation with the database
def get_session():
    with Session(engine) as session:
        yield session
# yield session: gives the session to the caller
# When the with block ends, the session automatically closes
```

### CRUD with SQLModel
```python
# CREATE
new_product = Product(name="Mouse", price=200, stock=55)
session.add(new_product)
session.commit()
session.refresh(new_product)    # Fetches updated data from DB (e.g. auto-generated ID)

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
session.get(Model, primary_key)              # Search only by Primary Key (ID)
select(Model).where(Model.column == value)   # Search by any column (filter)
```

---

## 18. 💉 Dependency Injection

In FastAPI, **Depends()** is used to automatically inject shared logic (database sessions, auth checks) into your endpoints.

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
Dependencies can be nested in FastAPI — one dependency can use another dependency.

---

## 19. 📁 Project Structure

```
fastapi-lecture/
├── .env                        # Environment variables (SECRET keys)
├── .gitignore                  # Git ignore rules
├── app/
│   ├── main.py                 # FastAPI app, lifespan, router includes
│   ├── config.py               # pydantic-settings (loads values from .env)
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

When you need to run something when the app starts or shuts down (like creating database tables), use lifespan.

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- STARTUP (before the app starts) ---
    create_db_table()
    print("Database tables created!")
    yield
    # --- SHUTDOWN (when the app stops) ---
    print("Cleanup done!")

app = FastAPI(lifespan=lifespan)
```

---

## 21. 🛣️ APIRouter — Modular Routing

In large projects, you don't keep all endpoints in one file. **APIRouter** lets you organize endpoints into separate files.

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

# app/main.py — Connect all routers to the main app:
app.include_router(products.router, tags=['Products'])
app.include_router(seller.router, tags=['Sellers'])
```

### `prefix` and `tags`
- **prefix** = This path is added before all endpoints (`/seller/login`)
- **tags** = Used for grouping in Swagger docs

---

## 22. 📤 Response Model & Status Codes

### Response Model — Control the Response Shape
```python
class SellerRead(BaseModel):
    name: str
    email: EmailStr
    # password_hash is NOT here — so it won't appear in the response!

@router.post("/Signup", response_model=SellerRead, status_code=201)
async def register_seller(data: SellerCreate):
    ...
    return new_seller    # FastAPI will only send name & email
```

**Benefit:** Sensitive fields (password, hash) never leak in the response.

### Common Status Codes
```python
from fastapi import status

status.HTTP_200_OK              # Default GET success
status.HTTP_201_CREATED         # New resource created
status.HTTP_204_NO_CONTENT      # Success, no body
status.HTTP_400_BAD_REQUEST     # Client's mistake
status.HTTP_401_UNAUTHORIZED    # Login required / invalid token
status.HTTP_404_NOT_FOUND       # Resource not found
status.HTTP_422_UNPROCESSABLE_ENTITY  # Validation failed
status.HTTP_500_INTERNAL_SERVER_ERROR # Server crashed
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
            detail="Product not found"      # This message is sent to the client
        )
    return product
```

**`raise HTTPException`** — The function immediately stops and sends an error response to the client.

---

## 24. 🔐 Password Hashing — Passlib & Bcrypt

Passwords must **never be stored as plain text** in the database. Always **hash** them.

```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"])

# Hash a password (during Signup):
hashed = pwd_context.hash("mypassword123")
# → "$2b$12$LH73smP1ax1Wms/zGgIbCO..."

# Verify a password (during Login):
is_correct = pwd_context.verify("mypassword123", hashed)
# → True
```

### ⚠️ Version Compatibility
```
passlib==1.7.4  →  requires bcrypt<=4.0.1
bcrypt 4.1+ / 5.0+  →  NOT compatible with passlib
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
# tokenUrl: tells Swagger docs where the login endpoint is
```

### Step 2: Login — Generate a Token
```python
import jwt, uuid
from datetime import datetime, timezone, timedelta

@router.post("/login")
def login(request_from: Annotated[OAuth2PasswordRequestForm, Depends()], session: sessiondep):
    # 1. Find the seller by email
    seller = session.exec(select(Seller).where(Seller.email == request_from.username)).first()

    # 2. Verify the password
    if not pwd_context.verify(request_from.password, seller.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect password")

    # 3. Create a JWT Token
    token = jwt.encode(
        payload={
            "user": {"id": seller.id, "jwt": str(uuid.uuid4())},
            "exp": datetime.now(timezone.utc) + timedelta(minutes=5)
        },
        key=SECRET_KEY,
        algorithm="HS256"
    )
    return {"access_token": token, "token_type": "bearer"}
    #                                          ↑ IMPORTANT: must be "bearer"
```

### Step 3: Protected Route — Verify the Token
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
| `OAuth2PasswordRequestForm` needs `Depends()` | It is not a Pydantic model, it is a dependency |
| `jwt.decode()` takes `algorithms` as a list | `algorithms=["HS256"]` (plural, list) |
| `exp` claim should be in UTC time | `datetime.now(timezone.utc)` |

---

## 26. 🚪 Token Blacklisting — Redis Logout

JWT tokens are stateless — the server cannot revoke them. **Redis** is used to blacklist tokens for secure logout.

### Redis Setup
```python
# app/core/redis.py
import redis
from redis.exceptions import RedisError

redis_client = redis.Redis(
    host="localhost", port=6379,
    db=0, decode_responses=True,
    protocol=2      # For compatibility with older Redis versions
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
    jti = payload["user"]["jwt"]       # The token's unique ID

    # Blacklist it in Redis (until the token would have expired)
    exp = payload.get("exp")
    remaining = max(int(exp - datetime.now(timezone.utc).timestamp()), 1)
    add_token_to_blacklist(jti, expire_seconds=remaining)

    return {"message": "Logout successful"}
```

### Check in Protected Routes
```python
@router.get("/dashboard")
def dashboard(token: Annotated[str, Depends(oauth2_scheme)]):
    payload = jwt.decode(token, ...)
    jti = payload["user"]["jwt"]

    # ← THIS CHECK is essential:
    if is_token_blacklisted(jti):
        raise HTTPException(status_code=401, detail="Token has been revoked")

    # ... rest of the logic
```

### Flow
```
Login   → Put a unique "jwt" (UUID) inside the token
Logout  → Store that UUID in Redis (blacklist)
Request → First check: is this UUID blacklisted?
            Yes → 401 Unauthorized
            No  → Proceed with the request
```

---

## 27. ⚙️ Environment Variables — pydantic-settings

Sensitive values (secret keys, passwords) should not be in the code. Store them in a `.env` file.

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
        env_file=".env",          # Path to the .env file
        env_ignore_empty=True,    # Ignore empty values
        extra="ignore"            # Ignore extra variables
    )
    JWT_SECRET_KEY: str           # Must match the EXACT name in .env
    JWT_ALGORITHM: str

security_settings = SecuritySettings()
```

### ⚠️ Variable Names Must Match
```
.env file:     JWT_SECRET_KEY=INAM
Config class:  JWT_SECRET_KEY: str     ✅ Match

.env file:     SECRET_KEY=INAM
Config class:  JWT_SECRET_KEY: str     ❌ Mismatch → ValidationError
```

---

## 28. 🌍 CORS Middleware

If your frontend (React/Next.js) runs on a different port, the browser will block API calls due to CORS policy. **CORSMiddleware** solves this.

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],         # Allow all HTTP methods
    allow_headers=["*"],         # Allow all headers
)
```

> **Note:** CORS is not used in this project yet, but it will be needed when you connect a frontend.

---

## 29. 🐛 Common Errors & Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| `TypeError: Boolean value of this clause is not defined` | Passed a filter expression to `session.get()` | Use `select().where()` instead — `session.get()` only works with primary keys |
| `FastAPIError: Invalid args for response field` | Used `OAuth2PasswordRequestForm` without `Depends()` | Write `Annotated[OAuth2PasswordRequestForm, Depends()]` |
| `ValueError: password cannot be longer than 72 bytes` | Version mismatch between `bcrypt>=4.1` and `passlib==1.7.4` | `pip install "bcrypt<=4.0.1"` |
| `ValidationError: Field required` | Variable names in `.env` don't match the config class | Use the **exact same names** in both places |
| `AttributeError: datetime has no attribute timezone` | Wrote `datetime.timezone.utc` after importing only `datetime` | Import `timezone` separately: `from datetime import timezone` |
| `ResponseValidationError: Input should be a valid dictionary` | Set `response_model=SellerRead` but returned a raw string | Decode the token and return a dict/object instead |
| `TypeError: list indices must be integers, not str` | Wrote `payload.get(["user"]["id"])` — created a list and used a string index | Use `payload.get("user")` then `.get("id")` |
| `SyntaxError: non-default argument follows default argument` | Put `Depends()` parameter before a required parameter | Use `Annotated` or fix the parameter order |
| `401 Unauthorized` on Swagger UI | `token_type` was set to `"jwt"` or the token header was not sent | Always set `token_type` to `"bearer"` and use the Authorize button in Swagger UI |

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
# 1. Create a virtual environment
python -m venv venv
.\venv\Scripts\activate          # Windows

# 2. Install dependencies
pip install fastapi uvicorn sqlmodel pydantic[email] pydantic-settings
pip install passlib "bcrypt<=4.0.1" PyJWT redis python-multipart

# 3. Create the .env file
echo JWT_SECRET_KEY=your-secret-key-here > .env
echo JWT_ALGORITHM=HS256 >> .env

# 4. Start Redis (on Windows: redis-server.exe)
redis-server

# 5. Run the server
uvicorn app.main:app --reload

# 6. Open the docs
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

> **📝 Note:** These notes cover both the practice code files and the final production-ready `app/` folder.
