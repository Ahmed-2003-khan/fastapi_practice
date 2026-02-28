from pydantic import BaseModel
from datetime import datetime

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

# Post is the response schema - note it only exposes id and created_at
# This demonstrates that response_model acts as a FILTER:
# even if the ORM object has title, content, published - they won't be sent
# unless explicitly defined here. You control the exact API surface.
class Post(BaseModel):
    id: int
    created_at: datetime

    # from_attributes = True allows Pydantic to read from SQLAlchemy ORM object attributes
    class Config:
        from_attributes = True