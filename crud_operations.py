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

def find_index_post(id: int):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

@app.get("/posts")
def get_posts():
    return {"data": my_posts}

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

# DELETE endpoint with proper HTTP semantics
# 204 No Content is the standard status code for successful DELETE operations
# It indicates success but that there's no content to return in the response body
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # Find the index of the post to delete
    index = find_index_post(id)
    
    # Validate that the post exists before attempting deletion
    # index will be None if no matching post is found
    # Using == None instead of 'is None' works but 'is None' is more Pythonic
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    
    # Remove the post from the list
    my_posts.pop(index)
    
    # Return an empty Response with 204 status
    # 204 No Content means success but no response body should be sent
    # This is semantically correct for DELETE operations
    return Response(status_code=status.HTTP_204_NO_CONTENT)
