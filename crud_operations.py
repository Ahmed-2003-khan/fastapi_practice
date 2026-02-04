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

# Helper function to find the index position of a post in the list
# This is needed for deletion since list.pop() requires an index
def find_index_post(id: int):
    # enumerate() provides both the index (i) and the value (p) while iterating
    # This is more efficient than manually tracking the index with a counter
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

@app.get("/posts")
def get_posts():
    return {"data": my_posts}

# Custom status code for POST endpoint
# 201 Created is the semantically correct status for successful resource creation
# This is more specific than the default 200 OK
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"data": post_dict}

@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    return {"data": post}

# DELETE endpoint to remove a post by ID
# RESTful convention: DELETE /posts/{id} removes a specific resource
@app.delete("/posts/{id}")
def delete_post(id: int):
    # Find the position of the post in the list
    index = find_index_post(id)
    
    # Remove the post at the found index
    # pop() removes and returns the element at the given index
    my_posts.pop(index)

    # Return a confirmation message
    # In production, you might return 204 No Content or the deleted resource
    return {"message": "post was deleted"}
