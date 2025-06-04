from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import getpass

# Get your macOS username
user = getpass.getuser()

# Database URL: No password, connect as local user
DATABASE_URL = f"postgresql://{user}@localhost/nagesh"


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()
