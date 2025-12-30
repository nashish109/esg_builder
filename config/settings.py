import os

# Database settings
# Default to SQLite, configurable via environment
SQLALCHEMY_DATABASE_URL = os.environ.get("SQLALCHEMY_DATABASE_URL", "sqlite:///./esg_builder.db")

# PostgreSQL settings (if using PostgreSQL)
POSTGRES_DB = os.environ.get("POSTGRES_DB", "esg_db")
POSTGRES_USER = os.environ.get("POSTGRES_USER", "user")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "password")
POSTGRES_HOST = os.environ.get("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.environ.get("POSTGRES_PORT", "5432")



# News API settings
NEWS_API_KEY = os.environ.get("NEWS_API_KEY", "e5757131ff244f7db5a79d51c458646d")

# Web scraping settings
USER_AGENT = "ESG Builder Scraper/1.0"

# Application Configuration
APP_HOST = os.environ.get("APP_HOST", "0.0.0.0")
APP_PORT = int(os.environ.get("APP_PORT", "8000"))