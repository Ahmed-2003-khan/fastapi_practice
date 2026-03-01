from .database import Base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql import func

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, nullable=False, server_default='TRUE')
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())


# User model - the foundation for user authentication
# email is unique to ensure one account per email address
class User(Base):
    __tablename__ = "users"

    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    id = Column(Integer, primary_key=True, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())