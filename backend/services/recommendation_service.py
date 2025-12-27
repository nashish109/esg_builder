"""
Portfolio Recommendation Service
Generates optimized portfolios based on ESG filters, risk preferences, and sector allocations.
"""

import json
import random
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class RiskPreference(Enum):
    CONSERVATIVE = "conservative"
    MODERATE = "moderate"
    AGGRESSIVE = "aggressive"


@dataclass
class ESGFilter:
    """ESG filtering criteria for portfolio recommendations."""
    min_total_score: float = 60.0
    min_environmental_score: float = 50.0
    min_social_score: float = 50.0
    min_governance_score: float = 50.0
    preferred_sectors: List[str] = None
    excluded_sectors: List[str] = None
    preferred_regions: List[str] = None
    excluded_regions: List[str] = None

    def __post_init__(self):
        if self.preferred_sectors is None:
            self.preferred_sectors = []
        if self.excluded_sectors is None:
            self.excluded_sectors = []
        if self.preferred_regions is None:
            self.preferred_regions = []
        if self.excluded_regions is None:
            self.excluded_regions = []


@dataclass
class SectorAllocation:
    """Target sector allocation percentages."""
    targets: Dict[str, float]

    def validate(self) -> bool:
        """Validate that sector allocations sum to approximately 100%."""
        total = sum(self.targets.values())
        return 0.95 <= total <= 1.05  # Allow 5% tolerance

    def get_sector_list(self) -> List[str]:
        """Get list of sectors in allocation."""
        return list(self.targets.keys())


class PortfolioRecommendation:
    """Portfolio recommendation result."""

    def __init__(self, recommendation_id: str):
        self.id = recommendation_id
        self.companies: List[Dict] = []
        self.esg_scores: Dict[str, float] = {}
        self.sector_allocation: Dict[str, float] = {}
        self.risk_assessment: str = ""
        self.filters: ESGFilter = None
        self.risk_preference: RiskPreference = None
        self.target_allocation: SectorAllocation = None

    def to_dict(self) -> Dict:
        """Convert recommendation to dictionary."""
        return {
            "id": self.id,
            "companies": self.companies,
            "esg_scores": self.esg_scores,
            "sector_allocation": self.sector_allocation,
            "risk_assessment": self.risk_assessment,
            "filters": {
                "min_total_score": self.filters.min_total_score,
                "min_environmental_score": self.filters.min_environmental_score,
                "min_social_score": self.filters.min_social_score,
                "min_governance_score": self.filters.min_governance_score,
                "preferred_sectors": self.filters.preferred_sectors,
                "excluded_sectors": self.filters.excluded_sectors,
                "preferred_regions": self.filters.preferred_regions,
                "excluded_regions": self.filters.excluded_regions,
            } if self.filters else None,
            "risk_preference": self.risk_preference.value if self.risk_preference else None,
            "target_allocation": self.target_allocation.targets if self.target_allocation else None,
        }


class PortfolioRecommendationService:
    """Service for generating portfolio recommendations."""

    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.companies = self._load_companies()
        self.esg_scores = self._load_esg_scores()
        self.portfolios = self._load_portfolios()

    def _load_companies(self) -> List[Dict]:
        """Load company data."""
        try:
            with open(self.data_dir / "companies.json", "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading companies: {e}")
            return []

    def _load_esg_scores(self) -> List[Dict]:
        """Load ESG scores data."""
        try:
            with open(self.data_dir / "esg_scores.json", "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading ESG scores: {e}")
            return []

    def _load_portfolios(self) -> List[Dict]:
        """Load portfolio data."""
        try:
            with open(self.data_dir / "portfolios.json", "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading portfolios: {e}")
            return []

    def get_latest_esg_scores(self) -> Dict[int, Dict]:
        """Get the latest ESG scores for each company."""
        latest_scores = {}

        for score in self.esg_scores:
            company_id = score["company_id"]
            if company_id not in latest_scores:
                latest_scores[company_id] = score
            else:
                # Compare dates to get the latest
                current_date = latest_scores[company_id]["rating_date"]
                new_date = score["rating_date"]
                if new_date > current_date:
                    latest_scores[company_id] = score

        return latest_scores

    def get_company_by_id(self, company_id: int) -> Optional[Dict]:
        """Get company information by ID."""
        for company in self.companies:
            if company["id"] == company_id:
                return company
        return None

    def filter_companies_by_esg(self, filters: ESGFilter) -> List[Dict]:
        """Filter companies based on ESG criteria."""
        latest_scores = self.get_latest_esg_scores()
        filtered_companies = []

        for company in self.companies:
            company_id = company["id"]
            if company_id not in latest_scores:
                continue

            scores = latest_scores[company_id]

            # Check ESG score thresholds
            if scores["total_score"] < filters.min_total_score:
                continue
            if scores["environmental_score"] < filters.min_environmental_score:
                continue
            if scores["social_score"] < filters.min_social_score:
                continue
            if scores["governance_score"] < filters.min_governance_score:
                continue

            # Check sector filters
            if filters.preferred_sectors and company["sector"] not in filters.preferred_sectors:
                continue
            if filters.excluded_sectors and company["sector"] in filters.excluded_sectors:
                continue

            # Check region filters
            if filters.preferred_regions and company["region"] not in filters.preferred_regions:
                continue
            if filters.excluded_regions and company["region"] in filters.excluded_regions:
                continue

            # Company passes all filters
            filtered_companies.append({
                "id": company["id"],
                "name": company["name"],
                "ticker": company["ticker"],
                "sector": company["sector"],
                "region": company["region"],
                "esg_scores": scores
            })

        return filtered_companies

    def calculate_risk_score(self, total_score: float, risk_preference: RiskPreference) -> float:
        """Calculate risk score based on ESG score and risk preference."""
        if risk_preference == RiskPreference.CONSERVATIVE:
            # Conservative: prefer high ESG scores (>80)
            if total_score >= 80:
                return 1.0  # Low risk
            elif total_score >= 60:
                return 0.6  # Medium risk
            else:
                return 0.2  # High risk

        elif risk_preference == RiskPreference.MODERATE:
            # Moderate: balanced approach (60-80 optimal)
            if 60 <= total_score <= 80:
                return 1.0  # Optimal
            elif total_score > 80:
                return 0.8  # Good but conservative
            else:
                return 0.4  # Aggressive

        else:  # AGGRESSIVE
            # Aggressive: accept lower ESG for higher potential impact
            if total_score >= 70:
                return 0.7  # Still reasonable
            elif total_score >= 50:
                return 1.0  # Optimal for aggressive
            else:
                return 0.8  # Acceptable

    def optimize_sector_allocation(
        self,
        companies: List[Dict],
        sector_targets: Dict[str, float],
        portfolio_size: int = 10
    ) -> List[Dict]:
        """Optimize company selection based on sector allocation targets."""

        if not companies:
            return []

        # Group companies by sector
        sector_companies = {}
        for company in companies:
            sector = company["sector"]
            if sector not in sector_companies:
                sector_companies[sector] = []
            sector_companies[sector].append(company)

        selected_companies = []
        remaining_slots = portfolio_size

        # First, allocate companies to meet sector targets
        for sector, target_percentage in sector_targets.items():
            if sector not in sector_companies:
                continue

            sector_company_list = sector_companies[sector]
            target_count = max(1, int(portfolio_size * target_percentage))

            # Sort by ESG score (highest first)
            sector_company_list.sort(key=lambda x: x["esg_scores"]["total_score"], reverse=True)

            # Select top companies from this sector
            selected_from_sector = sector_company_list[:min(target_count, remaining_slots, len(sector_company_list))]
            selected_companies.extend(selected_from_sector)

            remaining_slots -= len(selected_from_sector)

        # If we still have slots and sectors left, fill with best remaining companies
        if remaining_slots > 0:
            remaining_companies = []
            for sector, company_list in sector_companies.items():
                if sector not in sector_targets:
                    remaining_companies.extend(company_list)

            # Sort remaining by ESG score
            remaining_companies.sort(key=lambda x: x["esg_scores"]["total_score"], reverse=True)
            selected_companies.extend(remaining_companies[:remaining_slots])

        return selected_companies[:portfolio_size]

    def generate_recommendation(
        self,
        filters: ESGFilter,
        risk_preference: RiskPreference,
        sector_targets: Dict[str, float],
        portfolio_size: int = 10
    ) -> PortfolioRecommendation:
        """Generate a portfolio recommendation."""

        # Create recommendation object
        recommendation_id = f"rec_{random.randint(10000, 99999)}"
        recommendation = PortfolioRecommendation(recommendation_id)

        # Store input parameters
        recommendation.filters = filters
        recommendation.risk_preference = risk_preference
        recommendation.target_allocation = SectorAllocation(sector_targets)

        # Filter companies by ESG criteria
        filtered_companies = self.filter_companies_by_esg(filters)

        if not filtered_companies:
            recommendation.risk_assessment = "No companies meet the specified ESG criteria."
            return recommendation

        # Optimize sector allocation
        selected_companies = self.optimize_sector_allocation(
            filtered_companies, sector_targets, portfolio_size
        )

        if not selected_companies:
            recommendation.risk_assessment = "Unable to create portfolio with specified sector allocations."
            return recommendation

        # Calculate portfolio metrics
        total_env = total_social = total_gov = total_esg = 0
        sector_counts = {}

        for company in selected_companies:
            scores = company["esg_scores"]
            total_env += scores["environmental_score"]
            total_social += scores["social_score"]
            total_gov += scores["governance_score"]
            total_esg += scores["total_score"]

            sector = company["sector"]
            sector_counts[sector] = sector_counts.get(sector, 0) + 1

        company_count = len(selected_companies)
        recommendation.esg_scores = {
            "average_environmental": round(total_env / company_count, 2),
            "average_social": round(total_social / company_count, 2),
            "average_governance": round(total_gov / company_count, 2),
            "average_total": round(total_esg / company_count, 2),
        }

        # Calculate actual sector allocation
        recommendation.sector_allocation = {
            sector: round(count / company_count, 3)
            for sector, count in sector_counts.items()
        }

        # Set companies (simplified for API)
        recommendation.companies = [
            {
                "id": c["id"],
                "name": c["name"],
                "ticker": c["ticker"],
                "sector": c["sector"],
                "esg_score": c["esg_scores"]["total_score"]
            }
            for c in selected_companies
        ]

        # Risk assessment
        avg_esg = recommendation.esg_scores["average_total"]
        if risk_preference == RiskPreference.CONSERVATIVE:
            if avg_esg >= 80:
                recommendation.risk_assessment = "Low risk - High ESG portfolio suitable for conservative investors."
            else:
                recommendation.risk_assessment = "Medium risk - ESG scores could be higher for conservative preferences."
        elif risk_preference == RiskPreference.MODERATE:
            if 60 <= avg_esg <= 80:
                recommendation.risk_assessment = "Balanced risk - Optimal ESG range for moderate preferences."
            else:
                recommendation.risk_assessment = "Adjusted risk - Portfolio ESG profile differs from moderate target."
        else:  # AGGRESSIVE
            recommendation.risk_assessment = "Higher risk - Portfolio includes companies with development potential."

        return recommendation