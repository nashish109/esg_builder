#!/usr/bin/env python3
#!/usr/bin/env python3
"""
Test script for the Portfolio Recommendation API
Tests the complete recommendation workflow.
"""

import requests
import json
import time

API_BASE_URL = "http://localhost:8000"

def test_api_health():
    """Test API health endpoint."""
    print("Testing API health...")
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ API is healthy")
            return True
        else:
            print(f"❌ API health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Could not connect to API: {e}")
        return False

def test_available_sectors():
    """Test getting available sectors."""
    print("\nTesting available sectors...")
    try:
        response = requests.get(f"{API_BASE_URL}/api/recommendations/sectors", timeout=5)
        if response.status_code == 200:
            sectors = response.json()["sectors"]
            print(f"✅ Available sectors: {sectors}")
            return sectors
        else:
            print(f"❌ Failed to get sectors: {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ Error getting sectors: {e}")
        return []

def test_company_count():
    """Test company count with filters."""
    print("\nTesting company count...")
    try:
        params = {"min_total_score": 70}
        response = requests.get(
            f"{API_BASE_URL}/api/recommendations/companies/count",
            params=params,
            timeout=5
        )
        if response.status_code == 200:
            count = response.json()["count"]
            print(f"✅ Companies with ESG >= 70: {count}")
            return count
        else:
            print(f"❌ Failed to get company count: {response.status_code}")
            return 0
    except Exception as e:
        print(f"❌ Error getting company count: {e}")
        return 0

def test_generate_recommendation():
    """Test generating a portfolio recommendation."""
    print("\nTesting portfolio recommendation generation...")

    # Sample recommendation request
    request_data = {
        "filters": {
            "min_total_score": 60.0,
            "min_environmental_score": 50.0,
            "min_social_score": 50.0,
            "min_governance_score": 50.0,
            "preferred_sectors": [],
            "excluded_sectors": [],
            "preferred_regions": [],
            "excluded_regions": []
        },
        "risk_preference": "moderate",
        "sector_targets": {
            "Technology": 0.4,
            "Healthcare": 0.3,
            "Financials": 0.3
        },
        "portfolio_size": 8
    }

    try:
        response = requests.post(
            f"{API_BASE_URL}/api/recommendations/generate",
            json=request_data,
            timeout=30
        )

        if response.status_code == 200:
            recommendation = response.json()
            print("✅ Recommendation generated successfully!")
            print(f"   - ID: {recommendation['id']}")
            print(f"   - Companies: {len(recommendation['companies'])}")
            print(f"   - Average ESG: {recommendation['esg_scores']['average_total']:.1f}")
            print(f"   - Risk preference: {recommendation['risk_preference']}")
            print(f"   - Risk assessment: {recommendation['risk_assessment']}")

            # Show company details
            print("   - Selected companies:")
            for company in recommendation['companies']:
                print(f"     • {company['name']} ({company['ticker']}) - ESG: {company['esg_score']:.1f}")

            return recommendation
        else:
            print(f"❌ Failed to generate recommendation: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error generating recommendation: {e}")
        return None

def main():
    """Run all tests."""
    print("🚀 Testing Portfolio Recommendation API")
    print("=" * 50)

    # Test API health
    if not test_api_health():
        print("❌ API is not available. Make sure the server is running.")
        return

    # Test basic endpoints
    sectors = test_available_sectors()
    count = test_company_count()

    if count == 0:
        print("⚠️ No companies meet the minimum ESG criteria. Tests may fail.")

    # Test recommendation generation
    recommendation = test_generate_recommendation()

    if recommendation:
        print("\n🎉 All tests passed!")
        print("\n💡 Next steps:")
        print("   1. Start the Streamlit dashboard: streamlit run dashboard/app.py")
        print("   2. Navigate to 'Portfolio Recommendations' in the sidebar")
        print("   3. Set your ESG filters and generate a personalized portfolio!")
    else:
        print("\n❌ Some tests failed. Check the API implementation.")

if __name__ == "__main__":
    main()