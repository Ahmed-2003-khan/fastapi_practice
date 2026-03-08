from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# UserOut is defined BEFORE Post so that Post.owner can reference it (Python reads top-to-bottom)
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


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut  # nested Pydantic model — Pydantic serializes the related User object into this shape automatically

    class Config:
        from_attributes = True  # required so Pydantic can read post.owner (an ORM object) not just plain dicts


