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

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# PUT endpoint for updating (replacing) an entire resource
# PUT is used for full replacement - the client sends the complete updated resource
# HTTP 202 Accepted indicates the request was accepted but processing may not be complete
# Note: 200 OK is more common for synchronous updates; 202 is for async processing
@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_post(id: int, post: Post):
    # Find the index of the post to update
    index = find_index_post(id)
    
    # Validate that the resource exists before attempting to update
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    
    # Convert the Pydantic model to a dictionary
    post_dict = post.dict()
    
    # Preserve the ID from the URL path parameter
    # This ensures the ID cannot be changed through the request body
    # The URL is the source of truth for the resource identifier
    post_dict['id'] = id
    
    # Replace the entire resource at the specified index
    # This is a full replacement, not a partial update (which would be PATCH)
    my_posts[index] = post_dict
    
    # Return the updated collection
    # Better practice: return {"data": post_dict} to show only the updated resource
    return {"data": my_posts}

