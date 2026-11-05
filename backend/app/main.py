from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.endpoints import api_router

from app.database.session import engine, Base 
from app.database.models import user, chat, document, product

def get_application() -> FastAPI:
    """
    Factory function to initialize the FastAPI application.
    """
    Base.metadata.create_all(bind=engine)

    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        openapi_url=f"{settings.API_V1_STR}/openapi.json"
    )

    # Set up CORS middleware to allow the frontend to communicate with the API
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["https://spice-ai-assistant.vercel.app"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Mount the API router
    app.include_router(api_router, prefix=settings.API_V1_STR)

    return app

app = get_application()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)