# FastAPI is the main class that creates the web application instance
from fastapi import FastAPI
# Body is a special parameter class that tells FastAPI to extract data from the request body
from fastapi.params import Body

# Create the FastAPI application instance that will handle all HTTP requests
app = FastAPI()

# Define a GET endpoint at the root path "/"
# GET requests are used to retrieve data from the server
@app.get("/")
def root():
    return {"message": "Hello World"}

# Define a POST endpoint at "/createposts"
# POST requests are used to send data to the server to create or modify resources
@app.post("/createposts")
def create_posts(payload: dict = Body(...)):
    # The Body(...) parameter tells FastAPI to:
    # 1. Extract JSON data from the request body
    # 2. Parse it into a Python dictionary
    # 3. The ellipsis (...) marks this parameter as required
    
    # Print the received payload to the console for debugging and learning
    print(payload)
    
    # Return a JSON response confirming the operation
    # FastAPI automatically converts Python dictionaries to JSON
    return {"message": "Posts were created"}