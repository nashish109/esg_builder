# Portfolio Recommendation Engine Design

## Overview
The portfolio recommendation engine will generate optimized portfolios based on ESG criteria, risk preferences, and sector allocations. It will filter companies, balance risk/ESG trade-offs, and optimize sector diversification.

## Architecture Components

### 1. Data Structure Enhancements
Current ESG data only includes `total_score`. We need to add individual pillar scores:

```json
{
  "company_id": 1,
  "rating_date": "2024-06-01",
  "environmental_score": 85.5,
  "social_score": 82.3,
  "governance_score": 88.7,
  "total_score": 85.5,
  "source": "NLP Analysis"
}
```

### 2. ESG Filters Class
```python
class ESGFilter:
    def __init__(self):
        self.min_total_score = 60.0
        self.min_environmental_score = 50.0
        self.min_social_score = 50.0
        self.min_governance_score = 50.0
        self.preferred_sectors = []  # empty means all sectors
        self.excluded_sectors = []
        self.preferred_regions = []  # empty means all regions
        self.excluded_regions = []
```

### 3. Risk Preference Mapping
- **Conservative**: ESG > 80, stable companies (lower volatility assumption)
- **Moderate**: ESG 60-80, balanced approach
- **Aggressive**: ESG < 70, higher risk tolerance for potentially higher ESG impact

### 4. Sector Allocation Targets
```python
sector_targets = {
    "Technology": 0.4,    # 40%
    "Healthcare": 0.2,    # 20%
    "Financials": 0.15,   # 15%
    "Energy": 0.1,        # 10%
    "Consumer Goods": 0.15 # 15%
}
```

### 5. Recommendation Algorithm Flow

1. **Filter Companies by ESG Criteria**
   - Apply ESG score thresholds
   - Filter by sector/region preferences
   - Remove excluded sectors/regions

2. **Calculate Risk Scores**
   - Use ESG scores as proxy for risk (higher ESG = lower risk)
   - Conservative: ESG > 80
   - Moderate: ESG 60-80
   - Aggressive: ESG < 70

3. **Sector Allocation Optimization**
   - Select companies to meet sector targets
   - Balance ESG performance within sectors
   - Ensure minimum diversification (max 30% per sector)

4. **Portfolio Optimization**
   - Equal-weighted allocation within targets
   - Final ESG score calculation
   - Risk assessment based on company mix

### 6. API Endpoints

```python
POST /api/recommendations/generate
{
  "filters": {
    "min_total_score": 70.0,
    "min_environmental_score": 60.0,
    "preferred_sectors": ["Technology", "Healthcare"],
    "excluded_sectors": ["Tobacco"]
  },
  "risk_preference": "moderate",
  "sector_targets": {
    "Technology": 0.4,
    "Healthcare": 0.3,
    "Financials": 0.3
  },
  "portfolio_size": 10
}

Response:
{
  "id": "rec_123",
  "companies": [...],
  "esg_scores": {...},
  "sector_allocation": {...},
  "risk_assessment": "..."
}
```

### 7. UI Components

#### Filter Definition Page
- ESG score sliders (min values for total and pillars)
- Sector selection (multi-select with checkboxes)
- Region selection
- Risk preference radio buttons
- Sector allocation sliders (must sum to 100%)
- Portfolio size selector

#### Recommendation Display Page
- Company list with ESG scores and sector info
- Portfolio ESG breakdown (E/S/G averages)
- Sector allocation chart
- Risk assessment summary
- Save portfolio button

## Implementation Plan

1. Enhance data structure with individual ESG scores
2. Create filter classes and validation
3. Implement recommendation service logic
4. Build optimization algorithm
5. Create API endpoints
6. Develop UI components
7. Integrate with dashboard navigation
8. Add portfolio saving functionality
9. Testing and validation

## Risk Assessment Methodology

Since we don't have traditional financial metrics, we'll use ESG scores as risk indicators:

- **High ESG (>80)**: Low risk, stable companies
- **Medium ESG (60-80)**: Moderate risk, balanced
- **Low ESG (<60)**: Higher risk, potential volatility

This is a simplification - in production, this would use actual volatility, beta, and correlation data.