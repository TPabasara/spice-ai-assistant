import pytest
from typing import Generator
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database.session import Base, get_db

# Use an isolated test database URL (e.g., an alternate local postgres instance)
TEST_DATABASE_URL = "postgresql://user:password@localhost:5432/spicedb_test"

engine = create_engine(TEST_DATABASE_URL, pool_pre_ping=True)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session", autouse=True)
def setup_test_database() -> Generator:
    """
    Creates the database tables once at the start of the testing execution lifecycle 
    and drops them entirely when all tests conclude.
    """
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db_session() -> Generator:
    """
    Provides an isolated transaction context per test.
    Rolls back changes automatically to ensure tests do not leak state to one another.
    """
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def client(db_session) -> Generator[TestClient, None, None]:
    """
    Generates a test client with overridden database dependencies.
    All runtime API requests will target the isolated test database session context.
    """
    def _get_test_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()