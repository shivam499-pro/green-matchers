# routes/system.py
from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from ..models.database import get_db, get_mariadb_connection
from ..models.user import User
from ..models.job import Job, Application
from ..models.system import JobDemand

router = APIRouter()

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "2.0.0",
        "service": "Green Matchers API"
    }

@router.get("/stats")
async def get_stats(db: Session = Depends(get_db)):
    """Get system statistics"""
    try:
        # Get real counts from database
        users_count = db.query(User).count()
        jobs_count = db.query(Job).filter(Job.status == "active").count()
        applications_count = db.query(Application).count()
        companies_count = db.query(Job.company).distinct().count()

        return {
            "total_jobs": jobs_count,
            "companies": companies_count,
            "sdg_goals": 15,
            "favorites": 0,  # TODO: Implement favorites
            "applications": applications_count,
            "users": users_count,
            "profile_views": 143
        }
    except Exception as e:
        # Fallback stats if database error
        return {
            "total_jobs": 547,
            "companies": 51,
            "sdg_goals": 15,
            "favorites": 0,
            "applications": 8,
            "users": users_count if 'users_count' in locals() else 0,
            "profile_views": 143,
            "error": str(e)
        }

@router.get("/job_trends")
async def job_trends(db: Session = Depends(get_db)):
    """Get job trends data for charts"""
    try:
        # Get location-based demand data
        demand_data = db.query(JobDemand)\
            .order_by(JobDemand.demand_score.desc())\
            .limit(5).all()

        if not demand_data:
            # Fallback demo data
            demand_data = [
                {"location": "Mumbai", "demand_score": 85},
                {"location": "Delhi", "demand_score": 82},
                {"location": "Bangalore", "demand_score": 78},
                {"location": "Chennai", "demand_score": 75},
                {"location": "Pune", "demand_score": 72}
            ]
        else:
            demand_data = [
                {"location": d.location, "demand_score": d.demand_score}
                for d in demand_data
            ]

        return {
            "chart": {
                "type": "bar",
                "data": {
                    "labels": [d["location"] for d in demand_data],
                    "datasets": [{
                        "label": "Job Demand",
                        "data": [d["demand_score"] for d in demand_data],
                        "backgroundColor": [
                            "#FF6384", "#36A2EB", "#FFCE56",
                            "#4BC0C0", "#9966FF", "#FF9F40"
                        ]
                    }]
                },
                "options": {"scales": {"y": {"beginAtZero": True}}}
            }
        }
    except Exception as e:
        return {
            "chart": {
                "type": "bar",
                "data": {
                    "labels": ["Mumbai", "Delhi", "Bangalore"],
                    "datasets": [{
                        "label": "Job Demand",
                        "data": [85, 82, 78],
                        "backgroundColor": ["#FF6384", "#36A2EB", "#FFCE56"]
                    }]
                },
                "options": {"scales": {"y": {"beginAtZero": True}}}
            },
            "error": str(e)
        }

@router.get("/trends/skills")
async def get_skills_trends():
    """Get skills trends for demo"""
    return {
        "skills": [
            {"name": "Solar PV Design", "demand": 95, "growth": "+25%", "jobs": 145},
            {"name": "Carbon Accounting", "demand": 92, "growth": "+30%", "jobs": 128},
            {"name": "ESG Reporting", "demand": 88, "growth": "+22%", "jobs": 156},
            {"name": "Renewable Analytics", "demand": 85, "growth": "+20%", "jobs": 112},
            {"name": "Green Building (LEED)", "demand": 82, "growth": "+18%", "jobs": 98},
            {"name": "Wind Energy Systems", "demand": 78, "growth": "+15%", "jobs": 87}
        ]
    }

@router.get("/trends/companies")
async def get_companies_trends():
    """Get companies trends for demo"""
    return {
        "companies": [
            {"name": "Tata Power Renewables", "openings": 47, "growth": "+35%", "rating": 4.5},
            {"name": "Adani Green Energy", "openings": 38, "growth": "+28%", "rating": 4.3},
            {"name": "ReNew Power", "openings": 32, "growth": "+22%", "rating": 4.4},
            {"name": "Suzlon Energy", "openings": 28, "growth": "+18%", "rating": 4.2},
            {"name": "Azure Power", "openings": 24, "growth": "+30%", "rating": 4.3},
            {"name": "Hero Future Energies", "openings": 19, "growth": "+25%", "rating": 4.1}
        ]
    }