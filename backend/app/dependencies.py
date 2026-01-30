from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Optional

import auth
import models
from database import get_db

# Defines the token endpoint for Swagger UI
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    """
    Dependency that extracts the JWT token, validates it,
    and retrieves the corresponding user from the database.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Verify token signature and expiration
    payload = auth.verify_access_token(token)
    if payload is None:
        raise credentials_exception

    # Extract user identifier (email) from payload
    email: Optional[str] = payload.get("sub")
    if email is None:
        raise credentials_exception

    # Retrieve user from database
    user = db.query(models.User).filter(models.User.email == email).first()
    if user is None:
        raise credentials_exception

    return user