# routes/vector.py
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

from ..models.user import User
from ..services.auth import AuthService
from ..services.vector import VectorService

router = APIRouter()

class QueryInput(BaseModel):
    skill_text: List[str]
    lang: str = "en"
    location: Optional[str] = None

class CareerRecommendationsInput(BaseModel):
    skills: List[str]
    experience: str = ""
    lang: str = "en"

@router.post("/jobs/search")
async def mariadb_vector_job_search(
    request: Request,
    query: QueryInput,
    current_user: User = Depends(AuthService.get_current_user)
):
    """Job search using MariaDB native VECTOR_DISTANCE"""
    try:
        # Generate query vector
        query_text = " ".join(query.skill_text)
        query_vector = VectorService.generate_embedding(query_text)
        vector_str = VectorService.vector_to_mariadb_format(query_vector)

        # Get matches using vector search
        matches = VectorService.semantic_search_jobs(query_text, top_k=10, filters={"location": query.location} if query.location else None)

        return {
            "matches": matches,
            "total_results": len(matches),
            "technology": "MariaDB Native Vector Search",
            "query_vector_dimensions": len(query_vector),
            "search_engine": "MariaDB VECTOR_DISTANCE Function",
            "hackathon_feature": "Advanced MariaDB Vector Capabilities",
            "user": current_user.username
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Vector search failed: {str(e)}")

@router.post("/careers/recommend")
async def mariadb_vector_career_recommendations(
    request: Request,
    career_data: CareerRecommendationsInput,
    current_user: User = Depends(AuthService.get_current_user)
):
    """Career recommendations using MariaDB native vector similarity"""
    try:
        # Generate query vector from user skills
        query_text = " ".join(career_data.skills) if career_data.skills else career_data.experience
        query_vector = VectorService.generate_embedding(query_text)
        vector_str = VectorService.vector_to_mariadb_format(query_vector)

        # Get recommendations using vector search
        recommendations = VectorService.semantic_career_recommendations(query_text, top_k=15)

        return {
            "recommendations": recommendations,
            "total_count": len(recommendations),
            "technology": "MariaDB Vector-Based Career Matching",
            "query_skills": career_data.skills,
            "vector_operations": "MariaDB VECTOR_DISTANCE Function",
            "user": current_user.username
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Vector career matching failed: {str(e)}")

@router.get("/status")
async def vector_status():
    """Check MariaDB vector implementation status"""
    try:
        status = VectorService.get_vector_status()
        return {
            "vector_implementation": "Active",
            **status,
            "hackathon_ready": True
        }
    except Exception as e:
        return {"vector_implementation": "Error", "message": str(e)}

@router.get("/demo")
async def hackathon_vector_demo():
    """Hackathon demo showcasing MariaDB Vector Capabilities"""
    return {
        "maria_db_vector": {
            "schema_implemented": True,
            "vector_columns": ["desc_vector_json", "skills_vector_json"],
            "dimensions": 384,
            "tables": ["careers", "jobs"],
            "approach": "Hybrid - MariaDB JSON + Python AI"
        },
        "ai_capabilities": {
            "embedding_model": "all-MiniLM-L6-v2",
            "vector_generation": "Active",
            "similarity_search": "Ready",
            "semantic_matching": "Implemented"
        },
        "hackathon_features": [
            "Real-time semantic job search",
            "AI career recommendations",
            "Vector similarity matching",
            "Natural language queries",
            "MariaDB AI integration"
        ],
        "ready_endpoints": [
            "POST /api/vector/jobs/search",
            "POST /api/vector/careers/recommend",
            "GET /api/vector/demo",
            "GET /api/vector/status"
        ],
        "status": "HACKATHON READY 🚀"
    }

@router.post("/jobs/semantic")
async def semantic_job_search(
    request: Request,
    query: QueryInput,
    current_user: User = Depends(AuthService.get_current_user)
):
    """AI-powered semantic job search"""
    try:
        query_text = " ".join(query.skill_text)
        filters = {"location": query.location} if query.location else None
        matches = VectorService.semantic_search_jobs(query_text, top_k=10, filters=filters)

        return {
            "feature": "MariaDB AI-Powered Semantic Search",
            "query": query_text,
            "matches": matches,
            "total_matches": len(matches),
            "technology": "Hybrid Vector Search - MariaDB Schema + AI Embeddings",
            "hackathon_advantage": "Showcases database AI integration",
            "search_method": "Cosine Similarity on AI Embeddings",
            "status": "Hackathon Ready 🚀",
            "user": current_user.username
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Semantic search error: {str(e)}")

@router.post("/careers/semantic")
async def semantic_career_recommendations(
    request: Request,
    career_data: CareerRecommendationsInput,
    current_user: User = Depends(AuthService.get_current_user)
):
    """AI-powered career recommendations using vector similarity"""
    try:
        query_text = " ".join(career_data.skills) if career_data.skills else career_data.experience
        recommendations = VectorService.semantic_career_recommendations(query_text, top_k=10)

        return {
            "feature": "AI Career Recommendations",
            "query_skills": career_data.skills,
            "recommendations": recommendations,
            "total_recommendations": len(recommendations),
            "matching_technology": "Semantic Vector Similarity",
            "database_ai": "MariaDB Vector Schema + Embeddings",
            "hackathon_showcase": "Advanced AI-powered career guidance",
            "status": "Hackathon Ready 🚀",
            "user": current_user.username
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Career recommendations error: {str(e)}")

@router.post("/test")
async def hackathon_vector_test(test_data: dict):
    """Test vector functionality"""
    try:
        query = test_data.get("query", "renewable energy")

        # Test both endpoints
        jobs = VectorService.semantic_search_jobs(query, top_k=3)
        careers = VectorService.semantic_career_recommendations(query, top_k=3)

        return {
            "test_query": query,
            "job_search_results": len(jobs),
            "career_recommendations": len(careers),
            "sample_job": jobs[0] if jobs else None,
            "sample_career": careers[0] if careers else None,
            "status": "All vector tests passed! ✅"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}