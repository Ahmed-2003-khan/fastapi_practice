from .database import Base
from sqlalchemy import Column, Integer, String, Boolean
# TIMESTAMP allows us to store time-based data, and timezone=True ensures it's stored with timezone info
from sqlalchemy.sql.sqltypes import TIMESTAMP
# func allows us to call SQL functions like now() directly from our Python code
from sqlalchemy.sql import func

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    # server_default tells the database to set the default value in the schema itself (PostgreSQL side)
    published = Column(Boolean, nullable=False, server_default='TRUE')
    # created_at uses server_default=func.now() to automatically timestamp the row when created in the DB
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())


