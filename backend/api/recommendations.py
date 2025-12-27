"""
Portfolio Recommendations API
FastAPI endpoints for generating and managing portfolio recommendations.
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from backend.services.recommendation_service import (
    PortfolioRecommendationService,
    ESGFilter,
    RiskPreference,
    SectorAllocation
)

router = APIRouter()
recommendation_service = PortfolioRecommendationService()


class ESGFilterRequest(BaseModel):
    """Request model for ESG filters."""
    min_total_score: float = Field(default=60.0, ge=0, le=100, description="Minimum total ESG score")
    min_environmental_score: float = Field(default=50.0, ge=0, le=100, description="Minimum environmental score")
    min_social_score: float = Field(default=50.0, ge=0, le=100, description="Minimum social score")
    min_governance_score: float = Field(default=50.0, ge=0, le=100, description="Minimum governance score")
    preferred_sectors: List[str] = Field(default_factory=list, description="Preferred sectors (empty for all)")
    excluded_sectors: List[str] = Field(default_factory=list, description="Excluded sectors")
    preferred_regions: List[str] = Field(default_factory=list, description="Preferred regions (empty for all)")
    excluded_regions: List[str] = Field(default_factory=list, description="Excluded regions")


class SectorAllocationRequest(BaseModel):
    """Request model for sector allocation targets."""
    targets: Dict[str, float] = Field(..., description="Sector allocation targets (percentages)")


class RecommendationRequest(BaseModel):
    """Request model for generating portfolio recommendations."""
    filters: ESGFilterRequest
    risk_preference: str = Field(..., description="Risk preference: conservative, moderate, or aggressive")
    sector_targets: Dict[str, float] = Field(..., description="Target sector allocations")
    portfolio_size: int = Field(default=10, ge=1, le=50, description="Number of companies in portfolio")


class RecommendationResponse(BaseModel):
    """Response model for portfolio recommendations."""
    id: str
    companies: List[Dict]
    esg_scores: Dict[str, float]
    sector_allocation: Dict[str, float]
    risk_assessment: str
    filters: Dict
    risk_preference: str
    target_allocation: Dict[str, float]


@router.post("/generate", response_model=RecommendationResponse)
async def generate_recommendation(request: RecommendationRequest):
    """
    Generate a portfolio recommendation based on ESG filters and preferences.

    This endpoint:
    1. Filters companies based on ESG criteria
    2. Applies risk preference adjustments
    3. Optimizes sector allocation
    4. Returns a balanced portfolio recommendation
    """
    try:
        # Validate risk preference
        try:
            risk_pref = RiskPreference(request.risk_preference.lower())
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid risk preference. Must be one of: {[rp.value for rp in RiskPreference]}"
            )

        # Validate sector allocation
        sector_allocation = SectorAllocation(request.sector_targets)
        if not sector_allocation.validate():
            raise HTTPException(
                status_code=400,
                detail="Sector allocations must sum to approximately 100%"
            )

        # Create ESG filter object
        esg_filter = ESGFilter(
            min_total_score=request.filters.min_total_score,
            min_environmental_score=request.filters.min_environmental_score,
            min_social_score=request.filters.min_social_score,
            min_governance_score=request.filters.min_governance_score,
            preferred_sectors=request.filters.preferred_sectors,
            excluded_sectors=request.filters.excluded_sectors,
            preferred_regions=request.filters.preferred_regions,
            excluded_regions=request.filters.excluded_regions,
        )

        # Generate recommendation
        recommendation = recommendation_service.generate_recommendation(
            filters=esg_filter,
            risk_preference=risk_pref,
            sector_targets=request.sector_targets,
            portfolio_size=request.portfolio_size
        )

        return recommendation.to_dict()

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating recommendation: {str(e)}")


@router.get("/sectors")
async def get_available_sectors():
    """Get list of available sectors for filtering."""
    try:
        sectors = set()
        for company in recommendation_service.companies:
            sectors.add(company["sector"])

        return {"sectors": sorted(list(sectors))}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching sectors: {str(e)}")


@router.get("/regions")
async def get_available_regions():
    """Get list of available regions for filtering."""
    try:
        regions = set()
        for company in recommendation_service.companies:
            regions.add(company["region"])

        return {"regions": sorted(list(regions))}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching regions: {str(e)}")


@router.get("/companies/count")
async def get_filtered_company_count(
    min_total_score: float = Query(60.0, ge=0, le=100),
    preferred_sectors: Optional[List[str]] = Query(None),
    excluded_sectors: Optional[List[str]] = Query(None),
    preferred_regions: Optional[List[str]] = Query(None),
    excluded_regions: Optional[List[str]] = Query(None),
):
    """Get count of companies that match the specified filters."""
    try:
        esg_filter = ESGFilter(
            min_total_score=min_total_score,
            preferred_sectors=preferred_sectors or [],
            excluded_sectors=excluded_sectors or [],
            preferred_regions=preferred_regions or [],
            excluded_regions=excluded_regions or [],
        )

        filtered_companies = recommendation_service.filter_companies_by_esg(esg_filter)

        return {"count": len(filtered_companies)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error counting companies: {str(e)}")