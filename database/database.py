from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pymongo import MongoClient
from config.settings import SQLALCHEMY_DATABASE_URL, MONGO_URI

# --- Database Setup (now using SQLite) ---
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- MongoDB Setup ---
mongo_client = MongoClient(MONGO_URI)
mongo_db = mongo_client.get_default_database()

def get_mongo_db():
    return mongo_db
