def calculate_combined_esg_score(base_rating, sentiment_scores, weights={"base": 0.7, "nlp": 0.3}):
    """
    Calculates a combined ESG score from a base rating and NLP sentiment scores.
    
    :param base_rating: The existing ESG rating (e.g., from a provider like MSCI).
    :param sentiment_scores: A list of sentiment scores from the NLP engine.
    :param weights: A dictionary specifying the weight of the base rating and NLP scores.
    :return: A combined ESG score.
    """
    if not sentiment_scores:
        return base_rating
        
    # Normalize sentiment scores (assuming they are between -1 and 1)
    # A simple average is used here. More complex methods can be implemented.
    avg_sentiment_score = sum(score['score'] if score['label'] == 'POSITIVE' else -score['score'] for score in sentiment_scores) / len(sentiment_scores)
    
    # For simplicity, let's scale the sentiment score to be on a similar scale to the base_rating (e.g., 0-100)
    # This is a placeholder and should be refined based on the actual rating scale.
    nlp_score_contribution = avg_sentiment_score * 50 + 50 # Scale from [-1, 1] to [0, 100]
    
    # Calculate the combined score
    combined_score = (weights["base"] * base_rating) + (weights["nlp"] * nlp_score_contribution)
    
    return round(combined_score, 2)

if __name__ == '__main__':
    # Example usage:
    base_esg_rating = 75  # Example base rating
    
    # Example sentiment scores from news articles
    sentiments = [
        {'label': 'POSITIVE', 'score': 0.9},
        {'label': 'NEGATIVE', 'score': 0.6},
        {'label': 'POSITIVE', 'score': 0.8},
    ]
    
    final_score = calculate_combined_esg_score(base_esg_rating, sentiments)
    
    print(f"Base ESG Rating: {base_esg_rating}")
    print(f"Combined ESG Score: {final_score}")

def normalize_esg_scores_by_sector(companies):
    """
    Normalizes ESG scores for a list of companies based on their sector.
    Uses z-score normalization.

    :param companies: A list of dictionaries, where each dictionary represents a company
                      and must contain 'id', 'sector', and 'total_score' keys.
    :return: The list of companies with an added 'normalized_score' key.
    """
    if not companies:
        return []

    # Group companies by sector
    sectors = {}
    for company in companies:
        sector = company.get("sector")
        if sector not in sectors:
            sectors[sector] = []
        sectors[sector].append(company)

    # Calculate z-scores for each sector
    for sector, companies_in_sector in sectors.items():
        scores = [c['total_score'] for c in companies_in_sector]
        
        if len(scores) > 1:
            mean_score = sum(scores) / len(scores)
            std_dev = (sum([(s - mean_score) ** 2 for s in scores]) / len(scores)) ** 0.5
        else:
            mean_score = scores[0] if scores else 0
            std_dev = 0

        for company in companies_in_sector:
            if std_dev > 0:
                company['normalized_score'] = (company['total_score'] - mean_score) / std_dev
            else:
                company['normalized_score'] = 0 # Or some other default for single-company sectors

    # Flatten the list of companies
    normalized_companies = [company for companies_in_sector in sectors.values() for company in companies_in_sector]
    
    return normalized_companies

if __name__ == '__main__':
    # ... (previous example usage)

    # Example for normalization
    sample_companies = [
        {'id': 1, 'sector': 'Technology', 'total_score': 85},
        {'id': 2, 'sector': 'Technology', 'total_score': 90},
        {'id': 3, 'sector': 'Technology', 'total_score': 80},
        {'id': 4, 'sector': 'Financials', 'total_score': 70},
        {'id': 5, 'sector': 'Financials', 'total_score': 75},
    ]

    normalized_data = normalize_esg_scores_by_sector(sample_companies)
    print("\nNormalized ESG Scores:")
    for company in normalized_data:
        print(f"  Company {company['id']} ({company['sector']}): Original Score = {company['total_score']}, Normalized Score = {company['normalized_score']:.2f}")

def calculate_weighted_esg_score(e_score, s_score, g_score, weights={"E": 0.4, "S": 0.3, "G": 0.3}):
    """
    Calculates a final ESG score based on user-defined weights for E, S, and G components.

    :param e_score: The environmental score.
    :param s_score: The social score.
    :param g_score: The governance score.
    :param weights: A dictionary with weights for 'E', 'S', and 'G'.
    :return: The final weighted ESG score.
    """
    if sum(weights.values()) != 1.0:
        raise ValueError("The sum of weights must be 1.0")

    weighted_score = (e_score * weights["E"]) + (s_score * weights["S"]) + (g_score * weights["G"])
    
    return round(weighted_score, 2)

if __name__ == '__main__':
    # ... (previous example usage)

    # Example for weighted score calculation
    environmental = 80
    social = 70
    governance = 90
    
    # Default weights
    final_weighted_score = calculate_weighted_esg_score(environmental, social, governance)
    print(f"\nDefault Weighted ESG Score: {final_weighted_score}")
    
    # Custom weights (e.g., focus on Social)
    custom_weights = {"E": 0.2, "S": 0.6, "G": 0.2}
    custom_weighted_score = calculate_weighted_esg_score(environmental, social, governance, weights=custom_weights)
    print(f"Custom Weighted ESG Score (Social Focus): {custom_weighted_score}")