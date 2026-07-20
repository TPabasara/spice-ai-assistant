from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

def test_user_registration_and_login_flow(client: TestClient, db_session: Session):
    """
    Validates that a new visitor can register an account, secure their payload, 
    and exchange credentials for an authentic JWT access bearer token.
    """
    registration_payload = {
        "email": "tester@spicecraft.com",
        "password": "SecurePassword123",
        "full_name": "QA Automation Engineer"
    }

    # 1. Test registration endpoint
    reg_response = client.post("/api/v1/auth/register", json=registration_payload)
    assert reg_response.status_code == 200
    data = reg_response.json()
    assert data["email"] == registration_payload["email"]
    assert "id" in data
    assert "hashed_password" not in data  # Double check data leak protection

    # 2. Test login endpoint exchanging credentials for a token
    login_payload = {
        "username": registration_payload["email"],
        "password": registration_payload["password"]
    }
    login_response = client.post("/api/v1/auth/login", data=login_payload)
    assert login_response.status_code == 200
    token_data = login_response.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"