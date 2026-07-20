from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):
    """
    Application configuration strictly validated by Pydantic.
    Reads from environment variables or a .env file.
    """
    PROJECT_NAME: str = "Spice AI Assistant API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # CORS Configuration
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000"] # Next.js default port
    
    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/spicedb"
    
    # Security
    SECRET_KEY: str = "your-super-secret-key-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8 # 8 days
    
    # AI Credentials
    GEMINI_API_KEY: str = ""

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

# Instantiate settings to be imported across the app
settings = Settings()