from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

# psycopg2 is the most popular PostgreSQL adapter for Python
# It allows Python applications to connect to and interact with PostgreSQL databases
import psycopg2

# RealDictCursor returns query results as dictionaries instead of tuples
# This makes it easier to work with column names: row['id'] instead of row[0]
from psycopg2.extras import RealDictCursor

import os

# python-dotenv loads environment variables from a .env file
# This keeps sensitive data (passwords, API keys) out of source code
from dotenv import load_dotenv

# Load environment variables from .env file in the project root
# This should be called before accessing any environment variables
load_dotenv()


app = FastAPI()

my_posts = [{'title': 'title of post 1', 'content': 'content of post 1', 'id': 1}, {'title': 'title of post 2', 'content': 'content of post 2', 'id': 2}]

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None
    
# Establish connection to PostgreSQL database
# This runs at application startup (module level)
try:
    # psycopg2.connect() creates a connection to the database
    # Parameters:
    # - host: database server location ('localhost' for local development)
    # - database: name of the database to connect to
    # - user: PostgreSQL username
    # - password: retrieved from environment variable for security
    # - cursor_factory: RealDictCursor makes results dict-like instead of tuples
    conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password=os.getenv("DATABASE_PASSWORD"), cursor_factory=RealDictCursor)
    
    # Cursor is used to execute SQL queries and fetch results
    # Think of it as a pointer that moves through query results
    cursor = conn.cursor()
    print("Database connection was successful")
except Exception as error:
    # Catch any connection errors (wrong password, database doesn't exist, etc.)
    print("Connection to database failed")
    print("Error: ", error)

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

@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_post(id: int, post: Post):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {"data": my_posts}

