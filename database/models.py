from sqlalchemy import Column, Integer, String, Numeric, Date, ForeignKey, TIMESTAMP, Table
from sqlalchemy.orm import relationship
from .database import Base

# Association Table for the many-to-many relationship between Portfolios and Companies
portfolio_companies = Table('portfolio_companies', Base.metadata,
    Column('portfolio_id', Integer, ForeignKey('portfolios.id'), primary_key=True),
    Column('company_id', Integer, ForeignKey('companies.id'), primary_key=True)
)

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    ticker = Column(String, unique=True)
    sector = Column(String)
    region = Column(String)
    created_at = Column(TIMESTAMP(timezone=True))

    esg_scores = relationship("ESGScore", back_populates="company")
    financial_data = relationship("FinancialData", back_populates="company")
    portfolios = relationship("Portfolio", secondary=portfolio_companies, back_populates="companies")

class ESGScore(Base):
    __tablename__ = "esg_scores"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"))
    environmental_score = Column(Numeric(5, 2))
    social_score = Column(Numeric(5, 2))
    governance_score = Column(Numeric(5, 2))
    total_score = Column(Numeric(5, 2))
    rating_date = Column(Date, nullable=False)
    source = Column(String)
    created_at = Column(TIMESTAMP(timezone=True))

    company = relationship("Company", back_populates="esg_scores")

class FinancialData(Base):
    __tablename__ = "financial_data"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"))
    pe_ratio = Column(Numeric(10, 2))
    roe = Column(Numeric(10, 2))
    market_cap = Column(Integer)
    data_date = Column(Date, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True))

    company = relationship("Company", back_populates="financial_data")

class Portfolio(Base):
    __tablename__ = "portfolios"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String)

    companies = relationship("Company", secondary=portfolio_companies, back_populates="portfolios")