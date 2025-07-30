def filter_companies(companies, filters):
    """
    Filters a list of companies based on user-defined criteria.

    :param companies: A list of company dictionaries.
    :param filters: A dictionary of filters, e.g., {"sector": "Technology", "min_esg": 70}.
    :return: A filtered list of companies.
    """
    if not filters:
        return companies

    filtered_companies = companies

    if "sector" in filters:
        filtered_companies = [c for c in filtered_companies if c.get("sector") == filters["sector"]]
    
    if "region" in filters:
        filtered_companies = [c for c in filtered_companies if c.get("region") == filters["region"]]

    if "min_esg" in filters:
        filtered_companies = [c for c in filtered_companies if c.get("total_score", 0) >= filters["min_esg"]]
        
    if "max_esg" in filters:
        filtered_companies = [c for c in filtered_companies if c.get("total_score", 0) <= filters["max_esg"]]

    return filtered_companies

if __name__ == '__main__':
    # Example usage:
    sample_companies = [
        {'id': 1, 'name': 'TechCorp', 'sector': 'Technology', 'region': 'USA', 'total_score': 85},
        {'id': 2, 'name': 'FinanceInc', 'sector': 'Financials', 'region': 'USA', 'total_score': 75},
        {'id': 3, 'name': 'EcoEnergy', 'sector': 'Energy', 'region': 'EU', 'total_score': 90},
        {'id': 4, 'name': 'HealthCo', 'sector': 'Healthcare', 'region': 'USA', 'total_score': 65},
        {'id': 5, 'name': 'InnovateIO', 'sector': 'Technology', 'region': 'EU', 'total_score': 88},
    ]

    # Filter for Technology companies in the USA with an ESG score of 80 or higher
    user_filters = {"sector": "Technology", "region": "USA", "min_esg": 80}
    
    results = filter_companies(sample_companies, user_filters)
    
    print("Filtered Companies:")
    for company in results:
        print(f"  - {company['name']} (Score: {company['total_score']})")

def rank_companies(companies, weights={"esg": 0.6, "roi": 0.4}):
    """
    Ranks companies based on a weighted combination of their ESG score and a financial metric.

    :param companies: A list of company dictionaries. Each must have 'normalized_score' and a financial metric (e.g., 'roe').
    :param weights: A dictionary specifying the weights for ESG and ROI.
    :return: A sorted list of companies, ranked from best to worst.
    """
    if not companies:
        return []

    for company in companies:
        # For this example, we'll use ROE as the ROI metric.
        # We need to handle cases where financial data might be missing.
        roi_metric = company.get("roe", 0)
        
        # A simple ranking score. This can be made more sophisticated.
        # We assume higher ROE is better.
        company['rank_score'] = (weights["esg"] * company.get("normalized_score", 0)) + (weights["roi"] * roi_metric)

    # Sort companies by the rank_score in descending order
    ranked_companies = sorted(companies, key=lambda c: c.get('rank_score', 0), reverse=True)
    
    return ranked_companies

if __name__ == '__main__':
    # ... (previous example usage)

    # Example for ranking
    sample_companies_for_ranking = [
        {'id': 1, 'name': 'TechCorp', 'normalized_score': 1.5, 'roe': 25},
        {'id': 2, 'name': 'FinanceInc', 'normalized_score': 0.5, 'roe': 15},
        {'id': 5, 'name': 'InnovateIO', 'normalized_score': 1.8, 'roe': 22},
    ]

    ranked_list = rank_companies(sample_companies_for_ranking)
    
    print("\nRanked Companies:")
    for i, company in enumerate(ranked_list, 1):
        print(f"  {i}. {company['name']} (Rank Score: {company['rank_score']:.2f})")

def optimize_portfolio(ranked_companies, num_assets=5):
    """
    Selects the top N companies to form a portfolio.
    This is a placeholder for a more advanced optimization algorithm.

    :param ranked_companies: A list of ranked companies.
    :param num_assets: The number of companies to include in the portfolio.
    :return: A list of companies representing the optimized portfolio.
    """
    return ranked_companies[:num_assets]

if __name__ == '__main__':
    # ... (previous example usage)

    # Example for portfolio optimization
    optimized_portfolio = optimize_portfolio(ranked_list, num_assets=2)
    
    print("\nOptimized Portfolio:")
    for company in optimized_portfolio:
        print(f"  - {company['name']}")