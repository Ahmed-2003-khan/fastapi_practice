from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv
import time

load_dotenv()


app = FastAPI()

my_posts = [{'title': 'title of post 1', 'content': 'content of post 1', 'id': 1}, {'title': 'title of post 2', 'content': 'content of post 2', 'id': 2}]

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password=os.getenv("DATABASE_PASSWORD"), cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful")
        break
    except Exception as error:
        print("Connection to database failed")
        print("Error: ", error)
        time.sleep(2)


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
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *", (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}

# GET single post by ID - now using database instead of in-memory list
@app.get("/posts/{id}")
def get_post(id: int):
    # SELECT with WHERE clause to filter by specific id
    # str(id) converts the integer to string for the parameterized query
    cursor.execute("SELECT * FROM posts WHERE id = %s", (str(id),))
    
    # fetchone() returns None if no matching row is found
    post = cursor.fetchone()
    
    # Check if post exists before returning
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    return {"data": post}


# DELETE endpoint - now using database instead of in-memory list
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # DELETE FROM removes rows matching the WHERE condition
    # RETURNING * returns the deleted row so we can check if anything was deleted
    cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (str(id),))
    
    # fetchone() returns the deleted row, or None if no row was deleted
    deleted_post = cursor.fetchone()
    
    # Commit the transaction to persist the deletion
    conn.commit()
    
    # If nothing was deleted, the post didn't exist
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    
    # 204 No Content should have an empty body, but we're including the deleted post for debugging
    # In production, you might want to return just Response(status_code=status.HTTP_204_NO_CONTENT)
    return Response(status_code=status.HTTP_204_NO_CONTENT, content=str(deleted_post))


# UPDATE endpoint - now using database instead of in-memory list
@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_post(id: int, post: Post):
    # UPDATE posts SET updates the specified columns
    # Multiple columns are updated: title, content, published
    # WHERE id = %s ensures only the specified post is updated
    # RETURNING * returns the updated row
    cursor.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *", (post.title, post.content, post.published, str(id)))
    
    # fetchone() returns the updated row, or None if no row was updated
    updated_post = cursor.fetchone()
    
    # Commit the transaction to persist the update
    conn.commit()
    
    # If nothing was updated, the post didn't exist
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    
    # Return the updated post with all its current values
    return {"data": updated_post}

# 🎉 MIGRATION COMPLETE! All CRUD operations now use PostgreSQL instead of in-memory storage
# The my_posts list and helper functions (find_post, find_index_post) are no longer used

