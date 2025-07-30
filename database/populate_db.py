import datetime
import sys
import os
import random
from pymongo import MongoClient
from sqlalchemy.orm import sessionmaker

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.database import engine
from database.models import Company, ESGScore, Portfolio, portfolio_companies
from config.settings import MONGO_URI

# --- SQL Data ---
def populate_sql_data():
    Session = sessionmaker(bind=engine)
    session = Session()

    # Clear existing data
    session.execute(portfolio_companies.delete())
    session.query(ESGScore).delete()
    session.query(Portfolio).delete()
    session.query(Company).delete()

    # Create sample companies
    companies_data = [
        {"id": 1, "name": "Apple Inc.", "ticker": "AAPL", "base_score": 75},
        {"id": 2, "name": "Microsoft Corp.", "ticker": "MSFT", "base_score": 82},
        {"id": 3, "name": "Alphabet Inc.", "ticker": "GOOGL", "base_score": 65},
        {"id": 4, "name": "Procter & Gamble Co.", "ticker": "PG", "base_score": 85},
        {"id": 5, "name": "NextEra Energy, Inc.", "ticker": "NEE", "base_score": 90},
    ]
    
    companies = [Company(id=c["id"], name=c["name"], ticker=c["ticker"]) for c in companies_data]
    session.add_all(companies)
    session.commit()

    # Create sample ESG scores with more history
    scores = []
    for company_data in companies_data:
        base_score = company_data["base_score"]
        for i in range(12): # Generate 12 months of data
            date = datetime.date(2023, 1, 1) + datetime.timedelta(days=i*30)
            score_fluctuation = random.uniform(-2.5, 2.5)
            score = base_score + score_fluctuation
            scores.append(
                ESGScore(company_id=company_data["id"], total_score=round(score, 2), rating_date=date)
            )
    
    session.add_all(scores)
    session.commit()

    # Create sample portfolios
    p1 = Portfolio(name="Tech Giants", description="A portfolio of leading technology companies.")
    p2 = Portfolio(name="Sustainable Innovators", description="A portfolio focused on innovative and sustainable companies.")
    p3 = Portfolio(name="Consumer Staples", description="A portfolio of well-established consumer goods companies.")
    p4 = Portfolio(name="Clean Energy Leaders", description="A portfolio of companies leading the transition to clean energy.")
    p5 = Portfolio(name="Mixed ESG Focus", description="A diversified portfolio with a focus on ESG.")

    # Add companies to portfolios
    p1.companies.extend([companies[0], companies[1], companies[2]])
    p2.companies.extend([companies[0], companies[4]])
    p3.companies.append(companies[3])
    p4.companies.append(companies[4])
    p5.companies.extend([companies[1], companies[3], companies[4]])

    session.add_all([p1, p2, p3, p4, p5])
    session.commit()

    session.close()
    print("Successfully populated SQL database with sample data.")

# --- MongoDB Data ---
def populate_mongo_data():
    client = MongoClient(MONGO_URI)
    db = client.get_default_database()
    
    # Clear existing data
    db.news_articles.delete_many({})

    # Create sample news articles
    articles = [
        {"source": "TechCrunch", "title": "Apple announces new accessibility features.", "url": "https://example.com/apple-accessibility", "company_id": 1, "published_at": datetime.datetime.fromisoformat("2023-10-01T12:00:00Z")},
        {"source": "Reuters", "title": "Microsoft pledges to be carbon negative by 2030.", "url": "https://example.com/microsoft-carbon-negative", "company_id": 2, "published_at": datetime.datetime.fromisoformat("2023-09-28T10:00:00Z")},
        {"source": "The Verge", "title": "Google faces new antitrust lawsuit.", "url": "https://example.com/google-antitrust", "company_id": 3, "published_at": datetime.datetime.fromisoformat("2023-09-25T15:00:00Z")},
        {"source": "Wall Street Journal", "title": "Procter & Gamble to invest in sustainable packaging.", "url": "https://example.com/pg-packaging", "company_id": 4, "published_at": datetime.datetime.fromisoformat("2023-09-22T11:00:00Z")},
        {"source": "Bloomberg", "title": "NextEra Energy expands wind power capacity.", "url": "https://example.com/nextera-wind", "company_id": 5, "published_at": datetime.datetime.fromisoformat("2023-09-20T09:00:00Z")},
    ]
    
    if articles:
        db.news_articles.insert_many(articles)
        print(f"Successfully populated MongoDB with {len(articles)} sample news articles.")
    else:
        print("No news articles were populated.")
        
    client.close()


if __name__ == "__main__":
    populate_sql_data()
    populate_mongo_data()