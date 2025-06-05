from datetime import datetime, timedelta
from jose import jwt, JWTError
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
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError as e:
        print("JWT decode error:", str(e))
        return None


# print(jwt.decode('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzc0BleGFtcGxlLmNvbSIsImV4cCI6MTc0OTEwNDQ1MX0.v1kxhZInk1dPY4dRRUUCzEy1eOenwj25L5tB7oOQ4ak', SECRET_KEY, algorithms=[ALGORITHM]))