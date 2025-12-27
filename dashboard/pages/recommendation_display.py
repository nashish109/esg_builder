"""
Portfolio Recommendation Display Page
Shows generated portfolio recommendations and allows saving to portfolio library.
"""

import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import json

# Configuration
API_BASE_URL = "http://localhost:8000"  # Will be configurable
DATA_DIR = Path(__file__).parent.parent.parent / "data"


def generate_recommendation(request_data):
    """Generate recommendation using API."""
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/recommendations/generate",
            json=request_data,
            timeout=30
        )

        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"Error connecting to API: {str(e)}")
        return None


def save_portfolio_to_library(recommendation, portfolio_name):
    """Save recommendation as a new portfolio."""
    try:
        # Load existing portfolios
        with open(DATA_DIR / "portfolios.json", "r") as f:
            portfolios = json.load(f)

        # Create new portfolio
        risk_assessment = recommendation.get('risk_assessment', 'No risk assessment available.')
        companies = recommendation.get('companies', [])
        new_portfolio = {
            "id": max(p["id"] for p in portfolios) + 1 if portfolios else 1,
            "name": portfolio_name,
            "description": f"AI-generated portfolio with ESG focus. {risk_assessment}",
            "companies": [
                {"id": company.get("id", 0)}
                for company in companies
            ]
        }

        # Add to portfolios
        portfolios.append(new_portfolio)

        # Save back to file
        with open(DATA_DIR / "portfolios.json", "w") as f:
            json.dump(portfolios, f, indent=2)

        return True, new_portfolio["id"]

    except Exception as e:
        return False, str(e)


def page():
    """Main page function for displaying portfolio recommendations."""

    st.markdown('<h1 class="main-header" style="background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);">📊 Portfolio Recommendation Results</h1>', unsafe_allow_html=True)

    # Check if we have recommendation request data
    if "recommendation_request" not in st.session_state:
        st.error("❌ No recommendation request found. Please go back to the filters page.")
        if st.button("🔙 Go to Filters"):
            st.session_state.force_page = "Portfolio Recommendations"
            st.rerun()
        return

    request_data = st.session_state.recommendation_request

    # Generate recommendation if not already done
    if "recommendation_result" not in st.session_state or not st.session_state.get("recommendation_generated", False):
        with st.spinner("🤖 Generating your personalized portfolio recommendation..."):
            with st.container():
                progress_bar = st.progress(0)
                status_text = st.empty()

                status_text.text("Analyzing ESG data...")
                progress_bar.progress(25)

                status_text.text("Applying your filters...")
                progress_bar.progress(50)

                status_text.text("Optimizing portfolio selection...")
                progress_bar.progress(75)

                recommendation = generate_recommendation(request_data)

                progress_bar.progress(100)
                status_text.empty()
                progress_bar.empty()

        if recommendation is None:
            st.error("❌ Failed to generate recommendation. Please check your filters and try again.")
            st.info("💡 **Troubleshooting tips:**")
            st.info("- Ensure the backend API is running on port 8000")
            st.info("- Try relaxing your ESG score thresholds")
            st.info("- Check if sufficient companies match your sector/region preferences")
            return

        st.session_state.recommendation_result = recommendation
        st.session_state.recommendation_generated = True

        # Success message
        st.success("✅ Portfolio recommendation generated successfully!")
    else:
        recommendation = st.session_state.recommendation_result

    # Display recommendation summary
    col1, col2, col3 = st.columns(3)

    with col1:
        avg_total_score = recommendation.get('esg_scores', {}).get('average_total', 0.0)
        st.metric(
            "📈 Average ESG Score",
            f"{avg_total_score:.1f}",
            help="Average total ESG score across portfolio companies"
        )

    with col2:
        companies = recommendation.get('companies', [])
        st.metric(
            "🏢 Companies",
            len(companies),
            help="Number of companies in the recommended portfolio"
        )

    with col3:
        risk_preference = recommendation.get('risk_preference', 'Unknown')
        risk_level = risk_preference.title() if risk_preference != 'Unknown' else 'Unknown'
        risk_assessment = recommendation.get('risk_assessment', 'No assessment available')
        st.metric(
            "⚖️ Risk Profile",
            risk_level,
            help=risk_assessment
        )

    # Risk assessment
    st.markdown('<h2 class="section-header">🎯 Risk Assessment</h2>', unsafe_allow_html=True)
    risk_assessment = recommendation.get('risk_assessment', 'No risk assessment available.')
    st.info(risk_assessment)

    # ESG Score breakdown
    st.markdown('<h2 class="section-header">📊 ESG Score Breakdown</h2>', unsafe_allow_html=True)

    esg_data = recommendation.get('esg_scores', {})
    esg_df = pd.DataFrame({
        'Pillar': ['Environmental', 'Social', 'Governance', 'Total'],
        'Score': [
            esg_data.get('average_environmental', 0.0),
            esg_data.get('average_social', 0.0),
            esg_data.get('average_governance', 0.0),
            esg_data.get('average_total', 0.0)
        ]
    })

    fig = px.bar(
        esg_df,
        x='Pillar',
        y='Score',
        color='Pillar',
        title='Average ESG Pillar Scores',
        color_discrete_map={
            'Environmental': '#4ECDC4',
            'Social': '#45B7D1',
            'Governance': '#96CEB4',
            'Total': '#FF6B6B'
        }
    )
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

    # Sector allocation
    st.markdown('<h2 class="section-header">🏢 Sector Allocation</h2>', unsafe_allow_html=True)

    sector_data = recommendation.get('sector_allocation', {})
    if sector_data:
        sector_df = pd.DataFrame({
            'Sector': list(sector_data.keys()),
            'Allocation': [v * 100 for v in sector_data.values()]
        })
    else:
        sector_df = pd.DataFrame({'Sector': ['No data'], 'Allocation': [0.0]})

    fig = px.pie(
        sector_df,
        values='Allocation',
        names='Sector',
        title='Portfolio Sector Distribution',
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    st.plotly_chart(fig, use_container_width=True)

    # Company details
    st.markdown('<h2 class="section-header">🏢 Recommended Companies</h2>', unsafe_allow_html=True)

    companies = recommendation.get('companies', [])
    if companies:
        # Prepare company data
        company_data = []
        for company in companies:
            company_data.append({
                'Company': company.get('name', 'Unknown'),
                'Ticker': company.get('ticker', 'N/A'),
                'Sector': company.get('sector', 'Unknown'),
                'ESG Score': company.get('esg_score', 0.0)
            })

        company_df = pd.DataFrame(company_data)
    else:
        company_df = pd.DataFrame({
            'Company': ['No companies found'],
            'Ticker': ['N/A'],
            'Sector': ['N/A'],
            'ESG Score': [0.0]
        })

    # Display as table
    st.dataframe(
        company_df,
        use_container_width=True,
        column_config={
            "ESG Score": st.column_config.NumberColumn(
                "ESG Score",
                format="%.1f",
                help="Total ESG score"
            )
        }
    )

    # ESG Score distribution
    fig = px.histogram(
        company_df,
        x='ESG Score',
        nbins=10,
        title='ESG Score Distribution',
        color_discrete_sequence=['#FF6B6B']
    )
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

    # Target vs Actual allocation comparison
    st.markdown('<h2 class="section-header">🎯 Allocation Comparison</h2>', unsafe_allow_html=True)

    target_allocation = recommendation.get('target_allocation', {})
    actual_allocation = recommendation.get('sector_allocation', {})

    if target_allocation or actual_allocation:
        comparison_data = []
        all_sectors = set(list(target_allocation.keys()) + list(actual_allocation.keys()))
        for sector in all_sectors:
            target_pct = target_allocation.get(sector, 0) * 100
            actual_pct = actual_allocation.get(sector, 0) * 100
            comparison_data.append({
                'Sector': sector,
                'Target %': target_pct,
                'Actual %': actual_pct,
                'Difference %': actual_pct - target_pct
            })

        comparison_df = pd.DataFrame(comparison_data)
    else:
        comparison_df = pd.DataFrame({
            'Sector': ['No allocation data'],
            'Target %': [0.0],
            'Actual %': [0.0],
            'Difference %': [0.0]
        })

    # Display comparison table
    st.dataframe(
        comparison_df,
        use_container_width=True,
        column_config={
            "Target %": st.column_config.NumberColumn("Target %", format="%.1f%%"),
            "Actual %": st.column_config.NumberColumn("Actual %", format="%.1f%%"),
            "Difference %": st.column_config.NumberColumn("Difference %", format="%.1f%%"),
        }
    )

    # Save portfolio functionality
    st.markdown("---")
    st.markdown('<h2 class="section-header">💾 Save Portfolio</h2>', unsafe_allow_html=True)

    col1, col2 = st.columns([3, 1])

    with col1:
        risk_preference = recommendation.get('risk_preference', 'unknown')
        portfolio_name = st.text_input(
            "Portfolio Name",
            value=f"ESG Portfolio - {risk_preference.title()}",
            help="Choose a name for your portfolio"
        )

    with col2:
        save_button = st.button("💾 Save Portfolio", type="primary", use_container_width=True)

    if save_button:
        if not portfolio_name.strip():
            st.error("❌ Please enter a portfolio name.")
        else:
            success, result = save_portfolio_to_library(recommendation, portfolio_name.strip())

            if success:
                st.success(f"✅ Portfolio '{portfolio_name}' saved successfully! (ID: {result})")
                st.info("🔄 Redirecting to dashboard to view your new portfolio...")
                st.session_state.force_page = "Dashboard"
                st.rerun()
            else:
                st.error(f"❌ Failed to save portfolio: {result}")

    # Navigation buttons
    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🔄 Generate New Recommendation", use_container_width=True):
            # Clear session state and go back to filters
            for key in ['recommendation_request', 'recommendation_result', 'recommendation_generated']:
                if key in st.session_state:
                    del st.session_state[key]
            st.session_state.force_page = "Portfolio Recommendations"
            st.rerun()

    with col2:
        if st.button("⚙️ Modify Filters", use_container_width=True):
            st.session_state.force_page = "Portfolio Recommendations"
            st.rerun()

    with col3:
        if st.button("🏠 Back to Dashboard", use_container_width=True):
            st.session_state.force_page = "Dashboard"
            st.rerun()