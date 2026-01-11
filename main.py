from fastapi import FastAPI
from fastapi.params import Body

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.post("/createposts")
def create_posts(payload: dict = Body(...)):
    # Print the entire payload dictionary to see what data was received
    print(payload)
    
    # Access specific keys from the payload dictionary using bracket notation
    # payload['content'] retrieves the value associated with the 'content' key
    # payload['title'] retrieves the value associated with the 'title' key
    
    # Use f-strings (formatted string literals) to create dynamic responses
    # The f-prefix allows embedding expressions inside curly braces {}
    # This creates a personalized response echoing back the received data
    return {"message": f"content : {payload['content']}, title : {payload['title']}"}