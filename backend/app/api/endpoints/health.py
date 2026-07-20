from fastapi import APIRouter

router = APIRouter()

@router.get("/health", response_model=dict)
async def health_check() -> dict:
    """
    Health check endpoint.
    Used by load balancers or Docker to ensure the API is running.
    """
    return {
        "status": "healthy",
        "message": "Spice AI Assistant API is running smoothly."
    }