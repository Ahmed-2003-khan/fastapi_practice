from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv
# Session from sqlalchemy.orm provides type hinting for the database session object
from sqlalchemy.orm import Session
# Depends is used for dependency injection in FastAPI, allowing us to share common logic (like database connections)
from fastapi import Depends
import time
from . import models
from .database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

load_dotenv()


app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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

# Test route to verify the database dependency injection
# db: Session = Depends(get_db) performs several tasks:
# 1. Calls get_db() to create a new database session
# 2. Injects that session into the 'db' parameter
# 3. Ensures the session is closed after the request is finished (via the finally block in get_db)
@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    # At this point, 'db' is a live SQLAlchemy session ready for ORM queries
    return {"message": "Hello World"}

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

@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("SELECT * FROM posts WHERE id = %s", (str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    return {"data": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT, content=str(deleted_post))


@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_post(id: int, post: Post):
    cursor.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *", (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    return {"data": updated_post}

