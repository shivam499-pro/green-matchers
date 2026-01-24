# services/translation.py
import asyncio
from typing import Dict, Optional
import json
from deep_translator import GoogleTranslator
from ..config import settings

class TranslationService:
    # Supported languages mapping
    SUPPORTED_LANGUAGES = {
        "en": "english", "hi": "hindi", "bn": "bengali", "te": "telugu",
        "ta": "tamil", "mr": "marathi", "gu": "gujarati", "ur": "urdu",
        "kn": "kannada", "or": "odia", "ml": "malayalam"
    }

    # Fallback translations for common terms
    FALLBACK_TRANSLATIONS = {
        "hi": {
            "Solar Energy Engineer": "सौर ऊर्जा इंजीनियर",
            "Environmental Analyst": "पर्यावरण विश्लेषक",
            "Wind Farm Technician": "पवन फार्म तकनीशियन",
            "Sustainability Manager": "सस्टेनेबिलिटी मैनेजर",
            "EV Battery Engineer": "ईवी बैटरी इंजीनियर",
            "Sustainability Data Analyst": "सस्टेनेबिलिटी डेटा विश्लेषक",
            "Senior Solar Energy Engineer": "सीनियर सौर ऊर्जा इंजीनियर",
            "Green Building Architect": "ग्रीन बिल्डिंग आर्किटेक्ट",
            "ESG Reporting Manager": "ईएसजी रिपोर्टिंग मैनेजर",
            "Wind Energy Analyst": "विंड एनर्जी एनालिस्ट",
            "Carbon Accounting Specialist": "कार्बन अकाउंटिंग विशेषज्ञ",
        },
        "bn": {
            "Solar Energy Engineer": "সৌর শক্তি প্রকৌশলী",
            "Environmental Analyst": "পরিবেশ বিশ্লেষক",
            "Wind Farm Technician": "বায়ু খামার টেকনিশিয়ান",
            "Sustainability Manager": "সুস্থিরতা ব্যবস্থাপক",
            "EV Battery Engineer": "ইভি ব্যাটারি ইঞ্জিনিয়ার",
            "Sustainability Data Analyst": "সুস্থিরতা তথ্য বিশ্লেষক",
            "Senior Solar Energy Engineer": "সিনিয়র সৌর শক্তি প্রকৌশলী",
            "Green Building Architect": "গ্রীন বিল্ডিং আর্কিটেক্ট",
            "ESG Reporting Manager": "ESG রিপোর্টিং ম্যানেজার",
            "Wind Energy Analyst": "বায়ু শক্তি বিশ্লেষক",
            "Carbon Accounting Specialist": "কার্বন অ্যাকাউন্টিং বিশেষজ্ঞ",
        },
        "te": {
            "Solar Energy Engineer": "సోలార్ ఎనర్జీ ఇంజనీర్",
            "Environmental Analyst": "పర్యావరణ విశ్లేషకుడు",
            "Wind Farm Technician": "విండ్ ఫార్మ్ టెక్నీషియన్",
            "Sustainability Manager": "సస్టైనబిలిటీ మేనేజర్",
            "EV Battery Engineer": "ఈవీ బ్యాటరీ ఇంజనీర్",
            "Sustainability Data Analyst": "సస్టైనబిలిటీ డేటా అనలిస్ట్",
            "Senior Solar Energy Engineer": "సీనియర్ సోలార్ ఎనర్జీ ఇంజనీర్",
            "Green Building Architect": "గ్రీన్ బిల్డింగ్ ఆర్కిటెక్ట్",
            "ESG Reporting Manager": "ESG రిపోర్టింగ్ మేనేజర్",
            "Wind Energy Analyst": "విండ్ ఎనర్జీ అనలిస్ట్",
            "Carbon Accounting Specialist": "కార్బన్ అకౌంటింగ్ స్పెషలిస్ట్",
        },
        "ta": {
            "Solar Energy Engineer": "சோலார் எனர்ஜி இன்ஜினியர்",
            "Environmental Analyst": "சுற்றுச்சூழல் பகுப்பாய்வாளர்",
            "Wind Farm Technician": "காற்று பண்ணை தொழில்நுட்ப வல்லுநர்",
            "Sustainability Manager": "நிலைத்தன்மை மேலாளர்",
            "EV Battery Engineer": "EV பேட்டரி இன்ஜினியர்",
            "Sustainability Data Analyst": "நிலைத்தன்மை தரவு பகுப்பாய்வாளர்",
            "Senior Solar Energy Engineer": "மூத்த சோலார் எனர்ஜி இன்ஜினியர்",
            "Green Building Architect": "பசுமை கட்டிடக் கலைஞர்",
            "ESG Reporting Manager": "ESG அறிக்கை மேலாளர்",
            "Wind Energy Analyst": "காற்று ஆற்றல் பகுப்பாய்வாளர்",
            "Carbon Accounting Specialist": "கார்பன் கணக்கியல் நிபுணர்",
        },
        "mr": {
            "Solar Energy Engineer": "सौर ऊर्जा अभियंता",
            "Environmental Analyst": "पर्यावरण विश्लेषक",
            "Wind Farm Technician": "विंड फार्म तंत्रज्ञ",
            "Sustainability Manager": "सातत्य व्यवस्थापक",
            "EV Battery Engineer": "ईव्ही बॅटरी अभियंता",
            "Sustainability Data Analyst": "सातत्य डेटा विश्लेषक",
            "Senior Solar Energy Engineer": "वरिष्ठ सौर ऊर्जा अभियंता",
            "Green Building Architect": "ग्रीन बिल्डिंग आर्किटेक्ट",
            "ESG Reporting Manager": "ESG अहवाल व्यवस्थापक",
            "Wind Energy Analyst": "विंड एनर्जी विश्लेषक",
            "Carbon Accounting Specialist": "कार्बन अकाउंटिंग तज्ञ",
        },
        "gu": {
            "Solar Energy Engineer": "સોલર એનર્જી એન્જિનિયર",
            "Environmental Analyst": "પર્યાવરણ વિશ્લેષક",
            "Wind Farm Technician": "વિન્ડ ફાર્મ ટેક્નિશિયન",
            "Sustainability Manager": "સસ્ટેનેબિલિટી મેનેજર",
            "EV Battery Engineer": "ઈવી બેટરી એન્જિનિયર",
            "Sustainability Data Analyst": "સસ્ટેનેબિલિટી ડેટા એનાલિસ્ટ",
            "Senior Solar Energy Engineer": "સિનિયર સોલર એનર્જી એન્જિનિયર",
            "Green Building Architect": "ગ્રીન બિલ્ડિંગ આર્કિટેક્ટ",
            "ESG Reporting Manager": "ESG રિપોર્ટિંગ મેનેજર",
            "Wind Energy Analyst": "વિન્ડ એનર્જી એનાલિસ્ટ",
            "Carbon Accounting Specialist": "કાર્બન એકાઉન્ટિંગ સ્પેશિયલિસ્ટ",
        },
        "kn": {
            "Solar Energy Engineer": "ಸೌರ ಶಕ್ತಿ ಎಂಜಿನಿಯರ್",
            "Environmental Analyst": "ಪರಿಸರ ವಿಶ್ಲೇಷಕ",
            "Wind Farm Technician": "ಗಾಳಿ ಫಾರ್ಮ್ ತಂತ್ರಜ್ಞ",
            "Sustainability Manager": "ಸುಸ್ಥಿರತೆ ಮ್ಯಾನೇಜರ್",
            "EV Battery Engineer": "ಇವಿ ಬ್ಯಾಟರಿ ಎಂಜಿನಿಯರ್",
            "Sustainability Data Analyst": "ಸುಸ್ಥಿರತೆ ಡೇಟಾ ವಿಶ್ಲೇಷಕ",
            "Senior Solar Energy Engineer": "ಸೀನಿಯರ್ ಸೌರ ಶಕ್ತಿ ಎಂಜಿನಿಯರ್",
            "Green Building Architect": "ಗ್ರೀನ್ ಬಿಲ್ಡಿಂಗ್ ಆರ್ಕಿಟೆಕ್ಟ್",
            "ESG Reporting Manager": "ESG ರಿಪೋರ್ಟಿಂಗ್ ಮ್ಯಾನೇಜರ್",
            "Wind Energy Analyst": "ಗಾಳಿ ಶಕ್ತಿ ವಿಶ್ಲೇಷಕ",
            "Carbon Accounting Specialist": "ಕಾರ್ಬನ್ ಅಕೌಂಟಿಂಗ್ ತಜ್ಞ",
        },
        "ml": {
            "Solar Energy Engineer": "സോളാർ എനർജി എഞ്ചിനീയർ",
            "Environmental Analyst": "പരിസ്ഥിതി വിശകലനകാരൻ",
            "Wind Farm Technician": "വിൻഡ് ഫാം ടെക്നീഷ്യൻ",
            "Sustainability Manager": "സസ്റ്റെയിനബിലിറ്റി മാനേജർ",
            "EV Battery Engineer": "ഇവി ബാറ്ററി എഞ്ചിനീയർ",
            "Sustainability Data Analyst": "സസ്റ്റെയിനബിലിറ്റി ഡാറ്റ അനലിസ്റ്റ്",
            "Senior Solar Energy Engineer": "സീനിയർ സോളാർ എനർജി എഞ്ചിനീയർ",
            "Green Building Architect": "ഗ്രീൻ ബിൽഡിംഗ് ആർക്കിടെക്റ്റ്",
            "ESG Reporting Manager": "ESG റിപ്പോർട്ടിംഗ് മാനേജർ",
            "Wind Energy Analyst": "വിൻഡ് എനർജി അനലിസ്റ്റ്",
            "Carbon Accounting Specialist": "കാർബൺ അക്കൗണ്ടിംഗ് സ്പെഷ്യലിസ്റ്റ്",
        },
        "or": {
            "Solar Energy Engineer": "ସୌର ଶକ୍ତି ଇଞ୍ଜିନିୟର",
            "Environmental Analyst": "ପରିବେଶ ବିଶ୍ଳେଷକ",
            "Wind Farm Technician": "ପବନ ଫାର୍ମ ଟେକ୍ନିସିଆନ",
            "Sustainability Manager": "ସ୍ଥିରତା ପରିଚାଳକ",
            "EV Battery Engineer": "ଇଭି ବ୍ୟାଟେରୀ ଇଞ୍ଜିନିୟର",
            "Sustainability Data Analyst": "ସ୍ଥିରତା ତଥ୍ୟ ବିଶ୍ଳେଷକ",
            "Senior Solar Energy Engineer": "ସିନିୟର ସୌର ଶକ୍ତି ଇଞ୍ଜିନିୟର",
            "Green Building Architect": "ଗ୍ରୀନ୍ ବିଲ୍ଡିଂ ଆର୍କିଟେକ୍ଟ",
            "ESG Reporting Manager": "ESG ରିପୋର୍ଟିଂ ମ୍ୟାନେଜର",
            "Wind Energy Analyst": "ପବନ ଶକ୍ତି ବିଶ୍ଳେଷକ",
            "Carbon Accounting Specialist": "କାର୍ବନ ଆକାଉଣ୍ଟିଂ ବିଶେଷଜ୍ଞ",
        }
    }

    @staticmethod
    async def translate_text(text: str, target_lang: str) -> str:
        """Translate text to target language with fallbacks"""
        if not text or not text.strip() or target_lang == "en":
            return text

        text = text.strip()
        target_lang = target_lang.lower()

        # Validate language
        if target_lang not in TranslationService.SUPPORTED_LANGUAGES:
            return text

        # Try fallback dictionary first
        if target_lang in TranslationService.FALLBACK_TRANSLATIONS:
            if text in TranslationService.FALLBACK_TRANSLATIONS[target_lang]:
                return TranslationService.FALLBACK_TRANSLATIONS[target_lang][text]

            # Try case-insensitive match
            text_lower = text.lower()
            for key, value in TranslationService.FALLBACK_TRANSLATIONS[target_lang].items():
                if key.lower() == text_lower:
                    return value

        # Fallback to Google Translate
        try:
            translated = GoogleTranslator(source='auto', target=target_lang).translate(text)
            return translated if translated and translated != text else text
        except Exception:
            return text

    @staticmethod
    async def translate_batch(texts: list, target_lang: str) -> list:
        """Translate multiple texts at once"""
        if not texts:
            return []

        tasks = [TranslationService.translate_text(text, target_lang) for text in texts]
        return await asyncio.gather(*tasks)

    @staticmethod
    def get_supported_languages():
        """Get list of supported languages"""
        return [
            {"code": code, "name": name.title(), "nativeName": code}
            for code, name in TranslationService.SUPPORTED_LANGUAGES.items()
        ]

    @staticmethod
    def validate_language(lang: str) -> bool:
        """Validate if language is supported"""
        return lang.lower() in TranslationService.SUPPORTED_LANGUAGES