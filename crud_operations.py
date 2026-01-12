from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# In-memory data storage using a Python list
# This simulates a database for learning purposes
# In production, you would use a real database (PostgreSQL, MongoDB, etc.)
# Each post is a dictionary with title, content, and a unique id
my_posts = [{'title': 'title of post 1', 'content': 'content of post 1', 'id': 1}, {'title': 'title of post 2', 'content': 'content of post 2', 'id': 2}]

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

# GET endpoint to retrieve all posts
# RESTful convention: GET /posts returns a collection of resources
@app.get("/posts")
def get_posts():
    # Return all posts wrapped in a data object
    # This is a common pattern for API responses
    return {"data": my_posts}

# POST endpoint to create a new post
# RESTful convention: POST /posts creates a new resource
@app.post("/posts")
def create_posts(post: Post):
    # In a real application, you would:
    # 1. Convert the Pydantic model to a dict
    # 2. Add a unique ID
    # 3. Append to the database/list
    # 4. Return the created resource
    return {"data": "post created"}