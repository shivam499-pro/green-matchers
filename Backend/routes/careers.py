# routes/careers.py
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional

from ..models.database import get_db
from ..models.user import User
from ..models.career import Career, CareerSkill
from ..services.auth import AuthService
from ..services.translation import TranslationService
from ..services.vector import VectorService

router = APIRouter()

class CareerRecommendationsInput(BaseModel):
    skills: List[str]
    experience: str = ""
    lang: str = "en"

class SkillGapInput(BaseModel):
    current_skills: List[str]
    target_role: str
    experience_level: str = "mid"
    lang: str = "en"

class LearningPathInput(BaseModel):
    current_skills: List[str]
    target_skills: List[str]
    lang: str = "en"

@router.post("/recommendations")
async def enhanced_career_recommendations(
    career_data: CareerRecommendationsInput,
    current_user: User = Depends(AuthService.get_current_user),
    db: Session = Depends(get_db)
):
    """Enhanced career recommendations with translation"""
    try:
        skills = [skill.lower() for skill in career_data.skills] if career_data.skills else []
        experience = career_data.experience
        lang = career_data.lang.lower() if career_data.lang else "en"

        # Get recommendations from database
        if skills:
            # Find careers with matching skills
            careers_query = db.query(Career)
            skill_conditions = []
            for skill in skills:
                skill_conditions.extend([
                    Career.title.ilike(f"%{skill}%"),
                    Career.description.ilike(f"%{skill}%"),
                    Career.required_skills.ilike(f"%{skill}%")
                ])
            careers_query = careers_query.filter(db.or_(*skill_conditions))
        else:
            # Get top careers by demand
            careers_query = db.query(Career).order_by(Career.demand.desc())

        careers_from_db = careers_query.limit(15).all()

        # If no matches from database, use fallback data
        if not careers_from_db:
            careers_from_db = [
                {
                    "career_id": 1,
                    "title": "Renewable Energy Specialist",
                    "description": "Focus on solar, wind, and other renewable energy sources. High growth potential in current market.",
                    "required_skills": ["Solar Energy", "Wind Power", "Project Management"],
                    "growth": "Very High",
                    "salary_range": "₹8-15 LPA",
                    "demand": 95,
                    "category": "Renewable Energy",
                    "experience_level": "Mid to Senior"
                },
                {
                    "career_id": 2,
                    "title": "Environmental Data Scientist",
                    "description": "Use data analytics to solve environmental challenges and optimize green initiatives.",
                    "required_skills": ["Python", "Data Analysis", "Machine Learning"],
                    "growth": "High",
                    "salary_range": "₹10-18 LPA",
                    "demand": 94,
                    "category": "Data Science",
                    "experience_level": "Mid to Senior"
                },
                {
                    "career_id": 3,
                    "title": "Sustainability Consultant",
                    "description": "Help organizations implement sustainable practices and reduce environmental impact.",
                    "required_skills": ["Sustainability", "Consulting", "ESG"],
                    "growth": "High",
                    "salary_range": "₹9-16 LPA",
                    "demand": 92,
                    "category": "Sustainability",
                    "experience_level": "Mid Level"
                }
            ]

        # Build recommendations list
        recommendations = []
        for career in careers_from_db:
            if isinstance(career, dict):
                # Fallback data
                rec = career.copy()
            else:
                # Database object
                rec = {
                    "id": career.career_id,
                    "title": career.title,
                    "description": career.description,
                    "skills_required": career.required_skills.split(',') if career.required_skills else ["Technical Skills"],
                    "growth": career.growth,
                    "salary_range": career.salary_range,
                    "demand": career.demand,
                    "category": career.category,
                    "experience_level": career.experience_level
                }
            recommendations.append(rec)

        # Translate recommendations if not English
        final_recommendations = []
        if lang != "en" and lang in TranslationService.SUPPORTED_LANGUAGES:
            for rec in recommendations:
                translated_rec = rec.copy()
                try:
                    translated_rec['title'] = await TranslationService.translate_text(rec['title'], lang)
                    translated_rec['description'] = await TranslationService.translate_text(rec['description'], lang)
                    translated_rec['skills_required'] = [await TranslationService.translate_text(skill, lang) for skill in rec['skills_required']]
                    translated_rec['growth'] = await TranslationService.translate_text(rec['growth'], lang)
                    translated_rec['salary_range'] = await TranslationService.translate_text(rec['salary_range'], lang)
                    translated_rec['category'] = await TranslationService.translate_text(rec['category'], lang)
                    translated_rec['experience_level'] = await TranslationService.translate_text(rec['experience_level'], lang)
                    final_recommendations.append(translated_rec)
                except Exception:
                    final_recommendations.append(rec)  # Fallback to original
        else:
            final_recommendations = recommendations

        return {
            'recommendations': final_recommendations,
            'total_count': len(final_recommendations),
            'language': lang,
            'language_name': TranslationService.SUPPORTED_LANGUAGES.get(lang, "English"),
            'success': True
        }

    except Exception as e:
        return {
            'recommendations': [],
            'total_count': 0,
            'language': career_data.lang if hasattr(career_data, 'lang') else 'en',
            'language_name': TranslationService.SUPPORTED_LANGUAGES.get(career_data.lang if hasattr(career_data, 'lang') else 'en', 'English'),
            'success': False,
            'error': str(e)
        }

@router.post("/skill-gap-analysis")
async def skill_gap_analysis(
    request: Request,
    gap_data: SkillGapInput,
    current_user: User = Depends(AuthService.get_current_user)
):
    """Analyze gap between current skills and target job requirements"""
    try:
        # Simplified role requirements mapping
        role_skills_map = {
            "solar engineer": ["PV System Design", "Renewable Energy", "Project Management", "AutoCAD"],
            "data scientist": ["Python", "Machine Learning", "Data Analysis", "SQL", "Statistics"],
            "sustainability manager": ["ESG Reporting", "Carbon Accounting", "Sustainability", "Compliance"],
            "wind technician": ["Wind Turbine Maintenance", "Electrical Systems", "Safety Protocols", "Troubleshooting"]
        }

        target_skills = role_skills_map.get(gap_data.target_role.lower(), ["Technical Skills", "Industry Knowledge"])

        # Find missing skills
        current_skills_set = set(skill.lower() for skill in gap_data.current_skills)
        target_skills_set = set(skill.lower() for skill in target_skills)

        missing_skills = list(target_skills_set - current_skills_set)
        matching_skills = list(current_skills_set.intersection(target_skills_set))

        # Get learning recommendations for missing skills
        learning_recommendations = []
        for skill in missing_skills[:3]:  # Limit to top 3
            learning_recommendations.append({
                "skill": skill,
                "courses": [
                    {
                        "platform": "Coursera",
                        "title": f"{skill} Fundamentals",
                        "duration": "4 weeks",
                        "level": "Beginner"
                    }
                ],
                "resources": [
                    {
                        "type": "YouTube",
                        "title": f"{skill} Tutorial Series"
                    }
                ]
            })

        # Translate if needed
        if gap_data.lang != "en" and gap_data.lang in TranslationService.SUPPORTED_LANGUAGES:
            matching_skills = [await TranslationService.translate_text(skill, gap_data.lang) for skill in matching_skills]
            missing_skills = [await TranslationService.translate_text(skill, gap_data.lang) for skill in missing_skills]

        return {
            "target_role": gap_data.target_role,
            "matching_skills": matching_skills,
            "missing_skills": missing_skills,
            "gap_percentage": len(missing_skills) / len(target_skills) * 100 if target_skills else 0,
            "learning_recommendations": learning_recommendations,
            "timeline_estimate": f"{len(missing_skills) * 2} weeks to learn essential skills",
            "language": gap_data.lang
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Skill gap analysis failed: {str(e)}")

@router.post("/learning-path")
async def get_learning_path(
    learning_data: LearningPathInput,
    current_user: User = Depends(AuthService.get_current_user)
):
    """Generate personalized learning path"""
    try:
        # Simplified learning path
        learning_path = [
            {
                "step": 1,
                "title": "Skill Assessment",
                "description": "Evaluate your current skill level and identify gaps",
                "duration": "1 week",
                "resources": ["Skill assessment tests", "Career counseling"],
                "milestone": "Complete skill assessment"
            },
            {
                "step": 2,
                "title": "Foundation Building",
                "description": "Learn fundamental concepts and basic skills",
                "duration": "4 weeks",
                "resources": ["Online courses", "Tutorial videos", "Practice exercises"],
                "milestone": "Complete foundation courses"
            },
            {
                "step": 3,
                "title": "Advanced Learning",
                "description": "Master advanced topics and specialized skills",
                "duration": "6 weeks",
                "resources": ["Advanced courses", "Real-world projects", "Mentorship"],
                "milestone": "Complete capstone project"
            },
            {
                "step": 4,
                "title": "Portfolio Development",
                "description": "Build projects and create portfolio",
                "duration": "2 weeks",
                "resources": ["Project ideas", "Portfolio templates", "Code reviews"],
                "milestone": "Portfolio ready for job applications"
            }
        ]

        return {
            "learning_path": learning_path,
            "current_skills_count": len(learning_data.current_skills),
            "target_skills_count": len(learning_data.target_skills),
            "language": learning_data.lang
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Learning path generation failed: {str(e)}")

@router.get("/pathways")
async def get_career_pathways(
    current_user: User = Depends(AuthService.get_current_user),
    db: Session = Depends(get_db)
):
    """Get all available career pathways"""
    try:
        careers = db.query(Career).order_by(Career.demand.desc()).limit(20).all()

        pathways = []
        for career in careers:
            pathways.append({
                "id": career.career_id,
                "title": career.title,
                "description": career.description,
                "category": career.category,
                "growth": career.growth,
                "salary_range": career.salary_range,
                "demand": career.demand,
                "experience_level": career.experience_level
            })

        return {"pathways": pathways, "total_count": len(pathways)}

    except Exception as e:
        return {"pathways": [], "total_count": 0, "error": str(e)}

@router.get("/trends")
async def get_career_trends():
    """Get career trends data"""
    return {
        "trending_careers": [
            {"name": "Solar Energy Engineer", "growth": "+35%", "demand": 95, "avg_salary": "₹12 LPA"},
            {"name": "Carbon Analyst", "growth": "+42%", "demand": 92, "avg_salary": "₹15 LPA"},
            {"name": "ESG Consultant", "growth": "+28%", "demand": 88, "avg_salary": "₹14 LPA"},
            {"name": "Wind Technician", "growth": "+31%", "demand": 85, "avg_salary": "₹8 LPA"},
            {"name": "Sustainability Manager", "growth": "+25%", "demand": 82, "avg_salary": "₹18 LPA"}
        ],
        "emerging_skills": [
            "Carbon Accounting", "ESG Reporting", "Renewable Energy Tech",
            "Sustainable Finance", "Green Building Design"
        ]
    }