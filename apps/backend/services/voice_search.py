# services/voice_search.py - Advanced Voice-Powered Job Search
import speech_recognition as sr
from gtts import gTTS
import io
import base64
import json
import re
from typing import Dict, List, Any, Optional
import asyncio
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class AdvancedVoiceSearch:
    def __init__(self):
        """Initialize the advanced voice search system"""
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8

        # Voice command patterns
        self.command_patterns = {
            'job_search': [
                r'find (?:me )?jobs? (?:in|for|with) (.+)',
                r'search (?:for )?jobs? (?:in|for|with) (.+)',
                r'i want jobs? (?:in|for|with) (.+)',
                r'looking for (.+) jobs?',
                r'(.+) jobs? please'
            ],
            'skill_search': [
                r'jobs? requiring (.+)',
                r'(.+) skilled jobs?',
                r'positions with (.+) skills?'
            ],
            'location_search': [
                r'jobs? in (.+)',
                r'positions in (.+)',
                r'(.+) based jobs?'
            ],
            'salary_search': [
                r'jobs? (?:paying|with salary) (.+)',
                r'(.+) salary jobs?',
                r'high paying (.+) jobs?'
            ],
            'career_advice': [
                r'what career should i choose',
                r'career advice',
                r'help me choose a career',
                r'what should i do for career'
            ]
        }

        # Response templates
        self.response_templates = {
            'search_results': [
                "Found {count} jobs matching '{query}'. The top match is {top_job} at {company} paying ₹{salary} LPA.",
                "I found {count} positions for '{query}'. Best match: {top_job} with {company}, salary ₹{salary} LPA.",
                "Search complete! {count} jobs available for '{query}'. Leading option: {top_job} at {company} for ₹{salary} LPA."
            ],
            'no_results': [
                "I couldn't find any jobs matching '{query}'. Try different keywords like 'python developer' or 'data analyst'.",
                "No matches found for '{query}'. Consider broadening your search terms.",
                "Sorry, no jobs found for '{query}'. Try searching for 'software engineer' or similar roles."
            ],
            'clarify_request': [
                "Could you please specify what type of job you're looking for? For example, 'find python developer jobs'.",
                "I need more details about the job you're interested in. Try saying 'find data analyst positions'.",
                "Please tell me what kind of job or skills you're looking for."
            ]
        }

        print("✅ Advanced Voice Search initialized!")

    async def process_voice_command(self, audio_data: bytes, user_id: int = None) -> Dict[str, Any]:
        """Process voice input and return structured response"""
        try:
            # Convert audio bytes to AudioData
            audio = sr.AudioData(audio_data, 16000, 2)  # 16kHz, 16-bit

            # Perform speech recognition
            text = self.recognizer.recognize_google(audio, language='en-IN')
            text = text.lower().strip()

            logger.info(f"🎤 Voice input recognized: '{text}'")

            # Analyze the command
            command_analysis = self._analyze_voice_command(text)

            # Generate response based on command type
            response = await self._generate_voice_response(command_analysis, user_id)

            return {
                'recognized_text': text,
                'command_type': command_analysis['type'],
                'confidence': command_analysis['confidence'],
                'search_parameters': command_analysis['parameters'],
                'response_audio': response['audio_base64'],
                'response_text': response['text'],
                'action_data': response['action_data'],
                'processing_time': datetime.utcnow().isoformat()
            }

        except sr.UnknownValueError:
            logger.warning("Speech recognition could not understand audio")
            return self._generate_error_response("could_not_understand")

        except sr.RequestError as e:
            logger.error(f"Speech recognition service error: {e}")
            return self._generate_error_response("service_error")

        except Exception as e:
            logger.error(f"Voice processing error: {e}")
            return self._generate_error_response("processing_error")

    def _analyze_voice_command(self, text: str) -> Dict[str, Any]:
        """Analyze voice command and extract parameters"""
        best_match = {
            'type': 'unknown',
            'confidence': 0.0,
            'parameters': {},
            'matched_pattern': None
        }

        # Check each command type
        for command_type, patterns in self.command_patterns.items():
            for pattern in patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    confidence = self._calculate_match_confidence(text, pattern)
                    if confidence > best_match['confidence']:
                        best_match = {
                            'type': command_type,
                            'confidence': confidence,
                            'parameters': self._extract_parameters(match, command_type),
                            'matched_pattern': pattern
                        }

        return best_match

    def _calculate_match_confidence(self, text: str, pattern: str) -> float:
        """Calculate how well the pattern matches the text"""
        # Simple confidence calculation based on pattern specificity
        pattern_length = len(pattern.split())
        text_length = len(text.split())

        if pattern_length == 0:
            return 0.0

        # Base confidence from pattern match
        base_confidence = min(pattern_length / text_length, 1.0)

        # Boost confidence for specific keywords
        specific_keywords = ['find', 'search', 'jobs', 'career', 'positions']
        keyword_matches = sum(1 for keyword in specific_keywords if keyword in text)

        confidence_boost = min(keyword_matches * 0.1, 0.3)

        return min(base_confidence + confidence_boost, 1.0)

    def _extract_parameters(self, match, command_type: str) -> Dict[str, Any]:
        """Extract search parameters from regex match"""
        if command_type in ['job_search', 'skill_search', 'location_search', 'salary_search']:
            query = match.group(1).strip() if match.groups() else ""
            return {
                'query': query,
                'search_type': command_type,
                'filters': self._parse_additional_filters(query)
            }
        elif command_type == 'career_advice':
            return {'request_type': 'general_career_guidance'}

        return {}

    def _parse_additional_filters(self, query: str) -> Dict[str, Any]:
        """Parse additional filters from query"""
        filters = {}

        # Location detection
        locations = ['mumbai', 'delhi', 'bangalore', 'chennai', 'pune', 'hyderabad', 'kolkata']
        for location in locations:
            if location in query.lower():
                filters['location'] = location.title()
                break

        # Experience level detection
        if any(word in query.lower() for word in ['junior', 'entry', 'beginner']):
            filters['experience_level'] = 'entry'
        elif any(word in query.lower() for word in ['senior', 'lead', 'experienced']):
            filters['experience_level'] = 'senior'
        elif any(word in query.lower() for word in ['mid', 'intermediate']):
            filters['experience_level'] = 'mid'

        # Salary range detection
        salary_patterns = [
            r'(\d+)(?:\s*to\s*|\s*-\s*)(\d+)\s*l(?:pa|akh)',
            r'(\d+)\s*l(?:pa|akh)',
        ]

        for pattern in salary_patterns:
            match = re.search(pattern, query, re.IGNORECASE)
            if match:
                if len(match.groups()) == 2:
                    filters['salary_min'] = int(match.group(1))
                    filters['salary_max'] = int(match.group(2))
                else:
                    filters['salary_min'] = int(match.group(1))
                break

        return filters

    async def _generate_voice_response(self, command_analysis: Dict, user_id: int = None) -> Dict[str, Any]:
        """Generate voice response and action data"""
        command_type = command_analysis['type']
        parameters = command_analysis['parameters']

        if command_type in ['job_search', 'skill_search', 'location_search', 'salary_search']:
            # Perform job search
            search_results = await self._perform_voice_job_search(parameters)

            if search_results['count'] > 0:
                template = self.response_templates['search_results'][
                    len(self.response_templates['search_results']) % 3
                ]
                response_text = template.format(
                    count=search_results['count'],
                    query=parameters.get('query', 'your search'),
                    top_job=search_results['top_job']['title'],
                    company=search_results['top_job']['company'],
                    salary=search_results['top_job']['salary']
                )
            else:
                response_text = self.response_templates['no_results'][0].format(
                    query=parameters.get('query', 'your search')
                )

            action_data = {
                'type': 'job_search',
                'search_results': search_results,
                'search_parameters': parameters
            }

        elif command_type == 'career_advice':
            response_text = "I'd be happy to help you with career guidance! Based on current market trends, green energy and sustainability roles are growing rapidly. Would you like me to analyze your skills and suggest suitable careers?"

            action_data = {
                'type': 'career_advice_request',
                'suggestion': 'redirect_to_career_coach'
            }

        else:
            response_text = self.response_templates['clarify_request'][0]
            action_data = {
                'type': 'clarification_needed',
                'suggestion': 'ask_for_clarification'
            }

        # Generate audio response
        audio_base64 = await self._generate_audio_response(response_text)

        return {
            'text': response_text,
            'audio_base64': audio_base64,
            'action_data': action_data
        }

    async def _perform_voice_job_search(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Perform job search based on voice parameters"""
        try:
            # Import vector service for search
            from .vector_services import vector_service

            query = parameters.get('query', '')
            filters = parameters.get('filters', {})

            # Perform semantic search
            search_results = vector_service.semantic_search_jobs(
                query=query,
                top_k=10,
                filters=filters
            )

            result = {
                'count': len(search_results),
                'results': search_results,
                'top_job': search_results[0] if search_results else None,
                'search_query': query,
                'applied_filters': filters
            }

            return result

        except Exception as e:
            logger.error(f"Voice job search error: {e}")
            return {'count': 0, 'results': [], 'top_job': None}

    async def _generate_audio_response(self, text: str) -> str:
        """Generate audio response using text-to-speech"""
        try:
            # Use gTTS for text-to-speech
            tts = gTTS(text=text, lang='en', slow=False)

            # Save to bytes buffer
            audio_buffer = io.BytesIO()
            tts.write_to_fp(audio_buffer)
            audio_buffer.seek(0)

            # Convert to base64
            audio_base64 = base64.b64encode(audio_buffer.getvalue()).decode('utf-8')

            return audio_base64

        except Exception as e:
            logger.error(f"Audio generation error: {e}")
            return ""

    def _generate_error_response(self, error_type: str) -> Dict[str, Any]:
        """Generate error response for voice processing failures"""
        error_responses = {
            'could_not_understand': {
                'recognized_text': '',
                'command_type': 'error',
                'confidence': 0.0,
                'search_parameters': {},
                'response_audio': '',
                'response_text': 'I couldn\'t understand that. Please try speaking more clearly or use text search instead.',
                'action_data': {'type': 'error', 'error_type': 'speech_recognition_failed'}
            },
            'service_error': {
                'recognized_text': '',
                'command_type': 'error',
                'confidence': 0.0,
                'search_parameters': {},
                'response_audio': '',
                'response_text': 'Speech recognition service is temporarily unavailable. Please use text search.',
                'action_data': {'type': 'error', 'error_type': 'service_unavailable'}
            },
            'processing_error': {
                'recognized_text': '',
                'command_type': 'error',
                'confidence': 0.0,
                'search_parameters': {},
                'response_audio': '',
                'response_text': 'Voice processing error occurred. Please try again or use text search.',
                'action_data': {'type': 'error', 'error_type': 'processing_failed'}
            }
        }

        return error_responses.get(error_type, error_responses['processing_error'])

    def get_voice_commands_help(self) -> Dict[str, Any]:
        """Get help information for voice commands"""
        return {
            'supported_commands': [
                "Find jobs in renewable energy",
                "Search for Python developer positions",
                "I want data analyst jobs",
                "Jobs requiring machine learning",
                "High paying software engineer jobs",
                "Career advice",
                "Help me choose a career"
            ],
            'examples': [
                "Say: 'Find me renewable energy jobs in Bangalore'",
                "Say: 'Search for Python developer positions'",
                "Say: 'What career should I choose?'"
            ],
            'tips': [
                "Speak clearly and at normal pace",
                "Use specific job titles or skills",
                "Include location if you prefer remote/on-site",
                "Mention salary preferences if specific"
            ]
        }

# Global instance
voice_search = AdvancedVoiceSearch()