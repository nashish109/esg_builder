import requests
import pdfplumber
from bs4 import BeautifulSoup
import re
from config.settings import USER_AGENT
from nlp_engine.analysis import extract_esg_entities, classify_esg_category, detect_controversy, analyze_sentiment, calculate_esg_score_from_nlp

def download_pdf(url, filename):
    """
    Downloads a PDF from the given URL and saves it to the specified filename.
    """
    headers = {'User-Agent': USER_AGENT}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    with open(filename, 'wb') as f:
        f.write(response.content)
    return filename

def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF file using pdfplumber.
    """
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

def find_annual_report_url(company_ticker):
    """
    Attempts to find the URL of the latest annual report for a company.
    This is a simplified implementation; in practice, you might use APIs or more sophisticated scraping.
    For US companies, use EDGAR search.
    """
    # Example for EDGAR: https://www.sec.gov/edgar/searchedgar/companies.htm
    # But for simplicity, search for company investor page
    search_url = f"https://www.google.com/search?q={company_ticker}+annual+report+pdf"
    headers = {'User-Agent': USER_AGENT}
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    # Find first PDF link
    for link in soup.find_all('a', href=True):
        if link['href'].endswith('.pdf') and 'annual' in link['href'].lower():
            return link['href']
    return None

def scrape_esg_reports(company_ticker):
    """
    Main function to scrape ESG reports for a company.
    Downloads the annual report, extracts text, and analyzes ESG information.
    Returns a dictionary with extracted text and analysis results.
    """
    report_url = find_annual_report_url(company_ticker)
    if not report_url:
        print(f"Could not find annual report for {company_ticker}")
        return None

    pdf_filename = f"temp_{company_ticker}_report.pdf"
    try:
        download_pdf(report_url, pdf_filename)
        text = extract_text_from_pdf(pdf_filename)
        # Clean up
        import os
        os.remove(pdf_filename)

        # Analyze the text
        entities = extract_esg_entities(text)
        sentiment = analyze_sentiment(text)  # Overall sentiment, but better to analyze sections
        controversies = detect_controversy(text)
        category = classify_esg_category(text)

        # Calculate ESG scores based on NLP analysis
        scores = calculate_esg_score_from_nlp(sentiment, entities, controversies)

        return {
            "text": text,
            "entities": entities,
            "sentiment": sentiment,
            "controversies": controversies,
            "primary_category": category,
            "scores": scores
        }
    except Exception as e:
        print(f"Error scraping report for {company_ticker}: {e}")
        return None

if __name__ == '__main__':
    # Example usage
    ticker = "AAPL"
    result = scrape_esg_reports(ticker)
    if result:
        print("Extracted text length:", len(result['text']))
        print("Entities:", result['entities'])
        print("Sentiment:", result['sentiment'])
        print("Controversies:", result['controversies'])
        print("Primary Category:", result['primary_category'])
    else:
        print("Failed to scrape and analyze report")