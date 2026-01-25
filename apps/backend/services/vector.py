# services/vector.py
from typing import List, Dict, Any
from ..vector_services import vector_service

class VectorService:
    """Wrapper service for vector operations"""

    @staticmethod
    def generate_embedding(text: str) -> List[float]:
        """Generate vector embedding for text"""
        return vector_service.generate_embedding(text)

    @staticmethod
    def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between vectors"""
        return vector_service.cosine_similarity(vec1, vec2)

    @staticmethod
    def semantic_search_jobs(query: str, top_k: int = 10, filters: Dict = None) -> List[Dict]:
        """Semantic job search using vector similarity"""
        return vector_service.semantic_search_jobs(query, top_k, filters)

    @staticmethod
    def semantic_career_recommendations(query: str, top_k: int = 10) -> List[Dict]:
        """AI-powered career recommendations using vector similarity"""
        return vector_service.semantic_career_recommendations(query, top_k)

    @staticmethod
    def initialize_vector_data():
        """Initialize vector data for all existing records"""
        return vector_service.initialize_vector_data()

    @staticmethod
    def test_vector_functionality():
        """Test vector functionality"""
        return vector_service.test_vector_functionality()

    @staticmethod
    def get_vector_status():
        """Get vector implementation status"""
        return vector_service.get_vector_status()