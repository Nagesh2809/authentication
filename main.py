from fastapi import FastAPI, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models, schemas, auth
from fastapi.security import OAuth2PasswordBearer

models.Base.metadata.create_all(bind=engine)

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime

app = FastAPI()

@app.get('/')
def name():
    return f'curd operation is running on port 8000 {datetime.now()}'
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
security = HTTPBearer()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# def get_current_user(token: str = Depends(security), db: Session = Depends(get_db)):
#     payload = auth.decode_token(token)
#     if payload is None:
#         raise HTTPException(status_code=401, detail="Invalid token")
#     user = db.query(models.User).filter(models.User.email == payload.get("sub")).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     return user

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials  # Extract the token string
    payload = auth.decode_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = db.query(models.User).filter(models.User.email == payload.get("sub")).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user




@app.post("/signup", response_model=schemas.ShowUser)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_pwd = auth.hash_password(user.password)
    new_user = models.User(**user.dict(exclude={"password"}), hashed_password=hashed_pwd)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not db_user or not auth.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = auth.create_access_token({"sub": db_user.email})
    return {"access_token": token, "token_type": "bearer"}

@app.put("/user", response_model=schemas.ShowUser)
def update_user(user_update: schemas.UserUpdate, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    current_user.name = user_update.name
    current_user.email = user_update.email
    current_user.date_of_birth = user_update.date_of_birth
    db.commit()
    db.refresh(current_user)
    return current_user

@app.get("/users", response_model=list[schemas.ShowUser])
def list_users(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    return db.query(models.User).all()

@app.get("/me", response_model=schemas.ShowUser)
def get_user_profile(current_user: models.User = Depends(get_current_user)):
    return current_user
