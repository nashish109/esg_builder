import streamlit as st

st.set_page_config(page_title="ESG Builder Dashboard", layout="wide")

import pandas as pd
import plotly.express as px
import requests

API_URL = "http://localhost:8000/api"

st.title("ESG Builder Dashboard")

st.write("Welcome to the ESG Builder. This dashboard will visualize ESG trends and portfolio performance.")

# --- Company-wise ESG Trends ---
st.header("Company ESG Trends")

def get_companies():
    response = requests.get(f"{API_URL}/companies/")
    return response.json()

def get_esg_scores(company_id):
    response = requests.get(f"{API_URL}/companies/{company_id}/esg-scores/")
    return response.json()

companies = get_companies()

if companies:
    company_options = {c['name']: c['id'] for c in companies}
    selected_company_names = st.multiselect(
        "Select companies to compare:",
        options=list(company_options.keys()),
        default=list(company_options.keys())[:2]
    )

    if selected_company_names:
        trend_data = []
        for name in selected_company_names:
            company_id = company_options[name]
            scores = get_esg_scores(company_id)
            for score in scores:
                trend_data.append({
                    "Company": name,
                    "Date": score['rating_date'],
                    "ESG Score": score['total_score']
                })
        
        if trend_data:
            df_trends = pd.DataFrame(trend_data)
            df_trends['Date'] = pd.to_datetime(df_trends['Date'])
            
            fig = px.line(
                df_trends,
                x="Date",
                y="ESG Score",
                color="Company",
                title="ESG Score Over Time"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No ESG data available for the selected companies.")
    else:
        st.warning("Please select at least one company.")
else:
    st.warning("No companies found in the database.")


# --- Portfolio Comparison ---
st.header("Portfolio Comparison")

def get_portfolios():
    response = requests.get(f"{API_URL}/portfolios/")
    return response.json()

portfolios = get_portfolios()

if portfolios:
    portfolio_data = []
    for p in portfolios:
        total_score = 0
        company_count = 0
        if 'companies' in p and p['companies']:
            for c in p['companies']:
                scores = get_esg_scores(c['id'])
                if scores:
                    # Use the latest score for each company
                    total_score += scores[-1]['total_score']
                    company_count += 1
            
            if company_count > 0:
                average_score = total_score / company_count
                portfolio_data.append({
                    "Portfolio": p['name'],
                    "Average ESG Score": average_score
                })

    if portfolio_data:
        df_portfolio = pd.DataFrame(portfolio_data)
        fig = px.bar(
            df_portfolio,
            x="Portfolio",
            y="Average ESG Score",
            color="Portfolio",
            title="Portfolio ESG Score Comparison"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No portfolio data available for comparison.")
else:
    st.warning("No portfolios found in the database.")


# --- ESG News Alerts ---
st.header("Recent ESG News Alerts")

def get_news():
    response = requests.get(f"{API_URL}/news/")
    return response.json()

news_articles = get_news()

if news_articles:
    for article in news_articles:
        st.info(f"**{article.get('source', 'N/A')} ({article.get('published_at', 'N/A')})**: {article.get('title', 'N/A')}")
else:
    st.warning("No recent news articles found.")