# routes/users.py
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
import uuid
from pathlib import Path

from ..models.database import get_db
from ..models.user import User, UserProfile, UserEducation, UserExperience
from ..models.job import Application
from ..services.auth import AuthService

router = APIRouter()

# Pydantic models
class UserProfileCreate(BaseModel):
    headline: Optional[str] = None
    summary: Optional[str] = None
    phone_number: Optional[str] = None
    current_salary: Optional[float] = None
    expected_salary: Optional[float] = None
    notice_period: Optional[int] = None
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    portfolio_url: Optional[str] = None

class EducationCreate(BaseModel):
    institution: str
    degree: str
    field_of_study: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    grade: Optional[str] = None
    description: Optional[str] = None

class ExperienceCreate(BaseModel):
    company: str
    position: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    current_job: bool = False
    description: Optional[str] = None

# File upload configuration
UPLOAD_DIR = Path("uploads")
RESUME_DIR = UPLOAD_DIR / "resumes"
RESUME_DIR.mkdir(exist_ok=True, parents=True)

@router.get("/profile")
async def get_user_profile(
    current_user: User = Depends(AuthService.get_current_user),
    db: Session = Depends(get_db)
):
    """Get complete user profile"""
    profile = db.query(UserProfile).filter(UserProfile.user_id == current_user.user_id).first()

    education = db.query(UserEducation).filter(UserEducation.user_id == current_user.user_id)\
        .order_by(UserEducation.end_date.desc()).all()

    experience = db.query(UserExperience).filter(UserExperience.user_id == current_user.user_id)\
        .order_by(UserExperience.start_date.desc()).all()

    applications = db.query(Application)\
        .join(User)\
        .filter(Application.user_id == current_user.user_id)\
        .order_by(Application.applied_at.desc()).all()

    return {
        "profile": profile,
        "education": education,
        "experience": experience,
        "applications": applications
    }

@router.post("/profile")
async def update_user_profile(
    profile_data: UserProfileCreate,
    current_user: User = Depends(AuthService.get_current_user),
    db: Session = Depends(get_db)
):
    """Create or update user profile"""
    # Check if profile exists
    existing_profile = db.query(UserProfile)\
        .filter(UserProfile.user_id == current_user.user_id).first()

    if existing_profile:
        # Update existing profile
        for field, value in profile_data.dict(exclude_unset=True).items():
            setattr(existing_profile, field, value)
        existing_profile.updated_at = None  # Trigger auto-update
    else:
        # Create new profile
        new_profile = UserProfile(
            user_id=current_user.user_id,
            **profile_data.dict()
        )
        db.add(new_profile)

    db.commit()
    return {"message": "Profile updated successfully"}

@router.post("/upload-resume")
async def upload_resume(
    file: UploadFile = File(...),
    current_user: User = Depends(AuthService.get_current_user),
    db: Session = Depends(get_db)
):
    """Upload resume file"""
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")

    # Validate file type
    allowed_extensions = {'.pdf', '.doc', '.docx'}
    file_extension = Path(file.filename).suffix.lower()
    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Only PDF and Word documents are allowed"
        )

    # Generate unique filename
    file_id = str(uuid.uuid4())
    filename = f"{file_id}{file_extension}"
    file_path = RESUME_DIR / filename

    try:
        # Save file
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)

        # Update user profile with resume URL
        resume_url = f"/uploads/resumes/{filename}"
        profile = db.query(UserProfile)\
            .filter(UserProfile.user_id == current_user.user_id).first()

        if profile:
            profile.resume_url = resume_url
            profile.updated_at = None
        else:
            new_profile = UserProfile(
                user_id=current_user.user_id,
                resume_url=resume_url
            )
            db.add(new_profile)

        db.commit()

        return {"message": "Resume uploaded successfully", "resume_url": resume_url}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to upload resume: {str(e)}")

@router.post("/education")
async def add_education(
    education_data: EducationCreate,
    current_user: User = Depends(AuthService.get_current_user),
    db: Session = Depends(get_db)
):
    """Add education record"""
    new_education = UserEducation(
        user_id=current_user.user_id,
        **education_data.dict()
    )

    db.add(new_education)
    db.commit()
    db.refresh(new_education)

    return {
        "message": "Education added successfully",
        "education_id": new_education.education_id
    }

@router.post("/experience")
async def add_experience(
    experience_data: ExperienceCreate,
    current_user: User = Depends(AuthService.get_current_user),
    db: Session = Depends(get_db)
):
    """Add experience record"""
    new_experience = UserExperience(
        user_id=current_user.user_id,
        **experience_data.dict()
    )

    db.add(new_experience)
    db.commit()
    db.refresh(new_experience)

    return {
        "message": "Experience added successfully",
        "experience_id": new_experience.experience_id
    }

@router.get("/applications")
async def get_user_applications(
    current_user: User = Depends(AuthService.get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's job applications"""
    applications = db.query(Application)\
        .filter(Application.user_id == current_user.user_id)\
        .order_by(Application.applied_at.desc()).all()

    return {"applications": applications}