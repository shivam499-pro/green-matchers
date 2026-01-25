# main.py - FastAPI Application Entry Point
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from .config import settings
from .routes import (
    auth_router, users_router, jobs_router, careers_router,
    translation_router, system_router, vector_router
)
from .models import create_tables

# Create FastAPI app
app = FastAPI(
    title="Green Matchers API",
    description="🚀 AI-Powered Green Jobs Platform | MariaDB Vector Search | 10 Languages | Production Ready",
    version=settings.app_version,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=[
        {
            "name": "Authentication",
            "description": "User login and token management"
        },
        {
            "name": "Users",
            "description": "User profiles, education, experience, and applications"
        },
        {
            "name": "Jobs",
            "description": "Job search, applications, and employer management"
        },
        {
            "name": "Careers",
            "description": "Career recommendations and skill development"
        },
        {
            "name": "Translation",
            "description": "Multi-language support for 10 Indian languages"
        },
        {
            "name": "Vector AI",
            "description": "Advanced MariaDB vector search and AI recommendations"
        },
        {
            "name": "System",
            "description": "Health checks and system statistics"
        }
    ]
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate limiting
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Include routers
app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])
app.include_router(users_router, prefix="/api/users", tags=["Users"])
app.include_router(jobs_router, prefix="/api/jobs", tags=["Jobs"])
app.include_router(careers_router, prefix="/api/career", tags=["Careers"])
app.include_router(translation_router, prefix="/api", tags=["Translation"])
app.include_router(vector_router, prefix="/api/vector", tags=["Vector AI"])
app.include_router(system_router, prefix="", tags=["System"])

# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize database and services on startup"""
    try:
        create_tables()
        print("✅ Database tables created/verified")
    except Exception as e:
        print(f"⚠️ Database initialization warning: {e}")

    print("🚀 Green Matchers API started successfully!")
    print(f"📊 Environment: {'Development' if settings.debug else 'Production'}")
    print(f"📚 API Documentation: http://localhost:8000/docs")
    print(f"🌐 CORS Origins: {settings.cors_origins}")

# Root endpoint
@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "message": "Welcome to Green Matchers API",
        "version": settings.app_version,
        "status": "operational",
        "features": [
            "AI-Powered Job Matching",
            "MariaDB Vector Search",
            "10 Indian Languages Support",
            "Real-time Career Recommendations",
            "Employer Dashboard",
            "Resume Processing"
        ],
        "docs": "/docs",
        "health": "/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level="info"
    )