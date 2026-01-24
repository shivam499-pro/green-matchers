# models/user.py
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Numeric, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    full_name = Column(String(100))
    role = Column(String(20), default="job_seeker")  # job_seeker, employer, admin
    phone_number = Column(String(15))
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_login = Column(DateTime(timezone=True))

    # Relationships
    profile = relationship("UserProfile", back_populates="user", uselist=False)
    applications = relationship("Application", back_populates="user")
    education = relationship("UserEducation", back_populates="user")
    experience = relationship("UserExperience", back_populates="user")
    notifications = relationship("Notification", back_populates="user")

class UserProfile(Base):
    __tablename__ = "user_profiles"

    profile_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    headline = Column(String(200))
    summary = Column(Text)
    phone_number = Column(String(15))
    current_salary = Column(Numeric(10, 2))
    expected_salary = Column(Numeric(10, 2))
    notice_period = Column(Integer)  # days
    resume_url = Column(String(500))
    linkedin_url = Column(String(200))
    github_url = Column(String(200))
    portfolio_url = Column(String(200))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="profile")

class UserEducation(Base):
    __tablename__ = "user_education"

    education_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    institution = Column(String(200), nullable=False)
    degree = Column(String(100), nullable=False)
    field_of_study = Column(String(100))
    start_date = Column(Date)
    end_date = Column(Date)
    grade = Column(String(50))
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="education")

class UserExperience(Base):
    __tablename__ = "user_experience"

    experience_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    company = Column(String(200), nullable=False)
    position = Column(String(100), nullable=False)
    start_date = Column(Date)
    end_date = Column(Date)
    current_job = Column(Boolean, default=False)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="experience")