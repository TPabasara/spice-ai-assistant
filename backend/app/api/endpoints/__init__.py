from fastapi import APIRouter
from app.api.endpoints import health, auth, documents, chat, analytics, products

# Create a main router for API v1
api_router = APIRouter()

# Mount all individual endpoint routers
api_router.include_router(health.router, prefix="/system", tags=["System"])
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(documents.router, prefix="/documents", tags=["RAG Documents"])
api_router.include_router(chat.router, prefix="/chat", tags=["AI Chatbot"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["Admin Analytics"])
api_router.include_router(products.router, prefix="/products", tags=["Products"])
