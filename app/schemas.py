from pydantic import BaseModel
from datetime import datetime

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

# Post response schema now inherits from PostBase instead of BaseModel
# This means it automatically includes title, content, published from PostBase
# PLUS adds the server-generated fields id and created_at
# Result: clients receive the full post data in every response
class Post(PostBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True