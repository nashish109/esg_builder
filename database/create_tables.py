import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.database import Base, engine
from database.models import Company, ESGScore, Portfolio

print("Creating database and tables for SQLite...")
Base.metadata.create_all(bind=engine)
print("Database and tables created successfully.")