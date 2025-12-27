"""
Portfolio Recommendation Filters Page
Allows users to define ESG filters and preferences for portfolio generation.
"""

import streamlit as st
import requests
import json
from pathlib import Path

# Configuration
API_BASE_URL = "http://localhost:8000"  # Will be configurable
DATA_DIR = Path(__file__).parent.parent.parent / "data"


def load_company_data():
    """Load company data for sector/region options."""
    try:
        with open(DATA_DIR / "companies.json", "r") as f:
            companies = json.load(f)

        sectors = sorted(set(c["sector"] for c in companies))
        regions = sorted(set(c["region"] for c in companies))

        return sectors, regions
    except Exception as e:
        st.error(f"Error loading company data: {e}")
        return [], []


def get_available_options():
    """Get available sectors and regions from API if possible, fallback to local data."""
    try:
        # Try API first
        sectors_response = requests.get(f"{API_BASE_URL}/api/recommendations/sectors", timeout=5)
        regions_response = requests.get(f"{API_BASE_URL}/api/recommendations/regions", timeout=5)

        if sectors_response.status_code == 200 and regions_response.status_code == 200:
            sectors = sectors_response.json()["sectors"]
            regions = regions_response.json()["regions"]
            return sectors, regions
    except:
        pass

    # Fallback to local data
    return load_company_data()


def page():
    """Main page function for portfolio recommendation filters."""

    st.markdown('<h1 class="main-header" style="background: linear-gradient(135deg, #10b981 0%, #059669 100%);">🎯 Portfolio Recommendation Filters</h1>', unsafe_allow_html=True)

    st.markdown("""
    <div style="background: #f0fdf4; padding: 1.5rem; border-radius: 12px; margin-bottom: 2rem; border-left: 4px solid #10b981;">
        <p style="margin: 0; font-size: 1.1rem; color: #166534;">
            Define your investment preferences and ESG criteria to generate a personalized portfolio recommendation.
            The system will optimize company selection based on your ESG requirements, risk preferences, and sector allocations.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Load available options
    available_sectors, available_regions = get_available_options()

    # Create two columns for better layout
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<h3 class="filter-header">📊 ESG Score Thresholds</h3>', unsafe_allow_html=True)

        # ESG Score filters
        min_total_score = st.slider(
            "Minimum Total ESG Score",
            min_value=0.0,
            max_value=100.0,
            value=60.0,
            step=5.0,
            help="Companies must have at least this total ESG score"
        )

        min_environmental_score = st.slider(
            "Minimum Environmental Score",
            min_value=0.0,
            max_value=100.0,
            value=50.0,
            step=5.0,
            help="Minimum environmental pillar score"
        )

        min_social_score = st.slider(
            "Minimum Social Score",
            min_value=0.0,
            max_value=100.0,
            value=50.0,
            step=5.0,
            help="Minimum social pillar score"
        )

        min_governance_score = st.slider(
            "Minimum Governance Score",
            min_value=0.0,
            max_value=100.0,
            value=50.0,
            step=5.0,
            help="Minimum governance pillar score"
        )

    with col2:
        st.markdown('<h3 class="filter-header">🎭 Risk Preferences</h3>', unsafe_allow_html=True)

        risk_preference = st.radio(
            "Risk Tolerance",
            options=["Conservative", "Moderate", "Aggressive"],
            index=1,  # Default to Moderate
            help="""
            Conservative: Prioritizes high ESG scores (>80) for stability
            Moderate: Balances ESG scores (60-80) with diversification
            Aggressive: Accepts lower ESG scores for higher potential impact
            """
        )

        st.markdown('<h3 class="filter-header">📏 Portfolio Size</h3>', unsafe_allow_html=True)

        portfolio_size = st.slider(
            "Number of Companies",
            min_value=1,
            max_value=20,
            value=10,
            step=1,
            help="Target number of companies in the recommended portfolio"
        )

    # Sector and Region preferences
    st.markdown('<h2 class="section-header">🏢 Sector & Region Preferences</h2>', unsafe_allow_html=True)

    col3, col4 = st.columns(2)

    with col3:
        st.markdown("**Preferred Sectors** (leave empty for all)")
        preferred_sectors = st.multiselect(
            "Include these sectors:",
            options=available_sectors,
            default=[],
            help="Only include companies from these sectors (empty = all sectors)"
        )

        st.markdown("**Excluded Sectors**")
        excluded_sectors = st.multiselect(
            "Exclude these sectors:",
            options=available_sectors,
            default=[],
            help="Never include companies from these sectors"
        )

    with col4:
        st.markdown("**Preferred Regions** (leave empty for all)")
        preferred_regions = st.multiselect(
            "Include these regions:",
            options=available_regions,
            default=[],
            help="Only include companies from these regions (empty = all regions)"
        )

        st.markdown("**Excluded Regions**")
        excluded_regions = st.multiselect(
            "Exclude these regions:",
            options=available_regions,
            default=[],
            help="Never include companies from these regions"
        )

    # Sector allocation targets
    st.markdown('<h2 class="section-header">📈 Sector Allocation Targets</h2>', unsafe_allow_html=True)

    st.markdown("Set target percentage allocations for each sector. Must sum to 100%.")

    # Create a dynamic sector allocation interface
    if available_sectors:
        # Initialize session state for sector allocations
        if "sector_allocations" not in st.session_state:
            # Default equal allocation
            equal_allocation = 100.0 / len(available_sectors)
            st.session_state.sector_allocations = {
                sector: equal_allocation for sector in available_sectors
            }

        # Display sector allocation sliders
        cols = st.columns(2)
        total_allocation = 0.0

        for i, sector in enumerate(available_sectors):
            with cols[i % 2]:
                current_value = st.session_state.sector_allocations.get(sector, 0.0)
                new_value = st.slider(
                    f"{sector} (%)",
                    min_value=0.0,
                    max_value=100.0,
                    value=current_value,
                    step=5.0,
                    key=f"sector_{sector}"
                )
                st.session_state.sector_allocations[sector] = new_value
                total_allocation += new_value

        # Display total and validation
        if abs(total_allocation - 100.0) > 0.1:
            st.error(f"⚠️ Sector allocations must sum to 100%. Current total: {total_allocation:.1f}%")
        else:
            st.success(f"✅ Sector allocations sum to {total_allocation:.1f}%")

        # Normalize button
        if st.button("🔄 Auto-balance allocations"):
            equal_allocation = 100.0 / len(available_sectors)
            for sector in available_sectors:
                st.session_state.sector_allocations[sector] = equal_allocation
            st.rerun()

    # Generate recommendation button
    st.markdown("---")

    if abs(sum(st.session_state.sector_allocations.values()) - 100.0) > 0.1:
        st.button("🚀 Generate Recommendation", disabled=True, help="Please ensure sector allocations sum to 100%")
    else:
        if st.button("🚀 Generate Recommendation", type="primary"):
            # Prepare request data
            request_data = {
                "filters": {
                    "min_total_score": min_total_score,
                    "min_environmental_score": min_environmental_score,
                    "min_social_score": min_social_score,
                    "min_governance_score": min_governance_score,
                    "preferred_sectors": preferred_sectors,
                    "excluded_sectors": excluded_sectors,
                    "preferred_regions": preferred_regions,
                    "excluded_regions": excluded_regions,
                },
                "risk_preference": risk_preference.lower(),
                "sector_targets": {sector: allocation / 100.0 for sector, allocation in st.session_state.sector_allocations.items()},
                "portfolio_size": portfolio_size
            }

            # Store request data in session state for the results page
            st.session_state.recommendation_request = request_data
            st.session_state.recommendation_generated = False

            # Navigate to results page
            st.session_state.force_page = "Recommendation Results"
            st.rerun()

    # Preview company count
    st.markdown("---")
    st.markdown('<h2 class="section-header">📊 Filter Preview</h2>', unsafe_allow_html=True)

    try:
        # Get company count that match filters
        params = {
            "min_total_score": min_total_score,
            "preferred_sectors": preferred_sectors,
            "excluded_sectors": excluded_sectors,
            "preferred_regions": preferred_regions,
            "excluded_regions": excluded_regions,
        }

        # Remove empty lists for API call
        params = {k: v for k, v in params.items() if v}

        count_response = requests.get(
            f"{API_BASE_URL}/api/recommendations/companies/count",
            params=params,
            timeout=5
        )

        if count_response.status_code == 200:
            count = count_response.json()["count"]
            st.info(f"📈 **{count} companies** match your current ESG filters")

            if count < portfolio_size:
                st.warning(f"⚠️ Only {count} companies match your filters, but you requested {portfolio_size}. Consider relaxing your criteria.")
        else:
            st.error("Unable to preview company count. API may not be running.")

    except Exception as e:
        st.warning("⚠️ Unable to preview company count. Make sure the API server is running on port 8000.")
        st.info("💻 To start the API server, run: `python -m uvicorn backend.api.main:app --host 0.0.0.0 --port 8000 --reload`")