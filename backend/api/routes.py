from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import database, models
from backend import schemas
from backend.api import crud

router = APIRouter()

@router.post("/companies/", response_model=schemas.Company)
def create_company(company: schemas.CompanyCreate, db: Session = Depends(database.get_db)):
    return crud.create_company(db=db, company=company)

@router.get("/companies/", response_model=List[schemas.Company])
def read_companies(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    companies = crud.get_companies(db, skip=skip, limit=limit)
    return companies

@router.get("/companies/{company_id}", response_model=schemas.Company)
def read_company(company_id: int, db: Session = Depends(database.get_db)):
    db_company = crud.get_company(db, company_id=company_id)
    if db_company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    return db_company

@router.get("/companies/{company_id}/esg-scores/", response_model=List[schemas.ESGScore])
def read_esg_scores(company_id: int, db: Session = Depends(database.get_db)):
    scores = crud.get_esg_scores(db, company_id=company_id)
    return scores

@router.get("/news/", response_model=List[schemas.NewsArticle])
def read_news(db: Session = Depends(database.get_mongo_db)):
    articles = []
    for article in db.news_articles.find().limit(20):
        # The _id field from MongoDB is not part of the Pydantic schema, so we exclude it.
        article_data = {k: v for k, v in article.items() if k != '_id'}
        articles.append(schemas.NewsArticle(**article_data))
    return articles

# --- Portfolio Routes ---

@router.post("/portfolios/", response_model=schemas.Portfolio)
def create_portfolio(portfolio: schemas.PortfolioCreate, db: Session = Depends(database.get_db)):
    return crud.create_portfolio(db=db, portfolio=portfolio)

@router.get("/portfolios/", response_model=List[schemas.Portfolio])
def read_portfolios(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    portfolios = crud.get_portfolios(db, skip=skip, limit=limit)
    return portfolios