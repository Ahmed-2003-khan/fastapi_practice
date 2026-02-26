from pydantic import BaseModel

# PostBase defines shared input fields for creating and updating posts
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

# PostCreate is used for validating incoming POST/PUT request bodies
# Inherits all fields from PostBase via 'pass'
class PostCreate(PostBase):
    pass

# Post is the RESPONSE schema - controls what fields are returned to the client
# It intentionally does NOT inherit PostBase; it's a separate contract for output
class Post(BaseModel):
    title: str
    content: str
    published: bool

    # Config class tells Pydantic how to read the data
    # from_attributes = True (formerly orm_mode = True in Pydantic v1) allows Pydantic to
    # read data from SQLAlchemy ORM object attributes (e.g. post.title) instead of dict keys
    # Without this, FastAPI cannot serialize ORM objects and will throw a validation error
    class Config:
        from_attributes = True