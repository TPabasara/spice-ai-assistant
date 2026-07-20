from fastapi import APIRouter
from app.api.endpoints import health

# Create a main router for API v1
api_router = APIRouter()

# Include individual endpoint routers
api_router.include_router(health.router, prefix="/system", tags=["System"])