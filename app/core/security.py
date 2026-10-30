from fastapi.security import OAuth2PasswordBearer

# create a oauth2 schema
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/seller/login")
