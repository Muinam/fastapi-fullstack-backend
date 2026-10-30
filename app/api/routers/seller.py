from redis import RedisError
from app.core import redis
import uuid
from app.core.security import oauth2_scheme
import jwt
from datetime import datetime, timedelta, timezone
from typing import Annotated
from sqlmodel import select
from fastapi import APIRouter, HTTPException, status, Depends
from app.schema.seller import SellerCreate, SellerRead
from app.databases.session import sessiondep
from app.databases.model import Seller
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm
from app.config import security_settings as st

router = APIRouter(prefix="/seller", tags=['Sellers'])

pwd_context = CryptContext(schemes=["bcrypt"])

@router.post("/Signup", response_model=SellerRead, status_code=status.HTTP_201_CREATED)
async def register_seller(data: SellerCreate, session:sessiondep):
    statement = select(Seller).where(Seller.email == data.email)
    existing_seller = session.exec(statement).first()
    if existing_seller:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
        )

    hashed_password = pwd_context.hash(data.password)
    new_seller = Seller(
        name = data.name,
        email = data.email,
        password_hash = hashed_password
    )
    session.add(new_seller)
    session.commit()
    session.refresh(new_seller)
    return new_seller

@router.post("/login")
def login(request_from: Annotated[OAuth2PasswordRequestForm, Depends()], session: sessiondep):
    statement = select(Seller).where(Seller.email == request_from.username)
    seller = session.exec(statement).first()
    if not seller:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Seller not found"
        )
    if not pwd_context.verify(request_from.password, seller.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password"
        )

    # generate access token
    token = jwt.encode(payload={
        "user":{
            'id':seller.id,
            "jwt": str(uuid.uuid4())
        },
        "exp": datetime.now(timezone.utc) + timedelta(minutes=5)
    },
    algorithm=st.JWT_ALGORITHM,
    key=st.JWT_SECRET_KEY
    )
    return {"access_token": token, "token_type": "bearer"}
    

@router.get("/dashboard", response_model=SellerRead)
def get_dashboard(token: Annotated[str, Depends(oauth2_scheme)], session: sessiondep):
    try:
        payload = jwt.decode(token, key=st.JWT_SECRET_KEY, algorithms=[st.JWT_ALGORITHM])
        user_data = payload.get("user")
        user_id = user_data.get("id") if isinstance(user_data, dict) else None
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload"
            )
        statement = select(Seller).where(Seller.id == user_id)
        seller = session.exec(statement).first()
        if not seller:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Seller not found"
            )
        return seller
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

@router.get("/logout")
def logout_seller(token_data:Annotated[dict,Depends(oauth2_scheme)]):
    jti = token_data['jwt']
    try:
        # add jti to the blacklist
        redis.set(f"blacklist_{jti}", "true", ex=60*60*24*7)  # 7 days
    except RedisError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Redis error"
        )
    return {"message": "Logout successful"}