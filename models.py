from sqlalchemy import Column, Integer, String, Date, Boolean
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    date_of_birth = Column(Date)
    mobile_number = Column(String)
    hashed_password = Column(String)
    is_admin = Column(Boolean, default=False)
    jwt = Column(String, nullable=True)