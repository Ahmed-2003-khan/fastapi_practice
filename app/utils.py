from passlib.context import CryptContext

# utils.py holds reusable helper functions for the application
# Keeping these separate from main.py follows the Single Responsibility Principle

# CryptContext configured with bcrypt for secure password hashing
# Requires bcrypt==4.0.1 (bcrypt 5.x is incompatible with passlib 1.7.4)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# hash() wraps pwd_context.hash() to provide a clean, importable utility
# Usage: hashed_password = utils.hash(plain_text_password)
def hash(password: str):
    return pwd_context.hash(password)