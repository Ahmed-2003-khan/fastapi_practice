from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# The database URL for SQLAlchemy to connect to the PostgreSQL database
# Format: 'postgresql://[user]:[password]@[host]/[database_name]'
SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:ahmed785@localhost/fastapi'

# Create the engine that will talk to the database
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a session class that will be used to create specific database sessions
# Each session is a "conversation" with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# The base class for all our database models (tables)
# Our models will inherit from this Base class
Base = declarative_base()

