# models/job.py
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Numeric, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class Company(Base):
    __tablename__ = "companies"

    company_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), unique=True, nullable=False)
    description = Column(Text)
    industry = Column(String(100))
    website = Column(String(200))
    location = Column(String(100))
    size = Column(String(50))  # Startup, Small, Medium, Large, Enterprise
    founded_year = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    jobs = relationship("Job", back_populates="company")
    employers = relationship("EmployerProfile", back_populates="company")

class Job(Base):
    __tablename__ = "jobs"

    job_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    company = Column(String(200), nullable=False)  # Denormalized for performance
    location = Column(String(100), nullable=False)
    job_type = Column(String(50), default="Full-time")  # Full-time, Part-time, Contract, Internship
    experience_level = Column(String(50), default="Mid")  # Entry, Mid, Senior, Executive
    skills = Column(Text)  # JSON string of required skills
    salary = Column(Numeric(10, 2))  # Annual salary in LPA
    salary_min = Column(Numeric(10, 2))
    salary_max = Column(Numeric(10, 2))
    currency = Column(String(3), default="INR")
    sdg_goal = Column(String(200), default="SDG 7: Affordable and Clean Energy")
    sdg_score = Column(Integer, default=8)  # 1-10 scale
    status = Column(String(20), default="active")  # active, inactive, filled
    posted_by = Column(Integer, ForeignKey("users.user_id"))  # User who posted the job
    employer_id = Column(Integer, ForeignKey("employer_profiles.employer_id"))
    views = Column(Integer, default=0)
    applications_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Vector search fields (for MariaDB vector extension)
    desc_vector_json = Column(Text)  # JSON string of description vector
    skills_vector_json = Column(Text)  # JSON string of skills vector

    # Relationships
    applications = relationship("Application", back_populates="job")

class Application(Base):
    __tablename__ = "applications"

    application_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    job_id = Column(Integer, ForeignKey("jobs.job_id"), nullable=False)
    cover_letter = Column(Text)
    resume_url = Column(String(500))
    status = Column(Enum('applied', 'viewed', 'shortlisted', 'rejected', 'hired'), default='applied')
    applied_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="applications")
    job = relationship("Job", back_populates="applications")

class EmployerProfile(Base):
    __tablename__ = "employer_profiles"

    employer_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    company_id = Column(Integer, ForeignKey("companies.company_id"), nullable=False)
    position = Column(String(100))
    phone_number = Column(String(15))
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="employer_profile", uselist=False)
    company = relationship("Company", back_populates="employers")
    jobs = relationship("Job", back_populates="employer")