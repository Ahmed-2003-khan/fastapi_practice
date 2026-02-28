from pydantic import BaseModel
# datetime is imported to properly type-hint timestamp fields from the database
from datetime import datetime

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

# Post is the response schema - defines exactly what the API returns to the client
# It includes server-generated fields (id, created_at) that clients receive but never send
class Post(BaseModel):
    id: int            # auto-generated primary key from PostgreSQL
    title: str
    content: str
    published: bool
    created_at: datetime   # auto-set by server_default=func.now() in the database

    # from_attributes = True enables Pydantic to read from SQLAlchemy ORM object attributes
    # This is how FastAPI bridges response_model with ORM objects
    class Config:
        from_attributes = True