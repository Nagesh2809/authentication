



# {
#   "name": "dd",
#   "email": "dd@example.com",
#   "date_of_birth": "1000-09-09",
#   "mobile_number": "string",
#   "password": "11111",
#   "is_admin": false
# }


from fastapi import FastAPI, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models, schemas, auth
# from schemas import ShowUser
from fastapi.security import OAuth2PasswordBearer

models.Base.metadata.create_all(bind=engine)

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime

app = FastAPI()

@app.get('/')   # health_check api
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


############################################################################################################################################################################################## 


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials
    print("Received token:", token)
    payload = auth.decode_token(token)
    print("Decoded payload:", payload)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(models.User).filter(models.User.email == payload.get("sub")).first()
    print("User found:", user)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user



############################################################################################################################################################################################## 

def create_access_token(user_email: str):
    return auth.create_access_token({"sub": user_email})
############################################################################################################################################################################################## 

@app.post("/signup", response_model=schemas.ShowUserWithToken)

def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_pwd = auth.hash_password(user.password)
    new_user = models.User(**user.dict(exclude={"password"}), hashed_password=hashed_pwd)
    access_token = create_access_token(user.email)
    try:
        if access_token :
            print(f'Acess token created {access_token}')
            # new_user['jwt'] = access_token  new_user is a SQLAlchemy model instance,
            #  not a dictionary, so you cannot assign like new_user['jwt'] = .... 
            new_user.jwt = access_token

    except Exception as e:
        print(e)


    
    # new_user['jwt']=access_token
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
        
    
    # new_user = new_user.model_dump
    # new_user['acess_token'] = access_token
    return new_user

############################################################################################################################################################################################## 

@app.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if not db_user or not auth.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = auth.create_access_token({"sub": db_user.email})
    
    # Save the token in the user's row
    db_user.jwt = token
    db.commit()
    
    return {"access_token": token, "token_type": "bearer"}

############################################################################################################################################################################################## 


@app.put("/user", response_model=schemas.ShowUser)
def update_user(user_update: schemas.UserUpdate, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    current_user.name = user_update.name
    current_user.email = user_update.email
    current_user.date_of_birth = user_update.date_of_birth
    db.commit()
    db.refresh(current_user)
    return current_user

############################################################################################################################################################################################## 

@app.get("/users", response_model=list[schemas.ShowUser])
def list_users(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    return db.query(models.User).order_by(models.User.name.asc()).all()

@app.get("/me", response_model=schemas.ShowUser)
def get_user_profile(current_user: models.User = Depends(get_current_user)):
    return current_user
