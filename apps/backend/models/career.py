# models/career.py
from sqlalchemy import Column, Integer, String, Text, DateTime, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class Career(Base):
    __tablename__ = "careers"

    career_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    growth = Column(String(50), default="Medium")  # Low, Medium, High, Very High
    salary_range = Column(String(100), nullable=False)  # e.g., "₹8-15 LPA"
    demand = Column(Integer, default=80)  # 1-100 scale
    category = Column(String(100), default="Green Energy")
    experience_level = Column(String(50), default="Mid-level")
    required_skills = Column(Text)  # JSON string of skills
    industry = Column(String(100), default="Renewable Energy")
    sdg_alignment = Column(String(200), default="SDG 7")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Vector search fields (for MariaDB vector extension)
    desc_vector_json = Column(Text)  # JSON string of description vector
    skills_vector_json = Column(Text)  # JSON string of skills vector

    # BART compression fields
    insights_summary = Column(Text)  # Compressed career insights
    insights_generated_at = Column(DateTime(timezone=True))  # When insights were generated

    # Relationships
    skills = relationship("CareerSkill", back_populates="career")

class CareerSkill(Base):
    __tablename__ = "career_skills"

    skill_id = Column(Integer, primary_key=True, index=True)
    career_id = Column(Integer, ForeignKey("careers.career_id"), nullable=False)
    skill_name = Column(String(100), nullable=False)
    proficiency_level = Column(String(50), default="Intermediate")  # Beginner, Intermediate, Advanced
    is_required = Column(Integer, default=1)  # 0 = optional, 1 = required
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    career = relationship("Career", back_populates="skills")