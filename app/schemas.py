from pydantic import BaseModel

# schemas.py defines Pydantic models (schemas) that handle request validation and response serialization
# This is intentionally separate from models.py (SQLAlchemy) to follow separation of concerns:
# - models.py = database table structure (SQLAlchemy)
# - schemas.py = API input/output shape (Pydantic)
class Post(BaseModel):
    title: str
    content: str
    published: bool = True