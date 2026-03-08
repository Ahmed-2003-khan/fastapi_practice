# Relationship: One User → Many Posts (one-to-many)
# The FK (owner_id) lives on the "many" side (posts table) — this is always the rule in SQL
# SQLAlchemy can also set up relationship() objects to navigate between models in Python code
from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey  # ForeignKey: creates a DB-level link between tables
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql import func

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, nullable=False, server_default='TRUE')
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    # owner_id creates a FK constraint: every post MUST belong to an existing user
    # ondelete="CASCADE" → if the user is deleted, all their posts are automatically deleted too
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())