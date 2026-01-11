from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
# Optional is a type hint that indicates a field can be None or the specified type
from typing import Optional

app = FastAPI()

class Post(BaseModel):
    # Required fields - must be provided in the request or validation fails
    title: str
    content: str
    
    # Optional field with a default value
    # If 'published' is not provided in the request, it defaults to True
    # The client can override this by explicitly sending published: false
    published: bool = True
    
    # Optional field that can be None
    # Optional[int] means the field accepts an integer OR None
    # Setting default to None makes this field completely optional
    # If not provided, rating will be None
    rating: Optional[int] = None

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.post("/createposts")
def create_posts(post: Post):
    # Access individual fields using dot notation
    # Since rating is Optional, it could be an int or None
    print(post.rating)
    return {"message": "post created"}