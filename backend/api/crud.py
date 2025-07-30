from sqlalchemy.orm import Session, joinedload
from backend import schemas
from database import models

# --- Company CRUD ---

def get_company(db: Session, company_id: int):
    return db.query(models.Company).filter(models.Company.id == company_id).first()

def get_companies(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Company).offset(skip).limit(limit).all()

def create_company(db: Session, company: schemas.CompanyCreate):
    db_company = models.Company(**company.dict())
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company

# --- ESG Score CRUD ---

def get_esg_scores(db: Session, company_id: int):
    return db.query(models.ESGScore).filter(models.ESGScore.company_id == company_id).order_by(models.ESGScore.rating_date).all()

# --- Portfolio CRUD ---

def get_portfolio(db: Session, portfolio_id: int):
    return db.query(models.Portfolio).filter(models.Portfolio.id == portfolio_id).first()

def get_portfolios(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Portfolio).options(joinedload(models.Portfolio.companies)).offset(skip).limit(limit).all()

def create_portfolio(db: Session, portfolio: schemas.PortfolioCreate):
    db_portfolio = models.Portfolio(**portfolio.dict())
    db.add(db_portfolio)
    db.commit()
    db.refresh(db_portfolio)
    return db_portfolio