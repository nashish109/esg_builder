import requests
import json

API_URL = "http://localhost:8000/api"

def print_step(title):
    print("\n" + "="*30)
    print(f" {title}")
    print("="*30)

def get_all_portfolios():
    """Fetches and prints all portfolios."""
    print("Fetching all portfolios...")
    response = requests.get(f"{API_URL}/portfolios/")
    if response.status_code == 200:
        portfolios = response.json()
        print("Success! Current portfolios:")
        print(json.dumps(portfolios, indent=2))
        return portfolios
    else:
        print(f"Error fetching portfolios: {response.status_code}")
        print(response.text)
        return []

def create_new_portfolio(name, description):
    """Creates a new portfolio and prints the result."""
    print_step(f"Creating new portfolio: '{name}'")
    payload = {"name": name, "description": description}
    response = requests.post(f"{API_URL}/portfolios/", json=payload)
    if response.status_code == 200:
        portfolio = response.json()
        print("Success! Created portfolio:")
        print(json.dumps(portfolio, indent=2))
        return portfolio
    else:
        print(f"Error creating portfolio: {response.status_code}")
        print(response.text)
        return None

if __name__ == "__main__":
    # Step 1: Show the initial state
    print_step("Initial State")
    get_all_portfolios()

    # Step 2: Create a new portfolio
    create_new_portfolio(
        name="Future Innovators",
        description="A collection of forward-thinking tech companies."
    )

    # Step 3: Show the final state
    print_step("Final State")
    get_all_portfolios()

    print("\nTest complete. Please REFRESH your Streamlit dashboard.")
    print("You should now see 'Future Innovators' in the portfolio dropdown.")