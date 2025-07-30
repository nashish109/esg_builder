-- Create a table to store company information
CREATE TABLE companies (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    ticker VARCHAR(20) UNIQUE,
    sector VARCHAR(100),
    region VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create a table to store ESG scores
CREATE TABLE esg_scores (
    id SERIAL PRIMARY KEY,
    company_id INTEGER REFERENCES companies(id),
    environmental_score NUMERIC(5, 2),
    social_score NUMERIC(5, 2),
    governance_score NUMERIC(5, 2),
    total_score NUMERIC(5, 2),
    rating_date DATE NOT NULL,
    source VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create a table for financial data
CREATE TABLE financial_data (
    id SERIAL PRIMARY KEY,
    company_id INTEGER REFERENCES companies(id),
    pe_ratio NUMERIC(10, 2),
    roe NUMERIC(5, 2),
    market_cap BIGINT,
    data_date DATE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create a table for user-defined portfolios
CREATE TABLE portfolios (
    id SERIAL PRIMARY KEY,
    user_id INTEGER, -- Or a reference to a users table
    name VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create a join table for portfolios and companies
CREATE TABLE portfolio_companies (
    portfolio_id INTEGER REFERENCES portfolios(id),
    company_id INTEGER REFERENCES companies(id),
    PRIMARY KEY (portfolio_id, company_id)
);