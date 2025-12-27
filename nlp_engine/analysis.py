from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import torch

# Load the sentiment analysis model
# Using ProsusAI/finbert for ESG sentiment analysis
sentiment_analyzer = pipeline("sentiment-analysis", model="ProsusAI/finbert")


def analyze_sentiment(text):
    """
    Analyzes the sentiment of a given text using the fine-tuned FinBERT model.
    """
    if not text:
        return None
    
    try:
        result = sentiment_analyzer(text)
        return result[0]
    except Exception as e:
        print(f"Error during sentiment analysis: {e}")
        return None

if __name__ == '__main__':
    # Example usage:
    sample_text = "The company announced a major investment in renewable energy, which is a positive step towards sustainability."
    sentiment = analyze_sentiment(sample_text)
    
    if sentiment:
        print(f"Text: '{sample_text}'")
        print(f"Sentiment: {sentiment['label']} (Score: {sentiment['score']:.4f})")
    else:
        print("Could not analyze sentiment.")
        
    sample_text_2 = "The company is facing scrutiny over its labor practices and supply chain transparency."
    sentiment_2 = analyze_sentiment(sample_text_2)
    
    if sentiment_2:
        print(f"\nText: '{sample_text_2}'")
        print(f"Sentiment: {sentiment_2['label']} (Score: {sentiment_2['score']:.4f})")
    else:
        print("Could not analyze sentiment.")

import spacy

# It's recommended to download the model separately, e.g., python -m spacy download en_core_web_sm
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Downloading spaCy model 'en_core_web_sm'...")
    from spacy.cli import download
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# Define ESG-related keywords
ESG_KEYWORDS = {
    "environmental": ["carbon emissions", "renewable energy", "waste management", "pollution", "sustainability"],
    "social": ["labor practices", "employee relations", "diversity", "human rights", "community relations"],
    "governance": ["board diversity", "executive compensation", "shareholder rights", "business ethics", "transparency"]
}

def extract_esg_entities(text):
    """
    Extracts ESG-related entities from a given text.
    """
    if not text:
        return {}
        
    doc = nlp(text.lower())
    
    found_entities = {"environmental": [], "social": [], "governance": []}
    
    for category, keywords in ESG_KEYWORDS.items():
        for keyword in keywords:
            if keyword in doc.text:
                found_entities[category].append(keyword)
                
    # Leverage spaCy's NER with custom patterns for more advanced entity extraction
    from spacy.matcher import Matcher
    matcher = Matcher(nlp.vocab)

    # Define patterns for specific ESG events
    patterns = {
        "CARBON_EMISSIONS": [[{"LOWER": "carbon"}, {"LOWER": "emissions"}]],
        "RENEWABLE_ENERGY": [[{"LOWER": "renewable"}, {"LOWER": "energy"}]],
        "LABOR_PRACTICES": [[{"LOWER": "labor"}, {"LOWER": "practices"}]],
    }

    for event, pattern in patterns.items():
        matcher.add(event, pattern)

    matches = matcher(doc)
    for match_id, start, end in matches:
        span = doc[start:end]
        # You can map the event to a category here
        # For simplicity, we'll just add the event text
        # A more robust solution would map the event to E, S, or G
        if "carbon" in span.text or "renewable" in span.text:
            if span.text not in found_entities["environmental"]:
                found_entities["environmental"].append(span.text)
        elif "labor" in span.text:
            if span.text not in found_entities["social"]:
                found_entities["social"].append(span.text)

    return found_entities

if __name__ == '__main__':
    # ... (previous example usage)

    esg_text = "The company is improving its waste management but faces challenges with board diversity and labor practices."
    entities = extract_esg_entities(esg_text)
    
    print(f"\nText: '{esg_text}'")
    print("Extracted ESG Entities:")
    for category, items in entities.items():
        if items:
            print(f"  {category.capitalize()}: {', '.join(items)}")

def classify_esg_category(text):
    """
    Classifies a text into E, S, or G categories based on keyword matching.
    """
    if not text:
        return "Unclassified"
        
    scores = {"environmental": 0, "social": 0, "governance": 0}
    
    doc = nlp(text.lower())
    
    for category, keywords in ESG_KEYWORDS.items():
        for keyword in keywords:
            if keyword in doc.text:
                scores[category] += 1
                
    # Determine the category with the highest score
    if all(score == 0 for score in scores.values()):
        return "Unclassified"
        
    primary_category = max(scores, key=scores.get)
    
    return primary_category.capitalize()

if __name__ == '__main__':
    # ... (previous example usage)

    classification = classify_esg_category(esg_text)
    print(f"\nPrimary ESG Category: {classification}")
CONTROVERSY_KEYWORDS = {
    "environmental": ["greenwashing", "environmental disaster", "pollution scandal"],
    "social": ["labor strike", "child labor", "workplace safety violation"],
    "governance": ["corruption", "bribery", "insider trading", "accounting fraud"]
}

def detect_controversy(text):
    """
    Detects potential ESG controversies in a given text.
    """
    text = text.lower()
    found_controversies = {"environmental": [], "social": [], "governance": []}

    for category, keywords in CONTROVERSY_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text:
                found_controversies[category].append(keyword)
    
    return found_controversies

def calculate_esg_score_from_nlp(sentiment_result, entities, controversies):
    """
    Calculates ESG scores based on NLP analysis results.
    Returns a dictionary with environmental, social, governance, and total scores.
    """
    base_score = 50  # Neutral base score

    # Initialize category scores
    scores = {
        "environmental": base_score,
        "social": base_score,
        "governance": base_score
    }

    # Adjust scores based on sentiment
    if sentiment_result:
        sentiment_label = sentiment_result.get('label', '').lower()
        sentiment_score = sentiment_result.get('score', 0)

        if sentiment_label == 'positive':
            # Boost all categories based on sentiment strength
            boost = sentiment_score * 20  # Max 20 points
            for category in scores:
                scores[category] += boost
        elif sentiment_label == 'negative':
            # Reduce all categories based on sentiment strength
            reduction = sentiment_score * 20  # Max 20 points reduction
            for category in scores:
                scores[category] -= reduction

    # Adjust scores based on ESG entities found
    entity_points = 5  # Points per entity found

    for category, entity_list in entities.items():
        if category in scores:
            scores[category] += len(entity_list) * entity_points

    # Adjust scores based on controversies detected
    controversy_penalty = 10  # Points deducted per controversy

    for category, controversy_list in controversies.items():
        if category in scores:
            scores[category] -= len(controversy_list) * controversy_penalty

    # Ensure scores are within 0-100 range
    for category in scores:
        scores[category] = max(0, min(100, scores[category]))

    # Calculate total score as average of the three pillars
    total_score = round((scores["environmental"] + scores["social"] + scores["governance"]) / 3, 2)

    return {
        "environmental_score": round(scores["environmental"], 2),
        "social_score": round(scores["social"], 2),
        "governance_score": round(scores["governance"], 2),
        "total_score": total_score
    }
