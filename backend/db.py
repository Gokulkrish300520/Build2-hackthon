
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
import os

# Use environment variable for Railway PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///backend/wildlife.db")

# For PostgreSQL, no need for 'check_same_thread'
if DATABASE_URL.startswith("sqlite"):
	engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
	engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)
