from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# Shared properties
class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None

# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str

# Properties to return to the client (Notice: No password field!)
class UserResponse(UserBase):
    id: int
    is_active: bool
    is_admin: bool
    created_at: datetime

    class Config:
        from_attributes = True  # Allows Pydantic to read from SQLAlchemy ORM models

# Token schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    sub: Optional[str] = None