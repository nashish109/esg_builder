import requests
from config.settings import NEWS_API_KEY
from nlp_engine.analysis import analyze_sentiment, extract_esg_entities, detect_controversy, calculate_esg_score_from_nlp

def get_news_for_company(company_name):
    """
    Fetches news articles for a given company using the NewsAPI.org service.
    Analyzes each article with NLP and computes ESG scores.
    """
    if not NEWS_API_KEY or NEWS_API_KEY == "[Your Key Here]":
        print("Warning: NewsAPI key is not configured. Skipping news fetch.")
        return []

    url = "https://newsapi.org/v2/everything"
    params = {
        "q": company_name,
        "apiKey": NEWS_API_KEY,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 20,
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        articles = data.get("articles", [])

        # Analyze each article with NLP
        analyzed_articles = []
        for article in articles:
            title = article.get('title', '')
            description = article.get('description', '') or ''
            content = title + ' ' + description  # Combine title and description for analysis

            # Perform NLP analysis
            sentiment = analyze_sentiment(content)
            entities = extract_esg_entities(content)
            controversies = detect_controversy(content)
            scores = calculate_esg_score_from_nlp(sentiment, entities, controversies)

            # Add analysis results to article
            analyzed_article = article.copy()
            analyzed_article['nlp_analysis'] = {
                'sentiment': sentiment,
                'entities': entities,
                'controversies': controversies,
                'scores': scores
            }
            analyzed_articles.append(analyzed_article)

        return analyzed_articles

    except requests.exceptions.RequestException as e:
        print(f"Error fetching news for {company_name}: {e}")
        return []

if __name__ == '__main__':
    # Example usage:
    company = "Apple Inc."
    articles = get_news_for_company(company)

    if articles:
        print(f"Latest news for {company}:")
        for i, article in enumerate(articles, 1):
            print(f"{i}. {article['title']}")
    else:
        print(f"Could not retrieve news for {company}.")