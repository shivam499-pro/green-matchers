# services/auth.py
from datetime import datetime, timedelta
from typing import Optional
import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from ..config import settings
from ..models.user import User

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

class AuthService:
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        try:
            return pwd_context.verify(plain_password, hashed_password)
        except Exception:
            return False

    @staticmethod
    def get_password_hash(password: str) -> str:
        """Hash a password"""
        return pwd_context.hash(password)

    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
        """Create JWT access token"""
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.access_token_expire_minutes))
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)

    @staticmethod
    def verify_token(token: str) -> Optional[str]:
        """Verify JWT token and return username"""
        try:
            payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
            username: str = payload.get("sub")
            return username
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    @staticmethod
    def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
        """Authenticate user with username and password"""
        user = db.query(User).filter(User.username == username).first()
        if not user:
            return None
        if not AuthService.verify_password(password, user.password):
            return None
        return user

    @staticmethod
    def get_current_user(db: Session, token: str) -> Optional[User]:
        """Get current user from JWT token"""
        username = AuthService.verify_token(token)
        if not username:
            return None
        user = db.query(User).filter(User.username == username).first()
        return user

    @staticmethod
    def update_last_login(db: Session, user: User):
        """Update user's last login timestamp"""
        user.last_login = datetime.utcnow()
        db.commit()