from jose import JWTError, jwt
from datetime import datetime, timedelta

# SECRET_KEY is used to sign the JWT - anyone with this key can forge tokens
# In production this MUST be stored in environment variables, never hardcoded
SECRET_KEY = "09239029120432048329482948329482344932vdvsdf7sdf7dsf7dsf7dsf7dsf7ddf"
# HS256 = HMAC + SHA-256 - a symmetric signing algorithm (same key to sign and verify)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    # Set token expiry time - tokens are invalid after this point
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # 'exp' is a standard JWT claim - libraries automatically validate it on decode
    to_encode.update({"exp": expire})
    # jwt.encode() signs the payload with the secret key and returns a JWT string
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt