from pydantic import BaseModel, EmailStr
from datetime import datetime

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# UserCreate is the REQUEST schema for registering a new user
# EmailStr (from pydantic[email]) validates that the value is a properly formatted email address
# password is a plain str here - hashing happens in the route logic (next step)
class UserCreate(BaseModel):
    email: EmailStr
    password: str

# UserOut is the RESPONSE schema for user endpoints
# It deliberately excludes password - never expose passwords in API responses
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True