import json
import sys
import os
from pathlib import Path
from datetime import datetime, timedelta
import random

# Add the dashboard directory to sys.path to import add_company functions
sys.path.append(str(Path(__file__).parent.parent / "dashboard" / "pages"))

from add_company import get_companies, save_company, generate_initial_esg_scores

def test_add_company_and_verify_esg_trends():
    """Test adding a new company programmatically and verify ESG trends data."""
    # Test data for a new company
    test_company = {
        "name": "Test Company Inc.",
        "ticker": "TEST",
        "sector": "Technology",
        "region": "North America"
    }

    # Get initial data
    initial_companies = get_companies()
    initial_esg_scores = []
    data_dir = Path(__file__).parent.parent / "data"
    try:
        with open(data_dir / "esg_scores.json", "r") as f:
            initial_esg_scores = json.load(f)
    except FileNotFoundError:
        initial_esg_scores = []

    # Add the company
    action = save_company(test_company)

    # Verify company was added
    updated_companies = get_companies()
    assert len(updated_companies) == len(initial_companies) + 1, "Company not added"
    added_company = next((c for c in updated_companies if c["name"] == test_company["name"]), None)
    assert added_company is not None, "Added company not found"
    assert added_company["ticker"] == test_company["ticker"], "Ticker mismatch"
    assert added_company["sector"] == test_company["sector"], "Sector mismatch"
    assert added_company["region"] == test_company["region"], "Region mismatch"
    company_id = added_company["id"]

    # Generate initial ESG scores (this would normally be called in save_company for new companies)
    if action == "added":
        generate_initial_esg_scores(company_id)

    # Load updated ESG scores
    with open(data_dir / "esg_scores.json", "r") as f:
        updated_esg_scores = json.load(f)

    # Verify ESG scores were generated
    company_scores = [s for s in updated_esg_scores if s["company_id"] == company_id]
    assert len(company_scores) == 4, f"Expected 4 ESG scores, got {len(company_scores)}"

    # Verify each score has required fields
    for score in company_scores:
        assert "company_id" in score
        assert "rating_date" in score
        assert "environmental_score" in score
        assert "social_score" in score
        assert "governance_score" in score
        assert "total_score" in score
        assert "source" in score
        assert score["source"] == "Generated"

        # Verify scores are in valid range
        for pillar in ["environmental_score", "social_score", "governance_score", "total_score"]:
            assert 0 <= score[pillar] <= 100, f"{pillar} out of range: {score[pillar]}"

    # Verify dates are sequential quarters
    dates = sorted([datetime.strptime(s["rating_date"], "%Y-%m-%d") for s in company_scores])
    for i in range(1, len(dates)):
        diff = (dates[i] - dates[i-1]).days
        assert abs(diff - 90) <= 30, f"Dates not approximately quarterly: {dates[i-1]} to {dates[i]}"

    print("✅ Test passed: Company added successfully and ESG trends data generated correctly.")

    # Cleanup: remove the test company
    updated_companies = [c for c in updated_companies if c["name"] != test_company["name"]]
    with open(data_dir / "companies.json", "w") as f:
        json.dump(updated_companies, f, indent=2)

    # Remove the ESG scores
    updated_esg_scores = [s for s in updated_esg_scores if s["company_id"] != company_id]
    with open(data_dir / "esg_scores.json", "w") as f:
        json.dump(updated_esg_scores, f, indent=2)

if __name__ == "__main__":
    test_add_company_and_verify_esg_trends()