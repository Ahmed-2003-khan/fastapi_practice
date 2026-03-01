from fastapi import FastAPI
from . import models
from .database import engine
# Import router modules - each handles its own routes, schemas, and db logic
from .routers import post, user

# Create all tables defined in models.py if they don't already exist
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Register routers - FastAPI mounts all their routes onto the main app
app.include_router(post.router)
app.include_router(user.router)

@app.get("/")
def root():
    return {"message": "Hello World"}