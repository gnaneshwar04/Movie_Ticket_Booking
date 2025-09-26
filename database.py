from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define the database URL. For SQLite, this is the path to the database file.
# "./booking.db" means the file will be created in the same directory as your project.
SQLALCHEMY_DATABASE_URL = "sqlite:///./booking.db"

# Create the SQLAlchemy engine. The engine is the entry point to the database.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
# The connect_args is needed only for SQLite to allow multiple threads to interact with the database.

# Create a SessionLocal class. Each instance of a SessionLocal class will be a database session.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a Base class. Our database models will inherit from this class.
Base = declarative_base()