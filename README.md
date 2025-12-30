# ESG Builder

ESG Builder is a comprehensive platform designed for sustainable investing by leveraging ESG (Environmental, Social, Governance) criteria. It integrates data collection, natural language processing (NLP) for ESG analysis, scoring mechanisms, and portfolio recommendation engines to help users make informed investment decisions.

### Key Features and Functionalities:
- **Data Collection**: Automated web scraping from ESG-related sources (news and reports) using custom scrapers. Includes a scheduler for periodic data updates and utility functions for data processing and storage.
- **NLP Engine**: Analyzes textual data from scraped sources to assess ESG performance, utilizing advanced NLP models (e.g., transformers and spaCy) for sentiment analysis and scoring.
- **ESG Scoring Service**: Calculates and tracks ESG scores for companies based on collected data, storing historical trends for comparison.
- **Portfolio Recommendations**: An intelligent recommendation system that generates personalized portfolios based on user-defined ESG filters, criteria, and preferences. Includes API endpoints for fetching recommendations.
- **Interactive Dashboard**: A Streamlit-based web interface for visualizing ESG trends over time, comparing portfolio performance, and displaying news alerts. Features include:
  - Company ESG trend charts.
  - Portfolio comparison bar charts.
  - Pages for adding/deleting companies, setting recommendation filters, and viewing results.
- **Backend API**: Built with FastAPI, providing RESTful endpoints for recommendations, health checks, and data access. Supports CORS for frontend integration.
- **Database Integration**: Uses PostgreSQL for structured data storage, with setup scripts, models, and connection testing.
- **Testing Suite**: Comprehensive unit tests covering backend services, data collection, NLP scoring, dashboard components, and API endpoints.
- **Deployment Support**: Includes Docker configuration, environment setup, and deployment guides for containerized deployment.

The platform combines real-time data ingestion with AI-driven insights to empower users in building and managing environmentally and socially responsible investment portfolios. It currently uses local JSON data files for quick setup but is architected to scale with database integration.
