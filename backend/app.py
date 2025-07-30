from fastapi import FastAPI
from backend.api import routes as api_routes

app = FastAPI(title="ESG Builder API")

app.include_router(api_routes.router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Welcome to the ESG Builder API"}