from fastapi import APIRouter, Depends, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import schemas
from app.core.config import settings
from app.core.limiter import limiter
from app.database import get_db
from app.services.auth_service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit(settings.AUTH_RATE_LIMIT)
def register(
    request: Request,
    user_create: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    """
    Registers a new user account with validated credentials.
    """
    auth_service = AuthService(db)
    return auth_service.register_user(user_create)


@router.post("/login")
@limiter.limit(settings.AUTH_RATE_LIMIT)
def login(
    request: Request,
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Authenticates user credentials and issues a JWT bearer access token.
    """
    auth_service = AuthService(db)
    user = auth_service.authenticate_user(user_credentials.username, user_credentials.password)
    return auth_service.create_access_token(user)