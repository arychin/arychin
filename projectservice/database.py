from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
from urllib.parse import quote_plus

from projectservice.config import settings


# Load environment variables
load_dotenv()

db_user = settings.db_user
db_pwd = settings.db_pwd
db_host = settings.db_host
db_name = settings.db_name
db_port = settings.db_port

DATABASE_URL = f"postgresql://{db_user}:{db_pwd}@{db_host}:{db_port}/{db_name}"


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autoflush=False, bind=engine)
Base = declarative_base()

# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


