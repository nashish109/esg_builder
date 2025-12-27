import json
from pathlib import Path
from datetime import datetime

DATA_DIR = Path(__file__).parent.parent / "data"

def save_articles_to_json(articles, company_name):
    """
    Saves a list of news articles to the news.json file,
    preserving the original structure from the NewsAPI.
    """
    if not articles:
        return

    # Load existing news
    news_file = DATA_DIR / "news.json"
    try:
        with open(news_file, "r") as f:
            existing_news = json.load(f)
    except FileNotFoundError:
        existing_news = []

    # Add new articles with source and published_at format
    for article in articles:
        # Skip if already exists (by title)
        if any(n["title"] == article.get("title") for n in existing_news):
            continue

        news_item = {
            "source": article.get("source", {}).get("name", "NewsAPI"),
            "published_at": article.get("publishedAt", datetime.now().isoformat()),
            "title": article.get("title", "No title")
        }
        existing_news.append(news_item)

    # Save back to file
    with open(news_file, "w") as f:
        json.dump(existing_news, f, indent=2)

    print(f"Saved {len(articles)} articles for {company_name} to news.json.")