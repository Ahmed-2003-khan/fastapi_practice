from fastapi import FastAPI
from fastapi.params import Body
# BaseModel is Pydantic's base class for creating data validation schemas
from pydantic import BaseModel

app = FastAPI()

# Define a Pydantic model to represent the structure of a Post
# This serves as both documentation and validation for incoming requests
class Post(BaseModel):
    # Type hints define what data type each field should be
    # Pydantic will automatically validate that 'title' is a string
    title: str
    # Similarly, 'content' must be a string or the request will be rejected
    content: str
    # Benefits: automatic validation, type checking, and auto-generated API docs

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.post("/createposts")
# Instead of a raw dict, use the Post model as the parameter type
# FastAPI automatically:
# 1. Parses the JSON request body
# 2. Validates it against the Post schema
# 3. Converts it to a Post object
# 4. Returns a 422 error if validation fails
def create_posts(post: Post):
    # 'post' is now a Post object with validated attributes
    # Access fields with dot notation: post.title, post.content
    print(post)
    return {"message": "post created"}