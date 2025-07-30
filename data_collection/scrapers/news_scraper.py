import requests
from config.settings import NEWS_API_KEY

def get_news_for_company(company_name):
    """
    Fetches news articles for a given company using the NewsAPI.org service.
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
        return data.get("articles", [])

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