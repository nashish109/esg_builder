from apscheduler.schedulers.background import BackgroundScheduler
from data_collection.scrapers.news_scraper import get_news_for_company
from data_collection.utils import save_articles_to_json
from backend.services.scoring_service import calculate_dynamic_esg_score
from database.database import SessionLocal
from database.models import ESGScore, Company
import json
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"

def get_companies():
    """
    Gets companies from the companies.json file.
    Returns list of dicts with id, name, ticker.
    """
    try:
        with open(DATA_DIR / "companies.json", "r") as f:
            companies = json.load(f)
        return companies
    except Exception as e:
        print(f"Error loading companies: {e}")
        return []

def get_company_names():
    """
    Gets company names from the companies.json file.
    """
    companies = get_companies()
    return [c["name"] for c in companies]

def update_esg_scores():
    """
    Updates ESG scores for all companies using NLP analysis.
    """
    print("Starting ESG score update cycle...")
    companies = get_companies()
    print(f"Found {len(companies)} companies to process.")

    if not companies:
        print("No companies found. Skipping score update.")
        return

    db = SessionLocal()
    try:
        for company_data in companies:
            company_id = company_data["id"]
            ticker = company_data["ticker"]
            name = company_data["name"]

            print(f"Calculating NLP-based ESG scores for: {name} ({ticker})")
            scores = calculate_dynamic_esg_score(ticker, name)

            if scores:
                # Create new ESG score record
                esg_score = ESGScore(
                    company_id=company_id,
                    environmental_score=scores["environmental_score"],
                    social_score=scores["social_score"],
                    governance_score=scores["governance_score"],
                    total_score=scores["total_score"],
                    rating_date=scores["rating_date"],
                    source=scores["source"]
                )
                db.add(esg_score)
                print(f"Updated scores for {name}: E={scores['environmental_score']}, S={scores['social_score']}, G={scores['governance_score']}, Total={scores['total_score']}")
            else:
                print(f"Could not calculate scores for {name}")

        db.commit()
        print("ESG score update cycle completed.")
    except Exception as e:
        print(f"Error updating ESG scores: {e}")
        db.rollback()
    finally:
        db.close()

def fetch_and_store_news():
    """
    Fetches news for all companies and stores the articles in news.json.
    Also updates ESG scores based on new data.
    """
    print("Starting news fetch and score update cycle...")
    company_names = get_company_names()
    print(f"Found {len(company_names)} companies to process: {company_names}")
    if not company_names:
        print("No companies found. Skipping news fetch.")
        return

    for company_name in company_names:
        print(f"Fetching news for: {company_name}")
        articles = get_news_for_company(company_name)
        print(f"Found {len(articles)} articles for {company_name}.")
        if articles:
            save_articles_to_json(articles, company_name)

    # Update ESG scores after fetching news
    update_esg_scores()
    print("Finished news fetch and score update cycle.")

def start_scheduler():
    """
    Starts the scheduler to fetch news every hour.
    """
    scheduler = BackgroundScheduler()
    # Run the job once on startup
    scheduler.add_job(fetch_and_store_news, 'date')
    # Then run it every hour
    scheduler.add_job(fetch_and_store_news, 'interval', hours=1)
    scheduler.start()
    print("Scheduler started. News will be fetched on startup and then every hour.")