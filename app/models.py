from .database import Base
from sqlalchemy import Column, Integer, String, Boolean

# Define the SQLAlchemy model for the "posts" table
# This class represents a table in our database
class Post(Base):
    # Specifies the name of the table in PostgreSQL
    __tablename__ = "posts"

    # Define the columns (fields) of the table
    # Integer as a primary key is automatically set to auto-increment by SQLAlchemy/PostgreSQL
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    # Boolean column with a default value of True
    published = Column(Boolean, nullable=False, default=True)


