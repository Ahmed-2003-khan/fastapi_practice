from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from fastapi import Depends
import time
from . import models
from .database import engine, SessionLocal, get_db


models.Base.metadata.create_all(bind=engine)

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
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post, db: Session = Depends(get_db)):
    # Create a new SQLAlchemy model instance from the Pydantic request body
    # This is equivalent to: INSERT INTO posts (title, content, published) VALUES (...)
    new_post = models.Post(title=post.title, content=post.content, published=post.published)
    
    # db.add() stages the new object - tells SQLAlchemy to track this new record
    db.add(new_post)
    
    # db.commit() writes the changes to the database permanently (equivalent to conn.commit())
    db.commit()
    
    # db.refresh() re-fetches the row from the database after the commit
    # This is essential to get server-generated values like id and created_at
    # Without this, new_post would still have None for those fields
    db.refresh(new_post)
    
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

