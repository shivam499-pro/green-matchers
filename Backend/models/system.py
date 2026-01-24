# models/system.py
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class Notification(Base):
    __tablename__ = "notifications"

    notification_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    type = Column(String(50), default="system")  # system, application, job_alert, message
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="notifications")

class SavedSearch(Base):
    __tablename__ = "saved_searches"

    search_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    search_name = Column(String(100))
    search_query = Column(JSON)  # Store search parameters as JSON
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="saved_searches")

class JobDemand(Base):
    __tablename__ = "job_demand"

    demand_id = Column(Integer, primary_key=True, index=True)
    location = Column(String(100), nullable=False)
    skill_category = Column(String(100))
    demand_score = Column(Integer, default=50)  # 1-100 scale
    trend_direction = Column(String(20), default="stable")  # increasing, decreasing, stable
    last_updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class SystemStats(Base):
    __tablename__ = "system_stats"

    stats_id = Column(Integer, primary_key=True, index=True)
    metric_name = Column(String(100), nullable=False, unique=True)
    metric_value = Column(Integer, default=0)
    last_updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())