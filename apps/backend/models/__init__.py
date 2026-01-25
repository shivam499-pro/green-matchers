# models/__init__.py
from .database import Base, get_db, create_tables
from .user import User, UserProfile, UserEducation, UserExperience
from .job import Job, Application, Company
from .career import Career, CareerSkill
from .system import Notification, SavedSearch

__all__ = [
    "Base", "get_db", "create_tables",
    "User", "UserProfile", "UserEducation", "UserExperience",
    "Job", "Application", "Company",
    "Career", "CareerSkill",
    "Notification", "SavedSearch"
]