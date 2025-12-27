import os

# Database settings
# Using SQLite to simplify setup and bypass connection issues.
SQLALCHEMY_DATABASE_URL = "sqlite:///./esg_builder.db"

# Original PostgreSQL settings (commented out)
# POSTGRES_DB = os.environ.get("POSTGRES_DB", "esg_db")
# POSTGRES_USER = os.environ.get("POSTGRES_USER", "user")
# POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "password")
# POSTGRES_HOST = os.environ.get("POSTGRES_HOST", "localhost")
# POSTGRES_PORT = os.environ.get("POSTGRES_PORT", "5432")



# News API settings
NEWS_API_KEY = os.environ.get("NEWS_API_KEY", "e5757131ff244f7db5a79d51c458646d")

# Web scraping settings
USER_AGENT = "ESG Builder Scraper/1.0"