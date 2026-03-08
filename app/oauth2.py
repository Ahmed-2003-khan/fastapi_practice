from jose import JWTError, jwt                          # python-jose: handles JWT encoding/decoding
from datetime import datetime, timedelta                # used to set token expiry time
from . import schemas, models                           # schemas for TokenData, models for User DB table
from fastapi import Depends, HTTPException, status      # Depends = dependency injection, HTTPException = raise HTTP errors
from fastapi.security import OAuth2PasswordBearer       # extracts Bearer token from Authorization header automatically
from .database import get_db                            # DB session dependency
from sqlalchemy.orm import Session

# tokenUrl="login" tells Swagger UI where to send credentials to get a token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# NEVER hardcode SECRET_KEY in production — use environment variables instead
SECRET_KEY = "09239029120432048329482948329482344932vdvsdf7sdf7dsf7dsf7dsf7dsf7ddf"
ALGORITHM = "HS256"                                     # HS256 = HMAC-SHA256, a symmetric signing algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = 60                        # token expires after 60 minutes of inactivity

def create_access_token(data: dict):
    to_encode = data.copy()                             # copy so we don't mutate the original dict
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})                   # "exp" is a standard JWT claim for expiry
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)  # sign the payload → JWT string
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        # jwt.decode validates signature + expiry; raises JWTError if invalid or expired
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: int = payload.get("user_id")                # extract our custom "user_id" claim from the payload
        if id is None:
            raise credentials_exception                 # token exists but has no user_id → invalid
        token_data = schemas.TokenData(id=id)           # wrap id in a Pydantic model for type safety
    except JWTError:
        raise credentials_exception                     # signature mismatch, expired, or malformed token
    
    return token_data                                   # return TokenData(id=...) to the caller

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    # This function is a FastAPI dependency — any route with Depends(get_current_user) calls this automatically
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    # verify_access_token extracts the user_id from the token and returns TokenData
    token = verify_access_token(token, credentials_exception)
    # Fetch the full User object from DB using the id stored in the token
    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user                                         # returning the User ORM object makes it available in the route