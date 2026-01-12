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

# RESTful endpoint naming convention
# Use resource names (nouns) rather than action names (verbs)
# The HTTP method (POST) already indicates the action (create)
# This follows REST principles: POST /posts creates a post
@app.post("/posts")
def create_posts(post: Post):
    print(post.rating)
    print(post.dict())
    return {"message": "post created"}