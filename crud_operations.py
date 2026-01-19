from fastapi import FastAPI, Response, status, HTTPException
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

# HTTPException is the preferred way to handle errors in FastAPI
# It allows us to interrupt the normal request flow and return an error response immediately
@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id)
    if not post:
        # Raising an exception is cleaner than manually editing the Response object
        # It automatically handles the status code and error detail format
        # This keeps the route signature simple and focused on the happy path
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    # If no exception is raised, FastAPI continues and returns the found resource
    return {"data": post}