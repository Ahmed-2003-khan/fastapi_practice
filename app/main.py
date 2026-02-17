from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv
# time module is used for adding delays between connection retry attempts
import time

load_dotenv()


app = FastAPI()

my_posts = [{'title': 'title of post 1', 'content': 'content of post 1', 'id': 1}, {'title': 'title of post 2', 'content': 'content of post 2', 'id': 2}]

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    # Removed 'rating' field - simplified model to match database schema
    

# Connection retry loop - keeps trying until database is available
# This is useful when the database might not be ready immediately (e.g., in Docker containers)
while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password=os.getenv("DATABASE_PASSWORD"), cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful")
        # Break out of the loop once connection succeeds
        break
    except Exception as error:
        print("Connection to database failed")
        print("Error: ", error)
        # Wait 2 seconds before retrying to avoid overwhelming the database
        time.sleep(2)


def find_post(id: int):
    for post in my_posts:
        if post['id'] == id:
            return post

def find_index_post(id: int):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

# First endpoint to use real database queries instead of in-memory list
@app.get("/posts")
def get_posts():
    # cursor.execute() runs the SQL query on the database
    # SELECT * FROM posts retrieves all columns from all rows in the 'posts' table
    cursor.execute("SELECT * FROM posts")
    
    # fetchall() retrieves all rows returned by the query
    # RealDictCursor makes each row a dictionary: {'id': 1, 'title': '...', 'content': '...'}
    posts = cursor.fetchall()
    
    # Return the database results instead of the in-memory my_posts list
    return {"data": posts}

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

@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_post(id: int, post: Post):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {"data": my_posts}

