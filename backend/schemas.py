from pydantic import BaseModel
from datetime import date, datetime
from typing import List, Optional

class CompanyBase(BaseModel):
    name: str
    ticker: Optional[str] = None
    sector: Optional[str] = None
    region: Optional[str] = None

class CompanyCreate(CompanyBase):
    pass

class Company(CompanyBase):
    id: int

    class Config:
        orm_mode = True

class ESGScoreBase(BaseModel):
    environmental_score: Optional[float] = None
    social_score: Optional[float] = None
    governance_score: Optional[float] = None
    total_score: Optional[float] = None
    rating_date: date
    source: Optional[str] = None

class ESGScoreCreate(ESGScoreBase):
    company_id: int

class ESGScore(ESGScoreBase):
    id: int
    company_id: int

    class Config:
        orm_mode = True

class NewsArticle(BaseModel):
    title: str
    url: str
    source: str
    published_at: datetime

class PortfolioBase(BaseModel):
    name: str
    description: Optional[str] = None

class PortfolioCreate(PortfolioBase):
    pass

class Portfolio(PortfolioBase):
    id: int
    companies: List[Company] = []

    class Config:
        orm_mode = True