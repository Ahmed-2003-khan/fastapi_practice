from pydantic import BaseModel

# PostBase holds shared fields common to all Post schemas
# It acts as the single source of truth for field definitions
# Other schemas inherit from it so changes only need to be made in one place
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

# PostCreate inherits all fields from PostBase
# Using 'pass' means it adds no new fields - it's a dedicated schema for POST requests
# Having a separate class allows future modification (e.g. adding extra create-only fields)
# without breaking other schemas that extend PostBase
class PostCreate(PostBase):
    pass
