# routes/translation.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional

from ..services.translation import TranslationService

router = APIRouter()

class TranslateInput(BaseModel):
    text: str
    target_language: str
    source_language: Optional[str] = None

class BatchTranslateInput(BaseModel):
    texts: List[str]
    target_lang: str = "en"

@router.post("/translate")
async def translate_text(translate_data: TranslateInput):
    """Translate single text to target language"""
    try:
        if not translate_data.text or not translate_data.text.strip():
            return {
                'original_text': '',
                'translated_text': '',
                'target_language': translate_data.target_language,
                'success': False,
                'error': 'No text provided'
            }

        text = translate_data.text.strip()
        target_lang = translate_data.target_language.lower()

        translated_text = await TranslationService.translate_text(text, target_lang)

        return {
            'original_text': text,
            'translated_text': translated_text,
            'target_language': target_lang,
            'success': True
        }

    except Exception as e:
        return {
            'original_text': translate_data.text,
            'translated_text': translate_data.text,
            'target_language': translate_data.target_language,
            'success': False,
            'error': str(e)
        }

@router.post("/translate/batch")
async def translate_batch(batch_data: BatchTranslateInput):
    """Translate multiple texts at once"""
    try:
        if not batch_data.texts:
            return {
                'original_texts': [],
                'translated_texts': [],
                'target_language': batch_data.target_lang,
                'success': True
            }

        texts = [text.strip() for text in batch_data.texts if text and text.strip()]
        target_lang = batch_data.target_lang.lower()

        if not texts:
            return {
                'original_texts': [],
                'translated_texts': [],
                'target_language': target_lang,
                'success': True
            }

        translated_texts = await TranslationService.translate_batch(texts, target_lang)

        return {
            'original_texts': texts,
            'translated_texts': translated_texts,
            'target_language': target_lang,
            'success': True
        }

    except Exception as e:
        return {
            'original_texts': batch_data.texts,
            'translated_texts': batch_data.texts,
            'target_language': batch_data.target_lang,
            'success': False,
            'error': str(e)
        }

@router.get("/languages")
async def get_supported_languages():
    """Get list of supported languages"""
    return {
        "languages": TranslationService.get_supported_languages()
    }