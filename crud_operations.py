from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
# randrange generates random integers within a specified range
# Used here to create unique IDs for posts
from random import randrange

app = FastAPI()

my_posts = [{'title': 'title of post 1', 'content': 'content of post 1', 'id': 1}, {'title': 'title of post 2', 'content': 'content of post 2', 'id': 2}]

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

@app.get("/posts")
def get_posts():
    return {"data": my_posts}

@app.post("/posts")
def create_posts(post: Post):
    # Step 1: Convert the Pydantic model to a dictionary
    # This allows us to manipulate the data and add additional fields
    post_dict = post.dict()
    
    # Step 2: Generate a unique ID for the new post
    # randrange(0, 1000000) creates a random integer between 0 and 999,999
    # In production, databases handle ID generation automatically
    post_dict['id'] = randrange(0, 1000000)
    
    # Step 3: Persist the data by appending to our in-memory list
    # This simulates saving to a database
    my_posts.append(post_dict)
    
    # Step 4: Return the created resource with its ID
    # RESTful best practice: return the complete created object
    # This confirms to the client what was actually saved
    return {"data": post_dict}