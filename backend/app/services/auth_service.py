from datetime import timedelta
from typing import Dict, Any
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models import User
from app.schemas import UserCreate
from app.repositories.user_repository import UserRepository
from app.core import security
from app.core.config import settings


class AuthService:
    """Service encapsulating user registration, authentication, and JWT issuing."""

    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)

    def register_user(self, user_create: UserCreate) -> User:
        """Validates user uniqueness and registers a new user with an Argon2 password hash."""
        # 1. Validate email uniqueness
        if self.user_repo.get_by_email(user_create.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email is already registered"
            )

        # 2. Validate username uniqueness
        if self.user_repo.get_by_username(user_create.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username is already taken"
            )

        # 3. Hash password and persist user
        hashed_password = security.get_password_hash(user_create.password)
        return self.user_repo.create(user_create, hashed_password)

    def authenticate_user(self, username_or_email: str, password: str) -> User:
        """Authenticates user credentials by checking email or username."""
        # Try finding user by email first
        user = self.user_repo.get_by_email(username_or_email)

        # If not found by email, try username
        if not user:
            user = self.user_repo.get_by_username(username_or_email)

        # Verify existence and password match
        if not user or not security.verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return user

    def create_access_token(self, user: User) -> Dict[str, str]:
        """Generates a bearer JWT access token for an authenticated user."""
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        token = security.create_access_token(
            data={"sub": user.email},
            expires_delta=access_token_expires
        )
        return {"access_token": token, "token_type": "bearer"}
