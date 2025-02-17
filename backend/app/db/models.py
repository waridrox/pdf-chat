from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from .database import Base
from passlib.context import CryptContext
import secrets


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="user")  # Roles: "user", "admin", "moderator"
    is_superuser = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    email_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    reset_token = Column(String, unique=True, nullable=True)

    def verify_password(self, password: str) -> bool:
        """Check if a plain password matches the hashed password."""
        return pwd_context.verify(password, self.hashed_password)

    def set_password(self, password: str):
        """Hash and store a password."""
        self.hashed_password = pwd_context.hash(password)

    def generate_reset_token(self):
        """Generate a secure reset token."""
        self.reset_token = secrets.token_urlsafe(32)

    def clear_reset_token(self):
        """Clear password reset token after use."""
        self.reset_token = None
