import streamlit as st
import pandas as pd
import plotly.express as px
import json
import os
from pathlib import Path
from pages import add_company, delete_company
from pages import recommendation_filters, recommendation_display

st.set_page_config(
    page_title="ESG Builder Dashboard",
    layout="wide",
    page_icon="🌱"
)

# Load custom CSS
def load_css():
    with open(Path(__file__).parent / "style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

DATA_DIR = Path(__file__).parent.parent / "data"

PAGES = {
    "Dashboard": "main_page",
    "Add Company": "add_company_page",
    "Delete Company": "delete_company_page",
    "Portfolio Recommendations": "recommendation_filters_page",
    "Recommendation Results": "recommendation_display_page"
}

def main_page():
    # Professional header with custom styling
    st.markdown("""
    <div class="main-header">
        <h1>🚀 ESG Builder Dashboard 🌍</h1>
        <p>⚡ Sustainable Investing Made EPIC! ⚡</p>
        <div style="font-size: 2em; margin-top: 10px;">
            🌱💚🔋⚡💰📈
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<p style="font-size: 1.1rem; color: #64748b; text-align: center; margin-bottom: 2rem;">Welcome to the ESG Builder platform. Analyze ESG trends, create sustainable portfolios, and make informed investment decisions.</p>', unsafe_allow_html=True)

    # --- Company-wise ESG Trends ---
    st.markdown('<h2 class="section-header">📈 Company ESG Trends</h2>', unsafe_allow_html=True)

    def get_companies():
        try:
            with open(DATA_DIR / "companies.json", "r") as f:
                return json.load(f)
        except Exception as e:
            st.error(f"Error loading companies: {e}")
            return []

    @st.cache_data(ttl=600)
    def get_esg_scores(company_id):
        try:
            with open(DATA_DIR / "esg_scores.json", "r") as f:
                all_scores = json.load(f)
            return [score for score in all_scores if score["company_id"] == company_id]
        except Exception as e:
            st.error(f"Error loading ESG scores for company {company_id}: {e}")
            return []

    companies = get_companies()

    if companies:
        company_options = {c['name']: c['id'] for c in companies}
        all_company_names = list(company_options.keys())
        selected_company_names = st.multiselect(
            "Select companies to compare:",
            options=all_company_names,
            default=all_company_names[:2] if all_company_names else []
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
    st.markdown('<h2 class="section-header">📊 Portfolio Comparison</h2>', unsafe_allow_html=True)

    @st.cache_data(ttl=600)
    def get_portfolios():
        try:
            with open(DATA_DIR / "portfolios.json", "r") as f:
                return json.load(f)
        except Exception as e:
            st.error(f"Error loading portfolios: {e}")
            return []

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
    st.markdown('<h2 class="section-header">📰 ESG News Alerts</h2>', unsafe_allow_html=True)

    @st.cache_data(ttl=3600)
    def get_news():
        try:
            with open(DATA_DIR / "news.json", "r") as f:
                return json.load(f)
        except Exception as e:
            st.error(f"Error loading news: {e}")
            return []

    news_articles = get_news()

    if news_articles:
        for article in news_articles:
            st.info(f"**{article.get('source', 'N/A')} ({article.get('published_at', 'N/A')})**: {article.get('title', 'N/A')}")
    else:
        st.warning("No recent news articles found.")

def run():
    st.sidebar.title("Navigation")

    # Check if we need to force a specific page (from session state)
    forced_page = st.session_state.get("force_page", None)
    if forced_page and forced_page in PAGES:
        default_index = list(PAGES.keys()).index(forced_page)
        # Clear the forced page after using it
        del st.session_state.force_page
    else:
        default_index = 0

    selection = st.sidebar.radio("Go to", list(PAGES.keys()), index=default_index)

    if selection == "Dashboard":
        main_page()
    elif selection == "Add Company":
        add_company.page()
    elif selection == "Delete Company":
        delete_company.page()
    elif selection == "Portfolio Recommendations":
        recommendation_filters.page()
    elif selection == "Recommendation Results":
        recommendation_display.page()

if __name__ == "__main__":
    run()