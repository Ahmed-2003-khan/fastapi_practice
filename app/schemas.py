from pydantic import BaseModel

# Base/generic schema for Post - used as a shared base or for general typing
class Post(BaseModel):
    title: str
    content: str
    published: bool = True

# Dedicated schema for POST /posts - defines what fields are required when creating a post
# Having a separate CreatePost schema allows future flexibility
# (e.g. some fields might be auto-generated and not needed in the request)
class CreatePost(BaseModel):
    title: str
    content: str
    published: bool = True

# Dedicated schema for PUT /posts/{id} - defines what fields are accepted when updating
# Note: published has no default here, making it required for a full update (PUT)
# Separating update schema from create allows each to evolve independently
class UpdatePost(BaseModel):
    title: str
    content: str
    published: bool
