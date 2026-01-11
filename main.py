from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.post("/createposts")
def create_posts(post: Post):
    print(post)
    # Return a confirmation message to the client
    # The response message confirms the operation completed successfully
    return {"message": "post createds"}