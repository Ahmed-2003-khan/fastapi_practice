from fastapi import FastAPI
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

# find_post is a utility function to search through our data collection
# It abstracts the search logic from the request handling path
def find_post(id: int):
    # Iterate through the list of posts to find a match by ID
    for post in my_posts:
        if post['id'] == id:
            return post
    # If no match is found, the function implicitly returns None

@app.get("/posts")
def get_posts():
    return {"data": my_posts}

@app.post("/posts")
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"data": post_dict}

# Path parameters like {id} allow capturing dynamic segments of a URL
# FastAPI automatically handles type conversion based on the function signature
@app.get("/posts/{id}")
def get_post(id: int):
    # Pass the captured id to our search helper
    # The 'id' variable is already an integer thanks to FastAPI's type hint
    post = find_post(id)
    # Return the specific resource or None if not found
    return {"data": post}