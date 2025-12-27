#!/usr/bin/env python3
"""
Test script for NLP-based ESG scoring integration.
"""

def test_scoring_function():
    """Test the calculate_esg_score_from_nlp function with mock data."""
    try:
        from nlp_engine.analysis import calculate_esg_score_from_nlp

        # Mock sentiment result
        mock_sentiment = {'label': 'positive', 'score': 0.8}

        # Mock entities
        mock_entities = {
            'environmental': ['renewable energy', 'carbon emissions'],
            'social': ['labor practices'],
            'governance': ['board diversity']
        }

        # Mock controversies
        mock_controversies = {
            'environmental': [],
            'social': ['labor strike'],
            'governance': []
        }

        scores = calculate_esg_score_from_nlp(mock_sentiment, mock_entities, mock_controversies)
        print("NLP Scoring Test Results:")
        print(f"Environmental Score: {scores['environmental_score']}")
        print(f"Social Score: {scores['social_score']}")
        print(f"Governance Score: {scores['governance_score']}")
        print(f"Total Score: {scores['total_score']}")
        return True
    except Exception as e:
        print(f"Error testing scoring function: {e}")
        return False

def test_scoring_service():
    """Test the scoring service with mock data."""
    try:
        from backend.services.scoring_service import calculate_dynamic_esg_score

        # Test with a mock company (without actual scraping)
        scores = calculate_dynamic_esg_score("AAPL", "Apple Inc.")
        if scores:
            print("Scoring Service Test Results:")
            print(f"Environmental Score: {scores.get('environmental_score')}")
            print(f"Social Score: {scores.get('social_score')}")
            print(f"Governance Score: {scores.get('governance_score')}")
            print(f"Total Score: {scores.get('total_score')}")
            print(f"Rating Date: {scores.get('rating_date')}")
            print(f"Source: {scores.get('source')}")
            return True
        else:
            print("Scoring service returned no scores")
            return False
    except Exception as e:
        print(f"Error testing scoring service: {e}")
        return False

if __name__ == "__main__":
    print("Testing NLP-ESG Scoring Integration...")

    print("\n1. Testing scoring function:")
    test1 = test_scoring_function()

    print("\n2. Testing scoring service:")
    test2 = test_scoring_service()

    if test1 and test2:
        print("\n✅ All tests passed! NLP-ESG scoring integration is working.")
    else:
        print("\n❌ Some tests failed. Check the errors above.")