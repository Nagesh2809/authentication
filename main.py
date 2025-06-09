



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
