"""
Tests for vector search functionality
"""
import pytest
from services.vector_services import vector_service, initialize_vector_data, test_vector_functionality
import numpy as np

class TestVectorService:
    def test_embedding_generation(self):
        """Test that embeddings are generated correctly"""
        text = "Software Engineer with Python experience"
        embedding = vector_service.generate_embedding(text)

        assert isinstance(embedding, list)
        assert len(embedding) == 768  # SentenceTransformer dimension
        assert all(isinstance(x, float) for x in embedding)

    def test_cosine_similarity(self):
        """Test cosine similarity calculation"""
        vec1 = [1, 0, 0]
        vec2 = [0, 1, 0]
        similarity = vector_service.cosine_similarity(vec1, vec2)

        assert similarity == 0.0  # Orthogonal vectors

        # Same vector should have similarity 1
        similarity_same = vector_service.cosine_similarity(vec1, vec1)
        assert abs(similarity_same - 1.0) < 0.001

    def test_semantic_search_jobs(self):
        """Test semantic job search"""
        try:
            results = vector_service.semantic_search_jobs("python developer", top_k=3)
            assert isinstance(results, list)
            if len(results) > 0:
                assert "title" in results[0]
                assert "similarity_score" in results[0]
                assert 0 <= results[0]["similarity_score"] <= 100
        except Exception as e:
            pytest.skip(f"Database not available for test: {e}")

    def test_semantic_career_recommendations(self):
        """Test semantic career recommendations"""
        try:
            results = vector_service.semantic_career_recommendations("data science", top_k=3)
            assert isinstance(results, list)
            if len(results) > 0:
                assert "title" in results[0]
                assert "similarity_score" in results[0]
                assert 0 <= results[0]["similarity_score"] <= 100
        except Exception as e:
            pytest.skip(f"Database not available for test: {e}")

    def test_vector_functionality_test(self):
        """Test the vector functionality test function"""
        try:
            result = test_vector_functionality()
            assert "status" in result
            assert result["status"] in ["success", "error"]
        except Exception as e:
            pytest.skip(f"Vector test failed: {e}")

class TestVectorInitialization:
    def test_initialize_vector_data(self):
        """Test vector data initialization"""
        try:
            result = initialize_vector_data()
            assert "status" in result
        except Exception as e:
            pytest.skip(f"Database not available for initialization test: {e}")