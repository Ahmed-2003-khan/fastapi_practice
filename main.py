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

@app.post("/posts")
def create_posts(post: Post):
    print(post.rating)
    print(post.dict())
    return {"message": "post created"}