from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    return pwd_context.hash(password)

# verify() compares a plain text password against a stored bcrypt hash
# pwd_context.verify() handles the bcrypt comparison securely (constant-time)
def verify(password: str, hashed_password: str):
    return pwd_context.verify(password, hashed_password)
