import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

# Load .env file (only affects local development)
load_dotenv()

# 1. Get the Database URL from the environment (Render sets this automatically)
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# 2. If no URL is found (running locally), build it manually from .env variables
if not SQLALCHEMY_DATABASE_URL:
    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_SERVER = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
    POSTGRES_DB = os.getenv("POSTGRES_DB")
    
    SQLALCHEMY_DATABASE_URL = (
        f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@"
        f"{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )

# 3. FIX: Render/Heroku sometimes use "postgres://" but SQLAlchemy needs "postgresql://"
if SQLALCHEMY_DATABASE_URL and SQLALCHEMY_DATABASE_URL.startswith("postgres://"):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Create the SQLAlchemy Engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the Base class for models
Base = declarative_base()

# Dependency for database session management
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()