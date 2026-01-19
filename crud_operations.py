from fastapi import FastAPI, Response, status
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()

my_posts = [{'title': 'title of post 1', 'content': 'content of post 1', 'id': 1}, {'title': 'title of post 2', 'content': 'content of post 2', 'id': 2}]

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

def find_post(id: int):
    for post in my_posts:
        if post['id'] == id:
            return post

@app.get("/posts")
def get_posts():
    return {"data": my_posts}

@app.post("/posts")
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"data": post_dict}

# The Response object allows for manual control over HTTP response headers and status codes
# The status module provides human-readable constants for standard HTTP status codes
@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    post = find_post(id)
    # Check if the resource was found
    if not post:
        # Manually set the HTTP status code to 404 (Not Found)
        # Using status.HTTP_404_NOT_FOUND is more readable than hardcoding 404
        response.status_code = status.HTTP_404_NOT_FOUND
        # Return a descriptive error message to help the client understand what went wrong
        return {"message": "post not found"}
    # If found, the default status code is 200 (OK)
    return {"data": post}