from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

db_url = settings.sqlalchemy_database_url
connect_args = {}

if db_url.startswith("sqlite"):
    connect_args["check_same_thread"] = False

# Create SQLAlchemy Engine with connection pre-ping for reliability
engine = create_engine(
    db_url,
    connect_args=connect_args,
    pool_pre_ping=True
)

# Session factory for generating database sessions per request
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declarative Base class for SQLAlchemy ORM models
Base = declarative_base()


def get_db():
    """
    Dependency providing a transactional SQLAlchemy database session.
    Ensures session closure after request handling.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()