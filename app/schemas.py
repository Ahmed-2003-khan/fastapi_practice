from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# PostBase holds the fields the CLIENT sends when creating/updating a post
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

# PostCreate inherits PostBase — no extra fields needed from client on creation
class PostCreate(PostBase):
    pass

# Post is the RESPONSE schema — includes server-generated fields (id, created_at, owner_id)
# owner_id is now included so the API consumer knows which user created each post
class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int  # exposes the FK value in the API response, so clients can filter posts by owner

    class Config:
        from_attributes = True  # allows Pydantic to read data from SQLAlchemy ORM objects (not just dicts)

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None
