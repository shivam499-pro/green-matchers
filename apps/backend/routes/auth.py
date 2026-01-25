# routes/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import Optional

from ..models.database import get_db
from ..models.user import User
from ..services.auth import AuthService

router = APIRouter()

# Pydantic models for request/response
class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str
    full_name: str
    role: str = "job_seeker"
    phone_number: Optional[str] = None

class UserLogin(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: dict

class UserResponse(BaseModel):
    message: str
    user_id: int
    access_token: str
    token_type: str
    role: str

@router.post("/register", response_model=UserResponse)
async def register_user(
    user_data: UserRegister,
    db: Session = Depends(get_db)
):
    """User registration with role-based accounts"""
    # Check if user already exists
    existing_user = db.query(User).filter(
        (User.username == user_data.username) | (User.email == user_data.email)
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already exists"
        )

    # Hash password
    try:
        hashed_password = AuthService.get_password_hash(user_data.password)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password processing failed"
        )

    # Create new user
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        password=hashed_password,
        full_name=user_data.full_name,
        role=user_data.role,
        phone_number=user_data.phone_number
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Create access token
    access_token = AuthService.create_access_token(data={"sub": new_user.username})

    return UserResponse(
        message="User registered successfully",
        user_id=new_user.user_id,
        access_token=access_token,
        token_type="bearer",
        role=new_user.role
    )

@router.post("/login", response_model=TokenResponse)
async def login_user(
    user_data: UserLogin,
    db: Session = Depends(get_db)
):
    """User login with JWT token"""
    # Authenticate user
    user = AuthService.authenticate_user(db, user_data.username, user_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Update last login
    AuthService.update_last_login(db, user)

    # Create token
    access_token = AuthService.create_access_token(data={"sub": user.username})

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user={
            "user_id": user.user_id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "is_verified": user.is_verified
        }
    )

@router.post("/token", response_model=TokenResponse)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """OAuth2 compatible token endpoint"""
    user = AuthService.authenticate_user(db, form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Update last login
    AuthService.update_last_login(db, user)

    access_token = AuthService.create_access_token(data={"sub": user.username})

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user={
            "user_id": user.user_id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "is_verified": user.is_verified
        }
    )