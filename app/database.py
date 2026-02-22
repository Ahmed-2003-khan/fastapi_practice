from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:ahmed785@localhost/fastapi'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# get_db is defined here in database.py (not in main.py) to follow separation of concerns
# Any module that needs a database session can import get_db from here
def get_db():
    db = SessionLocal()
    try:
        # yield makes this a generator - FastAPI calls the code before yield to get the session
        yield db
    finally:
        # Code after yield runs after the request is complete, ensuring the session is always closed
        db.close()
