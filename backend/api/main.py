"""
Main FastAPI application for ESG Builder backend.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .recommendations import router as recommendations_router

app = FastAPI(
    title="ESG Builder API",
    description="Portfolio recommendation engine with ESG filtering",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(
    recommendations_router,
    prefix="/api/recommendations",
    tags=["recommendations"]
)

@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "ESG Builder API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}