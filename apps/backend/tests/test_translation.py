"""
Tests for translation functionality
"""
import pytest
from app import translate_text_enhanced

@pytest.mark.asyncio
class TestTranslation:
    async def test_translate_english_to_hindi(self):
        """Test translation from English to Hindi"""
        result = await translate_text_enhanced("Hello", "hi")
        assert isinstance(result, str)
        assert len(result) > 0
        # Hindi translation should be different from English
        assert result != "Hello"

    async def test_translate_english_to_tamil(self):
        """Test translation from English to Tamil"""
        result = await translate_text_enhanced("Software Engineer", "ta")
        assert isinstance(result, str)
        assert len(result) > 0

    async def test_translate_empty_text(self):
        """Test translation of empty text"""
        result = await translate_text_enhanced("", "hi")
        assert result == ""

    async def test_translate_none_text(self):
        """Test translation of None text"""
        result = await translate_text_enhanced(None, "hi")
        assert result is None

    async def test_translate_english_to_english(self):
        """Test translation from English to English (should return same)"""
        text = "Hello World"
        result = await translate_text_enhanced(text, "en")
        assert result == text

    async def test_translate_job_title_hindi(self):
        """Test translation of job title to Hindi"""
        result = await translate_text_enhanced("Data Scientist", "hi")
        assert isinstance(result, str)
        assert len(result) > 0

    async def test_translate_company_name_telugu(self):
        """Test translation of company name to Telugu"""
        result = await translate_text_enhanced("Tata Power", "te")
        assert isinstance(result, str)
        assert len(result) > 0

    async def test_batch_translation(self):
        """Test batch translation functionality"""
        texts = ["Engineer", "Developer", "Manager"]
        # Test individual translations
        for text in texts:
            result = await translate_text_enhanced(text, "hi")
            assert isinstance(result, str)
            assert len(result) > 0

    async def test_fallback_translations(self):
        """Test fallback dictionary translations"""
        # Test exact matches from fallback dictionary
        result = await translate_text_enhanced("Solar Energy Engineer", "hi")
        assert isinstance(result, str)
        assert "सौर" in result  # Should contain Hindi word for solar

    async def test_unsupported_language(self):
        """Test translation to unsupported language"""
        result = await translate_text_enhanced("Hello", "xx")
        # Should return original text for unsupported languages
        assert result == "Hello"