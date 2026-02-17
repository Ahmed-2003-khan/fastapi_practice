from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:ahmed785@localhost/fastapi'

engine = create_engine(SQLALCHEMY_DATABASE_URL)