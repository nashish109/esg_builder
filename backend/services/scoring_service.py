from data_collection.scrapers.reports_scraper import scrape_esg_reports
from data_collection.scrapers.news_scraper import get_news_for_company
from datetime import datetime

def calculate_dynamic_esg_score(company_ticker, company_name):
    """
    Calculates dynamic ESG scores for a company based on NLP analysis of reports and news.

    Args:
        company_ticker (str): Company ticker symbol
        company_name (str): Company name for news search

    Returns:
        dict: ESG scores with individual pillar scores and total score
    """
    scores_list = []

    # Get report analysis
    report_data = scrape_esg_reports(company_ticker)
    if report_data and 'scores' in report_data:
        scores_list.append(report_data['scores'])

    # Get news analysis
    news_articles = get_news_for_company(company_name)
    for article in news_articles:
        if 'nlp_analysis' in article and 'scores' in article['nlp_analysis']:
            scores_list.append(article['nlp_analysis']['scores'])

    if not scores_list:
        # Fallback to default scores if no data available
        return {
            "environmental_score": 50.0,
            "social_score": 50.0,
            "governance_score": 50.0,
            "total_score": 50.0,
            "rating_date": datetime.now().date(),
            "source": "NLP Analysis - No Data"
        }

    # Aggregate scores (simple average)
    aggregated_scores = {
        "environmental_score": 0,
        "social_score": 0,
        "governance_score": 0,
        "total_score": 0
    }

    for scores in scores_list:
        aggregated_scores["environmental_score"] += scores.get("environmental_score", 0)
        aggregated_scores["social_score"] += scores.get("social_score", 0)
        aggregated_scores["governance_score"] += scores.get("governance_score", 0)
        aggregated_scores["total_score"] += scores.get("total_score", 0)

    # Calculate averages
    num_scores = len(scores_list)
    for key in aggregated_scores:
        aggregated_scores[key] = round(aggregated_scores[key] / num_scores, 2)

    aggregated_scores["rating_date"] = datetime.now().date()
    aggregated_scores["source"] = "NLP Analysis"

    return aggregated_scores