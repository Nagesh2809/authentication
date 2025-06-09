from datetime import datetime, timedelta
# from jose import jwt, JWTError
import jwt
from passlib.context import CryptContext

from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get the secret key from the environment
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY not set in .env")


ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

if not ALGORITHM or not ACCESS_TOKEN_EXPIRE_MINUTES:
    raise ValueError("ALGORITHM or ACCESS_TOKEN_EXPIRE_MINUTES is not set")


# ALGORITHM = 'HS256'
# ACCESS_TOKEN_EXPIRE_MINUTES = 480


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed: str) -> bool:
    return pwd_context.verify(plain_password, hashed)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# def decode_token(token: str):
#     try:
#         return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#     except JWTError:
#         return None
def decode_token(token: str):
    try:
        # x=1/0
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    # except JWTError as e:
    #     print("JWT decode error:", str(e))
    #     return None
    except Exception as e:
        print(e)


# print(jwt.decode('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzc0BleGFtcGxlLmNvbSIsImV4cCI6MTc0OTEwNDQ1MX0.v1kxhZInk1dPY4dRRUUCzEy1eOenwj25L5tB7oOQ4ak', SECRET_KEY, algorithms=[ALGORITHM]))

# a=decode_token('eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJPbmxpbmUgSldUIEJ1aWxkZXIiLCJpYXQiOjE3NDkxMjI5NzQsImV4cCI6MTc4MDY1ODk3NCwiYXVkIjoid3d3LmV4YW1wbGUuY29tIiwic3ViIjoianJvY2tldEBleGFtcGxlLmNvbSIsIkdpdmVuTmFtZSI6IkpvaG5ueSIsIlN1cm5hbWUiOiJSb2NrZXQiLCJFbWFpbCI6Impyb2NrZXRAZXhhbXBsZS5jb20iLCJSb2xlIjpbIk1hbmFnZXIiLCJQcm9qZWN0IEFkbWluaXN0cmF0b3IiXX0.GSTx7ss3IhjdGjf1uHYvyXgEPE97Ywf0r_OV310ltu0')
# print

# print(create_access_token({"sub": 'nagesh@gmail.com'}))
