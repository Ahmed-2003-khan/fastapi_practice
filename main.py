from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.post("/createposts")
def create_posts(post: Post):
    # Access a single attribute using dot notation
    print(post.rating)
    
    # Convert the entire Pydantic model instance into a standard Python dictionary
    # The .dict() method extracts all data fields into a key-value format
    # This is extremely useful for database operations or further data processing
    # Note: In newer Pydantic versions (v2), the preferred method is .model_dump()
    print(post.dict())
    
    return {"message": "post created"}