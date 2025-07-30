import sys
import os
from sqlalchemy.orm import sessionmaker

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.database import engine
from database.models import Portfolio

def verify_portfolio_data():
    """Connects to the database and prints portfolio data."""
    Session = sessionmaker(bind=engine)
    session = Session()

    print("--- Verifying Portfolios in Database ---")
    portfolios = session.query(Portfolio).all()

    if not portfolios:
        print("!!! No portfolios found in the database. !!!")
    else:
        print(f"Found {len(portfolios)} portfolios:")
        for p in portfolios:
            company_names = [c.name for c in p.companies]
            print(f"  - Portfolio ID: {p.id}, Name: {p.name}, Companies: {len(company_names)}")

    session.close()

if __name__ == "__main__":
    verify_portfolio_data()