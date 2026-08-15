from typing import Optional
from sqlalchemy.orm import Session
from app.models import User
from app.schemas import UserCreate


class UserRepository:
    """Repository encapsulating database operations for the User model."""

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: int) -> Optional[User]:
        """Retrieves a user by primary key ID."""
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_email(self, email: str) -> Optional[User]:
        """Retrieves a user by email address."""
        return self.db.query(User).filter(User.email == email).first()

    def get_by_username(self, username: str) -> Optional[User]:
        """Retrieves a user by username."""
        return self.db.query(User).filter(User.username == username).first()

    def create(self, user_create: UserCreate, hashed_password: str) -> User:
        """Persists a new user record in the database."""
        db_user = User(
            username=user_create.username,
            email=user_create.email,
            hashed_password=hashed_password
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
