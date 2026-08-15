from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core import security
from app.core.config import settings
from app.models import User
from app.database import get_db
from app.repositories.user_repository import UserRepository

# OAuth2 scheme defining token URL for Swagger UI authorization
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """
    Dependency extracting JWT bearer token from request header,
    decoding token claims, and retrieving current user from DB.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # 1. Decode and verify JWT access token
    payload = security.verify_access_token(token)
    if payload is None:
        raise credentials_exception

    # 2. Extract user identifier (email) from token sub claim
    email: Optional[str] = payload.get("sub")
    if email is None:
        raise credentials_exception

    # 3. Retrieve user from repository
    user_repo = UserRepository(db)
    user = user_repo.get_by_email(email)
    if user is None:
        raise credentials_exception

    return user