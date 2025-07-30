from pymongo import MongoClient
from config.settings import MONGO_URI

def setup_mongo():
    """
    Connects to MongoDB and creates collections if they don't exist.
    """
    client = MongoClient(MONGO_URI)
    db = client.get_default_database()

    collections = ["news_articles", "company_reports"]

    for collection_name in collections:
        if collection_name not in db.list_collection_names():
            db.create_collection(collection_name)
            print(f"Collection '{collection_name}' created.")
        else:
            print(f"Collection '{collection_name}' already exists.")

if __name__ == "__main__":
    setup_mongo()