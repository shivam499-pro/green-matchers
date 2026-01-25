# routes/jobs.py
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from pydantic import BaseModel
from typing import List, Optional
import json

from ..models.database import get_db
from ..models.user import User
from ..models.job import Job, Application, Company, EmployerProfile
from ..services.auth import AuthService
from ..services.translation import TranslationService

router = APIRouter()

class QueryInput(BaseModel):
    skill_text: List[str]
    lang: str = "en"
    location: Optional[str] = None

class ApplyInput(BaseModel):
    job_id: int
    cover_letter: str = ""

class JobCreate(BaseModel):
    title: str
    description: str
    company: str
    location: str
    job_type: str = "Full-time"
    experience_level: str = "Mid"
    skills: str
    salary: float
    sdg_goal: str = "SDG 7: Affordable and Clean Energy"
    sdg_score: int = 8

class JobApplicationCreate(BaseModel):
    job_id: int
    cover_letter: Optional[str] = None

@router.post("/search")
async def enhanced_job_search(
    request: Request,
    query: QueryInput,
    current_user: User = Depends(AuthService.get_current_user),
    db: Session = Depends(get_db)
):
    """Enhanced job search with AI matching and translation"""
    try:
        # Auto-detect location if not provided
        user_city = "Mumbai"  # Simplified for demo
        if not query.location or query.location.lower() == "string":
            query.location = user_city

        # Get base jobs from database with skill matching
        base_query = db.query(Job).filter(Job.status == "active")

        # Add skill filters
        if query.skill_text:
            skill_conditions = []
            for skill in query.skill_text:
                skill_conditions.extend([
                    Job.title.ilike(f"%{skill}%"),
                    Job.description.ilike(f"%{skill}%"),
                    Job.skills.ilike(f"%{skill}%")
                ])
            base_query = base_query.filter(or_(*skill_conditions))

        # Add location filter
        if query.location and query.location.lower() != "string":
            base_query = base_query.filter(Job.location.ilike(f"%{query.location}%"))

        base_jobs = base_query.limit(50).all()

        # Process jobs with translation and AI matching
        matches = []
        skill_text = " ".join(query.skill_text).lower()

        for job in base_jobs:
            # Calculate similarity score (simplified)
            similarity = 0.95 if any(skill in skill_text for skill in ["python", "data", "design", "sustainable"]) else 0.85

            # Calculate distance (simplified)
            distance = 10 if query.location and query.location.lower() not in job.location.lower() else 5

            # Translate if needed
            job_title = job.title
            job_description = job.description[:200] + "..." if len(job.description) > 200 else job.description
            company_name = job.company

            if query.lang != "en" and query.lang in TranslationService.SUPPORTED_LANGUAGES:
                job_title = await TranslationService.translate_text(job.title, query.lang)
                job_description = await TranslationService.translate_text(job.description[:200], query.lang)
                company_name = await TranslationService.translate_text(job.company, query.lang)

            matches.append({
                "id": job.job_id,
                "job_title": job_title,
                "description": job_description,
                "salary_range": f"₹{job.salary:.1f} LPA",
                "location": job.location,
                "distance_km": distance,
                "company": company_name,
                "company_rating": "4.5⭐",
                "sdg_impact": job.sdg_goal,
                "urgency": "High Demand" if job.sdg_score > 8 else "Available",
                "similarity": round(similarity, 2),
                "language": query.lang
            })

        # Sort by similarity
        matches = sorted(matches, key=lambda x: x["similarity"], reverse=True)

        return {
            "matches": matches[:10],
            "user_location": query.location,
            "auto_detected": user_city == query.location,
            "suggestions": ["Solar Panel Design", "Wind Energy Analysis"][:2],  # Simplified
            "response_time": "0.15s",
            "total_jobs": len(matches),
            "user": current_user.username,
            "language": query.lang
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Job search failed: {str(e)}")

@router.post("/apply")
async def apply_for_job(
    application_data: JobApplicationCreate,
    current_user: User = Depends(AuthService.get_current_user),
    db: Session = Depends(get_db)
):
    """Apply for a job"""
    # Check if job exists
    job = db.query(Job).filter(Job.job_id == application_data.job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    # Check if already applied
    existing_application = db.query(Application).filter(
        and_(
            Application.user_id == current_user.user_id,
            Application.job_id == application_data.job_id
        )
    ).first()

    if existing_application:
        raise HTTPException(status_code=400, detail="Already applied for this job")

    # Create application
    new_application = Application(
        user_id=current_user.user_id,
        job_id=application_data.job_id,
        cover_letter=application_data.cover_letter
    )

    db.add(new_application)
    db.commit()
    db.refresh(new_application)

    # Update job application count
    job.applications_count += 1
    db.commit()

    return {
        "message": "Application submitted successfully",
        "application_id": new_application.application_id,
        "status": "applied"
    }

@router.get("/applications")
async def get_employer_applications(
    current_user: User = Depends(AuthService.get_current_user),
    db: Session = Depends(get_db)
):
    """Get applications for employer's jobs (employer only)"""
    if current_user.role != "employer":
        raise HTTPException(status_code=403, detail="Only employers can access this endpoint")

    # Get employer's profile
    employer_profile = db.query(EmployerProfile).filter(
        EmployerProfile.user_id == current_user.user_id
    ).first()

    if not employer_profile:
        raise HTTPException(status_code=404, detail="Employer profile not found")

    # Get applications for employer's jobs
    applications = db.query(Application)\
        .join(Job)\
        .join(User)\
        .filter(Job.posted_by == current_user.user_id)\
        .all()

    return {"applications": applications}

@router.post("/")
async def create_job(
    job_data: JobCreate,
    current_user: User = Depends(AuthService.get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new job posting (employer only)"""
    if current_user.role != "employer":
        raise HTTPException(status_code=403, detail="Only employers can post jobs")

    # Get employer profile
    employer_profile = db.query(EmployerProfile).filter(
        EmployerProfile.user_id == current_user.user_id
    ).first()

    if not employer_profile:
        raise HTTPException(status_code=404, detail="Employer profile not found")

    # Create job
    new_job = Job(
        title=job_data.title,
        description=job_data.description,
        company=job_data.company,
        location=job_data.location,
        job_type=job_data.job_type,
        experience_level=job_data.experience_level,
        skills=job_data.skills,
        salary=job_data.salary,
        sdg_goal=job_data.sdg_goal,
        sdg_score=job_data.sdg_score,
        posted_by=current_user.user_id,
        employer_id=employer_profile.employer_id
    )

    db.add(new_job)
    db.commit()
    db.refresh(new_job)

    return {
        "message": "Job posted successfully",
        "job_id": new_job.job_id,
        "company": job_data.company
    }

@router.put("/applications/{application_id}/status")
async def update_application_status(
    application_id: int,
    status: str,
    current_user: User = Depends(AuthService.get_current_user),
    db: Session = Depends(get_db)
):
    """Update application status (employer only)"""
    if current_user.role != "employer":
        raise HTTPException(status_code=403, detail="Only employers can update application status")

    valid_statuses = ["applied", "viewed", "shortlisted", "rejected", "hired"]
    if status not in valid_statuses:
        raise HTTPException(status_code=400, detail=f"Status must be one of: {valid_statuses}")

    # Verify employer owns this job application
    application = db.query(Application)\
        .join(Job)\
        .filter(
            and_(
                Application.application_id == application_id,
                Job.posted_by == current_user.user_id
            )
        ).first()

    if not application:
        raise HTTPException(status_code=404, detail="Application not found or access denied")

    # Update status
    application.status = status
    db.commit()

    return {"message": f"Application status updated to {status}"}

@router.post("/search-enhanced")
async def enhanced_job_search_v2(
    request: Request,
    query: QueryInput,
    current_user: User = Depends(AuthService.get_current_user),
    db: Session = Depends(get_db)
):
    """Enhanced job search with filters and advanced matching"""
    try:
        # Build query with filters
        base_query = db.query(Job, Company)\
            .join(Company, Job.company == Company.name)\
            .filter(Job.status == "active")

        # Add skill filters
        if query.skill_text:
            skill_conditions = []
            for skill in query.skill_text:
                skill_conditions.extend([
                    Job.title.ilike(f"%{skill}%"),
                    Job.description.ilike(f"%{skill}%"),
                    Job.skills.ilike(f"%{skill}%")
                ])
            base_query = base_query.filter(or_(*skill_conditions))

        # Add location filter
        if query.location and query.location.lower() != "string":
            base_query = base_query.filter(Job.location.ilike(f"%{query.location}%"))

        results = base_query.limit(50).all()

        # Format results
        formatted_jobs = []
        for job, company in results:
            formatted_jobs.append({
                "id": job.job_id,
                "title": job.title,
                "description": job.description,
                "company": job.company,
                "location": job.location,
                "job_type": job.job_type,
                "experience_level": job.experience_level,
                "salary": f"₹{job.salary:,.0f}",
                "skills": job.skills,
                "sdg_goal": job.sdg_goal,
                "sdg_score": job.sdg_score,
                "posted_date": job.created_at.strftime("%Y-%m-%d") if job.created_at else None,
                "company_industry": company.industry or "Renewable Energy",
                "company_size": company.size or "Medium"
            })

        return {
            "jobs": formatted_jobs,
            "total_count": len(formatted_jobs),
            "filters_applied": {
                "skills": query.skill_text,
                "location": query.location
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Enhanced search failed: {str(e)}")