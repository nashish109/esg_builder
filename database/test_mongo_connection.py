import sys
import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config.settings import MONGO_URI

print("Attempting to connect to MongoDB...")
print(f"  URI: {MONGO_URI}")

try:
    # Set a timeout to prevent the script from hanging indefinitely
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    
    # The ismaster command is cheap and does not require auth.
    client.admin.command('ismaster')
    
    print("Successfully connected to the MongoDB server.")
    
    # Check collections
    db = client.get_default_database()
    print(f"Database: '{db.name}'")
    collections = db.list_collection_names()
    print(f"Existing collections: {collections}")

except ConnectionFailure as e:
    print("\n--- MONGODB CONNECTION FAILED ---")
    print(f"Error: {e}")
    print("\nTroubleshooting steps:")
    print("1. Ensure the MongoDB service is running.")
    print("   - On Windows, check for 'MongoDB Server' in 'services.msc'.")
    print("2. Check if a firewall is blocking port 27017.")
    print("3. Verify that MongoDB is configured to accept connections from localhost.")
    print("   - Check your 'mongod.conf' file (usually in the MongoDB installation's 'bin' or 'etc' directory).")
    print("   - Ensure the `net.bindIp` setting includes '127.0.0.1' or is set to '0.0.0.0'.")
    print("4. After any configuration changes, restart the MongoDB service.")

except Exception as e:
    print(f"\nAn unexpected error occurred: {e}")

finally:
    if 'client' in locals():
        client.close()