from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from pydantic import BaseModel
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from passlib.context import CryptContext
from typing import Optional
import os
import uuid

from ..database import get_session
from ..models.user import User
from ..dependencies import SECRET_KEY, ALGORITHM

router = APIRouter()

# Password hashing - use pbkdf2 which is more reliable on Windows
pwd_context = CryptContext(
    schemes=["pbkdf2_sha256"],
    deprecated="auto"
)


class SignUpRequest(BaseModel):
    email: str
    password: str
    name: Optional[str] = None


class SignInRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password."""
    if not hashed_password:
        return False
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        return False


def get_password_hash(password: str) -> str:
    """Hash a plain password."""
    # Ensure password is not longer than 72 bytes for bcrypt
    if len(password) > 72:
        password = password[:72]
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        # Default to 30 minutes if no expiration is provided
        expire = datetime.now(timezone.utc) + timedelta(minutes=30)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@router.post("/signup", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def signup(signup_data: SignUpRequest, db: Session = Depends(get_session)):
    """Register a new user and return an access token."""
    try:
        # Check if user already exists
        existing_user = db.exec(select(User).where(User.email == signup_data.email)).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this email already exists"
            )

        # Hash the password
        hashed_password = get_password_hash(signup_data.password)

        # Create new user
        user_id = f"user_{str(uuid.uuid4()).replace('-', '')}"  # Generate a unique ID
        user = User(
            id=user_id,
            email=signup_data.email,
            hashedPassword=hashed_password,
            name=signup_data.name
            # createdAt and updatedAt will be set by the database due to server_default
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        # Create access token
        access_token_expires = timedelta(minutes=10080)  # 7 days
        access_token = create_access_token(
            data={"sub": user.id},
            expires_delta=access_token_expires
        )

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }
    except Exception as e:
        print(f"Signup error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise e


@router.post("/signin", response_model=TokenResponse)
def signin(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_session)):
    """Authenticate user and return an access token."""
    # Find user by email
    user = db.exec(select(User).where(User.email == form_data.username)).first()
    if not user or not verify_password(form_data.password, user.hashedPassword or ""):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=10080)  # 7 days
    access_token = create_access_token(
        data={"sub": user.id},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }