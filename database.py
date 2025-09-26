# database.py
import os # <-- ADD THIS IMPORT
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Heroku provides the DATABASE_URL. If not found, we use our local SQLite DB.
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./booking.db")

# Heroku's postgres URL starts with 'postgres://', but SQLAlchemy needs 'postgresql://'
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Modify the engine creation
engine = create_engine(
    DATABASE_URL,
    # For SQLite only, we need connect_args. For Postgres, we don't.
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()