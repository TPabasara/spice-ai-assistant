from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.core.config import settings

# Create the SQLAlchemy engine using our validated database URL
# pool_pre_ping=True checks connection health before utilizing it
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    echo=False  # Set to True during debugging to see raw SQL queries
)

# SessionLocal will be instantiated per HTTP request
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    """
    Base class for all SQLAlchemy declarative models.
    Every model will inherit from this class.
    """
    pass

def get_db() -> Generator:
    """
    FastAPI Dependency that provides an isolated database session per request.
    Ensures the session is cleanly closed after the request lifecycle completes.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()